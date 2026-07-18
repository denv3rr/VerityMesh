# Eval Core Package

Owns deterministic evaluation behavior.

Implemented v0:

- suite validation;
- result bundle generation;
- exact match, substring/regex, structured-output, citation, and tool-call
  scorers;
- deterministic fake workflow fixtures;
- CLI behavior for offline runs;

Future responsibilities:

- score aggregation without hiding dimensions;
- golden fixtures and property tests.

This package must not require network access or paid model calls.

Source package: `packages/eval-core/src/veritymesh_eval_core/`.
