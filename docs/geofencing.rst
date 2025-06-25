Geofencing
----------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


The map supports registering polygonal geofences that trigger callbacks when
the user's location crosses the boundary.

Geofences are registered by name along with a polygon and optional callbacks.
When GPS updates occur the current position is checked against each polygon and
the appropriate callback fired. ``on_enter`` and ``on_exit`` may also be message
strings containing ``{name}`` which is replaced with the geofence name.

See the tests ``test_geofence_clustering.py`` and ``test_geofence_handling.py``
for example usage.

Geofence Editor
~~~~~~~~~~~~~~~

Polygons can be drawn directly from the web dashboard. They are stored in
``~/.config/piwardrive/geofences.json`` and loaded on startup.

Web UI
------

The browser dashboard includes a matching geofence editor. Click on the map to
draw polygons and press "Finish" to save them. Existing geofences can be
renamed or removed and optional entry/exit messages configured. All operations
are performed through the ``/geofences`` REST API and saved to the same
``geofences.json`` file used by the on-device editor.
