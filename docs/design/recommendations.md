# Recommendation Engine Design

## 1. Purpose

The Recommendation Engine converts detected system anomalies and
high-risk predictions into safe, human-readable recommendations.

The engine does not execute system commands.

Its purpose is to help the administrator understand the problem and
suggest a possible action for human review.

## 2. Position in the System

```text
Anomaly Detection / Prediction
            |
            v
   Recommendation Engine
            |
            v
      Recommendation
            |
            v
       Human Review
            |
            v
 Future Self-Healing Action
3. Responsibilities

The Recommendation Engine is responsible for:

Interpreting anomaly results.
Interpreting high-risk predictions.
Identifying the affected system metric.
Generating a suitable recommendation.
Providing a human-readable explanation.
Suggesting a safe administrative action.

The engine does not directly execute commands.

4. Recommendation Model

Each recommendation contains:

Field	Description
timestamp	Time associated with the condition
metric	System metric related to the recommendation
severity	Severity level of the condition
title	Short recommendation title
description	Explanation of the detected condition
suggested_action	Suggested action for human review
5. Supported Anomaly Recommendations

The current engine supports recommendations for:

CPU Usage

When high CPU usage is detected, the engine recommends checking
the top CPU-consuming process.

Memory Usage

When high memory usage is detected, the engine recommends inspecting
memory-intensive processes.

Disk Usage

When high disk usage is detected, the engine recommends identifying
large or unnecessary files before performing cleanup.

System Load

When high system load is detected, the engine recommends inspecting
active processes and workloads contributing to the load.

6. Prediction Recommendations

The engine generates recommendations for high-risk predictions.

For example, if CPU usage is predicted to exceed the configured
threshold, the system recommends monitoring the metric and
investigating the responsible process before the threshold is exceeded.

Low- and medium-risk predictions currently do not generate
recommendations.

7. Safety Principle

The Recommendation Engine follows a human-approval principle.

Detection
    |
    v
Recommendation
    |
    v
Human Decision
    |
    +---- Reject
    |
    +---- Approve
             |
             v
      Future Action

The current implementation only produces recommendations.

It does not:

Execute shell commands.
Stop processes automatically.
Restart services automatically.
Delete files automatically.
Modify system configuration.

This provides a safety boundary between AI-generated decisions and
system-level actions.

8. Software Design

The recommendation component is separated into:

src/recommendations/
├── __init__.py
├── models.py
└── engine.py
models.py

Defines the Recommendation data model.

engine.py

Contains RecommendationEngine, which converts anomaly and
prediction results into recommendations.

This separation keeps the data model independent from recommendation
logic.

9. Testing

The Recommendation Engine is tested using unit tests.

The tests verify:

High CPU anomalies generate recommendations.
Normal conditions generate no recommendation.
High-risk predictions generate recommendations.
Low-risk predictions generate no recommendation.
High memory anomalies generate recommendations.
High disk anomalies generate recommendations.
High system-load anomalies generate recommendations.

The Recommendation Engine test suite currently contains:

7 passed

The complete project test suite previously contained:

21 passed

After adding the three additional recommendation tests, the expected
complete suite is:

24 passed
10. Design Benefits

The Recommendation Engine provides:

Separation of detection and response logic.
Human-readable system guidance.
Safer system administration.
Clear separation between AI decisions and system actions.
A foundation for future human-approved self-healing.
11. Future Enhancement

Future versions may add:

Recommendation confidence scores.
Multiple possible actions.
Action priority levels.
Human approval tracking.
Approved/rejected recommendation history.
Integration with the self-healing execution layer.
