# CLI Reference

Status: implemented for the offline evaluation core.

## Local Source-Layout Usage

```powershell
$env:PYTHONPATH = "packages/contracts/src;packages/eval-core/src"
python -m veritymesh_eval_core validate benchmarks/support-v1/suites/fake-support-suite.json
python -m veritymesh_eval_core run benchmarks/support-v1/suites/fake-support-suite.json --output result-bundles/support-smoke.json
```

## Editable Install Usage

```powershell
python -m pip install -e .
veritymesh validate benchmarks/support-v1/suites/fake-support-suite.json
veritymesh run benchmarks/support-v1/suites/fake-support-suite.json --output result-bundles/support-smoke.json
```

## Commands

### `validate`

Validates a `.json`, `.yaml`, or `.yml` suite.

```text
veritymesh validate <suite>
```

Behavior:

- parses the suite file;
- rejects files larger than 1,000,000 bytes;
- validates the `veritymesh.suite.v0` contract;
- prints a concise success message;
- exits `2` on parse or validation failure.

YAML support uses `PyYAML` when installed. JSON suites work without external
dependencies.

### `run`

Runs a suite against the deterministic fake support workflow and writes a result
bundle.

```text
veritymesh run <suite> [--workflow fake-support-agent] [--seed 0] [--code-version development] [--output path]
```

Behavior:

- validates the suite;
- runs each case through `fake-support-agent`;
- evaluates configured deterministic scorers;
- writes a `veritymesh.result.v0` JSON bundle;
- prints run id, suite, workflow, case pass count, score pass count, and output
  path;
- exits `2` on validation or unsupported-workflow errors.

The default output path is `result-bundles/<run-id>.json`. `result-bundles/` is
ignored by Git because result bundles are generated artifacts.

