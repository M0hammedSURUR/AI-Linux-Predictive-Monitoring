from dataclasses import dataclass

from src.anomaly_detection.models import AnomalyResult
from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry


@dataclass
class CombinedAnomalyResult:
    """Represents the combined rule-based and ML analysis result."""

    telemetry: ProcessedTelemetry
    rule_anomalies: list[AnomalyResult]
    ml_is_anomaly: bool
    confidence: str
    explanation: str


class CombinedAnomalyDetector:
    """
    Combine rule-based anomaly detection with ML anomaly detection.

    Rule-based detection remains the primary known-condition signal.
    ML detection provides an additional experimental signal.
    """

    def analyze(
        self,
        telemetry: ProcessedTelemetry,
        rule_anomalies: list[AnomalyResult],
        ml_is_anomaly: bool,
    ) -> CombinedAnomalyResult:
        """Combine rule-based and ML anomaly signals."""

        rule_is_anomaly = bool(rule_anomalies)

        if rule_is_anomaly and ml_is_anomaly:
            confidence = "high"
            explanation = (
                "Both rule-based and ML detection identified an "
                "unusual system condition."
            )

        elif rule_is_anomaly:
            confidence = "medium"
            explanation = (
                "Rule-based detection identified a known threshold "
                "violation. ML detection did not identify an anomaly."
            )

        elif ml_is_anomaly:
            confidence = "experimental"
            explanation = (
                "ML detection identified an unusual telemetry pattern, "
                "but no configured rule-based threshold was exceeded."
            )

        else:
            confidence = "normal"
            explanation = (
                "Neither rule-based nor ML detection identified "
                "an abnormal condition."
            )

        return CombinedAnomalyResult(
            telemetry=telemetry,
            rule_anomalies=rule_anomalies,
            ml_is_anomaly=ml_is_anomaly,
            confidence=confidence,
            explanation=explanation,
        )
