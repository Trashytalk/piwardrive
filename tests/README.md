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

## Running Unit Tests

Both the Python and Node.js test suites expect the required modules to be
installed. From the repository root run:

```bash
pip install -r config/requirements-dev.txt
npm install
```

Node based tests also need access to the Python sources. Export
`PYTHONPATH=src` when invoking them:

```bash
PYTHONPATH=src node --test tests/*.test.js
```

Tests that rely on Vitest (such as `tileMaintenanceCli.test.js`) can be run
with:

```bash
npx vitest run tests/tileMaintenanceCli.test.js
```
