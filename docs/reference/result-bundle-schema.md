# Result Bundle Schema v0

Schema version: `veritymesh.result.v0`

Implementation: `packages/contracts/src/veritymesh_contracts/result.py`

The v0 result bundle records run metadata, aggregate summary, case outputs,
evidence, invocations, and dimensional score results. It deliberately preserves
individual scores instead of collapsing everything into one quality number.

## Top-Level Shape

```json
{
  "schema_version": "veritymesh.result.v0",
  "run": {},
  "cases": []
}
```

## Run Fields

- `id`: stable run id derived from suite hash, workflow id, seed, and code
  version.
- `suite_id`: suite identifier.
- `suite_version`: suite version.
- `suite_hash`: SHA-256 hash of the suite file text for CLI runs.
- `workflow_id`: workflow id used for execution.
- `workflow_version`: workflow implementation version.
- `seed`: deterministic seed recorded for reproducibility.
- `code_version`: caller-supplied code version string.
- `environment`: Python/platform/offline execution metadata.
- `summary`: aggregate counts and pass rates.

## Case Fields

- `id`;
- `category`;
- `difficulty`;
- `input`;
- `output`;
- `evidence`;
- `scores`;
- `passed`;
- `duration_ms`;
- `model_invocations`;
- `tool_invocations`.

For the fake support workflow, `duration_ms`, token counts, and cost are
deterministic zeros. Hosted and local model adapters should later record
measured values without changing the deterministic default path.

## Score Fields

- `name`;
- `type`;
- `version`;
- `passed`;
- `actual`;
- `expected`;
- `reason`, when failed or explanatory;
- `details`, when a scorer emits dimensional diagnostics such as citation
  precision and recall.

