# roi_function.py
from sample_data import MODELS, STUDENT_MODELS # Import Student list too

def calculate_metrics(teacher_model_name, student_model_name, application, num_requests):
    # ... (Keep the existing calculate_metrics function unchanged) ...
    t = MODELS[teacher_model_name]
    s = MODELS[student_model_name]

    teacher_total_cost = t["cost_per_request"] * num_requests
    student_total_cost = s["cost_per_request"] * num_requests

    cost_savings = teacher_total_cost - student_total_cost
    cost_savings_pct = (cost_savings / teacher_total_cost) * 100 if teacher_total_cost > 0 else 0

    teacher_acc = t["accuracy"][application]
    student_acc = s["accuracy"][application]
    acc_drop = teacher_acc - student_acc # Raw drop, not percent
    acc_drop_pct = ((teacher_acc - student_acc) / teacher_acc) * 100 if teacher_acc > 0 else 0

    performance_tradeoff = cost_savings_pct / acc_drop_pct if acc_drop_pct > 0 else float("inf")

    # Include raw accuracy drop for ranking logic
    return {
        "teacher_total_cost": teacher_total_cost,
        "student_total_cost": student_total_cost,
        "cost_savings_pct": cost_savings_pct,
        "acc_drop_pct": acc_drop_pct,
        "performance_tradeoff": performance_tradeoff,
        "acc_drop": acc_drop, 
        "student_acc": student_acc,
        "student_latency": s["latency_ms"]
    }


def rank_student_models(teacher_model_name, application, num_requests):
    """
    Compares the Teacher model against all Student models for the given application.
    Ranks them based on a custom "Suitability Score".
    """
    teacher_model_data = MODELS[teacher_model_name]
    teacher_acc = teacher_model_data["accuracy"][application]
    all_results = []
    
    for student_name in STUDENT_MODELS:
        s_data = MODELS[student_name]
        
        # Calculate standard ROI metrics
        metrics = calculate_metrics(teacher_model_name, student_name, application, num_requests)
        
        # --- Custom Suitability Score Calculation ---
        # Prioritize Cost Savings and minimize Accuracy Drop and Latency
        
        # 1. Cost Factor (Higher is better)
        cost_score = metrics['cost_savings_pct']
        
        # 2. Accuracy Factor (Higher is better, penalize big drops)
        # Weight the raw student accuracy and penalize drops aggressively
        acc_penalty = 50 * metrics['acc_drop_pct'] # 50x multiplier for quick drop-off
        acc_score = (s_data["accuracy"][application] * 100) - acc_penalty
        
        # 3. Performance Factor (Higher is better, penalize high latency)
        # Use throughput/latency relationship
        perf_score = s_data["throughput_rps"] - (s_data["latency_ms"] / 100)
        
        # Combined Score: Cost is most important, then performance, then a safety net for accuracy
        suitability_score = (2.0 * cost_score) + (1.0 * perf_score) + (0.5 * acc_score)
        
        all_results.append({
            "Model": student_name,
            "Suitability Score": suitability_score,
            "Cost Savings %": metrics['cost_savings_pct'],
            "Accuracy Drop %": metrics['acc_drop_pct'],
            "Throughput (req/s)": s_data["throughput_rps"],
            "Average Latency (ms)": s_data["latency_ms"]
        })

    # Sort by the Suitability Score (highest first)
    ranked_results = sorted(all_results, key=lambda x: x['Suitability Score'], reverse=True)
    return ranked_results
