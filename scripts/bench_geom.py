import timeit

import utils

try:
    import cgeom
except Exception:  # pragma: no cover - extension not built
    cgeom = None

POINT1 = (37.7749, -122.4194)
POINT2 = (34.0522, -118.2437)
POLY = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]

reps = 10000

print("haversine_distance python:", timeit.timeit(
    lambda: utils._haversine_distance_py(POINT1, POINT2), number=reps))
if cgeom:
    print("haversine_distance c:", timeit.timeit(
        lambda: cgeom.haversine_distance(POINT1, POINT2), number=reps))

print("polygon_area python:", timeit.timeit(
    lambda: utils._polygon_area_py(POLY), number=reps))
if cgeom:
    print("polygon_area c:", timeit.timeit(
        lambda: cgeom.polygon_area(POLY), number=reps))

print("point_in_polygon python:", timeit.timeit(
    lambda: utils._point_in_polygon_py((0.5, 0.5), POLY), number=reps))
if cgeom:
    print("point_in_polygon c:", timeit.timeit(
        lambda: cgeom.point_in_polygon((0.5, 0.5), POLY), number=reps))
