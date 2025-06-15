Building the CKML Extension
===========================

PiWardrive ships with a small C extension ``ckml`` used by the GUI.
Build the project from the repository root using ``python -m build``::

    pip install build
    python -m build
    pip install dist/*.whl

The resulting wheel contains the compiled module so imports succeed without
additional configuration.
