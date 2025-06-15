Geofencing
----------

The map supports registering polygonal geofences that trigger callbacks when
the user's location crosses the boundary.

``MapScreen.add_geofence(name, polygon, on_enter=None, on_exit=None)`` simply
appends a dictionary with the polygon and callback functions to
``MapScreen.geofences``. When GPS updates occur, ``_check_geofences`` evaluates
whether the current position is inside each polygon. ``on_enter`` is invoked the
first time the point is found inside; ``on_exit`` fires when leaving the area.

See the tests ``test_geofence_clustering.py`` and ``test_geofence_handling.py``
for example usage.
