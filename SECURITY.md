# Security Policy

VerityMesh handles untrusted suites, documents, model outputs, tool outputs,
reports, and user-supplied workflow data. Security requirements are part of the
product, not a later hardening phase.

## Baseline Requirements

- Parse untrusted input with strict schemas and size limits.
- Use parameterized SQL and safe rendering.
- Separate system instructions, user data, retrieved content, and tool output in
  the execution model.
- Grant tools explicit capabilities only.
- Default tools to read-only, least privilege, short timeouts, bounded
  arguments, and bounded output.
- Never commit secrets, API keys, `.env` files, prompt payloads containing
  secrets, or secret-bearing traces.
- Redact sensitive values before logging, persistence, and report export.
- Record security-relevant actions in append-only audit events.

## Reporting

This repository is not yet public-release ready. Until a public vulnerability
process is established, report security findings privately to the repository
owner.

