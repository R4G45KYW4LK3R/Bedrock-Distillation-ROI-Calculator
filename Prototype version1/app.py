# app.py
import streamlit as st
import pandas as pd
import altair as alt
from sample_data import MODELS, TEACHER_MODELS, MODEL_COMPATIBILITY, PREDEFINED_USE_CASES
from roi_function import calculate_tco, rank_student_models

st.set_page_config(page_title="Bedrock TCO Calculator", page_icon="Dollar", layout="wide")
st.title("Bedrock TCO Calculator: Teacher vs Distilled Models")

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    teacher = st.selectbox("Teacher Model", TEACHER_MODELS, index=0)
with col2:
    compatible = MODEL_COMPATIBILITY.get(teacher, [])
    student = st.selectbox("Student Model", compatible or ["No compatible models"], index=0)

use_case = st.selectbox("Use Case", ["Custom Tokens"] + list(PREDEFINED_USE_CASES.keys()))

if use_case == "Custom Tokens":
    col_in, col_out = st.columns(2)
    with col_in:
        input_tokens = st.number_input("Input Tokens per Request", min_value=1, value=2000, step=100)
    with col_out:
        output_tokens = st.number_input("Output Tokens per Request", min_value=1, value=500, step=100)
else:
    input_tokens, output_tokens = PREDEFINED_USE_CASES[use_case]
    st.info(f"Using: **{input_tokens:,} input** | **{output_tokens:,} output** tokens")

monthly_requests = st.number_input("Monthly Requests", min_value=100, value=100000, step=10000)
inference_mode = st.radio("Inference Mode", ["On-Demand", "Batch", "Provisioned (1-mo)"])
is_custom = st.checkbox("Custom Distilled Model? (+$1.95/mo storage)", value=True)

if st.button("Compare Models"):
    if not compatible or student == "No compatible models":
        st.error("No compatible student model.")
    elif teacher == student:
        st.error("Select different models.")
    else:
        st.session_state.comparison_run = True

st.divider()

# --- Results ---
if st.session_state.get("comparison_run", False):
    t_tco = calculate_tco(teacher, input_tokens, output_tokens, monthly_requests, inference_mode)
    s_tco = calculate_tco(student, input_tokens, output_tokens, monthly_requests, inference_mode, is_custom)

    savings_pct = (t_tco["total_tco"] - s_tco["total_tco"]) / t_tco["total_tco"] * 100
    savings_amount = t_tco["total_tco"] - s_tco["total_tco"]

    st.subheader("Monthly TCO Comparison")
    cols = st.columns(3)
    cols[0].metric("Teacher TCO", f"${t_tco['total_tco']:.2f}")
    cols[1].metric("Student TCO", f"${s_tco['total_tco']:.2f}", delta=f"-${savings_amount:.2f}")
    cols[2].metric("Savings", f"{savings_pct:.1f}%", delta="Good" if savings_pct > 30 else "Warning")

    if inference_mode.startswith("Provisioned") and s_tco["utilization"] < 0.7:
        st.warning(f"Warning: Utilization: {s_tco['utilization']:.0%} < 70% → Provisioned will cost more!")

    # Table
    data = {
        "Metric": ["Inference", "Storage", "Data Transfer", "Total TCO", "Latency", "Throughput"],
        teacher: [
            f"${t_tco['inference_cost']:.2f}",
            f"${t_tco['storage_cost']:.2f}",
            f"${t_tco['data_transfer_cost']:.2f}",
            f"${t_tco['total_tco']:.2f}",
            f"{t_tco['latency_ms']} ms",
            f"{t_tco['throughput_rps']}/s"
        ],
        student: [
            f"${s_tco['inference_cost']:.2f}",
            f"${s_tco['storage_cost']:.2f}",
            f"${s_tco['data_transfer_cost']:.2f}",
            f"${s_tco['total_tco']:.2f}",
            f"${s_tco['latency_ms']} ms",
            f"${s_tco['throughput_rps']}/s"
        ],
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)

    # Chart
    chart_df = pd.DataFrame({
        "Model": [teacher, student],
        "Monthly TCO ($)": [t_tco["total_tco"], s_tco["total_tco"]],
        "Latency (ms)": [t_tco["latency_ms"], s_tco["latency_ms"]],
    }).melt("Model", var_name="Metric", value_name="Value")

    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("Model"),
        y=alt.Y("Value", title=""),
        color="Model",
        column=alt.Column("Metric", title=None)
    ).properties(title="Monthly TCO & Performance").interactive()
    st.altair_chart(chart, use_container_width=True)

    st.divider()

    # --- Best Student Models ---
    with st.expander("Top 3 Student Models"):
        ranked = rank_student_models(teacher, input_tokens, output_tokens, monthly_requests, inference_mode)
        top3 = pd.DataFrame(ranked[:3])

        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Best Savings", f"{top3.iloc[0]['TCO Savings %']:.1f}%")
        with col2:
            chart = alt.Chart(top3).mark_bar().encode(
                x=alt.X("Model", sort="-y"),
                y=alt.Y("Suitability Score", scale=alt.Scale(domain=[0, 100])),
                color="Model"
            ).properties(title="Suitability (0–100)")
            st.altair_chart(chart, use_container_width=True)

        st.dataframe(top3.set_index("Model"), use_container_width=True)
