# ADR 0001: Start as a Modular Monolith

Status: proposed
Date: 2026-07-17

## Context

VerityMesh needs API, worker, evaluation, provider adapter, telemetry, storage,
and web-console boundaries. The project guidelines explicitly warn against
microservices and distributed infrastructure before measurable need exists.

## Decision

Start as a monorepo with clear package and app boundaries:

- `apps/api`;
- `apps/worker`;
- `apps/web`;
- `packages/contracts`;
- `packages/eval-core`;
- `packages/provider-adapters`;
- `packages/telemetry`.

Run a small number of processes locally. Use PostgreSQL and Redis when
persistence and queued execution begin. Extract services only after load tests,
fault-isolation needs, or deployment constraints provide evidence.

## Consequences

Benefits:

- faster first vertical slice;
- simpler local development;
- easier offline deterministic CI;
- clearer data-model evolution;
- fewer operational claims before evidence exists.

Costs:

- package boundaries must be enforced through code review, tests, and contracts;
- future service extraction requires discipline around interfaces;
- scaling claims must wait for measured load tests.

## Review Triggers

Revisit this ADR when:

- worker execution saturates API resources under measured load;
- queue recovery or fault isolation cannot be solved inside current boundaries;
- independent deployment becomes necessary;
- tenancy, security, or data isolation requires a harder boundary;
- recurring operations work exceeds the benefit of the simpler topology.

