import streamlit as st
import pandas as pd

from src.database.database import initialize_database
from src.database.repository import TelemetryRepository

# NEW: Import prediction result model for safe dashboard simulation
from src.prediction.models import PredictionResult

# NEW: Import preprocessing and anomaly detection
from src.preprocessing.telemetry_preprocessor import TelemetryPreprocessor
from src.anomaly_detection.detector import AnomalyDetector
from src.anomaly_detection.ml_detector import MLAnomalyDetector
from src.anomaly_detection.combined_detector import CombinedAnomalyDetector

# NEW: Import prediction engine
from src.prediction.predictor import TelemetryPredictor

# NEW: Import recommendation engine
from src.recommendations.engine import RecommendationEngine

# NEW: Import the complete self-healing workflow
from src.self_healing.workflow import SelfHealingWorkflow


# Initialize the SQLite database
initialize_database()


# Configure the Streamlit dashboard
st.set_page_config(
    page_title="AI Linux Predictive Monitoring",
    page_icon="🖥️",
    layout="wide",
)


# Dashboard title
st.title("AI-Powered Linux Predictive Monitoring")

st.caption(
    "Real-time Linux system monitoring, anomaly detection, "
    "prediction, and human-approved self-healing."
)


# NEW: Store healing action statuses across Streamlit reruns
if "healing_statuses" not in st.session_state:
    st.session_state.healing_statuses = {}


# NEW: Store execution results across Streamlit reruns
if "healing_execution_results" not in st.session_state:
    st.session_state.healing_execution_results = {}


# NEW: Create the complete self-healing workflow
self_healing_workflow = SelfHealingWorkflow()


# Create the telemetry repository
repository = TelemetryRepository()


# Load recent telemetry records from SQLite
records = repository.get_recent_records(limit=20)


# Handle an empty telemetry database
if not records:
    st.warning(
        "No telemetry data is available in the database yet. "
        "Start the telemetry collector to generate data."
    )
    st.stop()


# Get the latest telemetry record
latest = records[-1]


# Display actual telemetry values
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "CPU Usage",
        f"{latest.cpu_percent:.1f}%",
    )

with col2:
    st.metric(
        "Memory Usage",
        f"{latest.memory_percent:.1f}%",
    )

with col3:
    st.metric(
        "Disk Usage",
        f"{latest.disk_percent:.1f}%",
    )

with col4:
    st.metric(
        "System Load",
        f"{latest.load_1m:.2f}",
    )


st.divider()


# Display the timestamp of the latest telemetry record
st.subheader("Latest Telemetry")

st.write(
    f"Last updated: **{latest.timestamp}**"
)


# Convert telemetry records into a DataFrame
telemetry_data = pd.DataFrame(
    [
        {
            "Timestamp": record.timestamp,
            "CPU Usage": record.cpu_percent,
            "Memory Usage": record.memory_percent,
            "Disk Usage": record.disk_percent,
            "System Load": record.load_1m,
        }
        for record in records
    ]
)

# Set timestamp as the DataFrame index
telemetry_data = telemetry_data.set_index("Timestamp")


# System monitoring charts
st.subheader("System Monitoring")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### CPU Usage")
    st.line_chart(
        telemetry_data["CPU Usage"],
        y_label="Usage (%)",
    )

with chart_col2:
    st.markdown("#### Memory Usage")
    st.line_chart(
        telemetry_data["Memory Usage"],
        y_label="Usage (%)",
    )


chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown("#### Disk Usage")
    st.line_chart(
        telemetry_data["Disk Usage"],
        y_label="Usage (%)",
    )

with chart_col4:
    st.markdown("#### System Load")
    st.line_chart(
        telemetry_data["System Load"],
        y_label="Load",
    )


# Recent telemetry table
st.subheader("Recent Telemetry")

telemetry_rows = [
    {
        "Timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "CPU (%)": round(record.cpu_percent, 1),
        "Memory (%)": round(record.memory_percent, 1),
        "Swap (%)": round(record.swap_percent, 1),
        "Disk (%)": round(record.disk_percent, 1),
        "Load": round(record.load_1m, 2),
        "Processes": record.process_count,
    }
    for record in records
]

st.dataframe(
    telemetry_rows,
    width="stretch",
    hide_index=True,
)


# ============================================================
# Anomaly Detection
# ============================================================

st.subheader("Anomaly Detection")

# Create the telemetry preprocessor
preprocessor = TelemetryPreprocessor(repository)

# Convert raw telemetry into processed telemetry
processed_records = preprocessor.process(limit=20)

# Create the rule-based anomaly detector
anomaly_detector = AnomalyDetector()

# Create the experimental ML anomaly detector
ml_detector = MLAnomalyDetector(
    contamination=0.23,
    random_state=42,
)

# Create the combined analysis layer
combined_detector = CombinedAnomalyDetector()

# Detect rule-based anomalies
anomaly_results = [
    anomaly
    for record in processed_records
    for anomaly in anomaly_detector.detect(record)
]

# Get only the detected rule-based anomalies
active_anomalies = [
    result
    for result in anomaly_results
    if result.is_anomaly
]

# Run ML detection only when enough telemetry records are available
ml_predictions = []

if len(processed_records) >= 10:
    try:
        ml_detector.fit(processed_records)
        ml_predictions = ml_detector.predict(processed_records)
    except ValueError:
        ml_predictions = [False] * len(processed_records)
else:
    ml_predictions = [False] * len(processed_records)


# Combine rule-based and ML results
combined_results = []

for index, record in enumerate(processed_records):
    rule_anomalies = anomaly_detector.detect(record)

    combined_result = combined_detector.analyze(
        telemetry=record,
        rule_anomalies=rule_anomalies,
        ml_is_anomaly=ml_predictions[index],
    )

    combined_results.append(combined_result)


# Display rule-based anomaly status
if not active_anomalies:
    st.success("No active rule-based anomalies detected.")
else:
    st.warning(
        f"{len(active_anomalies)} rule-based anomaly/anomalies detected."
    )

    for anomaly in active_anomalies:
        st.error(
            f"**Anomaly detected at {anomaly.timestamp}**"
        )

        st.write(f"**Metric:** {anomaly.metric}")
        st.write(f"**Observed value:** {anomaly.observed_value:.2f}")
        st.write(f"**Threshold:** {anomaly.threshold:.2f}")
        st.write(f"**Severity:** {anomaly.severity}")
        st.write(f"**Explanation:** {anomaly.explanation}")


# Display ML status separately because it is experimental
ml_anomaly_count = sum(ml_predictions)

st.info(
    f"Experimental ML detection: {ml_anomaly_count} "
    "unusual pattern(s) identified."
)


# Display combined analysis
for result in combined_results:
    if result.confidence == "normal":
        continue

    if result.confidence == "experimental":
        st.info(
            f"**Experimental ML signal at {result.telemetry.timestamp}**"
        )
    elif result.confidence == "high":
        st.warning(
            f"**High-confidence anomaly at "
            f"{result.telemetry.timestamp}**"
        )
    else:
        st.warning(
            f"**Rule-based anomaly at "
            f"{result.telemetry.timestamp}**"
        )

    st.write(f"**Confidence:** {result.confidence}")
    st.write(f"**Explanation:** {result.explanation}")


# ============================================================
# Predictions
# ============================================================

st.subheader("Predictions")

# Create the prediction engine
predictor = TelemetryPredictor()

# Generate predictions from processed telemetry
prediction_results = predictor.predict(processed_records)

# NEW: Safe simulation mode for testing the self-healing workflow
simulation_mode = st.sidebar.checkbox(
    "Enable Self-Healing Simulation"
)

if simulation_mode:
    simulated_prediction = PredictionResult(
        timestamp=latest.timestamp,
        metric="disk_percent",
        current_value=85.0,
        predicted_value=95.0,
        threshold=90.0,
        risk_level="high",
        message=(
            "SIMULATION: Disk usage is predicted to exceed "
            "the configured threshold."
        ),
    )

    prediction_results.append(simulated_prediction)

    st.sidebar.warning(
        "Simulation mode is active. No real system action "
        "will be executed. Any healing action still requires "
        "human approval."
    )

# Display prediction results
if not prediction_results:
    st.info(
        "Not enough telemetry data available to generate predictions."
    )
else:
    for prediction in prediction_results:

        # Display risk level
        if prediction.risk_level == "high":
            st.error(
                f"🔴 **{prediction.metric} — HIGH RISK**"
            )
        elif prediction.risk_level == "medium":
            st.warning(
                f"🟠 **{prediction.metric} — MEDIUM RISK**"
            )
        else:
            st.success(
                f"🟢 **{prediction.metric} — LOW RISK**"
            )

        # Display prediction details
        prediction_col1, prediction_col2, prediction_col3 = st.columns(3)

        with prediction_col1:
            st.metric(
                "Current Value",
                f"{prediction.current_value:.1f}%",
            )

        with prediction_col2:
            st.metric(
                "Predicted Value",
                f"{prediction.predicted_value:.1f}%",
            )

        with prediction_col3:
            st.metric(
                "Threshold",
                f"{prediction.threshold:.1f}%",
            )

        st.write(prediction.message)

        st.divider()


# ============================================================
# Recommendations
# ============================================================

st.subheader("Recommendations")

# Create the recommendation engine
recommendation_engine = RecommendationEngine()

# Store generated recommendations
recommendations = []


# Generate recommendations from detected anomalies
for anomaly in active_anomalies:
    recommendations.extend(
        recommendation_engine.generate_from_anomaly(anomaly)
    )


# Generate recommendations from high-risk predictions
for prediction in prediction_results:
    recommendations.extend(
        recommendation_engine.generate_from_prediction(prediction)
    )


# Display recommendations
if not recommendations:
    st.success(
        "No actions are currently recommended."
    )
else:
    st.warning(
        f"{len(recommendations)} recommendation(s) require attention."
    )

    for recommendation in recommendations:

        st.markdown(
            f"### {recommendation.title}"
        )

        st.write(
            f"**Severity:** {recommendation.severity}"
        )

        st.write(
            f"**Description:** {recommendation.description}"
        )

        st.info(
            f"**Suggested Action:** "
            f"{recommendation.suggested_action}"
        )

        st.divider()


# ============================================================
# Human-Approved Self-Healing
# ============================================================

st.subheader("Human-Approved Self-Healing")

st.caption(
    "Healing actions require explicit human approval. "
    "Only predefined actions can be executed."
)


# NEW: Convert recommendations using the complete workflow
healing_actions = []

for index, recommendation in enumerate(recommendations):

    # NEW: Create a stable key for this healing action
    action_key = (
        f"{recommendation.timestamp.isoformat()}_"
        f"{recommendation.metric}_"
        f"{index}"
    )

    # NEW: Create a healing action through the workflow
    healing_action = self_healing_workflow.create_action(
        recommendation
    )

    # NEW: Skip recommendations without a safe action mapping
    if healing_action is None:
        continue

    # NEW: Restore approval status after Streamlit rerun
    stored_status = st.session_state.healing_statuses.get(
        action_key,
        "pending",
    )

    healing_action.status = stored_status

    healing_actions.append(
        (action_key, healing_action)
    )


# Display healing actions
if not healing_actions:
    st.success(
        "No healing actions are waiting for approval."
    )
else:

    for action_key, healing_action in healing_actions:

        st.markdown(
            f"### Proposed Action — {healing_action.metric}"
        )

        st.write(
            f"**Reason:** {healing_action.reason}"
        )

        st.info(
            f"**Predefined Action:** `{healing_action.action}`"
        )

        st.write(
            f"**Status:** `{healing_action.status.upper()}`"
        )


        # NEW: Only pending actions can be approved or rejected
        if healing_action.status == "pending":

            approve_col, reject_col = st.columns(2)

            with approve_col:
                if st.button(
                    "✅ Approve",
                    key=f"approve_{action_key}",
                ):
                    approved_action = (
                        self_healing_workflow.approve(
                            healing_action
                        )
                    )

                    st.session_state.healing_statuses[
                        action_key
                    ] = approved_action.status

                    st.rerun()


            with reject_col:
                if st.button(
                    "❌ Reject",
                    key=f"reject_{action_key}",
                ):
                    rejected_action = (
                        self_healing_workflow.reject(
                            healing_action
                        )
                    )

                    st.session_state.healing_statuses[
                        action_key
                    ] = rejected_action.status

                    st.rerun()


        # NEW: Approved actions can be explicitly executed
        elif healing_action.status == "approved":

            st.success(
                "Action approved by the human operator."
            )

            # NEW: Check whether this action has already been executed
            execution_result = (
                st.session_state.healing_execution_results.get(
                    action_key
                )
            )

            if execution_result is None:

                st.warning(
                    "Execution requires a separate operator action."
                )

                if st.button(
                    "▶️ Execute Approved Action",
                    key=f"execute_{action_key}",
                ):
                    audit = self_healing_workflow.execute(
                        healing_action
                    )

                    # NEW: Store execution result across reruns
                    st.session_state.healing_execution_results[
                        action_key
                    ] = audit

                    st.rerun()

            else:

                # NEW: Display the persisted execution result
                if execution_result.execution_status == "success":
                    st.success(
                        "Healing action executed successfully."
                    )
                else:
                    st.error(
                        "Healing action execution failed."
                    )

                st.write(
                    f"**Execution Status:** "
                    f"`{execution_result.execution_status.upper()}`"
                )

                st.write(
                    f"**Result:** {execution_result.result}"
                )

                if execution_result.error:
                    st.error(
                        f"**Error:** {execution_result.error}"
                    )


        # NEW: Rejected actions are already audited by the workflow
        elif healing_action.status == "rejected":

            st.error(
                "Action rejected by the human operator."
            )

            st.caption(
                "The rejection has been recorded in the audit log."
            )


        st.divider()
