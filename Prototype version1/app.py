# app.py (Final Version with Optimization Feature)
import streamlit as st
from sample_data import MODELS, TEACHER_MODELS, STUDENT_MODELS 
# Import the new ranking function
from roi_function import calculate_metrics, rank_student_models 
import pandas as pd
import altair as alt

st.set_page_config(page_title="LLM ROI Calculator", page_icon="📊", layout="wide")

# Initialize session state for persistence
if 'comparison_run' not in st.session_state:
    st.session_state.comparison_run = False

# --- 1. Input Section ---
st.title("📊 ROI Calculator for Distilled Models")

st.divider()

col1, col2 = st.columns(2)
with col1:
    teacher = st.selectbox("Select Teacher Model (Original)", TEACHER_MODELS, index=0)
with col2:
    student = st.selectbox("Select Student Model (Distilled)", STUDENT_MODELS, index=0)

application = st.selectbox("Select Application Type", ["qa", "summarization"])
num_requests = st.number_input("Total Number of Requests (Scalability View)", min_value=1000, step=10000, value=100000)

if st.button("🔍 Compare Models"):
    if teacher == student:
        st.error("Please select different models for Teacher and Student comparison.")
        st.session_state.comparison_run = False
    else:
        st.session_state.comparison_run = True

st.divider()


# --- 2. Main Comparison Results (Unchanged from last step) ---
if st.session_state.comparison_run and teacher != student:
    
    t = MODELS[teacher]
    s = MODELS[student]
    results = calculate_metrics(teacher, student, application, num_requests)

    st.subheader("📑 Comparison Summary")
    # ... (The st.table(data) section here is unchanged) ...
    data = {
        "Metric": [
            "Cost per request ($)",
            f"Total cost for {num_requests:,} requests ($)",
            f"Accuracy ({application.upper()}) (%)",
            "Human Eval (1-5)",
            "Latency (avg ms)",
            "Latency (P95 ms)",
            "Throughput (req/s)",
            "Memory (GB)",
            "Compute"
        ],
        teacher: [
            f"${t['cost_per_request']:.6f}",
            f"${results['teacher_total_cost']:.2f}",
            f"{t['accuracy'][application]*100:.1f}%", 
            f"{t['human_eval']}",
            f"{t['latency_ms']} ms",
            f"{t['p95_latency_ms']} ms",
            f"{t['throughput_rps']}/s",
            f"{t['resource_util']['memory_gb']}",
            f"{t['resource_util']['compute']}"
        ],
        student: [
            f"${s['cost_per_request']:.6f}",
            f"${results['student_total_cost']:.2f}",
            f"{s['accuracy'][application]*100:.1f}%", 
            f"{s['human_eval']}",
            f"{s['latency_ms']} ms",
            f"{s['p95_latency_ms']} ms",
            f"{s['throughput_rps']}/s",
            f"{s['resource_util']['memory_gb']}",
            f"{s['resource_util']['compute']}"
        ]
    }
    st.table(data)
    
    st.divider()

    st.subheader("📈 ROI Analysis: Cost vs. Performance Trade-off")
    c1, c2, c3 = st.columns(3)
    c1.metric("Cost Savings %", f"{results['cost_savings_pct']:.1f}%", delta="High Savings!")
    c2.metric("Accuracy Drop %", f"-{results['acc_drop_pct']:.1f}%", delta_color="inverse")
    tradeoff_value = "∞" if results['performance_tradeoff'] == float("inf") else f"{results['performance_tradeoff']:.2f}x"
    c3.metric("Trade-off Ratio (Cost/Acc Drop)", tradeoff_value, help="Higher is better: Cost savings relative to the drop in accuracy.")

    st.divider()
    
    # ... (Interactive Visualization section here is unchanged) ...
    st.header("📊 Performance Visualisation")
    st.markdown("Side-by-side comparison of key metrics.")

    chart_df = pd.DataFrame({
        "Model": [teacher, student],
        "Total Cost ($)": [results['teacher_total_cost'], results['student_total_cost']],
        "Accuracy (Raw)": [t["accuracy"][application], s["accuracy"][application]], 
        "Average Latency (ms)": [t["latency_ms"], s["latency_ms"]],
        "Throughput (req/s)": [t["throughput_rps"], s["throughput_rps"]]
    })

    chart_melted = chart_df.melt('Model', var_name='Metric', value_name='Value')
    plot_metric = st.selectbox(
        "Select Metric to Visualize",
        ["Total Cost ($)", "Accuracy (Raw)", "Average Latency (ms)", "Throughput (req/s)"]
    )
    df_plot = chart_melted[chart_melted['Metric'] == plot_metric]

    chart = alt.Chart(df_plot).mark_bar().encode(
        x=alt.X('Model', axis=alt.Axis(labelAngle=0)), 
        y=alt.Y('Value', title=plot_metric),
        color='Model'
    ).properties(
        title=f"Comparison of {plot_metric}"
    ).interactive() 

    st.altair_chart(chart, use_container_width=True)

    st.divider()

    # =======================================================
    # D. Optimization Mode (The NEW Feature)
    # =======================================================
    with st.expander("🚀 Find the Most Suitable Student Model (Optimization Mode)"):
        st.subheader(f"Top Student Models for {teacher} on {application.upper()}")
        st.markdown(f"The analysis ranks all Student Models based on **Cost Savings**, **Accuracy Retention**, and **Performance** for your selected application: **{application.upper()}**.")
        
        # Ranks models using the new function
        ranked_models = rank_student_models(teacher, application, num_requests)
        
        # Get the top 3
        top_3 = ranked_models[:3]
        
        # --- Display Summary Metrics ---
        st.metric(
            label=f"Cost Savings Range (vs. {teacher})",
            value=f"{top_3[0]['Cost Savings %']:.1f}% (Max) - {top_3[-1]['Cost Savings %']:.1f}% (Min)"
        )
        st.metric(
            label="Average Accuracy Drop for Top 3",
            value=f"{sum(m['Accuracy Drop %'] for m in top_3) / 3:.1f}%"
        )
        
        st.markdown("### Top 3 Recommended Models:")
        
        # Convert top_3 into a DataFrame for visualization
        top_3_df = pd.DataFrame(top_3)
        top_3_df = top_3_df.head(3) # Ensure only top 3 are shown
        
        # Use a bar chart to visualize the Suitability Score
        chart_score = alt.Chart(top_3_df).mark_bar().encode(
            x=alt.X('Model', sort='-y', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Suitability Score', title="Suitability Score (Higher is Better)"),
            color=alt.Color('Model'),
            tooltip=['Model', 'Suitability Score', 'Cost Savings %', 'Accuracy Drop %']
        ).properties(
            title="Model Suitability Ranking"
        ).interactive()
        
        st.altair_chart(chart_score, use_container_width=True)

        st.markdown("### Detailed Ranking Table")
        # Display the detailed table of the top 3 (and maybe a few more)
        st.dataframe(top_3_df.set_index('Model').head(5), use_container_width=True)
