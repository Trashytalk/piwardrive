# SIGINT Suite

The `sigint_suite` directory provides lightweight command-line tools for
collecting wireless and RF metadata. These helpers can be used separately from
the main PiWardrive UI when you only need quick scans or exports.

``sigint_suite`` is published as a standalone package on PyPI. Install it with

```bash
pip install sigint-suite
```

The installation provides the ``wifi-scan``, ``bluetooth-scan``, ``imsi-scan``,
``band-scan`` and ``scan-all`` entry points for quickly running scans from the
command line.

## Modules

- **bluetooth** – scan nearby Bluetooth devices via `hcitool`. Set
  ``BLUETOOTH_SCAN_TIMEOUT`` to change the scan duration (default ``10``
  seconds).
  
- **wifi** – discover Wi-Fi access points using `iwlist`. Results are enriched
  with vendor names when the IEEE OUI registry is available. Set the
  `IWLIST_CMD` environment variable to override the `iwlist` executable,
  `IW_PRIV_CMD` to change the privilege wrapper (default ``sudo``) and
  `WIFI_SCAN_TIMEOUT` to adjust the command timeout in seconds (default ``10``).
- **cellular.band_scanner** – scan available cellular bands via an external
  command specified by ``BAND_SCAN_CMD``. Set ``BAND_SCAN_TIMEOUT`` to change
  the timeout (default ``10`` seconds).
- **cellular.imsi_catcher** – stub for future IMSI catcher logic. Set
  ``IMSI_SCAN_TIMEOUT`` to control how long the external command may run
  (default ``10`` seconds).
- **cellular.tower_scanner** – scan LTE/5G towers. Use ``TOWER_SCAN_CMD`` to
  specify the executable and ``TOWER_SCAN_TIMEOUT`` for the timeout (default
  ``10`` seconds).
- **cellular.parsers** – parsers for raw cellular output.
- **cellular.tower_tracker** – persist cell towers, Wi‑Fi access points and
  Bluetooth devices in a SQLite database for historical queries.
- **dashboard** – minimal dashboard integration.
- **enrichment** – routines to enrich captured data.
- **exports** – helpers for writing results to JSON/CSV/YAML files.
- **gps** – GPS helpers for tagging results with location.
- **rf** – helpers powered by `pyrtlsdr` for spectrum scans and FM demodulation.
- **scripts** – shell scripts for running scans and installing dependencies.

### Async API

All scanner modules also provide asynchronous variants built with
``asyncio.create_subprocess_exec``. Use ``async_scan_wifi``,
``async_scan_bluetooth``, ``async_scan_bands`` and ``async_scan_imsis`` when
running inside an event loop.

Post-processing hooks can be registered with
`sigint_suite.hooks.register_post_processor` to enrich scan results (e.g.,
adding operator names for IMSI captures) without modifying the core library.

## Running `start_imsi_mode.sh`

The `scripts/start_imsi_mode.sh` script performs a single Wi-Fi and Bluetooth
scan and stores the results under `exports/`.

```bash
EXPORT_DIR=/tmp/exports ./sigint_suite/scripts/start_imsi_mode.sh
```

By default the JSON files `wifi.json` and `bluetooth.json` are written to
`sigint_suite/exports/`. Set the `EXPORT_DIR` environment variable to override
this location.

Use `IWLIST_CMD` to specify an alternate `iwlist` path and `IW_PRIV_CMD` to
change the privilege helper for Wi-Fi scans. Set `SIGINT_DEBUG=1` to enable
debug logging for all scanners.

## `scan-all` command

The ``scan-all`` entry point runs all available scans—Wi-Fi, Bluetooth,
cellular bands and IMSI numbers—in one go. Results are written as JSON files in
``sigint_suite/exports/`` by default. Override this location with the
``--export-dir`` option or by setting the ``EXPORT_DIR`` environment variable.

## Continuous Scans

The `continuous-scan` entry point repeats Wi-Fi and Bluetooth scans at a
configurable interval. Set `--interval` to change the delay between scans and
optionally limit the number of iterations with `--iterations`.

```bash
EXPORT_DIR=/tmp/exports python sigint_suite/scripts/continuous_scan.py --interval 30 --iterations 5

continuous-scan --interval 30 --iterations 5

```

## Dependencies

The suite expects `iwlist` (from the `wireless-tools` package) and either
`bluetoothctl` (from `bluez`) or the Python `bleak` package to be available on
the system. Running
`./sigint_suite/scripts/setup_all.sh` will install these packages and the
required Python dependencies. Vendor lookups use the IEEE OUI registry which is
automatically downloaded to `~/.config/piwardrive/oui.csv` when first needed and
refreshed weekly. The setup script can also fetch the file manually. Results are
cached in memory using a least recently used (LRU) cache that holds up to 1024
entries; the oldest prefix is evicted once the limit is reached.

## Plugins

PiWardrive exposes a small plugin system so custom scan logic can be added
without modifying the library itself. Modules placed under
`~/.config/piwardrive/sigint_plugins` are imported automatically at runtime.  A
plugin simply needs to provide a ``scan()`` function and may optionally export
additional helpers.  Once loaded, the module becomes available as an attribute
of :mod:`sigint_suite`.

The process for creating a plugin is outlined below.

1. **Create the plugin directory** if it does not already exist::

       mkdir -p ~/.config/piwardrive/sigint_plugins

2. **Implement the plugin.** Save the following example as
   ``~/.config/piwardrive/sigint_plugins/custom_wifi.py``::

       from typing import List, Dict

       def scan() -> List[Dict[str, str]]:
           """Return one or more Wi-Fi network records."""
           return [{"ssid": "Example"}]

3. **Refresh the plugin cache** so PiWardrive can pick up the new file::

       python -c "import sigint_suite.plugins as p; p.clear_plugin_cache()"

4. **Use the plugin** directly or through convenience commands::

       import sigint_suite
       networks = sigint_suite.custom_wifi.scan()

Plugins are reloaded automatically when the directory timestamp changes, but
calling ``clear_plugin_cache()`` ensures immediate discovery during
development.

## Workflow

The relationship between the command-line tools, optional plugins and the
exports is illustrated below. Scans start with one of the CLI entry points
(``wifi-scan``, ``bluetooth-scan`` and friends). Each tool invokes the
corresponding scanner module, optionally passing the collected records through
any registered plugins or hooks. Results are then written to JSON/CSV/YAML
files or stored in a SQLite database. Databases can be uploaded with
``remote_sync.sync_database_to_server`` so that the
:mod:`aggregation_service <piwardrive.aggregation_service>` can merge them with
other units.

```mermaid
flowchart TD
    subgraph CLI Tools
        A[wifi-scan]
        B[bluetooth-scan]
        C[imsi-scan]
        D[band-scan]
        E[scan-all]
    end
    CLI Tools --> F[Scanner modules]
    F --> G{Plugins / hooks?}
    G -->|yes| H[Custom logic]
    G -->|no| I[Records]
    H --> I
    I --> J{Export}
    J --> K[JSON/CSV/YAML]
    J --> L[SQLite DB]
    L --> M[remote_sync.sync_database_to_server]
    M --> N[Aggregation service]
```

