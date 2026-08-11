ADR-001 — Modular Monolithic Architecture

Decision:
Use a modular monolithic architecture for the initial implementation.

Reason:
The project targets one Linux machine and has limited development resources and time. Logical modularity provides maintainability and testability without the complexity of microservices.

Alternatives considered:

Microservices
Distributed architecture

Decision status:
Accepted

Future consideration:
The module boundaries should allow future extraction into distributed components if multi-server support is implemented.
