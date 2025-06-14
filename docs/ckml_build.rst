Building the CKML Extension
===========================

PiWardrive ships with a small C extension ``ckml`` used by the GUI.
Compile it from the project root using ``setuptools``::

    python setup.py build_ext --inplace

The ``--inplace`` flag places the compiled module next to ``ckml.c`` so
imports succeed without further configuration.
