from datetime import datetime, timedelta, timezone

from src.anomaly_detection.detector import AnomalyDetector
from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry
from src.recommendations.engine import RecommendationEngine
from src.self_healing.workflow import SelfHealingWorkflow


def create_processed_records():
    """Create deterministic telemetry for the integration test."""

    base_timestamp = datetime.now(timezone.utc)

    return [
        ProcessedTelemetry(
            timestamp=base_timestamp + timedelta(seconds=index),
            cpu_percent=30.0,
            memory_percent=45.0,
            swap_percent=0.0,
            disk_percent=disk,
            load_1m=0.5,
            process_count=100,
            disk_read_rate=0.0,
            disk_write_rate=0.0,
            network_send_rate=0.0,
            network_receive_rate=0.0,
            top_cpu_process="test-process",
            top_memory_process="test-process",
        )
        for index, disk in enumerate(
            [50.0, 55.0, 60.0, 95.0]
        )
    ]


def test_complete_monitoring_to_healing_pipeline():
    """Verify the complete monitoring-to-healing workflow."""

    records = create_processed_records()

    # 1. Anomaly detection
    anomaly_detector = AnomalyDetector()

    anomalies = []

    for record in records:
        anomalies.extend(
            anomaly_detector.detect(record)
        )

    assert anomalies
    assert any(
        anomaly.metric == "disk_percent"
        for anomaly in anomalies
    )

    disk_anomaly = next(
        anomaly
        for anomaly in anomalies
        if anomaly.metric == "disk_percent"
    )

    # 2. Recommendation generation
    recommendation_engine = RecommendationEngine()

    recommendations = (
        recommendation_engine.generate_from_anomaly(
            disk_anomaly
        )
    )

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.metric == "disk_percent"

    # 3. Create human-approved healing action
    workflow = SelfHealingWorkflow()

    healing_action = workflow.create_action(
        recommendation
    )

    assert healing_action is not None
    assert healing_action.action == "clear_cache"
    assert healing_action.status == "pending"

    # 4. Human approval
    approved_action = workflow.approve(
        healing_action
    )

    assert approved_action.status == "approved"

    # 5. Execute approved action
    audit = workflow.execute(
        approved_action
    )

    # 6. Verify execution and audit result
    assert audit.approval_status == "approved"
    assert audit.execution_status == "success"
    assert audit.error is None
