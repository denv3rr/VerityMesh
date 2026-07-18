# Eval Core Package

Owns deterministic evaluation behavior.

Future responsibilities:

- suite validation;
- result bundle generation;
- exact match, substring/regex, structured-output, citation, and tool-call
  scorers;
- score aggregation without hiding dimensions;
- deterministic fake workflow fixtures;
- CLI behavior for offline runs;
- golden fixtures and property tests.

This package must not require network access or paid model calls.

