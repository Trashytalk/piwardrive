Installation
============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


This guide covers installing PiWardrive on Raspberry Pi OS and general Linux distributions.
You can also run ``src/piwardrive/scripts/quickstart.sh`` from the repository root to
automatically install the required packages, create ``gui-env/`` and install
the Python dependencies.

Raspberry Pi OS
---------------

1. Install required system packages::

      sudo apt update && sudo apt install -y \
          git build-essential cmake kismet bettercap gpsd evtest python3-venv

2. Clone the repository::

      git clone https://github.com/TRASHYTALK/piwardrive.git
      cd piwardrive

3. Create and activate a virtual environment::

      python3 -m venv gui-env
      source gui-env/bin/activate

4. Install Python dependencies::

      pip install -r requirements.txt

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

9. (Optional) build the browser interface and start the combined API/frontend::

      cd webui
      npm install
      npm run build
      python 'In development/browser_server.py'


Generic Linux
-------------

The application can run on most Debian/Ubuntu based systems. Follow the same steps as above and ensure Kivy dependencies are available. Refer to the `Kivy documentation <https://kivy.org/doc/stable/gettingstarted/installation.html>`_ if you encounter build errors.

Before cloning the repository on a fresh Raspberry Pi, expand the filesystem and
enable SSH for remote access. A quality power supply is required when using
external Wi‑Fi adapters and an SSD. Insufficient power may lead to USB errors or
file system corruption.

Troubleshooting
---------------

* ``ModuleNotFoundError: No module named 'kivy'``
  - Verify that the virtual environment is activated and ``pip install -r requirements.txt`` completed successfully.
* ``kismet.service failed``
  - Check the service logs with ``sudo journalctl -u kismet`` to diagnose missing hardware or configuration errors.
* ``gpsd reports "can't bind to port"``
  - Ensure no other process is using the GPS device and that the ``gpsd`` service is running.
* Touch screen input not recognized
  - Confirm the correct ``/dev/input/eventX`` device is specified and install ``evtest`` to verify events.
