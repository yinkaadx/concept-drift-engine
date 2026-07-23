import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Data Stream Mining Engine", layout="wide")

st.title("Serverless Data Stream Mining Pipeline")
st.caption("Real-Time Concept Drift Detection & Ensemble Learning Adaptation")

st.sidebar.header("Stream Configuration")
selected_stream = st.sidebar.selectbox("Simulated Data Stream", ["Electricity Demand Forecast (Smart Grid)", "High-Frequency Financial Ticks", "IoT Sensor Telemetry"])
drift_severity = st.sidebar.slider("Simulate Concept Drift Severity", 1.0, 5.0, 3.0)
run_simulation = st.sidebar.button("Initialize Stream Mining Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: AWS Ingestion -> ADWIN Drift Detector -> Online Ensemble")

if run_simulation:
    st.subheader(f"Active Streaming Interface: {selected_stream}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_velocity = col1.empty()
    metric_error = col2.empty()
    metric_accuracy = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(909)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    stream_values = []
    model_accuracy = []
    
    base_value = 100.0 
    current_acc = 95.0
    
    for i in range(100):
        if i < 35:
            current_val = base_value + np.random.uniform(-5.0, 5.0)
            current_acc = 94.0 + np.random.uniform(-1.5, 1.5)
            error_rate = 100.0 - current_acc
            velocity = int(np.random.uniform(15000, 20000))
        elif i >= 35 and i < 55:
            current_val = base_value + (i - 35) * (5.0 * drift_severity) + np.random.uniform(-10.0, 10.0)
            current_acc = current_acc - (drift_severity * 1.5) + np.random.uniform(-2.0, 2.0)
            error_rate = 100.0 - current_acc
            velocity = int(np.random.uniform(20000, 25000))
        else:
            current_val = current_val + np.random.uniform(-5.0, 5.0)
            current_acc = min(96.0, current_acc + 3.0 + np.random.uniform(-1.0, 1.0))
            error_rate = 100.0 - current_acc
            velocity = int(np.random.uniform(18000, 22000))
            
        stream_values.append(current_val)
        model_accuracy.append(current_acc)
        
        metric_velocity.metric("Ingestion Velocity", f"{velocity:,} Nodes/s")
        metric_error.metric("Prequential Error Rate", f"{error_rate:.1f}%")
        
        if i >= 35 and i < 55:
            metric_accuracy.metric("Ensemble Accuracy", f"{current_acc:.1f}%", f"-{drift_severity * 1.5:.1f}%")
            metric_status.metric("ADWIN Drift Detector", "CONCEPT DRIFT DETECTED", "Warning")
        elif i >= 55:
            metric_accuracy.metric("Ensemble Accuracy", f"{current_acc:.1f}%", "+ Recovering")
            metric_status.metric("ADWIN Drift Detector", "MODEL ADAPTED", "Stable")
        else:
            metric_accuracy.metric("Ensemble Accuracy", f"{current_acc:.1f}%", "Stationary")
            metric_status.metric("ADWIN Drift Detector", "STATIONARY STREAM", "Stable")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=stream_values, mode='lines', name='Stream Target Variable', line=dict(color='purple')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=model_accuracy, mode='lines', name='Model Predictive Accuracy (%)', yaxis='y2', line=dict(color='green', dash='dot')))
        
        fig.update_layout(
            title="Data Stream Mining: Concept Drift vs Real-Time Ensemble Adaptation",
            xaxis=dict(title="High-Frequency Stream Timeline"),
            yaxis=dict(title="Target Variable Value"),
            yaxis2=dict(title="Accuracy (%)", overlaying='y', side='right', range=[40, 100]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if i == 35:
            log_placeholder.error(f"DRIFT ALERT: Sudden statistical distribution shift detected at {time_steps[i].strftime('%H:%M:%S')}. Prequential error rate exceeding ADWIN thresholds.")
        elif i == 55:
            log_placeholder.warning(f"ORCHESTRATION: AWS Lambda replacing deprecated Hoeffding Trees in the background ensemble. New models training on post-drift data distribution.")
        elif i > 55 and i % 5 == 0:
            log_placeholder.success(f"STREAM LOG: Ensemble adapted successfully. Predictive accuracy recovering to baseline levels.")
        elif i < 35 and i % 5 == 0:
            log_placeholder.info(f"Log: Telemetry tick {i} ingested via serverless middleware. Data distribution remains stationary.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless cloud pipeline successfully detected concept drift and dynamically adapted the online ensemble learning model.")
else:
    st.info("Click 'Initialize Stream Mining Engine' in the sidebar to simulate high-frequency data stream processing.")