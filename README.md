# PiWardrive

PiWardrive is a headless mapping and diagnostics toolkit targeting the Raspberry Pi. It merges war‑driving tools such as Kismet and BetterCAP with a lightweight command line SIGINT suite. The preferred interface is a React dashboard served by FastAPI.

## Installation

1. Install system packages (`git`, `build-essential`, `cmake`, `kismet`, `bettercap`, `gpsd`) and Python 3.10 or newer.
2. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/TRASHYTALK/piwardrive.git
   cd piwardrive
   python3 -m venv gui-env
   source gui-env/bin/activate
   ```
3. Install dependencies and the package:
   ```bash
   pip install -r requirements.txt
   pip install .
   ```
4. Build the React frontend (Node.js 18+ required):
   ```bash
   cd webui && npm install && npm run build
   ```

## Usage

Start the API and web interface after activating the environment:
```bash
python -m piwardrive.webui_server
```
The server listens on `0.0.0.0:8000` by default. Visit `http://<pi-ip>:8000/` to open the dashboard.

### Example: Sync recent health records

```python
import asyncio
from piwardrive import remote_sync

asyncio.run(
    remote_sync.sync_new_records(
        "~/piwardrive/health.db",
        "http://10.0.0.2:9000/",
        timeout=10,
        retries=5,
    )
)
```

### Example: Launch API only

```python
from piwardrive import service

if __name__ == "__main__":
    service.main()
```

## Contributing

Install the development requirements and run the linters/tests:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit run --all-files
pytest
```

See [docs/](docs/index.rst) and [REFERENCE.md](REFERENCE.md) for further guides.

## Legal Notice

Ensure all wireless and Bluetooth scans comply with local laws. The authors are not responsible for misuse of this software.
