import streamlit as st
import pandas as pd
from pathlib import Path

from streamlit import fragment

from src.database.database import initialize_database
from src.database.repository import TelemetryRepository

from src.preprocessing.telemetry_preprocessor import (
    TelemetryPreprocessor,
)

from src.anomaly_detection.detector import AnomalyDetector
from src.anomaly_detection.ml_detector import MLAnomalyDetector
from src.anomaly_detection.combined_detector import (
    CombinedAnomalyDetector,
)

from src.prediction.predictor import TelemetryPredictor
from src.prediction.models import PredictionResult

from src.recommendations.engine import RecommendationEngine

from src.self_healing.workflow import SelfHealingWorkflow

from src.service_monitor.systemd_monitor import (
    SystemdServiceMonitor,
)

from src.log_monitor.journal_monitor import JournalMonitor


# ============================================================
# Database initialization
# ============================================================

initialize_database()


# ============================================================
# Streamlit configuration
# ============================================================

st.set_page_config(
    page_title="AI Linux Predictive Monitoring",
    page_icon="🖥️",
    layout="wide",
)


st.title("AI-Powered Linux Predictive Monitoring")

st.caption(
    "Real-time Linux system monitoring, anomaly detection, "
    "prediction, and human-approved self-healing."
)


# ============================================================
# Streamlit session state
# ============================================================

if "healing_statuses" not in st.session_state:
    st.session_state.healing_statuses = {}


if "healing_execution_results" not in st.session_state:
    st.session_state.healing_execution_results = {}


# ============================================================
# Dashboard
# ============================================================

@fragment(run_every="5s")
def dashboard():

    self_healing_workflow = SelfHealingWorkflow()

    # --------------------------------------------------------
    # Telemetry
    # --------------------------------------------------------

    repository = TelemetryRepository()

    records = repository.get_recent_records(limit=20)

    if not records:
        st.warning(
            "No telemetry data is available in the database yet. "
            "Start the telemetry collector to generate data."
        )
        st.stop()

    latest = records[-1]

    # --------------------------------------------------------
    # Current telemetry metrics
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Latest telemetry
    # --------------------------------------------------------

    st.subheader("Latest Telemetry")

    st.write(
        f"Last updated: **{latest.timestamp}**"
    )

    # --------------------------------------------------------
    # Telemetry DataFrame
    # --------------------------------------------------------

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

    telemetry_data = telemetry_data.set_index("Timestamp")

    # --------------------------------------------------------
    # System monitoring charts
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Recent telemetry table
    # --------------------------------------------------------

    st.subheader("Recent Telemetry")

    telemetry_rows = [
        {
            "Timestamp": record.timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
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

    # ========================================================
    # Anomaly Detection
    # ========================================================

    st.subheader("Anomaly Detection")

    preprocessor = TelemetryPreprocessor(repository)

    processed_records = preprocessor.process(limit=20)

    anomaly_detector = AnomalyDetector()

    ml_detector = MLAnomalyDetector(
        contamination=0.23,
        random_state=42,
    )

    combined_detector = CombinedAnomalyDetector()

    # --------------------------------------------------------
    # Rule-based anomalies
    # --------------------------------------------------------

    anomaly_results = [
        anomaly
        for record in processed_records
        for anomaly in anomaly_detector.detect(record)
    ]

    active_anomalies = [
        result
        for result in anomaly_results
        if result.is_anomaly
    ]

    # --------------------------------------------------------
    # ML anomaly detection
    # --------------------------------------------------------

    ml_predictions = []

    if len(processed_records) >= 10:

        try:
            ml_detector.fit(processed_records)

            ml_predictions = ml_detector.predict(
                processed_records
            )

        except ValueError:

            ml_predictions = [
                False
                for _ in processed_records
            ]

    else:

        ml_predictions = [
            False
            for _ in processed_records
        ]

    # --------------------------------------------------------
    # Combined analysis
    # --------------------------------------------------------

    combined_results = []

    for index, record in enumerate(processed_records):

        rule_anomalies = anomaly_detector.detect(record)

        combined_result = combined_detector.analyze(
            telemetry=record,
            rule_anomalies=rule_anomalies,
            ml_is_anomaly=ml_predictions[index],
        )

        combined_results.append(combined_result)

    # --------------------------------------------------------
    # Rule-based anomaly status
    # --------------------------------------------------------

    if not active_anomalies:

        st.success(
            "No active rule-based anomalies detected."
        )

    else:

        st.warning(
            f"{len(active_anomalies)} "
            "rule-based anomaly/anomalies detected."
        )

        for anomaly in active_anomalies:

            st.error(
                f"**Anomaly detected at "
                f"{anomaly.timestamp}**"
            )

            st.write(
                f"**Metric:** {anomaly.metric}"
            )

            st.write(
                f"**Observed value:** "
                f"{anomaly.observed_value:.2f}"
            )

            st.write(
                f"**Threshold:** "
                f"{anomaly.threshold:.2f}"
            )

            st.write(
                f"**Severity:** {anomaly.severity}"
            )

            st.write(
                f"**Explanation:** "
                f"{anomaly.explanation}"
            )

    # --------------------------------------------------------
    # ML status
    # --------------------------------------------------------

    ml_anomaly_count = sum(ml_predictions)

    st.info(
        f"Experimental ML detection: "
        f"{ml_anomaly_count} unusual pattern(s) identified."
    )

    # --------------------------------------------------------
    # Combined analysis display
    # --------------------------------------------------------

    for result in combined_results:

        if result.confidence == "normal":
            continue

        if result.confidence == "experimental":

            st.info(
                f"**Experimental ML signal at "
                f"{result.telemetry.timestamp}**"
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

        st.write(
            f"**Confidence:** {result.confidence}"
        )

        st.write(
            f"**Explanation:** {result.explanation}"
        )

    # ========================================================
    # Overall System Health
    # ========================================================

    st.subheader("Overall System Health")

    critical_anomalies = [
        anomaly
        for anomaly in active_anomalies
        if anomaly.severity == "critical"
    ]

    high_anomalies = [
        anomaly
        for anomaly in active_anomalies
        if anomaly.severity == "high"
    ]

    if critical_anomalies:

        st.error(
            "🔴 CRITICAL — Critical system anomalies detected."
        )

    elif high_anomalies:

        st.warning(
            "🟡 WARNING — High-severity system anomalies detected."
        )

    elif active_anomalies:

        st.warning(
            "🟡 WARNING — System anomalies detected."
        )

    elif ml_anomaly_count > 0:

        st.info(
            "🟡 WARNING — Experimental ML signals detected."
        )

    else:

        st.success(
            "🟢 HEALTHY — No significant system anomalies detected."
        )

    # ========================================================
    # Predictions
    # ========================================================

    st.subheader("Predictions")

    predictor = TelemetryPredictor()

    prediction_results = predictor.predict(
        processed_records
    )

    # --------------------------------------------------------
    # Self-healing simulation mode
    # --------------------------------------------------------

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

        prediction_results.append(
            simulated_prediction
        )

        st.sidebar.warning(
            "Simulation mode is active. "
            "No real system action will be executed. "
            "Healing actions still require human approval."
        )

    # --------------------------------------------------------
    # Prediction display
    # --------------------------------------------------------

    if not prediction_results:

        st.info(
            "Not enough telemetry data available "
            "to generate predictions."
        )

    else:

        for prediction in prediction_results:

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

            prediction_col1, prediction_col2, prediction_col3 = (
                st.columns(3)
            )

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

            st.write(
                prediction.message
            )

            st.divider()

    # ========================================================
    # Recommendations
    # ========================================================

    st.subheader("Recommendations")

    recommendation_engine = RecommendationEngine()

    recommendations = []

    # --------------------------------------------------------
    # Recommendations from anomalies
    # --------------------------------------------------------

    for anomaly in active_anomalies:

        recommendations.extend(
            recommendation_engine.generate_from_anomaly(
                anomaly
            )
        )

    # --------------------------------------------------------
    # Recommendations from predictions
    # --------------------------------------------------------

    for prediction in prediction_results:

        recommendations.extend(
            recommendation_engine.generate_from_prediction(
                prediction
            )
        )

    # --------------------------------------------------------
    # Recommendation display
    # --------------------------------------------------------

    if not recommendations:

        st.success(
            "No actions are currently recommended."
        )

    else:

        st.warning(
            f"{len(recommendations)} "
            "recommendation(s) require attention."
        )

        for recommendation in recommendations:

            st.markdown(
                f"### {recommendation.title}"
            )

            st.write(
                f"**Severity:** "
                f"{recommendation.severity}"
            )

            st.write(
                f"**Description:** "
                f"{recommendation.description}"
            )

            st.info(
                f"**Suggested Action:** "
                f"{recommendation.suggested_action}"
            )

            st.divider()

    # ========================================================
    # Linux Service Monitoring
    # ========================================================

    st.subheader("Linux Service Monitoring")

    service_config_path = Path(
        "config/services.json"
    )

    if service_config_path.exists():

        service_monitor = (
            SystemdServiceMonitor.from_config(
                service_config_path
            )
        )

        service_statuses = (
            service_monitor.check_all()
        )

        if service_statuses:

            for service in service_statuses:

                if service.status == "active":

                    st.success(
                        f"**{service.service_name}** — "
                        f"{service.status}"
                    )

                elif service.status == "failed":

                    st.error(
                        f"**{service.service_name}** — "
                        f"{service.status}"
                    )

                else:

                    st.warning(
                        f"**{service.service_name}** — "
                        f"{service.status}"
                    )

                st.caption(
                    service.description
                )

        else:

            st.info(
                "No services are configured for monitoring."
            )

    else:

        st.warning(
            "Service monitoring configuration file "
            "was not found."
        )

    # ========================================================
    # Linux Log Monitoring
    # ========================================================

    st.subheader("Linux Log Monitoring")

    log_monitor = JournalMonitor(
        limit=10
    )

    log_entries = (
        log_monitor.get_recent_warnings_and_errors()
    )

    if log_entries:

        for entry in log_entries:

            st.warning(
                f"**{entry.source}** — "
                f"{entry.message}"
            )

            st.caption(
                entry.timestamp
            )

    else:

        st.info(
            "No recent warning or error journal entries found."
        )

    # ========================================================
    # Human-Approved Self-Healing
    # ========================================================

    st.subheader(
        "Human-Approved Self-Healing"
    )

    st.caption(
        "Healing actions require explicit human approval. "
        "Only predefined actions can be executed."
    )

    # --------------------------------------------------------
    # Create healing actions
    # --------------------------------------------------------

    healing_actions = []

    for recommendation in recommendations:

        action_key = (
            f"{recommendation.metric}_"
            f"{recommendation.suggested_action}_"
            f"{recommendation.title}"
        )

        healing_action = (
            self_healing_workflow.create_action(
                recommendation
            )
        )

        if healing_action is None:
            continue

        stored_status = (
            st.session_state.healing_statuses.get(
                action_key,
                "pending",
            )
        )

        healing_action.status = stored_status

        healing_actions.append(
            (
                action_key,
                healing_action,
            )
        )

    # --------------------------------------------------------
    # No healing actions
    # --------------------------------------------------------

    if not healing_actions:

        st.success(
            "No healing actions are waiting for approval."
        )

    # --------------------------------------------------------
    # Display healing actions
    # --------------------------------------------------------

    else:

        for action_key, healing_action in healing_actions:

            st.markdown(
                f"### Proposed Action — "
                f"{healing_action.metric}"
            )

            st.write(
                f"**Reason:** "
                f"{healing_action.reason}"
            )

            st.info(
                f"**Predefined Action:** "
                f"`{healing_action.action}`"
            )

            st.write(
                f"**Status:** "
                f"`{healing_action.status.upper()}`"
            )

            # ------------------------------------------------
            # Pending action
            # ------------------------------------------------

            if healing_action.status == "pending":

                approve_col, reject_col = (
                    st.columns(2)
                )

                with approve_col:

                    if st.button(
                        "✅ Approve Action",
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
                        "❌ Reject Action",
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

            # ------------------------------------------------
            # Rejected action
            # ------------------------------------------------

            elif healing_action.status == "rejected":

                st.error(
                    "Action rejected by the human operator."
                )

                st.caption(
                    "The rejection has been recorded "
                    "in the audit log."
                )

            # ------------------------------------------------
            # Approved action
            # ------------------------------------------------

            elif healing_action.status == "approved":

                st.success(
                    "Action approved by the human operator."
                )

                execution_result = (
                    st.session_state.healing_execution_results.get(
                        action_key
                    )
                )

                # --------------------------------------------
                # Action has not been executed yet
                # --------------------------------------------

                if execution_result is None:

                    st.warning(
                        "Execution requires a separate "
                        "operator action."
                    )

                    if st.button(
                        "▶️ Execute Approved Action",
                        key=f"execute_{action_key}",
                    ):

                        audit = (
                            self_healing_workflow.execute(
                                healing_action,
                                simulation=simulation_mode,
                            )
                        )

                        st.session_state.healing_execution_results[
                            action_key
                        ] = audit

                        st.rerun()

                # --------------------------------------------
                # Action already executed
                # --------------------------------------------

                else:

                    if (
                        execution_result.execution_status
                        == "success"
                    ):

                        st.success(
                            "Healing action executed successfully."
                        )

                    elif (
                        execution_result.execution_status
                        == "simulated"
                    ):

                        st.info(
                            "Simulation completed successfully. "
                            "No real system action was executed."
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
                        f"**Result:** "
                        f"{execution_result.result}"
                    )

                    if execution_result.error:

                        st.error(
                            f"**Error:** "
                            f"{execution_result.error}"
                        )

            st.divider()


# ============================================================
# Start dashboard
# ============================================================

dashboard()
