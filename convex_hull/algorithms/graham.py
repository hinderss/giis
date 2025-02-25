from point import Point
from utils import cross_product


def graham_convex_hull(points: list[(int, int)]):
    points = sorted([Point(*point) for point in points], key=lambda point: (point.x, point.y))
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(Point(*p))
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(Point(*p))
    return lower[:-1] + upper[:-1]
