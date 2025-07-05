# Backup and Disaster Recovery

This document outlines basic backup and recovery operations for a production
PiWardrive deployment.

## Backup Strategy Overview

```mermaid
graph TB
    A[Production System] --> B[Backup Strategy]
    B --> C[Database Backups]
    B --> D[Redis Backups]
    B --> E[Configuration Backups]
    B --> F[Application Data]
    
    C --> C1[PostgreSQL pg_dump]
    C --> C2[Scheduled Jobs]
    C --> C3[Compressed Archives]
    
    D --> D1[Redis SAVE Command]
    D --> D2[RDB Snapshots]
    D --> D3[Data Volume Sync]
    
    E --> E1[Config Files]
    E --> E2[Environment Variables]
    E --> E3[SSL Certificates]
    
    F --> F1[Scan Data]
    F --> F2[Log Files]
    F --> F3[User Data]
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#ffebee
```

## Recovery Process Flow

```mermaid
graph LR
    A[Disaster Event] --> B[Assessment]
    B --> C[Stop Services]
    C --> D[Restore Database]
    D --> E[Restore Redis]
    E --> F[Restore Config]
    F --> G[Start Services]
    G --> H[Verify Health]
    H --> I[Resume Operations]
    
    style A fill:#ffebee
    style B fill:#fff3e0
    style C fill:#fce4ec
    style D fill:#e8f5e8
    style E fill:#e1f5fe
    style F fill:#f3e5f5
    style G fill:#e0f2f1
    style H fill:#e8f5e8
    style I fill:#e8f5e8
```

## Database Backups

Run scheduled `pg_dump` jobs from the PostgreSQL container:

```bash
docker compose --file deploy/docker-compose.production.yml exec postgres \
  pg_dump -U piwardrive piwardrive | gzip > /backups/piwardrive.sql.gz
```

## Redis Backups

The Redis container stores data under `/data`. Create snapshots with:

```bash
docker compose --file deploy/docker-compose.production.yml exec redis \
  redis-cli save
```

## Restore Procedure

1. Stop the application containers.
2. Restore the PostgreSQL dump using `pg_restore`.
3. Copy Redis dump files back to the volume.
4. Start the stack and verify the application health endpoint.
