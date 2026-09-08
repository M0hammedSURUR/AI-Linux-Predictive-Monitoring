from datetime import datetime, timezone

from src.prediction.models import PredictionResult
from src.recommendations.engine import RecommendationEngine
from src.self_healing.engine import SelfHealingEngine
from src.self_healing.models import HealingAction


def test_high_risk_prediction_creates_healing_action():
    # Simulated high-risk prediction
    prediction = PredictionResult(
        timestamp=datetime.now(timezone.utc),
        metric="cpu_percent",
        current_value=75.0,
        predicted_value=85.0,
        threshold=80.0,
        risk_level="high",
        message="CPU usage is predicted to exceed the threshold.",
    )

    # Generate recommendation
    recommendation_engine = RecommendationEngine()

    recommendations = (
        recommendation_engine.generate_from_prediction(
            prediction
        )
    )

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    # Create proposed healing action
    healing_action = HealingAction(
        timestamp=recommendation.timestamp,
        metric=recommendation.metric,
        action=recommendation.suggested_action,
        reason=recommendation.description,
        status="pending",
    )

    # Verify initial state
    assert healing_action.status == "pending"

    # Human approves the action
    healing_engine = SelfHealingEngine()

    approved_action = healing_engine.approve(
        healing_action
    )

    assert approved_action.status == "approved"

def test_pending_healing_action_can_be_rejected():
    # Create a simulated healing action
    healing_action = HealingAction(
        timestamp=datetime.now(timezone.utc),
        metric="memory_percent",
        action="Inspect memory-intensive processes.",
        reason="Memory usage is predicted to become high.",
        status="pending",
    )

    # Human rejects the action
    healing_engine = SelfHealingEngine()

    rejected_action = healing_engine.reject(
        healing_action
    )

    assert rejected_action.status == "rejected"
