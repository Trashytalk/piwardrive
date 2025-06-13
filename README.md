# PiWardrive

PiWardrive is a headless Raspberry Pi 5 application that combines war-driving tools (Kismet & BetterCAP) with an interactive Kivy/KivyMD touchscreen interface. It provides real-time mapping of Wi‑Fi access points, GPS tracking, system/network diagnostics, and service controls—all without an X server.

## Features

* **Interactive Map**: Online/offline map tiles, AP overlays, long-press context menus.
* **Real‑time Metrics**: CPU, memory, disk I/O, GPS fix quality, RSSI, handshake counts.
* **Split View**: Simultaneous map + compact metrics panel.
* **Console & Dashboard**: Tail logs and a drag‑and‑drop widget dashboard with persistent layouts.
* **Service Management**: Start/stop and configure Kismet & BetterCAP from the GUI.
* **Offline Support**: Toggle MBTiles stored under `/mnt/ssd/tiles/`.
* **Diagnostic Tools**: Generate system reports and run connectivity tests.
* **Automatic Log Rotation**: Periodically rotate logs like `/var/log/syslog`.

## Hardware Prerequisites

* **Raspberry Pi 5** (16 GB RAM)
* **7" HDMI + USB touch screen**, `/dev/input/event2`
* **SSD** mounted at `/mnt/ssd` (fstab `nofail`)
* **GPS dongle** on `/dev/ttyACM0` (managed by `gpsd`)
* **Wi‑Fi adapter** compatible with monitor mode

## Prerequisites

* **OS**: Raspberry Pi OS Bookworm (or Bullseye backports)
* **Python**: 3.11.2 (virtualenv under `gui-env/`)
* **Kivy**: 2.3.1
* **KivyMD**: 1.1.1
* **Additional Python libs**: see `requirements.txt`
* **System Packages**: `kismet`, `gpsd`, `bettercap`, `evtest`, `git`, `build-essential`, `cmake`

## Installation

1. **Clone the repo**:

   ```bash
   git clone https://github.com/TRASHYTALK/piwardrive.git
   cd piwardrive
@@ -45,50 +46,51 @@ PiWardrive is a headless Raspberry Pi 5 application that combines war-driving to
   source gui-env/bin/activate
   pip install --upgrade pip setuptools
   ```

3. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

@@ PiWardrive is a headless Raspberry Pi 5 application that combines war-driving t
   /dev/sda1  /mnt/ssd  ext4  defaults,nofail  0  2
   ```

## Configuration

* **KV File**: `kv/main.kv` defines all screen layouts. Ensure it matches `main.py` IDs.
* **Config File**: `~/.config/piwardrive/config.json` (to implement persistence).
* **BetterCAP Caplet**: `/usr/local/etc/bettercap/alfa.cap`
* **Kismet Config**: `/usr/local/etc/kismet_site.conf`
* **Systemd Units**:

  * `kismet.service`
  * `bettercap.service`
  * (Optional) `piwardrive.service` to autostart the app.
* **Log Rotation**: Tune `log_rotate_interval` and `log_rotate_archives`.

## Running the App

```bash
cd ~/piwardrive
activate gui-env/bin/activate
python main.py
```

* **No X Server**: The app renders directly to DRM/framebuffer.
* **Touch Events**: Mapped via SDL2; verify with `evtest /dev/input/event2`.
## Screen Overview

* **Map**: interactive map with GPS and access point overlays.
* **Stats**: detailed system and network metrics.
* **Split**: two-pane view with the map and a metrics column.
* **Console**: tail of Kismet and BetterCAP logs.
* **Settings**: toggle services and theme (placeholder for persistence).
* **Dashboard**: empty workspace for custom widgets.


## Usage

* **Tabs**: Swipe or tap top buttons to switch between Map, Stats, Split, Console, Settings, Dashboard.
* **Map Gestures**: Single-finger long‑press for context; drag to pan; pinch to zoom.

## Troubleshooting

* **Repeated Screens**: Ensure `ScreenManager` in KV has no static children; screens are added dynamically in `main.py:on_start()`.
* **Missing IDs**: Match `kv/main.kv` IDs (`mapview`, `cpu_label`, etc.) with code references.
* **SSH/SFTP Access**: Enable SSH via `raspi-config` and use `sftp pi@<IP>` for file transfers.

## Contributing

1. Fork the repo and create a feature branch:

   ```bash
git checkout -b feature/your-feature
   ```

````
2. Commit your changes and push:

   ```bash
   git add .
   git commit -m "Describe your changes"
   git push origin feature/your-feature
   ```

3. Open a pull request and describe your updates.
