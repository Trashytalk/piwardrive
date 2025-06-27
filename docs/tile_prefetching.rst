Tile Prefetching Flow
=====================
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

The diagram below illustrates how PiWardrive predicts upcoming map tiles based on recent GPS data and keeps the cache within limits.

.. mermaid::

   sequenceDiagram
       participant MapScreen
       participant RoutePrefetcher
       participant Tiles
       participant TileMaintainer

       MapScreen->>MapScreen: store GPS in track_points
       MapScreen->>RoutePrefetcher: _predict_points()
       RoutePrefetcher-->>MapScreen: heading + destination
       MapScreen->>Tiles: prefetch_tiles()
       Tiles-->>MapScreen: tile images
       MapScreen->>TileMaintainer: enforce_cache_limit()

