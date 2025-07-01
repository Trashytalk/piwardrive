"""Advanced network analytics utilities."""

from __future__ import annotations

from typing import Any, Iterable, List, Mapping, Dict, Tuple

import math
from collections import defaultdict

import numpy as np
from sklearn.cluster import DBSCAN

from piwardrive.sigint_suite.enrichment import cached_lookup_vendor


def find_suspicious_aps(
    records: Iterable[Mapping[str, Any]],
) -> List[Mapping[str, Any]]:
    """Return Wi-Fi access points that may be suspicious.

    Heuristics flag open or WEP networks, duplicate BSSIDs broadcasting
    multiple SSIDs, out-of-range channels and unknown vendor prefixes.
    """
    aps: List[Mapping[str, Any]] = []
    seen_bssid: dict[str, set[str]] = {}
    for rec in records:
        bssid = rec.get("bssid")
        ssid = rec.get("ssid") or ""
        enc = (rec.get("encryption") or "").lower()
        channel = rec.get("channel")

        suspicious = False
        if "open" in enc or "wep" in enc:
            suspicious = True
        if bssid:
            seen_bssid.setdefault(bssid, set()).add(ssid)
            if len(seen_bssid[bssid]) > 1:
                suspicious = True
        if channel not in (None, ""):
            try:
                ch = int(str(channel).split()[0])
                if ch < 1 or ch > 196:
                    suspicious = True
            except ValueError:
                suspicious = True
        if bssid and cached_lookup_vendor(bssid) is None:
            suspicious = True

        if suspicious:
            aps.append(rec)
    return aps


def cluster_by_signal(
    records: Iterable[Mapping[str, Any]],
    eps: float,
    min_samples: int,
) -> Dict[str, Tuple[float, float]]:
    """Return signal-weighted location centroids for each BSSID.

    Records must contain ``bssid``, ``lat``, ``lon`` and ``signal_dbm`` (or
    ``rssi``) fields. Positions are clustered with DBSCAN and the centroid of
    the largest cluster for each BSSID is returned. RSSI values are used as
    inverse weights when averaging cluster coordinates.
    """

    grouped: Dict[str, list[tuple[float, float, float]]] = defaultdict(list)
    for rec in records:
        bssid = rec.get("bssid")
        try:
            lat = float(rec.get("lat"))
            lon = float(rec.get("lon"))
            rssi = float(rec.get("signal_dbm", rec.get("rssi")))
        except Exception:
            continue
        if bssid is None:
            continue
        grouped[bssid].append((lat, lon, rssi))

    centroids: Dict[str, Tuple[float, float]] = {}
    for bssid, vals in grouped.items():
        coords = np.array([(v[0], v[1]) for v in vals], dtype=float)
        if coords.size == 0:
            continue

        labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(coords)
        best: Tuple[float, float] | None = None
        best_weight = -math.inf
        for label in set(labels):
            if label == -1:
                continue
            mask = labels == label
            pts = coords[mask]
            rssis = np.array([vals[i][2] for i in range(len(vals)) if mask[i]], dtype=float)
            weights = 1.0 / np.maximum(1.0, np.abs(rssis))
            weight_sum = float(weights.sum())
            lat = float(np.average(pts[:, 0], weights=weights))
            lon = float(np.average(pts[:, 1], weights=weights))
            if weight_sum > best_weight:
                best_weight = weight_sum
                best = (lat, lon)
        if best is not None:
            centroids[bssid] = best

    return centroids


def detect_rogue_devices(
    records: Iterable[Mapping[str, Any]],
    *,
    eps: float = 0.0005,
    min_samples: int = 3,
    distance: float = 0.001,
) -> List[Mapping[str, Any]]:
    """Return records that may correspond to rogue APs.

    A device is considered rogue if it matches :func:`find_suspicious_aps`
    heuristics or if its observed location is far from the centroid computed by
    :func:`cluster_by_signal`.
    """

    suspicious = set(id(r) for r in find_suspicious_aps(records))
    rec_list = list(records)
    centroids = cluster_by_signal(rec_list, eps, min_samples)

    rogues: List[Mapping[str, Any]] = []
    for rec in rec_list:
        if id(rec) in suspicious:
            rogues.append(rec)
            continue
        bssid = rec.get("bssid")
        centroid = centroids.get(bssid)
        if not centroid:
            continue
        try:
            lat = float(rec.get("lat"))
            lon = float(rec.get("lon"))
        except Exception:
            continue
        dist = math.hypot(lat - centroid[0], lon - centroid[1])
        if dist > distance:
            rogues.append(rec)

    return rogues


__all__ = [
    "find_suspicious_aps",
    "cluster_by_signal",
    "detect_rogue_devices",
]
