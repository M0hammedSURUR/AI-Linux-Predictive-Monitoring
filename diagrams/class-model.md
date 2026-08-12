TelemetryCollector
        │
        ▼
TelemetryRecord
        │
        ▼
Preprocessor
        │
        ▼
FeatureRecord
        │
        ├───────────────┐
        ▼               ▼
AnomalyDetector    PredictionEngine
        │               │
        ▼               ▼
AnomalyResult     PredictionResult
        │               │
        └───────┬───────┘
                ▼
         RiskAssessment
                │
                ▼
        RecommendationEngine
                │
                ▼
          Recommendation
                │
                ▼
        ApprovalController
                │
                ▼
          ActionExecutor
                │
                ▼
           ActionResult
                │
                ▼
            AuditLog
