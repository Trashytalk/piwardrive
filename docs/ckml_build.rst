Building the CKML Extension
===========================

PiWardrive ships with a small C extension ``ckml`` used by the GUI. It must be
compiled when building the project.

Prerequisites
-------------

* C compiler (``build-essential`` on Debian/Ubuntu)
* Python development headers matching your interpreter (``python3-dev``)

Build the project from the repository root using ``python -m build``::

    pip install build
    python -m build

The wheel is written to ``dist/``. An example output path is::

    dist/piwardrive-0.1.0-cp312-cp312-linux_aarch64.whl

Install the wheel with::

    pip install dist/*.whl

Troubleshooting
---------------

* ``fatal error: Python.h: No such file or directory``
  - Install ``python3-dev`` (or your distribution's equivalent).
* ``gcc: command not found``
  - Ensure ``build-essential`` or another compiler package is installed.
