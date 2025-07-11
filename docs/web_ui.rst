Web Interface
=============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Web Interface Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   graph TB
       A[React Frontend] --> B[HTTP API]
       A --> C[WebSocket Connection]
       A --> D[Server-Sent Events]
       
       B --> E[Service Module]
       C --> F[Status Updates]
       D --> G[Fallback Connection]
       
       E --> H[Database]
       E --> I[Configuration]
       E --> J[Plugin System]
       
       A --> K[Dashboard Widgets]
       K --> L[Drag & Drop Layout]
       K --> M[Responsive Design]
       
       J --> N[Plugin Detection]
       N --> O[Widget Registration]
       
       style A fill:#e1f5fe
       style B fill:#e8f5e8
       style C fill:#fff3e0
       style D fill:#fce4ec
       style E fill:#f3e5f5

Frontend Data Flow
~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
       participant Browser
       participant React App
       participant HTTP API
       participant WebSocket
       participant Database
       
       Browser->>React App: Load Application
       React App->>HTTP API: Fetch Initial Data
       HTTP API->>Database: Query Data
       Database-->>HTTP API: Return Results
       HTTP API-->>React App: JSON Response
       React App->>WebSocket: Establish Connection
       WebSocket-->>React App: Live Updates
       React App-->>Browser: Render UI
       
       Note over React App,WebSocket: Falls back to SSE if WebSocket unavailable
       React App->>HTTP API: Heartbeat every 15s
       HTTP API-->>React App: Keep-alive Response


PiWardrive's main user experience is delivered through a React application under
``webui/``. It consumes the HTTP API provided by :mod:`service` to display
recent status information and logs.  When
available the frontend connects to ``/ws/status`` to receive live updates
without polling. If WebSockets are unavailable it falls back to the
``/sse/status`` endpoint using Server-Sent Events. The connection
automatically reconnects when dropped and sends a heartbeat ping every
15&nbsp;seconds to keep the stream alive.

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


The ``/config`` endpoint allows the web UI to modify settings on the device.
Configuration options are fetched from ``/config`` and saved back via a POST
request so changes persist to ``config.json``.

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

When GPS data is available the web interface predicts future positions using the
two most recent fixes. It then downloads tiles along the anticipated path based
on the ``route_prefetch_interval`` and ``route_prefetch_lookahead`` settings.

Playback
--------

Historical health records can be reviewed directly in the browser. The
``HealthPlayback`` component connects to ``/sse/history`` and displays each
record at a configurable interval. Add the widget to your dashboard layout to
step through past metrics.

Authentication
--------------

The API routes support optional HTTP basic authentication. Set the environment
variable ``PW_API_PASSWORD_HASH`` to a password hash created with::

   python -c "import security,sys;print(security.hash_password(sys.argv[1]))" mypass

to require a password. When the variable is not set, the endpoints are public.

Some routes performing privileged actions, such as
``/service/{name}`` and ``/service/{name}/{action}``, require a bearer token.
Post valid credentials to ``/token`` and supply the returned token in an
``Authorization: Bearer`` header for subsequent requests.
The console screen now only displays logs and no longer runs arbitrary
commands.

Launching in Kiosk Mode
-----------------------

After building the frontend you can start the API server and open Chromium in
kiosk mode with ``piwardrive-kiosk``::

   piwardrive-kiosk

The command launches ``piwardrive-webui`` in the background and then executes
``chromium-browser --kiosk http://localhost:8000`` (falling back to
``chromium`` when ``chromium-browser`` is unavailable).
Copy ``examples/kiosk.service`` alongside ``piwardrive-webui.service`` to start Chromium automatically on boot and launch the browser dashboard.
An active X server is required; headless systems may use ``Xvfb``.
