Deployment
----------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


This document outlines options for packaging PiWardrive so it can run on a dedicated device or inside a container.

SD Card Image
~~~~~~~~~~~~~

1. Download the latest Raspberry Pi OS (Lite) and write it to an SD card using ``raspberrypi-imager`` or ``dd``.
2. Boot the Pi and install system packages::

       sudo apt update && sudo apt install -y \
           git build-essential cmake kismet bettercap gpsd evtest python3-venv

3. Clone the repository and install Python dependencies inside a virtual environment::

       git clone https://github.com/TRASHYTALK/piwardrive.git
       cd piwardrive
       python3 -m venv gui-env
       source gui-env/bin/activate
       pip install -r requirements.txt

4. Enable ``kismet``, ``bettercap`` and ``gpsd`` so they start on boot (``systemctl enable <svc>``).
5. Grant your user permission to manage systemd units over DBus by creating a ``polkit`` rule allowing ``org.freedesktop.systemd1.manage-units``.
6. (Optional) copy ``examples/piwardrive.service`` into ``/etc/systemd/system/``
   and enable it with ``sudo systemctl enable --now piwardrive.service`` to
   autostart ``piwardrive-service``.
7. (Optional) compile the React web UI and serve it with ``piwardrive.webui_server``::

       cd webui
       npm install
       npm run build
       python -m piwardrive.webui_server
Copy `examples/piwardrive-webui.service` into `/etc/systemd/system/` and enable it with `sudo systemctl enable --now piwardrive-webui.service` to run the dashboard on boot.
8. Power down, remove the card and duplicate it with ``dd`` or other imaging tools to deploy multiple devices.

Docker Container
~~~~~~~~~~~~~~~~

1. Start from ``python:3.10-bullseye`` and install the same system packages with ``apt``.
2. Copy the project into ``/app`` and run ``pip install -r requirements.txt``.
3. Set ``WORKDIR /app`` and define ``CMD ["piwardrive-service"]``.
4. Map the host's USB devices (Wi‑Fi adapter, GPS dongle) into the container when running ``docker run``.
5. Persist ``~/.config/piwardrive`` with a volume so logs and configuration survive container restarts.
6. After building the image with ``docker build``, tag it and push to your registry::

       docker tag <IMAGE_ID> myuser/piwardrive:latest
       docker push myuser/piwardrive:latest

Both approaches produce a self-contained environment ready to capture Wi‑Fi and GPS data with minimal setup on new hardware.

Web UI Container
~~~~~~~~~~~~~~~~

``Dockerfile.webui`` builds the React dashboard and launches ``server/index.js``. Build it with::

    docker build -f Dockerfile.webui -t piwardrive-webui .

Run the container exposing port 8000::

    docker run --rm -p 8000:8000 piwardrive-webui

Set ``PW_API_PASSWORD_HASH`` and ``PORT`` as needed when running ``docker run``.


tmux or screen
~~~~~~~~~~~~~~

Running the service from a terminal multiplexer allows it to stay active after
disconnecting from SSH. Launch a detached session and start PiWardrive with::

    tmux new -s piwardrive -d 'piwardrive-service'

The same can be accomplished using ``screen``::

    screen -dmS piwardrive piwardrive-service

Reconnect later with ``tmux attach -t piwardrive`` or ``screen -r piwardrive``.


Editing service.py
~~~~~~~~~~~~~~~~~~
The API endpoints for PiWardrive live in ``src/piwardrive/service.py``.  Routes
are registered with helper decorators like ``GET`` and ``POST`` which wrap
the underlying FastAPI application.  Add your own async function and decorate
it to expose a new endpoint.

Example
-------
Adding a ``/hello`` route that returns a greeting::

    @GET("/hello")
    async def hello() -> dict[str, str]:
        return {"message": "Hello world"}

Restart ``piwardrive-service`` after saving the file so the new route is
available.
