Geofencing
----------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


The map supports registering polygonal geofences that trigger callbacks when
the user's location crosses the boundary.

``MapScreen.add_geofence(name, polygon, on_enter=None, on_exit=None)`` simply
appends a dictionary with the polygon and callback functions to
``MapScreen.geofences``. When GPS updates occur, ``_check_geofences`` evaluates
whether the current position is inside each polygon. ``on_enter`` is invoked the
first time the point is found inside; ``on_exit`` fires when leaving the area.
``on_enter`` and ``on_exit`` may also be message strings which are displayed via
``Snackbar`` when the boundary is crossed. Use ``{name}`` in the string to
insert the geofence name.

See the tests ``test_geofence_clustering.py`` and ``test_geofence_handling.py``
for example usage.

Geofence Overlays
~~~~~~~~~~~~~~~~~

Saved polygons are drawn on the map when the application starts.
:class:`~piwardrive.screens.map_screen.MapScreen` loads ``geofences.json`` and
adds a ``LineMapLayer`` for each polygon so the boundaries are visible.
The browser dashboard fetches the same file via the ``/geofences`` API and
renders ``<Polygon>`` overlays. Entry and exit messages configured in the
editor trigger ``alert`` pop-ups whenever the user crosses a geofence.

Geofence Editor
~~~~~~~~~~~~~~~

The :class:`~piwardrive.screens.geofence_editor.GeofenceEditor` screen provides a simple
map interface for drawing polygons directly. Points are added by tapping on the
map and a "Finish" button stores the completed polygon. All polygons are saved
to ``~/.config/piwardrive/geofences.json`` and reloaded whenever the editor is
opened. The editor exposes ``rename_polygon``, ``remove_polygon``,
``update_polygon`` and ``configure_alerts`` helpers for modifying existing
geofences and defining entry/exit alert messages which are loaded by the map
screen on startup.

Web UI
------

The browser dashboard includes a matching geofence editor. Click on the map to
draw polygons and press "Finish" to save them. Existing geofences can be
renamed or removed and optional entry/exit messages configured. All operations
are performed through the ``/geofences`` REST API and saved to the same
``geofences.json`` file used by the on-device editor.
