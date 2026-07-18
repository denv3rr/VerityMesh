# Scorers

Implementation: `packages/eval-core/src/veritymesh_eval_core/scorers.py`

Scorer version: `deterministic-scorers.v0`

All scorers return:

- scorer `name`;
- scorer `type`;
- scorer `version`;
- `passed`;
- `actual`;
- `expected`;
- optional failure `reason`;
- optional diagnostic `details`.

## Path Resolution

Scorers read values with dotted paths such as `output.answer`,
`output.structured.intent`, or `output.tool_calls.0.name`.

The evaluation context contains:

- `case`;
- `input`;
- `expected`;
- `output`;
- `evidence`;
- `tool_invocations`;
- `model_invocations`.

## `exact_match`

Compares the resolved actual value with `expected`.

Fields:

- `actual`;
- `expected`;
- `case_sensitive`, optional boolean for string comparisons.

## `contains`

Requires the resolved actual value to be a string containing `expected`.

Fields:

- `actual`;
- `expected`;
- `case_sensitive`, optional boolean.

## `regex`

Requires the resolved actual string to match `pattern`.

Fields:

- `actual`;
- `pattern`;
- `flags`, optional list containing `IGNORECASE`, `MULTILINE`, or `DOTALL`.

## `structured_output`

Validates the resolved value against a small JSON Schema subset.

Supported schema keywords:

- `type`;
- `required`;
- `properties`;
- `enum`;
- `items`.

Supported types:

- `object`;
- `array`;
- `string`;
- `number`;
- `integer`;
- `boolean`;
- `null`.

This is intentionally not a full JSON Schema implementation. If the project
needs full compliance later, add a dependency through an ADR or dependency
policy update.

## `citation`

Checks whether expected evidence ids appear in output citations.

Fields:

- `actual`, optional, default `output.citations`;
- `expected`, list of evidence ids;
- `require_all`, optional boolean, default `true`.

Diagnostics include:

- `precision`;
- `recall`;
- `matched`.

## `tool_call`

Checks whether required tool calls appear in `output.tool_calls`.

Fields:

- `actual`, optional, default `output.tool_calls`;
- `expected`, list of calls with `name` and optional `arguments`;
- `match_arguments`, optional, `subset` or `exact`.

The default argument matching mode is `subset`, which allows workflows to pass
additional safe arguments while still requiring the expected core arguments.

