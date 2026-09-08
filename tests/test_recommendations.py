from datetime import datetime, timezone

from src.anomaly_detection.models import AnomalyResult
from src.prediction.models import PredictionResult
from src.recommendations.engine import RecommendationEngine


def test_high_cpu_anomaly_generates_recommendation():
    """Verify that a high CPU anomaly produces a recommendation."""

    engine = RecommendationEngine()

    anomaly = AnomalyResult(
        timestamp=datetime.now(timezone.utc),
        is_anomaly=True,
        metric="cpu_percent",
        observed_value=95.0,
        threshold=80.0,
        severity="high",
        explanation="High CPU usage",
    )

    recommendations = engine.generate_from_anomaly(anomaly)

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.metric == "cpu_percent"
    assert recommendation.severity == "high"
    assert recommendation.title == "High CPU Usage"
    assert "CPU" in recommendation.description
    assert "process" in recommendation.suggested_action


def test_normal_condition_generates_no_recommendation():
    """Verify that normal conditions produce no recommendation."""

    engine = RecommendationEngine()

    anomaly = AnomalyResult(
        timestamp=datetime.now(timezone.utc),
        is_anomaly=False,
        metric=None,
        observed_value=None,
        threshold=None,
        severity="low",
        explanation="Normal system condition",
    )

    recommendations = engine.generate_from_anomaly(anomaly)

    assert recommendations == []


def test_high_risk_prediction_generates_recommendation():
    """Verify that a high-risk prediction produces a recommendation."""

    engine = RecommendationEngine()

    prediction = PredictionResult(
        timestamp=datetime.now(timezone.utc),
        metric="cpu_percent",
        current_value=85.0,
        predicted_value=95.0,
        threshold=80.0,
        risk_level="high",
        message="CPU usage is predicted to exceed the threshold.",
    )

    recommendations = engine.generate_from_prediction(prediction)

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.metric == "cpu_percent"
    assert recommendation.severity == "high"
    assert "Predicted High" in recommendation.title
    assert "95.0%" in recommendation.description


def test_low_risk_prediction_generates_no_recommendation():
    """Verify that a low-risk prediction produces no recommendation."""

    engine = RecommendationEngine()

    prediction = PredictionResult(
        timestamp=datetime.now(timezone.utc),
        metric="memory_percent",
        current_value=40.0,
        predicted_value=45.0,
        threshold=80.0,
        risk_level="low",
        message="Memory usage is stable.",
    )

    recommendations = engine.generate_from_prediction(prediction)

    assert recommendations == []

def test_high_memory_anomaly_generates_recommendation():
    """Verify that a high memory anomaly produces a recommendation."""

    engine = RecommendationEngine()

    # NEW: Create a high memory anomaly
    anomaly = AnomalyResult(
        timestamp=datetime.now(timezone.utc),
        is_anomaly=True,
        metric="memory_percent",
        observed_value=92.0,
        threshold=80.0,
        severity="high",
        explanation="High memory usage",
    )

    recommendations = engine.generate_from_anomaly(anomaly)

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.metric == "memory_percent"
    assert recommendation.severity == "high"
    assert recommendation.title == "High Memory Usage"
    assert "memory" in recommendation.description.lower()


def test_high_disk_anomaly_generates_recommendation():
    """Verify that a high disk anomaly produces a recommendation."""

    engine = RecommendationEngine()

    # NEW: Create a high disk anomaly
    anomaly = AnomalyResult(
        timestamp=datetime.now(timezone.utc),
        is_anomaly=True,
        metric="disk_percent",
        observed_value=95.0,
        threshold=90.0,
        severity="high",
        explanation="High disk usage",
    )

    recommendations = engine.generate_from_anomaly(anomaly)

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.metric == "disk_percent"
    assert recommendation.severity == "high"
    assert recommendation.title == "High Disk Usage"
    assert "disk" in recommendation.description.lower()


def test_high_load_anomaly_generates_recommendation():
    """Verify that a high system load anomaly produces a recommendation."""

    engine = RecommendationEngine()

    # NEW: Create a high system load anomaly
    anomaly = AnomalyResult(
        timestamp=datetime.now(timezone.utc),
        is_anomaly=True,
        metric="load_1m",
        observed_value=5.0,
        threshold=4.0,
        severity="high",
        explanation="High system load",
    )

    recommendations = engine.generate_from_anomaly(anomaly)

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.metric == "load_1m"
    assert recommendation.severity == "high"
    assert recommendation.title == "High System Load"
    assert "load" in recommendation.description.lower()
