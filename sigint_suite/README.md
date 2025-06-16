# SIGINT Suite

The `sigint_suite` directory provides lightweight command-line tools for
collecting wireless and RF metadata. These helpers can be used separately from
the main PiWardrive UI when you only need quick scans or exports.

## Modules

- **bluetooth** – scan nearby Bluetooth devices via `bluetoothctl` or the
  Python `bleak` library.
- **wifi** – discover Wi-Fi access points using `iwlist`. Results are enriched
  with vendor names when the IEEE OUI registry is available. Set the
  `IWLIST_CMD` environment variable to override the `iwlist` executable and
  `IW_PRIV_CMD` to change the privilege wrapper (default ``sudo``).
- **cellular.band_scanner** – scan available cellular bands via an external
  command specified by ``BAND_SCAN_CMD``.
- **cellular.imsi_catcher** – stub for future IMSI catcher logic.
- **cellular.parsers** – parsers for raw cellular output.
- **cellular.tower_tracker** – maintain a SQLite database of observed cell
  towers and expose simple query helpers.
- **dashboard** – minimal dashboard integration.
- **enrichment** – routines to enrich captured data.
- **exports** – helpers for writing results to JSON/CSV files.
- **gps** – GPS helpers for tagging results with location.
- **rf** – helpers powered by `pyrtlsdr` for spectrum scans and FM demodulation.
- **scripts** – shell scripts for running scans and installing dependencies.

## Running `start_imsi_mode.sh`

The `scripts/start_imsi_mode.sh` script performs a single Wi-Fi and Bluetooth
scan and stores the results under `exports/`.

```bash
./sigint_suite/scripts/start_imsi_mode.sh
```

By default the JSON files `wifi.json` and `bluetooth.json` are written to
`sigint_suite/exports/`. Set the `EXPORT_DIR` environment variable to override
this location.

Use `IWLIST_CMD` to specify an alternate `iwlist` path and `IW_PRIV_CMD` to
change the privilege helper for Wi-Fi scans.

## Continuous Scans

`scripts/continuous_scan.py` repeats Wi-Fi and Bluetooth scans at a configurable
interval. Set `--interval` to change the delay between scans and optionally
limit the number of iterations with `--iterations`.

```bash
python sigint_suite/scripts/continuous_scan.py --interval 30 --iterations 5
```

## Dependencies

The suite expects `iwlist` (from the `wireless-tools` package) and either
`bluetoothctl` (from `bluez`) or the Python `bleak` package to be available on
the system. Running
`./sigint_suite/scripts/setup_all.sh` will install these packages and the
required Python dependencies. Vendor lookups use the IEEE OUI registry which is
automatically downloaded to `~/.config/piwardrive/oui.csv` when first needed and
refreshed weekly. The setup script can also fetch the file manually.

