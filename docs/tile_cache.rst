Tile Cache
==========

PiWardrive can operate without an internet connection by storing map tiles on disk.  The
:class:`screens.map_screen.MapScreen` exposes helpers for prefetching tiles and keeping
the cache from growing indefinitely.

Prefetching Tiles
-----------------

Use :meth:`~screens.map_screen.MapScreen.prefetch_tiles` to download PNG images
covering a bounding box.  Tiles are saved under ``/mnt/ssd/tiles`` by default and
``prefetch_visible_region`` grabs the area currently shown on screen.  These
functions fetch data from OpenStreetMap so they should be run while online.

Command Line
------------

Tiles can also be prefetched without launching the GUI using the
``piwardrive-prefetch`` entry point::

   piwardrive-prefetch 37.7 -122.5 37.8 -122.4 --zoom 15

The four positional arguments represent ``min_lat min_lon max_lat max_lon``.
Specify ``--folder`` to override the cache directory.

Cache Maintenance
-----------------

:meth:`~screens.map_screen.MapScreen.purge_old_tiles` deletes cached files older
than ``max_age_days`` (30 days by default).  To avoid filling the SSD,
:meth:`~screens.map_screen.MapScreen.enforce_cache_limit` removes the oldest
tiles when the folder exceeds ``limit_mb`` megabytes.  A 512&nbsp;MB limit works
well for most deployments.

Paths
-----

The ``offline_tile_path`` setting determines the MBTiles file used when
``map_use_offline`` is enabled.  It and the cache directory default to
``/mnt/ssd/tiles``.
