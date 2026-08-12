| ID  | Risk                                          | Probability | Impact    | Mitigation                                   |
| --- | --------------------------------------------- | ----------- | --------- | -------------------------------------------- |
| R01 | Insufficient abnormal-event data              | Medium      | High      | Generate controlled test scenarios           |
| R02 | ML model performs poorly                      | Medium      | High      | Compare multiple lightweight models          |
| R03 | Excessive false positives                     | Medium      | High      | Tune thresholds and evaluate precision       |
| R04 | False negatives                               | Medium      | High      | Evaluate recall and detection coverage       |
| R05 | Project scope becomes too large               | High        | High      | Maintain strict MVP boundary                 |
| R06 | Self-healing action causes unintended effects | Low         | Very High | Approval + allowlist + dry-run               |
| R07 | Linux permissions prevent actions             | Medium      | Medium    | Use least-privilege controlled setup         |
| R08 | Insufficient development time                 | Medium      | High      | Sprint planning + backlog prioritization     |
| R09 | Database grows excessively                    | Medium      | Medium    | Measure storage and retention                |
| R10 | Laptop resource limitations                   | Medium      | Medium    | Lightweight models and controlled sampling   |
| R11 | Documentation falls behind development        | Medium      | High      | Documentation checkpoint every sprint        |
| R12 | Dependency/software compatibility issue       | Medium      | Medium    | Pin/test dependencies in virtual environment |
