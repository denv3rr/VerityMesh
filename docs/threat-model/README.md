# Threat Model

The threat model should cover assets, trust boundaries, abuse cases,
mitigations, residual risk, and test coverage.

Minimum abuse cases:

- cross-project access;
- poisoned documents;
- indirect prompt injection;
- unauthorized tool use;
- data exfiltration through model or tool output;
- judge manipulation;
- runaway cost;
- denial of service through oversized or malformed input;
- malicious exported HTML or Markdown;
- secret leakage through prompts, traces, logs, reports, or fixtures.

