# PiWardrive Reference

This document consolidates the key information from `README.md`, the `sigint_suite` guide and the various RST files under `docs/`.

## Overview

PiWardrive provides a headless mapping and diagnostic interface built with Kivy/KivyMD. It manages Wi‑Fi and Bluetooth scanning via Kismet and BetterCAP while polling GPS data and system metrics. Results are logged to `~/.config/piwardrive/app.log` and persisted in a SQLite database. A lightweight SIGINT suite for command-line scanning lives under `sigint_suite/`.

## Hardware and OS Requirements

- Raspberry Pi 5 with a 7" touch screen and SSD mounted at `/mnt/ssd`
- GPS dongle on `/dev/ttyACM0` managed by `gpsd`
- External Wi‑Fi adapter capable of monitor mode
- Raspberry Pi OS Bookworm (or Bullseye backports) with Python 3.12

## Installation

1. Install system packages:
   ```bash
   sudo apt update && sudo apt install -y \
       git build-essential cmake kismet bettercap gpsd evtest python3-venv
   ```
2. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/TRASHYTALK/piwardrive.git
   cd piwardrive
   python3 -m venv gui-env
   source gui-env/bin/activate
   ```
3. Install Python dependencies and build the C extensions:
   ```bash
   pip install -r requirements.txt
   pip install .
   pip install build
   python -m build
   pip install dist/*.whl
   ```
4. Optionally enable `kismet`, `bettercap` and `gpsd` to start on boot and create a `piwardrive.service` unit.

See `docs/installation.rst` and `docs/deployment.rst` for additional tips and troubleshooting notes.

## Configuration

Settings are stored in `~/.config/piwardrive/config.json`. Any value can be overridden with environment variables prefixed with `PW_`. Multiple profiles may be kept under `~/.config/piwardrive/profiles`; switch with `PW_PROFILE_NAME` or by editing `active_profile`.

Important options include GPS polling (`map_poll_gps` and `map_poll_gps_max`), Bluetooth scanning (`map_poll_bt` and `map_show_bt`), log rotation intervals and the `health_poll_interval` controlling diagnostics. Invalid values raise errors on startup. Example configuration lives in `examples/default_profile.json`.

## Running the Application

```bash
cd ~/piwardrive
source gui-env/bin/activate
python main.py
```
The UI renders directly to the framebuffer without X. Use the top tabs to switch between Map, Stats, Split, Console, Settings and Dashboard screens. Widgets can be dragged on the Dashboard and their layout is persisted.

## Widgets and Plugins

Dashboard widgets display metrics such as CPU temperature, handshake counts and service status. Custom widgets may be placed in `~/.config/piwardrive/plugins` and are discovered automatically at startup. Each widget subclasses `widgets.base.DashboardWidget` and implements an `update()` method. A built-in battery widget is available when the hardware exposes charge information.

## Diagnostics and Persistence

The `diagnostics` module gathers system metrics and rotates logs according to the configured schedule. Results are stored in a SQLite database via the `persistence` module which also remembers the last active screen between runs. Diagnostics can be accessed through the Stats screen or queried over HTTP.

## Status Service and Web UI

Running `python -m service` starts a FastAPI server on `0.0.0.0:8000`. The `/status` endpoint returns recent health records and `/logs` tails `app.log`. Set `PW_API_PASSWORD_HASH` to require HTTP basic authentication. The optional React frontend under `webui/` consumes this API and can be built with `npm run build`.

## GPS and Bluetooth Polling

The application polls `gpsd` at a configurable interval, increasing the delay when movement stops to conserve power. Bluetooth scanning is also optional and can be toggled or scheduled via configuration variables.

## Mobile Builds

Helper scripts `scripts/build_android.sh` and `scripts/build_ios.sh` package PiWardrive for Android or iOS. Android builds rely on Buildozer while iOS builds require `kivy-ios`. Some diagnostics and service management features are disabled on mobile platforms.

## Building the CKML Extension

The project includes small C extensions `ckml` and `cgeom`. Build them with:
```bash
pip install build
python -m build
pip install dist/*.whl
```
See `docs/ckml_build.rst` for troubleshooting compiler issues.

## R Integration

`scripts/health_summary.R` can analyse exported `HealthRecord` data. Install `rpy2`, `r-base` and the `ggplot2`/`jsonlite` R packages to enable `r_integration.health_summary`.
`scripts/health_export.py` dumps recent metrics to JSON or CSV while
`scripts/health_import.py` loads such files back into the tracking database.
`scripts/service_status.py` prints the active state of common services.

Additional optional features use `pandas`, `orjson` and `pyprof2calltree` which can be installed via:

```bash
pip install pandas orjson pyprof2calltree
```

## Deployment Options

The software can run from an SD card image or inside a Docker container. For Docker, start from `python:3.11-bullseye`, install the system packages, copy the project to `/app`, run `pip install -r requirements.txt` and set `CMD ["python", "main.py"]`. Map USB devices and persist `~/.config/piwardrive` with a volume.

## Workflows and Function Flows

The `docs/` directory contains mermaid diagrams showing scanning, logging and diagnostic sequences. `function_flows.rst` illustrates how `PollScheduler.register_widget` schedules callbacks and how `utils.run_async_task` offloads coroutines.

## SIGINT Suite

Under `sigint_suite/` you will find lightweight command-line tools for scanning Wi‑Fi and Bluetooth. The `scripts/start_imsi_mode.sh` helper runs one Wi‑Fi and Bluetooth scan and writes JSON results under `sigint_suite/exports/`. Override `EXPORT_DIR` to change the location. Ensure `iwlist` and either `bluetoothctl` or the Python ``bleak`` library are installed (`./sigint_suite/scripts/setup_all.sh` can install them).


## Environment Variables

The application recognises numerous `PW_*` variables. Any option in `config.py` can be overridden by prefixing it with `PW_`. Additional variables enable profiling, authentication and localisation.

`PW_THEME` – Select the UI theme.

`PW_MAP_POLL_GPS` – GPS polling interval while moving.

`PW_MAP_POLL_GPS_MAX` – Maximum GPS delay when stationary.

`PW_MAP_POLL_APS` – Wi-Fi access point scan interval.

`PW_MAP_POLL_BT` – Bluetooth scan interval.

`PW_MAP_SHOW_GPS` – Show the GPS marker on the map.

`PW_MAP_SHOW_APS` – Show Wi-Fi markers on the map.

`PW_MAP_SHOW_BT` – Show Bluetooth markers on the map.

`PW_MAP_CLUSTER_APS` – Enable AP clustering.

`PW_MAP_CLUSTER_CAPACITY` – Number of APs per cluster cell.

`PW_MAP_USE_OFFLINE` – Use the offline tile set for map data.

`PW_DISABLE_SCANNING` – Disable all Wi-Fi and Bluetooth scanning.

`PW_KISMET_LOGDIR` – Directory where Kismet writes logs.

`PW_BETTERCAP_CAPLET` – Path to the BetterCAP caplet.

`PW_DASHBOARD_LAYOUT` – JSON encoded dashboard widget layout.

`PW_DEBUG_MODE` – Enable verbose debug output.

`PW_OFFLINE_TILE_PATH` – Location of the offline MBTiles file.

`PW_LOG_PATHS` – JSON array of log files shown in the console screen.

`PW_HEALTH_POLL_INTERVAL` – Interval between health metric polls.

`PW_LOG_ROTATE_INTERVAL` – Seconds between log rotations.

`PW_LOG_ROTATE_ARCHIVES` – Number of rotated archives to keep.

`PW_CLEANUP_ROTATED_LOGS` – Remove rotated logs when `1`.

`PW_WIDGET_BATTERY_STATUS` – Enable the battery status widget.

`PW_UI_FONT_SIZE` – Override the global font size.

`PW_ADMIN_PASSWORD_HASH` – Stored hash for privileged actions.

`PW_ADMIN_PASSWORD` – Plain text admin password prompt override.

`PW_API_PASSWORD_HASH` – HTTP basic auth hash for the API.

`PW_DB_PATH` – Path to the SQLite database.

`PW_PROFILE_NAME` – Configuration profile name to load.

`PW_PROFILE` – Set to `1` to enable runtime profiling.

`PW_PROFILE_CALLGRIND` – Callgrind output path when profiling.

`PW_LANG` – Two-letter code selecting the interface language.


## Further Reference

Additional details on each module are documented in the source code and in the individual RST files under `docs/`.
