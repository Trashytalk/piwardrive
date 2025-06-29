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

Cleaning and Segmenting Tracks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Before replaying data captured from other devices it is useful to remove
duplicate points and break long gaps into separate segments.  `gpsbabel`
can clean a GPX file and produce a new track that is easier to replay::

   gpsbabel -i gpx -f raw_track.gpx -x clean -x track,pack,segment \
            -o gpx -F clean_track.gpx

The resulting ``clean_track.gpx`` can then be converted to the JSON format
required by ``uav-track-playback``:

.. code-block:: bash

   gpsbabel -i gpx -f clean_track.gpx -o geojson -F - | \
       jq '.features[0].geometry.coordinates' > uav_track.json

Run ``uav-track-playback uav_track.json`` to replay the cleaned segments.
