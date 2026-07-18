# Suite Schema v0

Schema version: `veritymesh.suite.v0`

Implementation: `packages/contracts/src/veritymesh_contracts/suite.py`

The v0 suite schema defines a deterministic evaluation suite. It is strict:
unknown fields are rejected so accidental or misspelled configuration does not
silently change evaluation behavior.

## Top-Level Shape

```json
{
  "schema_version": "veritymesh.suite.v0",
  "suite": {
    "id": "support-smoke-v1",
    "version": "2026-07-17",
    "name": "Support smoke suite",
    "description": "Optional description",
    "metadata": {}
  },
  "workflow": {
    "id": "fake-support-agent",
    "version": "fake-support-agent.v0"
  },
  "cases": []
}
```

Required top-level fields:

- `schema_version`;
- `suite`;
- `workflow`;
- `cases`.

Limits:

- max suite file size: 1,000,000 bytes;
- max cases: 5,000;
- max string length for validated string fields: 20,000 characters.

## Case Shape

```json
{
  "id": "password-reset",
  "category": "normal",
  "difficulty": "easy",
  "input": {
    "question": "How do I reset my password?"
  },
  "expected": {},
  "scorers": [],
  "metadata": {}
}
```

Required case fields:

- `id`;
- `category`;
- `difficulty`;
- `input`;
- `expected`;
- `scorers`.

Case ids must be unique inside a suite.

## Scorer Shape

All scorers require:

- `name`: unique within the case;
- `type`: one of the supported deterministic scorer types.

Supported types:

- `exact_match`;
- `contains`;
- `regex`;
- `structured_output`;
- `citation`;
- `tool_call`.

Detailed scorer behavior is documented in `docs/reference/scorers.md`.

