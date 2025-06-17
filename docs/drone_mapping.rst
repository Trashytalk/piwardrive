Drone Mapping
-------------
.. note::
   Ensure you comply with all local laws and obtain proper authorization before collecting wireless data from a UAV.

This mode relies on the optional ``dronekit`` package to read GPS telemetry from a flight controller.

Recording
~~~~~~~~~
Use ``uav-record`` to capture Wi-Fi networks alongside GPS coordinates:

.. code-block:: bash

   uav-record --connect 127.0.0.1:14550 --duration 300 --export-dir ./exports

Two files are produced:

``uav_track.json``
    Ordered list of ``[lat, lon]`` points.
``uav_wifi.json``
    Wi-Fi observations with timestamp and position.

Playback
~~~~~~~~
Replay a saved track with ``uav-track-playback``:

.. code-block:: bash

   uav-track-playback uav_track.json --interval 0.5

Each coordinate is printed to stdout and can be piped into other tools.
