from point import Point


def jarvis_convex_hull(points: list[(int, int)]) -> list[Point]:
    n = len(points)
    if n < 3:
        return points

    hull = []
    l = min(range(n), key=lambda i: points[i][0])
    p = l
    while True:
        hull.append(Point(*points[p]))
        q = (p + 1) % n
        for i in range(n):
            if i == p:
                continue
            val = (points[i][1] - points[p][1]) * (points[q][0] - points[p][0]) - \
                  (points[q][1] - points[p][1]) * (points[i][0] - points[p][0])
            if val < 0:
                q = i
        p = q
        if p == l:
            break
    return hull
