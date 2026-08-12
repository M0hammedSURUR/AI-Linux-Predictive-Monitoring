START
  │
  ▼
Collect telemetry
  │
  ▼
Store telemetry
  │
  ▼
Preprocess data
  │
  ▼
Analyze behavior
  │
  ▼
Anomaly detected?
  │
 ┌┴───────────┐
NO            YES
│              │
│              ▼
│       Run predictive analysis
│              │
│              ▼
│       Calculate risk
│              │
│              ▼
│       Generate explanation
│              │
│              ▼
│       Generate recommendation
│              │
│              ▼
│       Administrator review
│              │
│         ┌────┴────┐
│       REJECT    APPROVE
│         │          │
│         ▼          ▼
│       Audit    Safety validation
│                    │
│                    ▼
│              Execute action
│                    │
│                    ▼
│                  Audit
│                    │
└────────────┬───────┘
             ▼
       Continue monitoring
             │
             ▼
            END
