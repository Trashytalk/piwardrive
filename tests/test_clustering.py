from piwardrive.analytics.clustering import cluster_positions


def test_cluster_positions_basic() -> None:
    records = [
        {"lat": 0.0, "lon": 0.0},
        {"lat": 0.0001, "lon": 0.0},
        {"lat": 1.0, "lon": 1.0},
    ]
    centers = cluster_positions(records, eps=0.001, min_samples=1)
    assert len(centers) == 2


def test_cluster_positions_empty() -> None:
    assert cluster_positions([]) == []
