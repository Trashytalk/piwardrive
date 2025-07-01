Network Analytics
=================

Utilities in ``piwardrive.network_analytics`` help analyze Wi‑Fi observations.

Clustering by signal strength
-----------------------------

``cluster_by_signal(records, eps, min_samples)`` groups access point
observations by location using DBSCAN and returns signal weighted
centroids per BSSID. Records should contain ``bssid``, ``lat``, ``lon`` and
``signal_dbm`` (or ``rssi``).

Rogue device detection
----------------------

``detect_rogue_devices(records)`` combines the heuristics of
``find_suspicious_aps`` with location clusters. A record is flagged as
rogue when it matches the heuristic checks or when its coordinates are
far from the computed centroid for its BSSID.
