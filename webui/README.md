# PiWardrive Web UI Setup

![Coverage](https://github.com/TRASHYTALK/piwardrive/raw/main/webui/badges/coverage.svg)

> **Note**
> Refer to the Legal Notice in [../README.md](../README.md) before running PiWardrive.

This guide explains how to build and launch the React based dashboard that accompanies the PiWardrive API. Every command shown should be executed from the project root unless otherwise noted. The instructions assume a freshly cloned repository on Raspberry Pi OS or another Debian based distribution.

## 1. Install System Requirements

PiWardrive relies on several native tools such as Kismet, BetterCAP and gpsd. Install them first so the API can collect data:

```bash
sudo apt update && sudo apt install -y \
    git build-essential cmake kismet bettercap gpsd evtest python3-venv
```

The web interface uses **Node.js 18+** to compile the frontend. Verify the version with `node --version`. If Node is missing, install it via your package manager or from <https://nodejs.org>.

## 2. Clone the Repository

Download the source code and switch into the project folder:

```bash
git clone https://github.com/TRASHYTALK/piwardrive.git
cd piwardrive
```

## 3. Create the Python Environment

The backend API runs under Python 3.10 or newer. Create a virtual environment so the dependencies remain isolated:

```bash
python3 -m venv gui-env
source gui-env/bin/activate
```

Install the Python packages and PiWardrive itself:

```bash
pip install -r requirements.txt
pip install .
```

## 4. Build the Web UI

The React application lives inside the `webui/` directory. Install its dependencies and generate the optimized build:

```bash
cd webui
npm install
npm run build
```

The compiled assets appear in `webui/dist`. They include a service worker so the interface works offline after the first visit.

## 5. Start the API and Dashboard

Return to the repository root and run the bundled server. It serves the API under `/api` and the static files generated above at the site root:

```bash
cd ..
npm start  # launches the Node server
# python -m piwardrive.webui_server  # alternative Python version
```

Open a browser and navigate to `http://localhost:8000`. You should see the dashboard showing live system metrics. The server listens on all interfaces so other devices on the network may connect using the Pi's IP address.

Set `PW_API_PASSWORD_HASH` if you want to require HTTP basic authentication. Generate the hash with:

```bash
python -c "import security,sys;print(security.hash_password(sys.argv[1]))" mypass
```

Assign the resulting value to the environment variable before launching `piwardrive.webui_server`.

## PW_API_PASSWORD_HASH and PORT

`server/index.js` reads two environment variables:

- `PW_API_PASSWORD_HASH` enables HTTP basic auth. Generate the hash as shown above and export it before starting the server.
- `PORT` sets the listening port (default `8000`).

Example:

```bash
PW_API_PASSWORD_HASH=$MY_HASH PORT=9000 node server/index.js
# or with npm
PW_API_PASSWORD_HASH=$MY_HASH PORT=9000 npm start
```

## PW_HEALTH_FILE

`server/index.js` also checks for `PW_HEALTH_FILE`. Set it to the path of a
JSON file containing health records. The server reads this file whenever the
`/api/status` route is requested and returns its contents.

Example:

```bash
PW_HEALTH_FILE=/var/log/piwardrive/health.json npm start
```


## 6. Development Mode

While working on the frontend you can run the Vite development server instead of rebuilding on every change:

```bash
cd webui
npm run dev
```

The dev server watches the source files and automatically reloads the page. API requests are proxied to `http://localhost:8000`, so keep the Python backend running in another terminal. Visit the port printed by Vite (usually `http://localhost:5173`).

## 7. Kiosk Launch Helper

For a dedicated dashboard device you can automate the startup process with the helper command:

```bash
piwardrive-kiosk
```

The command runs `piwardrive-webui` in the background and then opens Chromium in kiosk mode pointing to the local web UI. If `chromium-browser` is not installed it falls back to `chromium`. An X server must be available; headless environments may use `Xvfb`.

## 8. Serving the Build Elsewhere

`piwardrive.webui_server` reads the `PW_WEBUI_DIST` environment variable to locate the build directory. You can copy `webui/dist` to another location or web server and point the variable there when starting the API:

```bash
export PW_WEBUI_DIST=/var/www/piwardrive
python -m piwardrive.webui_server
```

Any static web server can host the contents of `webui/dist` as long as the API is reachable.

## 9. Plugin Widgets

Custom widgets placed under `~/.config/piwardrive/plugins` are detected at runtime. The `/plugins` API route lists the discovered classes so you can confirm your plugin was loaded. When a matching React component exists under `webui/src/components/`, it will be loaded dynamically without further code changes.

## 10. Offline Usage

After the first successful build, the dashboard registers a service worker. It caches the HTML, JavaScript and CSS files so subsequent visits work even without a network connection. Reloading the page picks up newer builds automatically.

---

Once these steps are complete you have a functioning browser based dashboard. Use the interface to monitor running services, view logs and adjust configuration without needing the on-device GUI.

## 11. Export Utilities

`exportUtils.js` mirrors the Python helpers for exporting collected records. It can filter result sets and save them to various geospatial formats.

```javascript
import { filterRecords, exportRecords, exportMapKml } from './src/exportUtils.js';

const records = [{ ssid: 'AP', bssid: 'AA', lat: 1, lon: 2 }];
const track = [[1, 2], [3, 4]];

const filtered = filterRecords(records, { encryption: 'OPEN' });
await exportRecords(filtered, 'out.csv', 'csv');
await exportMapKml(track, filtered, [], 'track.kml');
```

Supported formats are **CSV**, **JSON**, **GPX**, **KML**, **GeoJSON** and **SHP**.

## 12. Diagnostics Helpers

`diagnostics.js` offers utilities for gathering system metrics and rotating log files similar to the Python module.

```javascript
import { selfTest, rotateLog } from './src/diagnostics.js';

const report = selfTest();
rotateLog('/var/log/piwardrive.log');
```

