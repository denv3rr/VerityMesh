# SPDX-License-Identifier: Apache-2.0
"""Versioned evaluation suite contract.

The v0 suite schema is intentionally small. It defines enough structure for the
offline evaluation core while keeping future API and persistence layers free to
version the same concepts without model-provider coupling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from veritymesh_contracts.errors import ContractValidationError, ValidationIssue


SUITE_SCHEMA_VERSION = "veritymesh.suite.v0"
MAX_CASES = 5_000
MAX_STRING_LENGTH = 20_000

_TOP_LEVEL_KEYS = {"schema_version", "suite", "workflow", "cases"}
_SUITE_KEYS = {"id", "version", "name", "description", "metadata"}
_WORKFLOW_KEYS = {"id", "version"}
_CASE_KEYS = {"id", "category", "difficulty", "input", "expected", "scorers", "metadata"}
_SCORER_BASE_KEYS = {"type", "name"}
_SCORER_KEYS_BY_TYPE = {
    "exact_match": _SCORER_BASE_KEYS | {"actual", "expected", "case_sensitive"},
    "contains": _SCORER_BASE_KEYS | {"actual", "expected", "case_sensitive"},
    "regex": _SCORER_BASE_KEYS | {"actual", "pattern", "flags"},
    "structured_output": _SCORER_BASE_KEYS | {"actual", "schema"},
    "citation": _SCORER_BASE_KEYS | {"actual", "expected", "require_all"},
    "tool_call": _SCORER_BASE_KEYS | {"actual", "expected", "match_arguments"},
}


@dataclass(frozen=True)
class SuiteMetadata:
    id: str
    version: str
    name: str
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "version": self.version,
            "name": self.name,
        }
        if self.description is not None:
            payload["description"] = self.description
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload


@dataclass(frozen=True)
class WorkflowSpec:
    id: str
    version: str

    def to_mapping(self) -> dict[str, str]:
        return {"id": self.id, "version": self.version}


@dataclass(frozen=True)
class ScorerSpec:
    name: str
    type: str
    config: dict[str, Any]

    def to_mapping(self) -> dict[str, Any]:
        return {"name": self.name, "type": self.type, **self.config}


@dataclass(frozen=True)
class EvalCase:
    id: str
    category: str
    difficulty: str
    input: dict[str, Any]
    expected: dict[str, Any]
    scorers: list[ScorerSpec]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "input": self.input,
            "expected": self.expected,
            "scorers": [scorer.to_mapping() for scorer in self.scorers],
        }
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload


@dataclass(frozen=True)
class EvalSuite:
    schema_version: str
    suite: SuiteMetadata
    workflow: WorkflowSpec
    cases: list[EvalCase]

    @classmethod
    def from_mapping(cls, payload: Any) -> "EvalSuite":
        issues: list[ValidationIssue] = []
        if not isinstance(payload, Mapping):
            raise ContractValidationError([ValidationIssue("$", "must be an object", "type")])
        _reject_unknown_keys(payload, _TOP_LEVEL_KEYS, "$", issues)

        schema_version = _required_str(payload, "schema_version", "$.schema_version", issues)
        if schema_version and schema_version != SUITE_SCHEMA_VERSION:
            issues.append(
                ValidationIssue(
                    "$.schema_version",
                    f"expected {SUITE_SCHEMA_VERSION!r}",
                    "unsupported_schema_version",
                )
            )

        suite_payload = _required_mapping(payload, "suite", "$.suite", issues)
        workflow_payload = _required_mapping(payload, "workflow", "$.workflow", issues)
        cases_payload = _required_list(payload, "cases", "$.cases", issues)

        suite = _parse_suite_metadata(suite_payload, issues)
        workflow = _parse_workflow(workflow_payload, issues)
        cases = _parse_cases(cases_payload, issues)

        if issues:
            raise ContractValidationError(issues)
        return cls(
            schema_version=schema_version,
            suite=suite,
            workflow=workflow,
            cases=cases,
        )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "suite": self.suite.to_mapping(),
            "workflow": self.workflow.to_mapping(),
            "cases": [case.to_mapping() for case in self.cases],
        }


def _parse_suite_metadata(payload: Mapping[str, Any], issues: list[ValidationIssue]) -> SuiteMetadata:
    _reject_unknown_keys(payload, _SUITE_KEYS, "$.suite", issues)
    return SuiteMetadata(
        id=_required_str(payload, "id", "$.suite.id", issues),
        version=_required_str(payload, "version", "$.suite.version", issues),
        name=_required_str(payload, "name", "$.suite.name", issues),
        description=_optional_str(payload, "description", "$.suite.description", issues),
        metadata=_optional_mapping(payload, "metadata", "$.suite.metadata", issues),
    )


def _parse_workflow(payload: Mapping[str, Any], issues: list[ValidationIssue]) -> WorkflowSpec:
    _reject_unknown_keys(payload, _WORKFLOW_KEYS, "$.workflow", issues)
    return WorkflowSpec(
        id=_required_str(payload, "id", "$.workflow.id", issues),
        version=_required_str(payload, "version", "$.workflow.version", issues),
    )


def _parse_cases(payload: list[Any], issues: list[ValidationIssue]) -> list[EvalCase]:
    if not payload:
        issues.append(ValidationIssue("$.cases", "must contain at least one case", "empty"))
    if len(payload) > MAX_CASES:
        issues.append(ValidationIssue("$.cases", f"must contain no more than {MAX_CASES} cases", "too_large"))

    cases: list[EvalCase] = []
    seen_ids: set[str] = set()
    for index, case_payload in enumerate(payload):
        path = f"$.cases[{index}]"
        if not isinstance(case_payload, Mapping):
            issues.append(ValidationIssue(path, "must be an object", "type"))
            continue
        _reject_unknown_keys(case_payload, _CASE_KEYS, path, issues)
        case_id = _required_str(case_payload, "id", f"{path}.id", issues)
        if case_id in seen_ids:
            issues.append(ValidationIssue(f"{path}.id", "case ids must be unique", "duplicate"))
        seen_ids.add(case_id)

        input_payload = _required_mapping(case_payload, "input", f"{path}.input", issues)
        expected_payload = _required_mapping(case_payload, "expected", f"{path}.expected", issues)
        scorers_payload = _required_list(case_payload, "scorers", f"{path}.scorers", issues)
        scorers = _parse_scorers(scorers_payload, f"{path}.scorers", issues)

        cases.append(
            EvalCase(
                id=case_id,
                category=_required_str(case_payload, "category", f"{path}.category", issues),
                difficulty=_required_str(case_payload, "difficulty", f"{path}.difficulty", issues),
                input=dict(input_payload),
                expected=dict(expected_payload),
                scorers=scorers,
                metadata=_optional_mapping(case_payload, "metadata", f"{path}.metadata", issues),
            )
        )
    return cases


def _parse_scorers(payload: list[Any], path: str, issues: list[ValidationIssue]) -> list[ScorerSpec]:
    if not payload:
        issues.append(ValidationIssue(path, "must contain at least one scorer", "empty"))
    scorers: list[ScorerSpec] = []
    seen_names: set[str] = set()
    for index, scorer_payload in enumerate(payload):
        scorer_path = f"{path}[{index}]"
        if not isinstance(scorer_payload, Mapping):
            issues.append(ValidationIssue(scorer_path, "must be an object", "type"))
            continue
        scorer_type = _required_str(scorer_payload, "type", f"{scorer_path}.type", issues)
        scorer_name = _required_str(scorer_payload, "name", f"{scorer_path}.name", issues)
        if scorer_name in seen_names:
            issues.append(ValidationIssue(f"{scorer_path}.name", "scorer names must be unique per case", "duplicate"))
        seen_names.add(scorer_name)

        allowed_keys = _SCORER_KEYS_BY_TYPE.get(scorer_type)
        if allowed_keys is None and scorer_type:
            issues.append(ValidationIssue(f"{scorer_path}.type", f"unsupported scorer type {scorer_type!r}", "unsupported"))
            allowed_keys = _SCORER_BASE_KEYS
        _reject_unknown_keys(scorer_payload, allowed_keys, scorer_path, issues)

        config = {key: value for key, value in scorer_payload.items() if key not in _SCORER_BASE_KEYS}
        _validate_scorer_config(scorer_type, config, scorer_path, issues)
        scorers.append(ScorerSpec(name=scorer_name, type=scorer_type, config=config))
    return scorers


def _validate_scorer_config(
    scorer_type: str,
    config: Mapping[str, Any],
    path: str,
    issues: list[ValidationIssue],
) -> None:
    if scorer_type in {"exact_match", "contains"}:
        _config_str(config, "actual", f"{path}.actual", issues)
        if "expected" not in config:
            issues.append(ValidationIssue(f"{path}.expected", "is required", "required"))
        if "case_sensitive" in config and not isinstance(config["case_sensitive"], bool):
            issues.append(ValidationIssue(f"{path}.case_sensitive", "must be a boolean", "type"))
    elif scorer_type == "regex":
        _config_str(config, "actual", f"{path}.actual", issues)
        _config_str(config, "pattern", f"{path}.pattern", issues)
        if "flags" in config and not isinstance(config["flags"], list):
            issues.append(ValidationIssue(f"{path}.flags", "must be a list of flag names", "type"))
    elif scorer_type == "structured_output":
        _config_str(config, "actual", f"{path}.actual", issues)
        if not isinstance(config.get("schema"), Mapping):
            issues.append(ValidationIssue(f"{path}.schema", "must be an object", "type"))
    elif scorer_type == "citation":
        if "actual" in config:
            _config_str(config, "actual", f"{path}.actual", issues)
        if not _is_string_list(config.get("expected")):
            issues.append(ValidationIssue(f"{path}.expected", "must be a list of evidence ids", "type"))
        if "require_all" in config and not isinstance(config["require_all"], bool):
            issues.append(ValidationIssue(f"{path}.require_all", "must be a boolean", "type"))
    elif scorer_type == "tool_call":
        if "actual" in config:
            _config_str(config, "actual", f"{path}.actual", issues)
        if not isinstance(config.get("expected"), list):
            issues.append(ValidationIssue(f"{path}.expected", "must be a list of expected calls", "type"))
        if "match_arguments" in config and config["match_arguments"] not in {"subset", "exact"}:
            issues.append(ValidationIssue(f"{path}.match_arguments", "must be 'subset' or 'exact'", "unsupported"))


def _required_str(payload: Mapping[str, Any], key: str, path: str, issues: list[ValidationIssue]) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        issues.append(ValidationIssue(path, "must be a non-empty string", "type"))
        return ""
    if len(value) > MAX_STRING_LENGTH:
        issues.append(ValidationIssue(path, f"must be no longer than {MAX_STRING_LENGTH} characters", "too_large"))
        return ""
    return value


def _optional_str(payload: Mapping[str, Any], key: str, path: str, issues: list[ValidationIssue]) -> str | None:
    if key not in payload:
        return None
    value = payload[key]
    if value is None:
        return None
    if not isinstance(value, str):
        issues.append(ValidationIssue(path, "must be a string or null", "type"))
        return None
    if len(value) > MAX_STRING_LENGTH:
        issues.append(ValidationIssue(path, f"must be no longer than {MAX_STRING_LENGTH} characters", "too_large"))
        return None
    return value


def _required_mapping(
    payload: Mapping[str, Any],
    key: str,
    path: str,
    issues: list[ValidationIssue],
) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        issues.append(ValidationIssue(path, "must be an object", "type"))
        return {}
    return value


def _optional_mapping(
    payload: Mapping[str, Any],
    key: str,
    path: str,
    issues: list[ValidationIssue],
) -> dict[str, Any]:
    if key not in payload:
        return {}
    value = payload[key]
    if not isinstance(value, Mapping):
        issues.append(ValidationIssue(path, "must be an object", "type"))
        return {}
    return dict(value)


def _required_list(
    payload: Mapping[str, Any],
    key: str,
    path: str,
    issues: list[ValidationIssue],
) -> list[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        issues.append(ValidationIssue(path, "must be a list", "type"))
        return []
    return value


def _require_mapping(value: Any, path: str, issues: list[ValidationIssue]) -> None:
    if not isinstance(value, Mapping):
        issues.append(ValidationIssue(path, "must be an object", "type"))


def _reject_unknown_keys(
    payload: Mapping[str, Any],
    allowed: set[str],
    path: str,
    issues: list[ValidationIssue],
) -> None:
    for key in payload:
        if key not in allowed:
            issues.append(ValidationIssue(f"{path}.{key}", "unknown field", "unknown_field"))


def _config_str(config: Mapping[str, Any], key: str, path: str, issues: list[ValidationIssue]) -> None:
    if not isinstance(config.get(key), str) or not str(config.get(key)).strip():
        issues.append(ValidationIssue(path, "must be a non-empty string", "type"))


def _is_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)
