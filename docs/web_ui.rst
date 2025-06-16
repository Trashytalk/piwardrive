React Web UI
============

A small React application lives under ``webui/``. It consumes the HTTP API
provided by :mod:`service` to display recent status information and logs.  When
available the frontend connects to ``/ws/status`` to receive live updates
without polling.

Build the frontend with npm::

   cd webui
   npm install
   npm run build

During development you can run ``npm run dev`` which starts a Vite server
and proxies API requests to ``http://localhost:8000``.

Authentication
--------------

The API routes support optional HTTP basic authentication. Set the environment
variable ``PW_API_PASSWORD_HASH`` to a password hash created with::

   python -c "import security,sys;print(security.hash_password(sys.argv[1]))" mypass

to require a password. When the variable is not set, the endpoints are public.
