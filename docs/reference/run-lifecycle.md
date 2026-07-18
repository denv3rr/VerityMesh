# Offline Run Lifecycle

Implementation: `packages/eval-core/src/veritymesh_eval_core/runner.py`

Status: implemented for the deterministic fake support workflow.

## Steps

1. Load a suite file.
2. Enforce file size and parse JSON or YAML.
3. Validate the `veritymesh.suite.v0` contract.
4. Select workflow `fake-support-agent`.
5. Compute or accept a suite hash.
6. Execute each case through the deterministic fake support workflow.
7. Build a scoring context for each case.
8. Run configured deterministic scorers.
9. Preserve evidence, model invocation metadata, tool invocation metadata, and
   score details.
10. Aggregate case and score pass counts.
11. Build a stable run id.
12. Write a `veritymesh.result.v0` result bundle.

## Determinism

The fake support workflow uses rule-based responses, deterministic evidence,
deterministic tool invocations, zero token counts, zero cost, and zero measured
duration. The same suite hash, workflow id, seed, and code version produce the
same run id and result payload on the same Python/platform environment.

Real provider adapters should later record measured latency, token usage, and
cost while keeping the fake workflow available for offline CI.

## Current Workflow

Workflow id: `fake-support-agent`

Workflow version: `fake-support-agent.v0`

Handled support intents:

- password reset;
- audit log CSV export;
- destructive production-data deletion refusal;
- insufficient-evidence refusal for everything else.

The sample suite at `benchmarks/support-v1/suites/fake-support-suite.json`
intentionally includes one missing-coverage failure for API-key rotation.

