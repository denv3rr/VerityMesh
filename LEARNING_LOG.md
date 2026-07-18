# Learning Log

Use dated entries to show decisions, hypotheses, experiments, evidence, results,
and next actions.

## Template

```text
Date:
Area:
Decision or hypothesis:
Experiment or source:
Evidence:
Result:
Next action:
```

## Entries

### 2026-07-17

Area: offline evaluation core.

Decision or hypothesis: implement Milestone 1's smallest useful slice before
API, worker persistence, hosted providers, or web UI.

Experiment or source: `docs/EXECUTION_PLAN.md`, unit tests, and the fake support
suite.

Evidence: v0 contracts, deterministic scorers, fake workflow, CLI entry point,
and sample suite now run offline without model credentials.

Result: initial core functionality implemented with strict suite validation and
a result bundle containing one intentional missing-coverage failure.

Next action: add JSON Schema export/drift checks and broaden the public support
benchmark after Milestone 0 documents are complete.

### 2026-07-17

Area: repository setup.

Decision or hypothesis: start with the guideline-defined modular monorepo,
agent contract, execution plan, and market/model watch process before writing
application code.

Experiment or source: `Project_Guidelines.md`.

Evidence: the guideline requires an engineering contract, explicit non-goals,
security posture, repository standard, and dated market notes.

Result: initial scaffold created.

Next action: choose license and complete Milestone 0 documents.
