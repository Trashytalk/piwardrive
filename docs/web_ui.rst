Web Interface
=============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


PiWardrive's main user experience is delivered through a React application under
``webui/``. It consumes the HTTP API provided by :mod:`service` to display
recent status information and logs.  When
available the frontend connects to ``/ws/status`` to receive live updates
without polling.

Plugin widgets stored under ``~/.config/piwardrive/plugins`` are also
detected.  The new ``/plugins`` route lists the discovered classes so the web UI
can show them.

The UI can also poll ``/orientation`` and ``/gps`` for sensor data when running
on hardware equipped with accelerometers or a GPS module.

The layout now adapts responsively across screen sizes. On small Pi touch
screens the sections stack vertically, while wider monitors display two or three
columns.


The ``/config`` endpoint now allows the web UI to modify settings on the
device.  Each option is rendered as a simple form field and saved back to
``config.json`` via a POST request.  Changes take effect on the next reload.

Build the frontend with **Node.js 18+** and npm::

   cd webui
   npm install
   npm run build

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
