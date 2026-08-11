| ID     | Category        | Requirement                                                                                                 |
| ------ | --------------- | ----------------------------------------------------------------------------------------------------------- |
| NFR-01 | Performance     | The monitoring system shall maintain acceptable resource overhead on the monitored Linux server.            |
| NFR-02 | Reliability     | Failure of an individual telemetry source shall not unnecessarily terminate the complete monitoring system. |
| NFR-03 | Security        | The system shall follow least-privilege principles where possible.                                          |
| NFR-04 | Safety          | Corrective actions shall be restricted to predefined authorized actions.                                    |
| NFR-05 | Authorization   | A corrective action shall not execute without explicit administrator approval.                              |
| NFR-06 | Auditability    | Administrative decisions and corrective-action results shall be recorded.                                   |
| NFR-07 | Maintainability | The system shall use modular components with clear responsibilities.                                        |
| NFR-08 | Testability     | Major system components shall be independently testable.                                                    |
| NFR-09 | Usability       | The dashboard shall present monitoring and risk information clearly.                                        |
| NFR-10 | Scalability     | The architecture should allow future extension to multiple Linux servers.                                   |
| NFR-11 | Configurability | Monitoring intervals, thresholds and other appropriate parameters shall be configurable.                    |
| NFR-12 | Error Handling  | The system shall handle telemetry, model and action-execution errors without uncontrolled termination.      |
