# Integration Test Environment

Some integration tests rely on services defined in `docker-compose.yml`. The
helper script below starts the required containers in detached mode.

```bash
./scripts/start_test_env.sh
```

Run the script from the repository root before executing the tests. When finished
stop the services with:

```bash
docker compose down
```

See `docker-compose.yml` for the list of containers started.
