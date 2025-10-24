# roi_function.py
from sample_data import MODELS, MODEL_COMPATIBILITY, PREDEFINED_USE_CASES
from typing import Dict, List

def calculate_tco(
    model_name: str,
    input_tokens: int,
    output_tokens: int,
    monthly_requests: int,
    inference_mode: str,
    is_custom: bool = False
) -> Dict:
    m = MODELS[model_name]
    total_input_tokens = input_tokens * monthly_requests
    total_output_tokens = output_tokens * monthly_requests

    # Inference Cost
    if inference_mode == "Batch":
        inference_cost = (total_input_tokens * m["input_price_per_1k"] + total_output_tokens * m["output_price_per_1k"]) * 0.5 / 1000
    elif inference_mode.startswith("Provisioned"):
        # 1 Model Unit = 15M tokens/min → 10.8B tokens/month
        capacity_per_mu = 15_000_000 * 60 * 720
        total_tokens = total_input_tokens + total_output_tokens
        mus_needed = max(1, total_tokens / capacity_per_mu)
        inference_cost = m["provisioned_hourly"] * 720 * mus_needed
    else:  # On-Demand
        inference_cost = (total_input_tokens * m["input_price_per_1k"] + total_output_tokens * m["output_price_per_1k"]) / 1000

    # Storage
    storage_cost = 1.95 if is_custom else 0

    # Data Transfer Out
    data_transfer_gb = (total_output_tokens * 4) / (1024**3)  # ~4 bytes/token
    data_transfer_cost = data_transfer_gb * 0.09

    total_tco = inference_cost + storage_cost + data_transfer_cost

    # Utilization for Provisioned
    utilization = 1.0
    if inference_mode.startswith("Provisioned"):
        utilization = min(1.0, total_tokens / capacity_per_mu)

    return {
        "inference_cost": inference_cost,
        "storage_cost": storage_cost,
        "data_transfer_cost": data_transfer_cost,
        "total_tco": total_tco,
        "latency_ms": m["latency_ms"],
        "throughput_rps": m["throughput_rps"],
        "utilization": utilization
    }

def rank_student_models(teacher: str, input_tokens: int, output_tokens: int, monthly_requests: int, inference_mode: str) -> List[Dict]:
    teacher_tco = calculate_tco(teacher, input_tokens, output_tokens, monthly_requests, inference_mode)["total_tco"]
    results = []

    for student in MODEL_COMPATIBILITY.get(teacher, []):
        s_tco = calculate_tco(student, input_tokens, output_tokens, monthly_requests, inference_mode, is_custom=True)
        savings = (teacher_tco - s_tco["total_tco"]) / teacher_tco * 100 if teacher_tco > 0 else 0
        perf_score = s_tco["throughput_rps"] - (s_tco["latency_ms"] / 100)
        suitability = min(100, round(0.5 * savings + 0.5 * perf_score, 2))  # Balanced

        results.append({
            "Model": student,
            "Suitability Score": suitability,
            "TCO Savings %": round(savings, 1),
            "Monthly TCO ($)": round(s_tco["total_tco"], 2),
            "Latency (ms)": s_tco["latency_ms"],
            "Throughput (req/s)": s_tco["throughput_rps"]
        })

    return sorted(results, key=lambda x: x["Suitability Score"], reverse=True)
