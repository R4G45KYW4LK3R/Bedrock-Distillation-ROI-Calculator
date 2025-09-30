# sample_data.py

MODELS = {
    # --- TEACHER MODELS (High Cost, High Performance) ---
    "Claude 3 Opus (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.01500, "latency_ms": 1800, "p95_latency_ms": 2500, "throughput_rps": 10,
        "accuracy": {"qa": 0.98, "summarization": 0.97}, "human_eval": 4.9,
        "resource_util": {"memory_gb": 120, "compute": "16x A100"},
    },
    "GPT-4 Turbo (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.01000, "latency_ms": 1500, "p95_latency_ms": 2000, "throughput_rps": 12,
        "accuracy": {"qa": 0.97, "summarization": 0.96}, "human_eval": 4.8,
        "resource_util": {"memory_gb": 100, "compute": "12x A100"},
    },
    "Llama 3 70B (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.00047, "latency_ms": 1318, "p95_latency_ms": 1600, "throughput_rps": 15,
        "accuracy": {"qa": 0.95, "summarization": 0.93}, "human_eval": 4.5,
        "resource_util": {"memory_gb": 80, "compute": "8x A100"},
    },
    "Jurassic-2 Ultra (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.00090, "latency_ms": 1600, "p95_latency_ms": 2200, "throughput_rps": 9,
        "accuracy": {"qa": 0.94, "summarization": 0.95}, "human_eval": 4.6,
        "resource_util": {"memory_gb": 90, "compute": "10x A100"},
    },
    "Cochise v2 (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.00500, "latency_ms": 1400, "p95_latency_ms": 1800, "throughput_rps": 11,
        "accuracy": {"qa": 0.96, "summarization": 0.94}, "human_eval": 4.7,
        "resource_util": {"memory_gb": 110, "compute": "14x A100"},
    },
    "Titan Large (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.00060, "latency_ms": 1200, "p95_latency_ms": 1500, "throughput_rps": 18,
        "accuracy": {"qa": 0.93, "summarization": 0.92}, "human_eval": 4.4,
        "resource_util": {"memory_gb": 70, "compute": "7x A100"},
    },
    "Falcon 180B (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.00055, "latency_ms": 1450, "p95_latency_ms": 1750, "throughput_rps": 13,
        "accuracy": {"qa": 0.92, "summarization": 0.91}, "human_eval": 4.3,
        "resource_util": {"memory_gb": 85, "compute": "9x A100"},
    },
    "Command R (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.00350, "latency_ms": 1700, "p95_latency_ms": 2400, "throughput_rps": 8,
        "accuracy": {"qa": 0.95, "summarization": 0.96}, "human_eval": 4.7,
        "resource_util": {"memory_gb": 115, "compute": "15x A100"},
    },
    "Mistral Large (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.00400, "latency_ms": 1650, "p95_latency_ms": 2300, "throughput_rps": 7,
        "accuracy": {"qa": 0.96, "summarization": 0.95}, "human_eval": 4.8,
        "resource_util": {"memory_gb": 105, "compute": "13x A100"},
    },
    "Inflection-2.5 (Teacher)": {
        "type": "Teacher", "cost_per_request": 0.00800, "latency_ms": 1900, "p95_latency_ms": 2600, "throughput_rps": 6,
        "accuracy": {"qa": 0.97, "summarization": 0.98}, "human_eval": 4.9,
        "resource_util": {"memory_gb": 125, "compute": "18x A100"},
    },
    
    # --- STUDENT MODELS (Low Cost, Distilled/Smaller Performance) ---
    "Mistral 7B (Student)": {
        "type": "Student", "cost_per_request": 0.00006, "latency_ms": 600, "p95_latency_ms": 750, "throughput_rps": 55,
        "accuracy": {"qa": 0.89, "summarization": 0.87}, "human_eval": 4.1,
        "resource_util": {"memory_gb": 12, "compute": "1x A100"},
    },
    "Llama 3 8B (Student)": {
        "type": "Student", "cost_per_request": 0.00007, "latency_ms": 653, "p95_latency_ms": 800, "throughput_rps": 50,
        "accuracy": {"qa": 0.90, "summarization": 0.88}, "human_eval": 4.0,
        "resource_util": {"memory_gb": 16, "compute": "1x A100"},
    },
    "Gemma 7B (Student)": {
        "type": "Student", "cost_per_request": 0.00005, "latency_ms": 550, "p95_latency_ms": 700, "throughput_rps": 60,
        "accuracy": {"qa": 0.88, "summarization": 0.86}, "human_eval": 3.9,
        "resource_util": {"memory_gb": 10, "compute": "1x A100"},
    },
    "Falcon 7B (Student)": {
        "type": "Student", "cost_per_request": 0.00004, "latency_ms": 500, "p95_latency_ms": 650, "throughput_rps": 65,
        "accuracy": {"qa": 0.87, "summarization": 0.85}, "human_eval": 3.8,
        "resource_util": {"memory_gb": 8, "compute": "1x A100"},
    },
    "DistilGPT-2 (Student)": {
        "type": "Student", "cost_per_request": 0.00001, "latency_ms": 200, "p95_latency_ms": 300, "throughput_rps": 100,
        "accuracy": {"qa": 0.75, "summarization": 0.70}, "human_eval": 3.0,
        "resource_util": {"memory_gb": 4, "compute": "1x V100"},
    },
    "TinyLlama (Student)": {
        "type": "Student", "cost_per_request": 0.000005, "latency_ms": 150, "p95_latency_ms": 250, "throughput_rps": 120,
        "accuracy": {"qa": 0.65, "summarization": 0.60}, "human_eval": 2.5,
        "resource_util": {"memory_gb": 2, "compute": "1x T4"},
    },
    "Llama 2 13B (Student)": {
        "type": "Student", "cost_per_request": 0.00015, "latency_ms": 750, "p95_latency_ms": 900, "throughput_rps": 40,
        "accuracy": {"qa": 0.91, "summarization": 0.90}, "human_eval": 4.2,
        "resource_util": {"memory_gb": 20, "compute": "1x A100"},
    },
    "Mistral 8x7B (Student)": {
        "type": "Student", "cost_per_request": 0.00020, "latency_ms": 850, "p95_latency_ms": 1000, "throughput_rps": 35,
        "accuracy": {"qa": 0.92, "summarization": 0.91}, "human_eval": 4.3,
        "resource_util": {"memory_gb": 24, "compute": "2x A100"},
    },
    "Titan Express (Student)": {
        "type": "Student", "cost_per_request": 0.00009, "latency_ms": 700, "p95_latency_ms": 850, "throughput_rps": 45,
        "accuracy": {"qa": 0.89, "summarization": 0.89}, "human_eval": 4.0,
        "resource_util": {"memory_gb": 18, "compute": "1x A100"},
    },
    "Cohere 6B (Student)": {
        "type": "Student", "cost_per_request": 0.00008, "latency_ms": 680, "p95_latency_ms": 820, "throughput_rps": 48,
        "accuracy": {"qa": 0.90, "summarization": 0.87}, "human_eval": 3.9,
        "resource_util": {"memory_gb": 15, "compute": "1x A100"},
    }
}

# Helper lists for Streamlit selectbox filtering
TEACHER_MODELS = [k for k, v in MODELS.items() if v["type"] == "Teacher"]
STUDENT_MODELS = [k for k, v in MODELS.items() if v["type"] == "Student"]
