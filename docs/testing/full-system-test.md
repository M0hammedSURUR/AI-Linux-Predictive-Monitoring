# Full System Testing

## 1. Overview

This document records the full-system testing of the LinuxSentinel AI platform.

The purpose of the testing is to verify that the major components of the platform operate correctly together under a live Linux environment.

The testing includes real telemetry collection, dashboard monitoring, anomaly detection, prediction, recommendation generation, Linux service monitoring, journal log monitoring, and the human-approved self-healing workflow.

The self-healing workflow was tested using the project's safe simulation mode so that no artificial system failure or unsafe system modification was required.

## 2. Test Environment

The full-system test was performed on the development Linux system running:

* Linux Mint 22.3 Cinnamon
* Python 3.12.3
* Streamlit 1.63.0
* SQLite monitoring database
* systemd journal
* psutil-based telemetry collection
* scikit-learn-based experimental anomaly detection

The telemetry collector was configured to collect system information at a five-second interval.

The Streamlit dashboard was run using:

PYTHONPATH=. streamlit run src/dashboard/app.py

The continuous telemetry collector was run using:

python -m src.collector.run_collector

## 3. Live Telemetry Collection Test

### Test Objective

Verify that the telemetry collector continuously collects real Linux system metrics and stores timestamped records in the monitoring database.

### Test Procedure

The continuous collector was started using:

python -m src.collector.run_collector

The configured collection interval was five seconds.

### Observed Result

The collector successfully produced live telemetry records.

Example observations:

* CPU usage: 0.0% to 2.5%
* Memory usage: approximately 23.3% to 23.5%
* Disk usage: 9.2%
* System load: approximately 0.33 to 0.38
* Process count: 299

Example timestamped record:

2026-09-17T09:04:43.752341+00:00 | CPU: 1.3% | RAM: 23.5% | Disk: 9.2% | Load: 0.36 | Processes: 299

### Result

PASS — Real Linux telemetry was collected continuously at the configured five-second interval.

## 4. Live Dashboard Test

### Test Objective

Verify that the Streamlit dashboard receives and displays current telemetry from the monitoring database.

### Test Procedure

The dashboard was started using:

PYTHONPATH=. streamlit run src/dashboard/app.py

The dashboard was opened in a web browser while the telemetry collector continued running.

### Observed Result

The dashboard displayed live telemetry and updated successfully.

Observed values during the test included:

* CPU usage: 18.8%
* Memory usage: 30.1%
* Disk usage: 9.2%
* System load: 0.54

The dashboard also displayed a current telemetry timestamp and historical telemetry charts.

### Result

PASS — The dashboard successfully displayed live telemetry from the running Linux system.

## 5. Live Anomaly Detection Test

### Test Objective

Verify that the anomaly detection components operate during live monitoring and that experimental ML signals are clearly distinguished from rule-based anomalies.

### Observed Result

During live monitoring, no active rule-based anomalies were detected.

The experimental ML detector identified five unusual telemetry patterns.

The dashboard explicitly classified these signals as experimental and explained that no configured rule-based threshold had been exceeded.

### Result

PASS — Rule-based anomaly detection and experimental ML detection operated during live monitoring, with the ML signals clearly identified as experimental.

## 6. Live System Health and Prediction Test

### Test Objective

Verify that the platform provides an understandable system health status and generates predictions from recent telemetry.

### Observed Result

During the live test, the dashboard reported:

* Overall health: WARNING — Experimental ML signals detected.
* CPU prediction: LOW RISK
* Memory prediction: LOW RISK
* Disk prediction: LOW RISK

Example CPU prediction:

* Current value: 18.8%
* Predicted value: 20.4%
* Configured threshold: 80.0%

Example memory prediction:

* Current value: 30.1%
* Predicted value: 30.6%
* Configured threshold: 80.0%

Example disk prediction:

* Current value: 9.2%
* Predicted value: 9.2%
* Configured threshold: 90.0%

### Result

PASS — The platform generated live predictions and presented understandable risk information without triggering unnecessary corrective actions.

## 7. Linux Service Monitoring Test

### Test Objective

Verify that configured Linux systemd services can be monitored during live operation.

### Observed Result

The dashboard successfully checked the configured services:

* cron.service — active
* bluetooth.service — active
* cups.service — active

Service descriptions were also displayed.

### Result

PASS — Configured Linux services were monitored successfully during the live test.

## 8. Linux Journal Log Monitoring Test

### Test Objective

Verify that recent warning and error messages from the Linux system journal can be collected and displayed by the platform.

### Observed Result

The dashboard displayed recent journal warning and error entries from sources including:

* evolution-calendar
* evolution-addressbook
* systemd
* kernel

Examples included service startup messages, deprecated configuration warnings, and kernel warnings.

### Result

PASS — Recent warning and error journal entries were successfully collected and displayed.

## 9. Self-Healing Simulation Test

### Test Objective

Verify the complete human-approved self-healing workflow without intentionally creating a harmful condition on the Linux system.

### Test Procedure

The dashboard's:

Enable Self-Healing Simulation

option was enabled.

The simulation generated a controlled disk prediction:

* Simulated current disk usage: 85.0%
* Simulated predicted disk usage: 95.0%
* Configured disk threshold: 90.0%
* Risk level: HIGH RISK

The dashboard generated a recommendation and created a predefined healing action:

* Metric: disk_percent
* Predefined action: clear_cache
* Initial status: PENDING

The dashboard explicitly indicated that simulation mode would not execute a real system action automatically.

### Result

PASS — The controlled high-risk prediction generated the expected recommendation and pending healing action.

## 10. Human Rejection Test

### Test Objective

Verify that a human operator can reject a proposed healing action and that the rejected action is not executed.

### Observed Result

The simulated disk cleanup action was rejected by the human operator.

The dashboard reported:

Status: REJECTED

The dashboard also confirmed:

Action rejected by the human operator.

The rejection was recorded in the audit log.

### Result

PASS — Human rejection prevented execution and was recorded successfully.

## 11. Human Approval and Healing Execution Test

### Test Objective

Verify that an approved predefined healing action can be executed only after explicit human approval.

### Observed Result

A new simulated disk prediction generated the following proposed action:

* Metric: disk_percent
* Reason: disk_percent was predicted to reach 95.0%.
* Predefined action: clear_cache
* Approval status: APPROVED

The dashboard required a separate operator action for execution.

After the operator selected Execute, the healing action completed successfully.

Execution result:

* Execution status: SUCCESS
* Items removed: 9
* Cache target: /home/msr4/.cache

The dashboard reported:

Healing action executed successfully.

### Result

PASS — The approved predefined healing action executed successfully after explicit human approval.

## 12. Audit Log Persistence Test

### Test Objective

Verify that approval, rejection, execution status, and healing results are persisted in the SQLite audit log.

### Observed Result

The SQLite database contained the following recent records:

Successful execution:

2026-09-17T09:29:08.560446+00:00 | disk_percent | clear_cache | approved | success | Cache cleanup completed successfully. 9 items removed from /home/msr4/.cache.

Rejected action:

2026-09-17T09:23:30.958726+00:00 | disk_percent | clear_cache | rejected | not_executed | Healing action rejected by human operator.

These records confirm that both successful and rejected healing decisions were persisted.

### Result

PASS — Healing decisions and execution results were successfully recorded in the SQLite audit log.

## 13. Full-System Test Summary

The live full-system test verified the major LinuxSentinel AI components under a running Linux environment.

| Test Area | Result |
|---|---|
| Live telemetry collection | PASS |
| Live dashboard monitoring | PASS |
| Rule-based anomaly detection | PASS |
| Experimental ML detection | PASS |
| System health status | PASS |
| Predictive monitoring | PASS |
| Service monitoring | PASS |
| Journal log monitoring | PASS |
| Self-healing simulation | PASS |
| Human rejection | PASS |
| Human approval | PASS |
| Healing execution | PASS |
| Audit log persistence | PASS |

## 14. Conclusion

The full-system test demonstrated that the LinuxSentinel AI platform can operate as an integrated monitoring and response system on a live Linux environment.

Real system telemetry was collected and displayed through the dashboard. Anomaly detection, predictive monitoring, service monitoring, and journal log monitoring operated together.

The human-approved self-healing workflow was also verified using the project's safe simulation mode. Both rejection and approval paths were tested, and the approved predefined cache-cleanup action executed successfully.

The audit database confirmed that human decisions and execution results were persisted.

The live test therefore provides evidence that the major implemented functional components operate together as intended. The experimental ML detector remains subject to the limitations documented in the ML evaluation report.
