Web Interface
=============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


PiWardrive's main user experience is delivered through a React application under
``webui/``. It consumes the HTTP API provided by :mod:`service` to display
recent status information and logs.  When
available the frontend connects to ``/ws/status`` to receive live updates
without polling. If WebSockets are unavailable it falls back to the
``/sse/status`` endpoint using Server-Sent Events.

Plugin widgets stored under ``~/.config/piwardrive/plugins`` are also
detected.  The new ``/plugins`` route lists the discovered classes so the web UI
can show them.

Dashboard widgets appear in a drag-and-drop layout identical to the on-device
interface. Positions are stored in ``config.json`` via the
``/dashboard-settings`` API so rearranging widgets from the browser persists the
order for both frontends.

The UI can also poll ``/orientation`` and ``/gps`` for sensor data when running
on hardware equipped with accelerometers or a GPS module.

The layout now adapts responsively across screen sizes. On small Pi touch
screens the sections stack vertically, while wider monitors display two or three
columns.


The ``/config`` endpoint now allows the web UI to modify settings on the
device.  The React dashboard exposes a dedicated **Settings** page mirroring the
former Kivy interface. Configuration options are fetched from ``/config`` and
saved back via a POST request so changes persist to ``config.json``.

Heatmap overlays derived from the aggregation service can be toggled on the map
screen. The layer uses ``leaflet.heat`` and displays points returned by the
``/overlay`` API. A simple **Vector Tile Customizer** form lets you apply
MapLibre style metadata to an MBTiles database via the
``/api/vector-tiles/style`` endpoint.

Build the frontend with **Node.js 18+** and npm::

   cd webui
   npm install
   npm run build

Use `examples/piwardrive-webui.service` to run `piwardrive-webui` automatically on boot after building.

During development you can run ``npm run dev`` which starts a Vite server
and proxies API requests to ``http://localhost:8000``.

Offline Caching
---------------

The frontend is configured as a progressive web app. When built it registers
a service worker that caches the compiled assets and ``index.html`` for offline
use. After visiting the site once, the UI will continue to load even without
network connectivity. New versions are picked up automatically on reload.

Authentication
--------------

The API routes support optional HTTP basic authentication. Set the environment
variable ``PW_API_PASSWORD_HASH`` to a password hash created with::

   python -c "import security,sys;print(security.hash_password(sys.argv[1]))" mypass

to require a password. When the variable is not set, the endpoints are public.

Launching in Kiosk Mode
-----------------------

After building the frontend you can start the API server and open Chromium in
kiosk mode with ``piwardrive-kiosk``::

   piwardrive-kiosk

The command launches ``piwardrive-webui`` in the background and then executes
``chromium-browser --kiosk http://localhost:8000`` (falling back to
``chromium`` when ``chromium-browser`` is unavailable).
An active X server is required; headless systems may use ``Xvfb``.
