# Core Functionality Index

Status: planned. This file should become the high-level map for implemented
core behavior. Keep it concise and link to deeper references as they are added.

## Evaluation Core

Planned responsibilities:

- validate versioned suites;
- run deterministic workflows;
- execute deterministic scorers;
- produce result bundles;
- preserve evidence and failure reasons separately from aggregate summaries.

Primary future package: `packages/eval-core/`.

## Contracts

Planned responsibilities:

- suite schema;
- result bundle schema;
- evaluator output schema;
- provider adapter contracts;
- telemetry event and metric conventions.

Primary future package: `packages/contracts/`.

## Provider Adapters

Planned responsibilities:

- deterministic fake adapter;
- local/offline adapter;
- hosted provider adapters behind opt-in tests;
- normalized model invocation metadata;
- structured error taxonomy.

Primary future package: `packages/provider-adapters/`.

## Worker Execution

Planned responsibilities:

- queue leases;
- retries;
- idempotency;
- cancellation;
- dead-letter handling;
- execution budgets;
- artifact capture.

Primary future app: `apps/worker/`.

## API

Planned responsibilities:

- projects;
- suites;
- workflows;
- runs;
- case executions;
- comparisons;
- release policies;
- users;
- audit events.

Primary future app: `apps/api/`.

## Web Console

Planned responsibilities:

- run overview;
- baseline/candidate comparison;
- case trace;
- human review;
- exportable reports;
- release decision view.

Primary future app: `apps/web/`.

