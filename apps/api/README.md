# API App

Owns the FastAPI control surface for projects, suites, workflows, runs,
comparisons, release policies, users, and audit events.

Future responsibilities:

- validate requests with strict schemas;
- enforce authorization;
- issue idempotent run requests;
- expose OpenAPI contracts;
- persist state through explicit transaction boundaries;
- return structured errors with user-safe messages.

Must not own provider-specific model behavior or evaluator implementation.

