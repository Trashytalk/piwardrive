# Scaling Architecture

This document outlines a progressive strategy for migrating from a single-node
SQLite deployment to a horizontally scalable PostgreSQL setup.

## Phases

1. **Abstraction Layer** – Introduce a database adapter pattern supporting
   SQLite, PostgreSQL and MySQL backends.  Existing persistence code can switch
   adapters without changing business logic.
2. **PostgreSQL Migration** – Deploy PostgreSQL alongside the existing SQLite
   database.  Data is copied using `migrate_sqlite_to_postgres.py` while the
   application continues to write to SQLite.  Once synchronization completes the
   service switches to the PostgreSQL adapter.
3. **Read Replicas** – Configure read-only replicas of the PostgreSQL primary.
   The `PostgresAdapter` performs round-robin load balancing for SELECT queries.
4. **Distributed Transactions** – Critical operations acquire advisory locks
   inside a transaction.  The `DatabaseManager` exposes `distributed_lock()`
   which wraps the adapter transaction and prevents concurrent writers.
5. **Horizontal Scaling** – Multiple application instances connect to the same
   PostgreSQL cluster with connection pooling via `asyncpg`.  Load balancers can
   distribute requests across nodes.

## Zero Downtime Migration

1. Start a PostgreSQL instance and run the migration script.
2. Verify data integrity using `validate_migration.py`.
3. Configure the application to use the `PostgresAdapter` while keeping the
   SQLite database as a fallback until the new backend is stable.

## Data Consistency

Row counts are compared across databases during validation.  Additional checks
can be implemented by querying hashes of table contents.

## Distributed Locking

`DatabaseManager.distributed_lock()` uses an asyncio lock combined with database
transactions to protect critical sections across the cluster.  PostgreSQL uses
`pg_advisory_xact_lock` to ensure only one writer performs an operation at a
time.

