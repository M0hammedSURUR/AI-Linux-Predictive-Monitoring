| ID    | Use Case                          | Actor         |
| ----- | --------------------------------- | ------------- |
| UC-01 | Monitor system                    | Administrator |
| UC-02 | View historical metrics           | Administrator |
| UC-03 | Review anomaly                    | Administrator |
| UC-04 | Review predicted risk             | Administrator |
| UC-05 | View risk explanation             | Administrator |
| UC-06 | Review maintenance recommendation | Administrator |
| UC-07 | Approve corrective action         | Administrator |

Precondition:

A valid recommendation exists.
The recommended action is predefined and authorized.
The system has identified the affected component.

Main flow:

1. System detects/predicts a problem.
2. System calculates risk.
3. System identifies contributing factors.
4. System generates a predefined recommendation.
5. Dashboard displays the recommendation.
6. Administrator reviews the recommendation.
7. Administrator selects APPROVE.
8. System verifies authorization.
9. System executes the predefined action.
10. System records the result.
11. Dashboard displays the execution status.

Alternative flow:

Administrator selects REJECT
        ↓
Action is not executed
        ↓
Rejection is recorded

Safety condition:

The administrator must never be able to provide an arbitrary shell command through the approval interface.

| UC-08 | Reject corrective action          | Administrator |
| UC-09 | Execute approved action           | System        |
| UC-10 | View action history               | Administrator |
| UC-11 | Run action in dry-run mode        | Administrator |
| UC-12 | Configure monitoring parameters   | Administrator |
