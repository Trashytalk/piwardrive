Tile Cache
==========
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


PiWardrive can operate without an internet connection by storing map tiles on disk.  The
:class:`piwardrive.screens.map_screen.MapScreen` exposes helpers for prefetching tiles and keeping
the cache from growing indefinitely.

Prefetching Tiles
-----------------

Use :meth:`~piwardrive.screens.map_screen.MapScreen.prefetch_tiles` to download PNG images
covering a bounding box.  Tiles are saved under ``/mnt/ssd/tiles`` by default and
``prefetch_visible_region`` grabs the area currently shown on screen.  These
functions fetch data from OpenStreetMap so they should be run while online.
Enabling ``map_auto_prefetch`` automatically downloads a small region around the
current GPS location whenever it updates.

Command Line
------------

Tiles can also be prefetched without launching the GUI using the
``piwardrive-prefetch`` entry point::

   piwardrive-prefetch 37.7 -122.5 37.8 -122.4 --zoom 15

The four positional arguments represent ``min_lat min_lon max_lat max_lon``.
Specify ``--folder`` to override the cache directory.

``piwardrive-prefetch-batch`` reads bounding boxes from a file and prefetches
them sequentially::

   piwardrive-prefetch-batch boxes.txt --zoom 15

Each line of ``boxes.txt`` should contain ``min_lat min_lon max_lat max_lon``.

Cache Maintenance
-----------------

:meth:`~piwardrive.screens.map_screen.MapScreen.purge_old_tiles` deletes cached files older
than ``max_age_days`` (30 days by default).  To avoid filling the SSD,
:meth:`~piwardrive.screens.map_screen.MapScreen.enforce_cache_limit` removes the oldest
tiles when the folder exceeds ``limit_mb`` megabytes.  A 512&nbsp;MB limit works
well for most deployments.

Automated Maintenance
~~~~~~~~~~~~~~~~~~~~~

``tile_maintenance_interval`` controls how often a periodic cleanup runs.  A
``watchdog`` observer triggers maintenance whenever the cache size or file count
exceeds limits, with the scheduled interval (weekly by default) serving as a
fallback. If ``compress_offline_tiles`` is ``true`` the offline MBTiles file is
compacted with ``VACUUM`` during each run.

Scheduled Prefetch
~~~~~~~~~~~~~~~~~~

``route_prefetch_interval`` determines how often PiWardrive predicts the next
set of tiles from recent GPS fixes. The prefetcher computes heading and speed
from the two most recent points and extrapolates future positions using
great‑circle math. ``route_prefetch_lookahead`` controls how far ahead of the
current location tiles are fetched.


Paths
-----

The ``offline_tile_path`` setting determines the MBTiles file used when
``map_use_offline`` is enabled.  It and the cache directory default to
``/mnt/ssd/tiles``.  You can override the MBTiles location at runtime by
setting the ``PW_OFFLINE_TILE_PATH`` environment variable before launching
PiWardrive.
