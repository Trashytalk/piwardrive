Installation
============

This guide covers installing PiWardrive on Raspberry Pi OS and general Linux distributions.

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

6. (Optional) configure the SSD mount by editing ``/etc/fstab``::

      /dev/sda1  /mnt/ssd  ext4  defaults,nofail  0  2

Generic Linux
-------------

The application can run on most Debian/Ubuntu based systems. Follow the same steps as above and ensure Kivy dependencies are available. Refer to the `Kivy documentation <https://kivy.org/doc/stable/gettingstarted/installation.html>`_ if you encounter build errors.

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
