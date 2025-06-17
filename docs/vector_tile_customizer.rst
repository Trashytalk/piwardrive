Offline Vector Tile Customizer
==============================
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

The :mod:`vector_tile_customizer` module provides helpers to create and style
MBTiles databases for offline mapping.

Building Tiles
--------------

Use ``piwardrive-mbtiles build`` to convert a directory of ``.pbf`` tiles in
XYZ layout into a single MBTiles file::

   piwardrive-mbtiles build tiles/ offline.mbtiles

Styling Tiles
-------------

Metadata such as the dataset name, description and a MapLibre style JSON file
can be embedded with ``piwardrive-mbtiles style``::

   piwardrive-mbtiles style offline.mbtiles --style osm-liberty.json \
       --name "OpenStreetMap" --description "Vector tile extract"

PiWardrive reads the style information when ``map_use_offline`` is enabled,
allowing consistent rendering without network access.

