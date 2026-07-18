# Market and Model Watch

Purpose: keep VerityMesh aligned with current market signals, AI evaluation
practice, model/provider behavior, security expectations, and framework support
without letting trend-chasing expand scope.

The current guideline research notes were checked on July 17, 2026. Treat them
as a historical baseline, not permanent truth.

## Cadence

- Weekly: scan current signals that could affect the active milestone.
- Milestone entry: refresh only facts needed for the milestone.
- Monthly: review role-market and portfolio positioning.
- Quarterly: review architecture, dependencies, benchmark methodology, and
  provider strategy.
- Immediate: refresh sources when a user asks for latest/current information or
  when a dependency/provider/model/security fact may have changed.

## Source Priority

Use primary sources first:

- official provider docs, pricing pages, deprecation notices, model release
  notes, API references, and service status pages;
- official framework release notes and support policies;
- security advisories from maintainers, package registries, OSV, GitHub
  Security Advisories, and container base-image maintainers;
- original research papers, benchmark pages, or technical reports;
- official job postings and company career pages;
- standards or regulator publications when compliance or safety claims are in
  scope.

Use secondary sources only for discovery. Do not base architecture or portfolio
claims on unsourced commentary.

## Weekly Checklist

Record a dated entry if any checked item changes project decisions.

- Model APIs: structured outputs, tool calling, batch APIs, context limits,
  safety controls, rate limits, SDK changes, deprecations, and pricing.
- Local/offline model path: model availability, license, runtime support,
  hardware expectations, and deterministic test feasibility.
- Evaluation practice: new guidance on groundedness, citation evaluation,
  evaluator agreement, judge-model risk, benchmark contamination, and agent
  safety testing.
- Retrieval stack: PostgreSQL/pgvector need, embedding model changes, chunking
  strategy guidance, citation-span support, and hybrid retrieval options.
- Platform stack: Python, FastAPI, Pydantic, React, TypeScript, PostgreSQL,
  Redis, OpenTelemetry, container image, and test tool support.
- Security: dependency advisories, prompt-injection research, sandbox escape
  patterns, secret-handling guidance, and generated-content rendering risks.
- Market signals: backend/platform/evals/applied-AI job descriptions,
  relocation expectations, required skills, and portfolio evidence requested.

## Decision Rules

Make no change if the signal is interesting but does not affect the current
milestone, near-term dependency, benchmark validity, security posture, cost, or
portfolio positioning.

Open an issue or update the plan if:

- a provider deprecates or changes an API VerityMesh uses;
- pricing or rate limits threaten demos, tests, or experiments;
- a security advisory affects a dependency or deployment path;
- a framework reaches end of support;
- a model/provider feature simplifies the adapter layer without lock-in;
- current hiring signals consistently reward a different presentation of the
  same project evidence;
- evaluation research exposes a flaw in the benchmark or scoring methodology.

Write an ADR if the response changes architecture, storage, public contracts,
deployment topology, provider strategy, or recurring cost.

## Snapshot Template

```text
Date:
Reviewer:
Reason for review:

Sources checked:
- Source name:
  URL:
  Access date:
  Relevant fact:

Observed changes:
- 

Project impact:
- None / issue opened / ADR required / plan updated

Decision:
- 

Next review trigger:
- 
```

## Log

### 2026-07-17

Reason: initial project guideline snapshot.

Sources: see `Project_Guidelines.md`, section 15.

Decision: build a model-agnostic AI evaluation and evidence platform centered
on reproducible evals, provenance, security boundaries, observability, release
gates, and human review. Keep initial CI deterministic and offline.

Next review trigger: before choosing the first hosted provider adapter, public
benchmark corpus, or application-positioning claims.

