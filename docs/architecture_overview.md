# Architecture Overview

The project follows a modular design with a FastAPI backend and a React frontend. Data is collected by scheduled tasks and stored in SQLite. Optional services such as GPS or Bluetooth can be enabled via configuration.

```
[React Dashboard] <--REST--> [FastAPI Service] <---> [SQLite DB]
                              |
                              +--[Scheduler & Diagnostics]
                              +--[External Tools: Kismet, BetterCAP]
```

Additional diagrams and a deep dive into each component are available in `docs/architecture.md`.
