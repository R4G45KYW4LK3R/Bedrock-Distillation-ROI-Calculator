# sample_data.py
from typing import Dict, List

MODELS: Dict[str, Dict] = {
    "Amazon Nova Pro (Teacher)": {
        "type": "Teacher",
        "input_price_per_1k": 0.000100,
        "output_price_per_1k": 0.000400,
        "provisioned_hourly": 90.00,
        "latency_ms": 220,
        "throughput_rps": 45,
    },
    "Anthropic Claude 3 Sonnet (Teacher)": {
        "type": "Teacher",
        "input_price_per_1k": 0.00300,
        "output_price_per_1k": 0.01500,
        "provisioned_hourly": 75.00,
        "latency_ms": 250,
        "throughput_rps": 40,
    },
    "Mistral Large (24.02) (Teacher)": {
        "type": "Teacher",
        "input_price_per_1k": 0.00200,
        "output_price_per_1k": 0.00600,
        "provisioned_hourly": 80.00,
        "latency_ms": 270,
        "throughput_rps": 38,
    },
    "OpenAI GPT-OSS-120B (Teacher)": {
        "type": "Teacher",
        "input_price_per_1k": 0.00250,
        "output_price_per_1k": 0.00750,
        "provisioned_hourly": 100.00,
        "latency_ms": 300,
        "throughput_rps": 35,
    },
    "DeepSeek V3.1 (Teacher)": {
        "type": "Teacher",
        "input_price_per_1k": 0.00080,
        "output_price_per_1k": 0.00240,
        "provisioned_hourly": 65.00,
        "latency_ms": 240,
        "throughput_rps": 42,
    },
    "Anthropic Claude 3 Opus (Teacher)": {
        "type": "Teacher",
        "input_price_per_1k": 0.01500,
        "output_price_per_1k": 0.07500,
        "provisioned_hourly": 150.00,
        "latency_ms": 320,
        "throughput_rps": 32,
    },
    "Meta Llama 3 70B (Teacher)": {
        "type": "Teacher",
        "input_price_per_1k": 0.00195,
        "output_price_per_1k": 0.00260,
        "provisioned_hourly": 85.00,
        "latency_ms": 260,
        "throughput_rps": 36,
    },

    # === Student Models ===
    "Amazon Nova Lite (Student)": {
        "type": "Student",
        "input_price_per_1k": 0.000060,
        "output_price_per_1k": 0.000240,
        "provisioned_hourly": 25.00,
        "latency_ms": 120,
        "throughput_rps": 70,
    },
    "Anthropic Claude 3 Haiku (Student)": {
        "type": "Student",
        "input_price_per_1k": 0.000250,
        "output_price_per_1k": 0.001250,
        "provisioned_hourly": 20.00,
        "latency_ms": 130,
        "throughput_rps": 68,
    },
    "Mistral 7B (Student)": {
        "type": "Student",
        "input_price_per_1k": 0.00020,
        "output_price_per_1k": 0.00060,
        "provisioned_hourly": 18.00,
        "latency_ms": 110,
        "throughput_rps": 75,
    },
    "Mixtral 8x7B (Student)": {
        "type": "Student",
        "input_price_per_1k": 0.00080,
        "output_price_per_1k": 0.00240,
        "provisioned_hourly": 30.00,
        "latency_ms": 140,
        "throughput_rps": 65,
    },
    "OpenAI GPT-OSS-20B (Student)": {
        "type": "Student",
        "input_price_per_1k": 0.00100,
        "output_price_per_1k": 0.00300,
        "provisioned_hourly": 35.00,
        "latency_ms": 150,
        "throughput_rps": 60,
    },
    "Meta Llama 3 8B (Student)": {
        "type": "Student",
        "input_price_per_1k": 0.00075,
        "output_price_per_1k": 0.00100,
        "provisioned_hourly": 15.00,
        "latency_ms": 100,
        "throughput_rps": 80,
    },
    "Amazon Nova Micro (Student)": {
        "type": "Student",
        "input_price_per_1k": 0.000035,
        "output_price_per_1k": 0.000140,
        "provisioned_hourly": 13.00,
        "latency_ms": 90,
        "throughput_rps": 85,
    },
}

MODEL_COMPATIBILITY = {
    "Amazon Nova Pro (Teacher)": ["Amazon Nova Lite (Student)", "Amazon Nova Micro (Student)"],
    "Anthropic Claude 3 Sonnet (Teacher)": ["Anthropic Claude 3 Haiku (Student)", "Mistral 7B (Student)"],
    "Mistral Large (24.02) (Teacher)": ["Mistral 7B (Student)", "Mixtral 8x7B (Student)"],
    "OpenAI GPT-OSS-120B (Teacher)": ["OpenAI GPT-OSS-20B (Student)", "Mixtral 8x7B (Student)"],
    "DeepSeek V3.1 (Teacher)": ["Mistral 7B (Student)", "OpenAI GPT-OSS-20B (Student)"],
    "Anthropic Claude 3 Opus (Teacher)": ["Anthropic Claude 3 Haiku (Student)", "Mistral 7B (Student)"],
    "Meta Llama 3 70B (Teacher)": ["Meta Llama 3 8B (Student)", "Mistral 7B (Student)"],
}

PREDEFINED_USE_CASES = {
    "2-Page PDF Summarization": (4000, 400),
    "Code Generation": (2000, 1000),
    "QA on Docs": (3000, 200),
    "Text Classification": (500, 50),
}

TEACHER_MODELS = [k for k, v in MODELS.items() if v["type"] == "Teacher"]
STUDENT_MODELS = [k for k, v in MODELS.items() if v["type"] == "Student"]
