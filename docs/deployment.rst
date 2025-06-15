Deployment
----------

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
6. (Optional) create ``piwardrive.service`` to autostart ``python /home/pi/piwardrive/main.py``.
7. Power down, remove the card and duplicate it with ``dd`` or other imaging tools to deploy multiple devices.

Docker Container
~~~~~~~~~~~~~~~~

1. Start from ``python:3.10-bullseye`` and install the same system packages with ``apt``.
2. Copy the project into ``/app`` and run ``pip install -r requirements.txt``.
3. Set ``WORKDIR /app`` and define ``CMD ["python", "main.py"]``.
4. Map the host's USB devices (Wi‑Fi adapter, GPS dongle) into the container when running ``docker run``.
5. Persist ``~/.config/piwardrive`` with a volume so logs and configuration survive container restarts.

Both approaches produce a self-contained environment ready to capture Wi‑Fi and GPS data with minimal setup on new hardware.
