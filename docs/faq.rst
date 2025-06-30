Frequently Asked Questions
==========================
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Build Problems
--------------
**Q: ``python -m build`` fails with ``fatal error: Python.h: No such file or directory``**

Install the system headers and compiler::

   sudo apt install -y build-essential python3-dev

Then rerun ``pip install -r requirements.txt``.

Missing Sensors
---------------
**Q: Orientation always shows ``None``**

Install ``iio-sensor-proxy`` and ``python3-dbus`` for built-in sensors or attach an
MPU‑6050 and ``pip install mpu6050``. The application runs without orientation
data but cannot rotate Wi‑Fi samples.

Node Build Errors
-----------------
**Q: The web UI build complains about the Node version**

Ensure Node.js 18 or newer is installed. Check with ``node --version`` and
upgrade via your package manager or the official installer.

GPS Issues
----------
**Q: ``gpsd reports \"can't bind to port\"``**

Another process may be using the GPS device. Stop the conflicting service and
ensure ``gpsd`` itself is running.

Compilation Errors
------------------
**Q: ``npm ERR! gyp`` or ``g++: command not found``**

Install the system compiler and Python headers::

   sudo apt install -y build-essential python3 python3-dev

**Q: ``command 'gcc' failed with exit status 1``**

Install ``build-essential`` or your distribution's compiler toolchain package.
