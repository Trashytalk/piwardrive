from __future__ import annotations

"""Simple demographic analytics using example data."""

import json
from functools import lru_cache
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List


_DATA_PATH = Path(__file__).resolve().parents[2] / "examples" / "demographic_data.json"


@lru_cache()
def load_data() -> List[Dict[str, Any]]:
    """Return demographic records from the example dataset."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def socioeconomic_correlation() -> Dict[str, Any]:
    data = load_data()
    incomes = [d.get("median_income", 0.0) for d in data]
    access = [d.get("tech_access", 0.0) for d in data]
    if not incomes or len(incomes) != len(access):
        return {"correlation": 0.0}
    avg_inc = mean(incomes)
    avg_acc = mean(access)
    cov = sum((i - avg_inc) * (a - avg_acc) for i, a in zip(incomes, access))
    var_i = sum((i - avg_inc) ** 2 for i in incomes)
    var_a = sum((a - avg_acc) ** 2 for a in access)
    corr = cov / (var_i ** 0.5 * var_a ** 0.5) if var_i and var_a else 0.0
    return {"correlation": corr}


def technology_adoption_patterns() -> Dict[str, Any]:
    data = load_data()
    avg_access = mean(d.get("tech_access", 0.0) for d in data)
    top = max(data, key=lambda d: d.get("tech_access", 0.0))
    return {
        "average_access": avg_access,
        "top_region": top.get("region"),
    }


def digital_divide_assessment() -> Dict[str, Any]:
    data = load_data()
    values = [d.get("tech_access", 0.0) for d in data]
    if not values:
        return {"gap": 0.0}
    return {"gap": max(values) - min(values)}


def community_network_detection() -> Dict[str, Any]:
    data = load_data()
    clusters: Dict[str, List[str]] = {}
    for rec in data:
        region = rec.get("region")
        lat = round(float(rec.get("latitude", 0.0)), 3)
        lon = round(float(rec.get("longitude", 0.0)), 3)
        key = f"{lat},{lon}"
        clusters.setdefault(key, []).append(region)
    return {"count": len(clusters), "clusters": clusters}


def adoption_summary() -> Dict[str, Any]:
    data = load_data()
    avg_access = mean(d.get("tech_access", 0.0) for d in data)
    penetration = mean(d.get("tech_access", 0.0) * d.get("population", 0) for d in data)
    total_pop = sum(d.get("population", 0) for d in data)
    penetration = penetration / total_pop if total_pop else 0.0
    correlation = socioeconomic_correlation()["correlation"]
    return {
        "average_access": avg_access,
        "market_penetration": penetration,
        "demographic_correlation": correlation,
        "top_region": max(data, key=lambda d: d.get("tech_access", 0.0)).get("region"),
    }


def digital_equity_metrics() -> Dict[str, Any]:
    data = load_data()
    values = [d.get("tech_access", 0.0) for d in data]
    incomes = [d.get("median_income", 0.0) for d in data]
    pop = [d.get("population", 0) for d in data]
    gap = max(values) - min(values) if values else 0.0
    avg_quality = mean(values) if values else 0.0
    affordability = mean(i / p if p else 0.0 for i, p in zip(incomes, pop))
    return {
        "connectivity_gap": gap,
        "avg_quality": avg_quality,
        "avg_affordability": affordability,
    }


__all__ = [
    "load_data",
    "socioeconomic_correlation",
    "technology_adoption_patterns",
    "digital_divide_assessment",
    "community_network_detection",
    "adoption_summary",
    "digital_equity_metrics",
]
