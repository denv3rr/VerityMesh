# Reference Documentation

This folder is for durable lookup material about core functionality. It should
help a future contributor quickly answer: what exists, where it lives, what
inputs and outputs look like, which invariants matter, and how the pieces fit
together.

Do not use this folder as a manual copy of every private function. That becomes
stale. Use it for stable system knowledge and generated references.

## What Belongs Here

- CLI command reference.
- Public API and OpenAPI notes.
- Suite, result bundle, evaluator, provider, and telemetry schema references.
- Run lifecycle and state-machine references.
- Scorer behavior and failure-reason references.
- Provider adapter contract references.
- Worker queue, retry, timeout, cancellation, and idempotency references.
- Generated function/module reference output once code exists.
- Cross-links to ADRs, architecture docs, and package READMEs.

## What Belongs In Code

Use docstrings or concise comments for:

- public functions, classes, modules, and extension points;
- non-obvious algorithms;
- invariants and preconditions;
- security assumptions;
- transaction boundaries;
- idempotency and retry behavior;
- timeout, budget, and cancellation semantics;
- normalization of provider-specific errors;
- edge cases that tests might not make obvious.

Do not comment obvious assignments or restate type names. Good comments explain
why behavior exists, what can go wrong, and what must stay true.

## Recommended Future Tooling

When implementation starts, use generated references instead of hand-maintained
symbol inventories:

- Python: docstrings plus a generator such as `pdoc`, `mkdocs-gen-files`, or
  Sphinx if the project grows enough to justify it.
- TypeScript: TSDoc comments plus TypeDoc for exported UI/client/contracts code.
- API: generated OpenAPI from FastAPI, checked for drift.
- Schemas: generated JSON Schema reference from `packages/contracts`.

Generated reference output should be reproducible. Commit it only if it is useful
for reviewers and drift-checked in CI; otherwise generate it locally or publish
it with docs builds.

## Suggested Files

Create these when the relevant implementation exists:

- `cli.md`;
- `suite-schema.md`;
- `result-bundle-schema.md`;
- `run-lifecycle.md`;
- `scorers.md`;
- `provider-adapters.md`;
- `worker-execution.md`;
- `telemetry.md`;
- `api.md`;
- `generated/README.md`.

## Maintenance Rules

- Update reference docs in the same change that changes public behavior.
- Link to source files once code exists.
- Prefer examples that are small, deterministic, and safe for public commits.
- Mark planned behavior as planned, not implemented.
- Date generated references and make the generating command visible.

