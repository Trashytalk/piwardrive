GPS Polling
-----------

The application polls ``gpsd`` on a timer to center the map and track
movement. Frequent polling yields more responsive updates but can drain
battery faster on portable setups. Conversely, long intervals conserve
power at the cost of stale position data. The client connects to
``127.0.0.1:2947`` by default. Set ``PW_GPSD_HOST`` and
``PW_GPSD_PORT`` to use a remote ``gpsd`` instance.

PiWardrive adapts its polling rate automatically. When movement is
detected the map polls at ``map_poll_gps`` seconds. If the location
remains nearly constant the interval is increased up to
``map_poll_gps_max``. These values can be tweaked in
``config.json`` or via ``PW_MAP_POLL_GPS`` and
``PW_MAP_POLL_GPS_MAX`` environment variables.

Advanced users can tune the motion detection threshold in ``config.json``.
Coordinates are compared with the previous fix to decide if polling should slow
down. Adjust ``gps_movement_threshold`` when operating in areas with erratic GPS
coverage to avoid unnecessary battery drain.
