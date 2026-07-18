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

Initial offline evaluation core. The current implementation can validate a v0
suite, run it against the deterministic fake support workflow, score each case,
and write a v0 result bundle without network access or a paid model key.

## Quickstart

Run from the repository root with the source-layout packages on `PYTHONPATH`:

```powershell
$env:PYTHONPATH = "packages/contracts/src;packages/eval-core/src"
python -m veritymesh_eval_core validate benchmarks/support-v1/suites/fake-support-suite.json
python -m veritymesh_eval_core run benchmarks/support-v1/suites/fake-support-suite.json --output result-bundles/support-smoke.json
```

Or install the local package in editable mode:

```powershell
python -m pip install -e .
veritymesh run benchmarks/support-v1/suites/fake-support-suite.json --output result-bundles/support-smoke.json
```

`result-bundles/` is ignored by Git because result bundles are generated
artifacts. The sample suite intentionally includes one missing-coverage failure
so the first result bundle has an inspectable failed case.

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

## License

VerityMesh is licensed under the Apache License, Version 2.0.

SPDX-License-Identifier: `Apache-2.0`
