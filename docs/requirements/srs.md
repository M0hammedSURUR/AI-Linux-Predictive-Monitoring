# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the functional and non-functional requirements for **LinuxSentinel AI**, an AI-powered Linux predictive monitoring and human-approved self-healing platform.

The purpose of the system is to monitor a Linux server, collect and store system telemetry, identify abnormal behavior, estimate selected system risks, provide understandable explanations and maintenance recommendations, and support controlled corrective actions requiring explicit administrator approval.

This document establishes the requirements baseline for system design, implementation, testing, and evaluation.

### 1.2 Project Scope

The initial implementation focuses on monitoring and analysing a single Linux server.

The system covers:

* Linux system telemetry collection
* CPU, memory, swap, disk, disk I/O, network, load, and process monitoring
* Historical telemetry storage
* Telemetry preprocessing and feature engineering
* Rule-based and machine-learning-assisted anomaly detection
* Selected predictive risk analysis
* Risk explanations and contributing factors
* Predefined maintenance recommendations
* Human approval and rejection of corrective actions
* Predefined and authorized remediation actions
* Dry-run/simulation support
* Audit logging
* Monitoring dashboard
* Automated testing
* Safety and performance evaluation

Selected service monitoring, system/application log monitoring, and a dedicated overall system health/risk score remain planned requirements and are not part of the current verified implementation.

### 1.3 Intended Users

The primary user of the system is:

**Administrator**

The administrator is responsible for:

* Monitoring the Linux server
* Reviewing detected anomalies and predicted risks
* Reviewing explanations and recommendations
* Approving or rejecting corrective actions
* Reviewing previous corrective actions and audit records
* Using simulation/dry-run capabilities
* Configuring appropriate monitoring parameters

### 1.4 Definitions and Abbreviations

| Term           | Definition                                                          |
| -------------- | ------------------------------------------------------------------- |
| AI             | Artificial Intelligence                                             |
| ML             | Machine Learning                                                    |
| SRS            | Software Requirements Specification                                 |
| CPU            | Central Processing Unit                                             |
| RAM            | Random Access Memory                                                |
| I/O            | Input/Output                                                        |
| API            | Application Programming Interface                                   |
| SQLite         | Lightweight relational database                                     |
| Telemetry      | Measured information collected from the monitored system            |
| Anomaly        | System behaviour that differs significantly from expected behaviour |
| Prediction     | Estimated future system risk based on observed telemetry            |
| Recommendation | Predefined maintenance action suggested by the system               |
| Self-Healing   | Controlled execution of predefined corrective actions               |
| Dry Run        | Simulation of an action without making an actual corrective change  |
| Audit Log      | Persistent record of administrative decisions and action results    |

---

## 2. Overall Description

### 2.1 Product Perspective

LinuxSentinel AI is designed as a modular Linux monitoring and decision-support platform.

The high-level processing flow is:

```text
Linux Server
     |
     v
Telemetry Collector
     |
     v
Preprocessing
     |
     v
SQLite Database
     |
     +--------------------+
     |                    |
     v                    v
Anomaly Detection      Prediction
     |                    |
     +---------+----------+
               |
               v
        Intelligence Layer
               |
               v
       Recommendations
               |
               v
      Human Approval
               |
               v
     Authorized Remediation
               |
               v
          Audit Log
               |
               v
           Dashboard
```

The current dashboard displays persisted telemetry and analysis results from the SQLite database. It should therefore be understood as a dashboard for collected and stored monitoring data rather than unrestricted live streaming.

### 2.2 Product Functions

The system provides the following major functions:

1. Collect Linux system telemetry.
2. Store timestamped telemetry data.
3. Preprocess collected telemetry.
4. Detect abnormal system behaviour.
5. Perform selected predictive risk analysis.
6. Identify contributing factors and provide explanations.
7. Generate predefined maintenance recommendations.
8. Require explicit administrator approval before corrective action.
9. Restrict corrective actions to predefined authorized actions.
10. Support safe simulation/dry-run workflows.
11. Record corrective-action decisions and results.
12. Provide a dashboard for monitoring and historical analysis.
13. Provide automated tests for major components.

### 2.3 User Characteristics

The intended user is an administrator or technically capable operator who has sufficient knowledge of:

* Linux systems
* Basic system resource monitoring
* System maintenance concepts
* Basic interpretation of monitoring information

The system should present important information in an understandable form so that the administrator does not need to inspect raw telemetry manually for every decision.

### 2.4 Operating Environment

The initial system is developed and tested in a Linux environment.

The current development environment is:

* Operating System: Linux Mint 22.3
* Programming Language: Python 3.x
* Database: SQLite
* Machine Learning: scikit-learn
* Dashboard: Streamlit
* Visualization: Plotly
* Version Control: Git
* Repository Hosting: GitHub

The architecture is intended to remain compatible with commonly used Linux distributions where the required system interfaces are available.

Distribution-specific system interfaces or commands should be isolated within appropriate system-integration components.

### 2.5 Constraints

#### Technical Constraints

* The initial implementation targets one Linux server.
* Machine-learning performance depends on available training and evaluation data.
* Some telemetry sources may require appropriate system permissions.
* Monitoring should avoid excessive resource overhead.
* Corrective actions must be restricted for safety.
* Predictive results represent risk estimates and are not guaranteed failure predictions.

#### Project Constraints

* The project is developed within an undergraduate final-year project scope.
* Development time is limited.
* Access to real production failure datasets is limited.
* Controlled test scenarios may be required to evaluate abnormal conditions.

#### Resource Constraints

* Free and open-source technologies are preferred.
* Unnecessary cloud infrastructure should be avoided.
* Complex distributed architecture is outside the initial implementation scope.

### 2.6 Assumptions

The following assumptions apply:

* The monitored machine is running Linux.
* Required telemetry interfaces are available.
* The administrator has appropriate permissions for authorized monitoring and remediation tasks.
* Training and evaluation data can be collected through normal operation and controlled scenarios.
* Selected failure scenarios can be safely reproduced in a test environment.
* The dashboard is accessed by an authorized administrator.
* Machine-learning predictions represent risk estimates rather than guaranteed failures.

---

## 3. Functional Requirements

### 3.1 Telemetry Collection

| ID    | Requirement                                                                                  |
| ----- | -------------------------------------------------------------------------------------------- |
| FR-01 | The system shall collect Linux system telemetry at configurable intervals.                   |
| FR-02 | The system shall collect CPU utilization information.                                        |
| FR-03 | The system shall collect memory and swap utilization information.                            |
| FR-04 | The system shall collect disk usage and disk I/O information.                                |
| FR-05 | The system shall collect network activity information.                                       |
| FR-06 | The system shall collect process-level resource information.                                 |
| FR-07 | The system shall support monitoring of selected Linux services.                              |
| FR-08 | The system shall support collection of selected relevant system/application log information. |

### 3.2 Data Storage and Processing

| ID    | Requirement                                                                |
| ----- | -------------------------------------------------------------------------- |
| FR-09 | The system shall store timestamped telemetry data for historical analysis. |
| FR-10 | The system shall preprocess collected telemetry for analysis.              |

### 3.3 Detection and Prediction

| ID    | Requirement                                                                        |
| ----- | ---------------------------------------------------------------------------------- |
| FR-11 | The system shall detect abnormal Linux system behaviour.                           |
| FR-12 | The system shall calculate selected system-risk predictions.                       |
| FR-13 | The system shall provide information about factors contributing to detected risks. |
| FR-14 | The system shall provide an understandable overall system health/risk status.      |

### 3.4 Recommendations and Self-Healing

| ID    | Requirement                                                                                              |
| ----- | -------------------------------------------------------------------------------------------------------- |
| FR-15 | The system shall generate predefined maintenance recommendations.                                        |
| FR-16 | The system shall require explicit administrator approval before executing corrective actions.            |
| FR-17 | The system shall execute only predefined and authorized corrective actions.                              |
| FR-18 | The system shall support dry-run or simulation mode for corrective actions.                              |
| FR-19 | The system shall record recommendations, approvals, rejections, executions, and results in an audit log. |

### 3.5 Dashboard

| ID    | Requirement                                                                         |
| ----- | ----------------------------------------------------------------------------------- |
| FR-20 | The system shall provide a dashboard for current and historical system information. |

### 3.6 Current Implementation Status

The current verified implementation includes:

* FR-01 to FR-06
* FR-09 to FR-13
* FR-15 to FR-20

The following requirements remain planned/not implemented in the current verified implementation:

* FR-07 — Selected Linux service monitoring
* FR-08 — Selected system/application log monitoring
* FR-14 — Dedicated overall system health/risk status

These requirements remain documented to preserve traceability with the original project scope.

---

## 4. Non-Functional Requirements

### 4.1 Performance

**NFR-01:** The monitoring system shall maintain acceptable resource overhead on the monitored Linux server.

### 4.2 Reliability

**NFR-02:** Failure of an individual telemetry source shall not unnecessarily terminate the complete monitoring system.

### 4.3 Security

**NFR-03:** The system shall follow least-privilege principles where possible.

### 4.4 Safety

**NFR-04:** Corrective actions shall be restricted to predefined authorized actions.

### 4.5 Authorization

**NFR-05:** A corrective action shall not execute without explicit administrator approval.

### 4.6 Auditability

**NFR-06:** Administrative decisions and corrective-action results shall be recorded.

### 4.7 Maintainability

**NFR-07:** The system shall use modular components with clear responsibilities.

### 4.8 Testability

**NFR-08:** Major system components shall be independently testable.

### 4.9 Usability

**NFR-09:** The dashboard shall present monitoring and risk information clearly.

### 4.10 Scalability

**NFR-10:** The architecture should allow future extension to multiple Linux servers.

### 4.11 Configurability

**NFR-11:** Monitoring intervals, thresholds, and other appropriate parameters shall be configurable.

### 4.12 Error Handling

**NFR-12:** The system shall handle telemetry, model, and action-execution errors without uncontrolled termination.

---

## 5. External Interface Requirements

### 5.1 User Interface

The system shall provide a dashboard through which the administrator can:

* View collected system metrics.
* View historical telemetry.
* Review detected anomalies.
* View selected predicted risks.
* Review explanations and contributing factors.
* View maintenance recommendations.
* Approve or reject corrective actions.
* Execute approved predefined actions.
* Review action results and audit information.
* Use simulation/dry-run functionality.
* Configure appropriate monitoring parameters where supported.

The user interface shall not provide an interface for entering arbitrary shell commands as corrective actions.

### 5.2 Hardware Interface

The system shall operate using the hardware resources available on the monitored Linux server.

No specialized hardware is required for the initial implementation.

### 5.3 Software Interface

The system interfaces with:

* Linux operating-system telemetry facilities
* Python runtime
* SQLite database
* scikit-learn machine-learning components
* Streamlit dashboard framework
* Plotly visualization components

### 5.4 Communication Interface

The initial implementation is designed primarily for local monitoring of a single Linux server.

Network-based multi-server communication is outside the initial implementation scope but may be supported by future architectural extensions.

---

## 6. Data Requirements

### 6.1 Telemetry Data

The system shall store timestamped telemetry including, where available:

* CPU utilization
* Memory utilization
* Swap utilization
* Disk utilization
* Disk read activity
* Disk write activity
* Network transmitted bytes
* Network received bytes
* System load
* Process count
* Top CPU-consuming process
* Top memory-consuming process

### 6.2 Processed Data

Preprocessing may derive analytical features such as:

* Disk I/O rates
* Network activity rates
* Other features required by anomaly detection and prediction components

### 6.3 Prediction Data

Prediction records shall contain information such as:

* Timestamp
* Monitored metric
* Current value
* Predicted value
* Relevant threshold
* Risk level
* Prediction message

### 6.4 Audit Data

Audit records shall contain information related to:

* Timestamp
* Metric
* Corrective action
* Approval status
* Execution status
* Result
* Error information where applicable

### 6.5 Data Persistence

SQLite is used for persistent storage in the initial implementation.

Historical telemetry shall remain available for analysis and dashboard display.

---

## 7. Safety and Security Requirements

### 7.1 Human Approval

No corrective action shall be executed without explicit administrator approval.

### 7.2 Authorized Actions

The system shall allow only predefined and authorized corrective actions.

### 7.3 Arbitrary Command Prevention

The approval interface shall not allow administrators or external input to provide arbitrary shell commands for execution.

### 7.4 Least Privilege

System operations shall use the minimum privileges necessary wherever practical.

### 7.5 Safe Remediation

Corrective actions shall be designed to minimize the possibility of destructive or irreversible system changes.

### 7.6 Simulation

Simulation/dry-run functionality shall be available for testing corrective-action workflows without performing an actual corrective change where applicable.

### 7.7 Audit Trail

Approval, rejection, execution, and execution-result information shall be recorded for accountability and traceability.

---

## 8. Use Cases

The primary actor is the **Administrator**.

| ID    | Use Case                          | Actor         |
| ----- | --------------------------------- | ------------- |
| UC-01 | Monitor system                    | Administrator |
| UC-02 | View historical metrics           | Administrator |
| UC-03 | Review anomaly                    | Administrator |
| UC-04 | Review predicted risk             | Administrator |
| UC-05 | View risk explanation             | Administrator |
| UC-06 | Review maintenance recommendation | Administrator |
| UC-07 | Approve corrective action         | Administrator |
| UC-08 | Reject corrective action          | Administrator |
| UC-09 | Execute approved action           | System        |
| UC-10 | View action history               | Administrator |
| UC-11 | Run action in dry-run mode        | Administrator |
| UC-12 | Configure monitoring parameters   | Administrator |

### Corrective Action Main Flow

1. The system detects or predicts a problem.
2. The system calculates the relevant risk.
3. The system identifies contributing factors.
4. The system generates a predefined recommendation.
5. The dashboard displays the recommendation.
6. The administrator reviews the recommendation.
7. The administrator selects APPROVE.
8. The system verifies authorization.
9. The system executes the predefined action.
10. The system records the result.
11. The dashboard displays the execution status.

### Alternative Flow — Rejection

1. The administrator selects REJECT.
2. The corrective action is not executed.
3. The rejection is recorded in the audit log.

### Safety Condition

The administrator shall not be able to provide an arbitrary shell command through the approval interface.

---

## 9. Acceptance Criteria

| Requirement           | Acceptance Criteria                                                             |
| --------------------- | ------------------------------------------------------------------------------- |
| Telemetry collection  | The system successfully records configured Linux metrics with timestamps.       |
| Historical monitoring | The dashboard displays previously collected telemetry.                          |
| Anomaly detection     | A controlled abnormal behaviour scenario produces a detectable anomaly.         |
| Prediction            | A selected test scenario produces a measurable risk prediction.                 |
| Explanation           | A prediction displays contributing features or factors.                         |
| Recommendation        | An identified scenario produces an appropriate predefined recommendation.       |
| Approval              | An unapproved action cannot execute.                                            |
| Rejection             | A rejected action is not executed.                                              |
| Safe action           | Only registered/whitelisted actions can execute.                                |
| Audit                 | Approval, rejection, execution, and results are recorded.                       |
| Dry run               | Dry-run produces no actual corrective change.                                   |
| Dashboard             | Current monitoring and risk information are visible through the user interface. |

---

## 10. Requirements Traceability

Requirements shall be traced through:

```text
User Requirements
        ↓
Objectives
        ↓
Functional / Non-Functional Requirements
        ↓
Use Cases
        ↓
System Design
        ↓
Implementation
        ↓
Test Cases
        ↓
Test Execution Evidence
```

The detailed requirement-to-use-case and implementation/test mapping is maintained separately in:

`docs/requirements/requirements-traceability.md`

The current traceability baseline contains:

* 20 functional requirements
* 12 non-functional requirements
* 10 user requirements
* 12 use cases
* Defined acceptance criteria
* Automated test evidence for implemented functionality

The current automated test suite contains 63 passing tests.

---

## 11. Out-of-Scope Requirements

The initial implementation shall not include:

* Multi-server orchestration
* Complete data-center management
* Prediction of every possible Linux failure
* Autonomous unrestricted shell-command execution
* Automatic kernel modification
* Automatic package upgrades
* Destructive system cleanup
* Enterprise-scale distributed monitoring
* Guaranteed prediction of unknown failure types

---

## 12. Future Extensions

Potential future extensions include:

* Selected Linux service monitoring
* Selected system/application log monitoring
* Dedicated overall system health/risk scoring
* Multi-server monitoring
* Improved predictive models
* Larger real-world datasets
* More advanced explanation techniques
* Additional safe remediation actions
* Expanded configuration management

Future extensions shall be evaluated against project scope, safety, available resources, and academic requirements before implementation.
