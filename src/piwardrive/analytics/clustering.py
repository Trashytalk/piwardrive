"""Clustering helpers using DBSCAN."""

from __future__ import annotations

from typing import Iterable, Mapping, Tuple, List

import numpy as np
from sklearn.cluster import DBSCAN


def cluster_positions(
    records: Iterable[Mapping[str, float]],
    eps: float = 0.0005,
    min_samples: int = 5,
) -> List[Tuple[float, float]]:
    """Return cluster centroids for ``records``.

    Each record should contain ``lat`` and ``lon`` keys. The coordinates
    are clustered using DBSCAN and the mean latitude/longitude for each
    cluster is returned.
    """

    coords = np.array(
        [
            (rec["lat"], rec["lon"])
            for rec in records
            if "lat" in rec and "lon" in rec
        ],
        dtype=float,
    )
    if coords.size == 0:
        return []

    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(coords)
    centers: list[tuple[float, float]] = []
    for label in set(labels):
        if label == -1:
            continue
        pts = coords[labels == label]
        centers.append((float(pts[:, 0].mean()), float(pts[:, 1].mean())))
    return centers


__all__ = ["cluster_positions"]
