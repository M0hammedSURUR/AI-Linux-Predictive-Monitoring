# LinuxSentinel AI

## AI-Powered Linux Predictive Monitoring & Human-Approved Self-Healing Platform

LinuxSentinel AI is a Linux system monitoring platform that combines real-time system telemetry, rule-based anomaly detection, machine-learning-based anomaly detection, predictive analysis, system service monitoring, Linux journal monitoring, and human-approved self-healing.

The platform is designed to detect potential system problems early, explain detected conditions, recommend appropriate actions, and allow a human operator to approve or reject proposed healing actions before execution.

> **Safety principle:** Potentially impactful healing actions require human approval before execution.

---

## Project Objectives

LinuxSentinel AI aims to:

* Monitor Linux system health continuously.
* Collect CPU, memory, swap, disk, load, network, disk I/O, and process information.
* Detect abnormal system conditions.
* Use machine learning to identify unusual telemetry patterns.
* Predict potential threshold violations from recent trends.
* Monitor configured Linux services.
* Monitor warning and error messages from the systemd journal.
* Generate understandable recommendations.
* Require human approval before executing supported healing actions.
* Record healing decisions and execution results in an audit log.
* Provide a live monitoring dashboard.

---

## Key Features

### 1. Real-Time System Monitoring

The collector continuously gathers Linux system telemetry using `psutil`.

Monitored information includes:

* CPU utilization
* Memory utilization
* Swap utilization
* Disk utilization
* System load
* Disk I/O
* Network traffic
* Process count
* Top CPU-consuming process
* Top memory-consuming process

### 2. Anomaly Detection

The platform uses two complementary approaches.

**Rule-Based Detection**

Predefined thresholds identify conditions such as:

* High CPU utilization
* High memory utilization
* High disk utilization
* High system load

**Machine Learning Detection**

An `IsolationForest` model is used to identify unusual telemetry patterns.

The ML detector is treated as an experimental signal and is not considered a substitute for production-grade validation.

### 3. Predictive Monitoring

Recent telemetry trends are analyzed to estimate whether important system metrics may approach defined thresholds.

The current prediction layer evaluates:

* CPU utilization
* Memory utilization
* Disk utilization

Predictions are classified into risk levels to support early intervention.

### 4. Linux Service Monitoring

Configured systemd services can be monitored for their current state.

Example monitored services include:

* `cron.service`
* `bluetooth.service`
* `cups.service`

The monitored services are configurable through:

`config/services.json`

### 5. Linux Log Monitoring

Linux journal messages are monitored for recent warning and error entries using `journalctl`.

The dashboard displays:

* Timestamp
* Source
* Message

### 6. Human-Approved Self-Healing

LinuxSentinel AI follows a human-in-the-loop approach.

The healing workflow is:

```text
Detection
   ↓
Prediction / Analysis
   ↓
Recommendation
   ↓
Human Approval or Rejection
   ↓
Execution
   ↓
Audit Logging
```

The currently supported safe healing action is:

* User cache cleanup

Service restart is intentionally not implemented in the current version to avoid uncontrolled or privileged system modifications.

### 7. Healing Audit Trail

Healing decisions and execution results are stored in SQLite.

The audit system records:

* Metric
* Proposed action
* Approval status
* Execution status
* Result
* Error information
* Timestamp

This provides traceability for human decisions and system actions.

### 8. Live Dashboard

The project includes a Streamlit dashboard providing a unified view of:

* Current system telemetry
* Historical telemetry
* Rule-based anomalies
* ML anomaly signals
* Predictions
* Recommendations
* Service status
* Linux journal warnings/errors
* Overall system health
* Self-healing workflow
* Healing audit information

---

## System Architecture

```text
┌───────────────────────────────────────┐
│          Linux Operating System       │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────┐
│          Telemetry Collector          │
│     CPU • RAM • Disk • Load • I/O     │
│     Network • Processes • Metrics     │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────┐
│        Preprocessing & Database       │
│              SQLite                   │
└───────────────┬───────────────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌───────────────┐ ┌────────────────────┐
│    Anomaly    │ │    Prediction      │
│   Detection   │ │      Engine        │
│   Rule + ML   │ │   Trend Analysis   │
└───────┬───────┘ └─────────┬──────────┘
        │                   │
        └─────────┬─────────┘
                  ▼
        ┌─────────────────────┐
        │ Recommendation      │
        │      Engine         │
        └──────────┬──────────┘
                   ▼
        ┌─────────────────────┐
        │ Human Approval      │
        │   / Rejection       │
        └──────────┬──────────┘
                   ▼
        ┌─────────────────────┐
        │ Self-Healing        │
        │ Executor            │
        └──────────┬──────────┘
                   ▼
        ┌─────────────────────┐
        │ Healing Audit Log   │
        └─────────────────────┘

Additional monitoring:
Linux systemd services ──► Service Monitor
Linux journal ───────────► Log Monitor

All monitoring information
              │
              ▼
       Streamlit Dashboard
```

---

## Technology Stack

| Component            | Technology                   |
| -------------------- | ---------------------------- |
| Operating System     | Linux                        |
| Programming Language | Python 3.12                  |
| System Monitoring    | psutil                       |
| Machine Learning     | scikit-learn                 |
| Numerical Computing  | NumPy                        |
| Database             | SQLite                       |
| Dashboard            | Streamlit                    |
| Testing              | pytest                       |
| Service Monitoring   | systemd / systemctl          |
| Log Monitoring       | systemd journal / journalctl |
| Version Control      | Git                          |
| Repository Hosting   | GitHub                       |

---

## Project Structure

```text
AI-Linux-Predictive-Monitoring/
│
├── config/
│   └── services.json
│
├── data/
│   └── monitoring.db
│
├── diagrams/
│   ├── architecture.md
│   ├── context-diagram.md
│   ├── data-model.md
│   ├── level-0-dfd.md
│   ├── use-case-diagram.md
│   └── ...
│
├── docs/
│   ├── agile/
│   ├── design/
│   ├── implementation/
│   ├── planning/
│   ├── requirements/
│   ├── standards/
│   └── testing/
│
├── experiments/
│   ├── anomaly_detection/
│   ├── data_generation/
│   └── prediction/
│
├── logs/
├── models/
├── screenshots/
│
├── src/
│   ├── anomaly_detection/
│   ├── collector/
│   ├── dashboard/
│   ├── database/
│   ├── log_monitor/
│   ├── prediction/
│   ├── preprocessing/
│   ├── recommendations/
│   ├── self_healing/
│   └── service_monitor/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/M0hammedSURUR/AI-Linux-Predictive-Monitoring.git
cd AI-Linux-Predictive-Monitoring
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the System

### Start the telemetry collector

```bash
python -m src.collector.run_collector
```

The collector continuously records telemetry into the SQLite database.

### Start the dashboard

Open another terminal:

```bash
cd AI-Linux-Predictive-Monitoring
source .venv/bin/activate
PYTHONPATH=. streamlit run src/dashboard/app.py
```

The Streamlit dashboard will display the live monitoring information.

---

## Running Tests

Run the complete automated test suite:

```bash
pytest -v
```

The latest documented test execution contains **69 automated tests**, all passing.

---

## Testing & Evaluation

The project includes testing for:

* Telemetry collection
* Database operations
* Preprocessing
* Rule-based anomaly detection
* ML anomaly detection
* Prediction
* Recommendation generation
* Self-healing workflow
* Healing audit logging
* Service monitoring
* Linux journal monitoring
* Dashboard-related functionality
* Pipeline integration
* Full-system behavior

Performance measurements and ML evaluation results are documented under:

* `docs/implementation/`
* `docs/testing/`

### ML Evaluation Limitation

The current IsolationForest evaluation uses a small synthetic dataset where the model is trained and evaluated on the same dataset.

Therefore, the measured evaluation metrics should **not** be interpreted as production accuracy.

Further validation with larger, independent, real-world datasets would be required for production deployment.

---

## Safety Considerations

LinuxSentinel AI is designed around controlled and explainable system actions.

The current implementation:

* Requires human approval before healing execution.
* Does not execute arbitrary shell commands.
* Does not modify arbitrary filesystem paths.
* Does not use `sudo` for automated healing.
* Restricts cache cleanup to the current user's cache directory.
* Records healing decisions and results in an audit log.
* Keeps potentially disruptive service restart functionality disabled.

---

## Software Engineering Documentation

The project documentation covers major Software Engineering activities including:

* Requirements engineering
* Functional requirements
* Non-functional requirements
* Software architecture
* Data modeling
* UML and system diagrams
* Agile planning
* Risk management
* Feasibility analysis
* Cost and effort estimation
* Acceptance criteria
* Requirements traceability
* Testing
* Performance evaluation
* Implementation documentation
* Coding standards

Documentation is available under:

* `docs/`
* `diagrams/`

---

## Current Project Status

The core monitoring and human-approved self-healing workflow has been implemented and tested.

Current implementation includes:

* Real-time telemetry collection
* SQLite persistence
* Preprocessing
* Rule-based anomaly detection
* ML-based anomaly detection
* Predictive monitoring
* Recommendation generation
* Human approval/rejection workflow
* Safe cache cleanup
* Healing audit logging
* Linux service monitoring
* Linux journal monitoring
* Streamlit dashboard
* Automated test suite
* Full-system testing
* Performance evaluation
* Requirements traceability
* Acceptance criteria
* Documentation audit

---

## Author

**Mohammed Surur**

B.Sc. Multimedia & Web Technology with Artificial Intelligence & Robotics

Nilgiri College of Arts and Science (Autonomous)

---

## Project

**LinuxSentinel AI**

*AI-Powered Linux Predictive Monitoring & Human-Approved Self-Healing Platform**opened*
