# Integration Tests

Integration tests should cover real component boundaries, including PostgreSQL,
Redis, migrations, API contracts, worker recovery, idempotency, cancellation,
and artifact persistence.

They should remain deterministic and should not require hosted model calls.

