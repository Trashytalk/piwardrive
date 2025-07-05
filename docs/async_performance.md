# Async Performance Optimization

This guide summarizes best practices for combining asyncio with CPU-bound workloads in PiWardrive.

## Async Performance Architecture

```mermaid
graph TB
    A[Async Event Loop] --> B[CPU-bound Tasks]
    A --> C[I/O-bound Tasks]
    A --> D[Background Jobs]
    
    B --> E[Process Pool Executor]
    B --> F[Multiple CPU Cores]
    
    C --> G[Network Operations]
    C --> H[Database Queries]
    C --> I[File I/O]
    
    D --> J[Priority Task Queue]
    D --> K[Scheduled Tasks]
    
    L[Distributed Caching] --> M[Redis Cache]
    L --> N[Cross-process Storage]
    
    O[Monitoring] --> P[Performance Metrics]
    O --> Q[Execution Times]
    O --> R[Grafana Visualization]
    
    S[Circuit Breaker] --> T[External Services]
    S --> U[Failure Recovery]
    
    style A fill:#e1f5fe
    style B fill:#ffebee
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style L fill:#fce4ec
    style O fill:#f3e5f5
    style S fill:#e0f2f1
```

## Performance Optimization Flow

```mermaid
graph LR
    A[Async Task] --> B{CPU-bound?}
    B -->|Yes| C[Process Pool]
    B -->|No| D[Async Execution]
    
    C --> E[Multiple Cores]
    D --> F[Event Loop]
    
    E --> G[Task Completion]
    F --> G
    
    G --> H[Cache Results]
    H --> I[Monitor Performance]
    I --> J[Apply Optimizations]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#ffebee
    style D fill:#e8f5e8
    style E fill:#fce4ec
    style F fill:#f3e5f5
    style G fill:#e0f2f1
    style H fill:#e8f5e8
    style I fill:#fff3e0
    style J fill:#fce4ec
```

## Process pool

Use `piwardrive.cpu_pool.run_cpu_bound` to execute expensive computations in a separate `ProcessPoolExecutor`. This prevents blocking the main event loop and allows multiple CPU cores to be utilized.

## Task priority

Background jobs can be scheduled using `PriorityTaskQueue` which processes tasks based on priority values. Lower numbers run first.

## Distributed caching

`RedisCache` stores results across processes. Call `.set(key, value, ttl)` to persist values and `.invalidate(key)` to remove them.

## Monitoring

Wrap critical sections with `performance.record(name)` to capture execution times. Metrics are available via `performance.get_metrics()` and can be visualized in Grafana.

## Circuit breaker

External services may become unreliable. Wrap async calls with `CircuitBreaker` to stop issuing requests after repeated failures and automatically recover after a timeout.
