Installation
============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


This guide covers installing PiWardrive on Raspberry Pi OS and general Linux
distributions. The recommended interface is the browser-based dashboard built
with React. It requires Node.js 18 or newer to compile.

You can also run ``scripts/quickstart.sh`` from the repository
root to automatically install the required packages, create ``gui-env/`` and
install the Python dependencies.

Raspberry Pi OS
---------------

1. Install required system packages::

     sudo apt update && sudo apt install -y \
         git build-essential cmake kismet bettercap gpsd evtest python3-venv \
         libsqlcipher-dev

2. Clone the repository::

      git clone https://github.com/TRASHYTALK/piwardrive.git
      cd piwardrive

3. Create and activate a virtual environment::

      python3 -m venv gui-env
      source gui-env/bin/activate

4. Install Python dependencies::

      pip install -r requirements.txt
      pip install pysqlcipher3

   Set ``PW_DB_KEY`` before running ``piwardrive-migrate`` to create an
   encrypted database::

      PW_DB_KEY=mysecret piwardrive-migrate

5. (Optional) install developer tools::

      pip install -r requirements-dev.txt

   ``requirements-dev.txt`` contains linters and test frameworks such as
   ``flake8``, ``mypy`` and ``pytest``.

6. (Optional) configure the SSD mount by editing ``/etc/fstab``::

      /dev/sda1  /mnt/ssd  ext4  defaults,nofail  0  2
7. (Optional) install R integration packages::

      pip install rpy2
      sudo apt install r-base
      Rscript -e "install.packages(c('ggplot2','jsonlite'), repos='https://cloud.r-project.org')"

8. (Optional) install extra Python packages used by some features::

      pip install pandas orjson pyprof2calltree

   The ``fastjson`` helper tries ``orjson`` first, then ``ujson`` and finally
   falls back to the builtin ``json`` module when the accelerators are absent.

9. Build the web interface (requires **Node.js 18+**) and start the combined
   API/frontend::

      cd webui
      npm install
      npm run build
      python -m piwardrive.webui_server

Copy `examples/piwardrive-webui.service` into `/etc/systemd/system/` and enable it with `sudo systemctl enable --now piwardrive-webui.service` to start the dashboard automatically on boot.


Generic Linux
-------------

The application can run on most Debian/Ubuntu based systems. Follow the same steps as above and install the Python dependencies listed in ``requirements.txt``.

Before cloning the repository on a fresh Raspberry Pi, expand the filesystem and
enable SSH for remote access. A quality power supply is required when using
external Wi‑Fi adapters and an SSD. Insufficient power may lead to USB errors or
file system corruption.

.. _wireless-tools:

Kismet and BetterCAP
--------------------

Sample ``kismet.conf``::

   suiduser=pi
   log_prefix=/mnt/ssd/kismet_logs
   source=wlan0:name=wlan0

Run BetterCAP with a simple caplet::

   sudo bettercap -iface wlan0 --caplet /usr/local/etc/bettercap/alfa.cap

Troubleshooting
---------------

* ``kismet.service failed``
  - Check the service logs with ``sudo journalctl -u kismet`` to diagnose missing hardware or configuration errors.
* ``gpsd reports "can't bind to port"``
  - Ensure no other process is using the GPS device and that the ``gpsd`` service is running.
* Touch screen input not recognized
  - Confirm the correct ``/dev/input/eventX`` device is specified and install ``evtest`` to verify events.

Compilation Issues
------------------

* ``npm ERR! gyp`` or ``g++: command not found``
  - ``node-gyp`` uses Python and a C++ compiler to build native modules. Install ``build-essential`` and ``python3`` (plus ``python3-dev`` on Debian/Ubuntu).
* ``npm ERR! not compatible with your version of Node``
  - Ensure Node.js 18 or newer is installed. ``node --version`` should report at least ``v18``.
* ``fatal error: Python.h: No such file or directory`` when installing Python packages
  - Install the interpreter headers with ``python3-dev`` (or your distribution's equivalent) and retry ``pip install``.
* ``command 'gcc' failed with exit status 1``
  - A compiler is missing. Install ``build-essential`` or the appropriate development tools for your system.
