# Worker App

Owns background case execution, queue leases, retries, timeouts, cancellation,
dead-letter handling, evaluator orchestration, and artifact capture.

Future responsibilities:

- execute workflows inside explicit time, tool, network, and budget limits;
- preserve idempotency across retries;
- normalize provider and workflow failures;
- record model invocations, tool invocations, evidence, scores, and telemetry;
- recover safely after process interruption.

Default worker tests must run with deterministic fake providers.

