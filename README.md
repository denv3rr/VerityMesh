# VerityMesh

VerityMesh is an open-source, model-agnostic AI reliability, evaluation, and
evidence platform.

The goal is to test AI workflows and retrieval systems against realistic,
versioned tasks; record case-level evidence and telemetry; detect quality,
latency, cost, citation, tool-use, and security regressions; and route uncertain
or severe results to human review.

The first complete slice must run offline with a deterministic fake workflow.
Hosted model calls are opt-in and must never be required for default CI.

## Current Status

Initial repository scaffold. The build plan lives in
`docs/EXECUTION_PLAN.md`. Agent operating rules live in `AGENTS.md`.

## Repository Map

- `apps/api/`: control API.
- `apps/worker/`: background execution worker.
- `apps/web/`: web console.
- `packages/contracts/`: shared schemas and generated contracts.
- `packages/eval-core/`: suite validation, scoring, result bundles, and CLI.
- `packages/provider-adapters/`: fake, local, and hosted model adapters.
- `packages/telemetry/`: traces, metrics, logs, and redaction helpers.
- `benchmarks/support-v1/`: first public support benchmark.
- `docs/`: ADRs, architecture, reference docs, threat model, operations, and
  execution plan.
- `tests/`: integration, end-to-end, load, and security tests.
- `deploy/compose/`: Docker Compose development environment.

## Guardrails

- No paid API key required for default tests.
- No fabricated benchmark, scale, pricing, model, or market claims.
- All untrusted inputs must pass strict schemas and size limits.
- Provider-specific behavior must stay behind adapters.
- Architecture expansions need measured evidence and an ADR.
