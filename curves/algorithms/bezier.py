import numpy as np

from point import Point


# def hermite_curve(p1, vend1, p4, vend4) -> list[Point]:

def bezier_curve(control_points: list[tuple[int, int]], num_points: int = 1000) -> list[Point]:
    n = len(control_points) - 1
    points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        x, y = 0, 0
        for j, point in enumerate(control_points):
            point_x, point_y = point
            binom = 1
            for k in range(1, j + 1):
                binom *= (n - k + 1) / k
            x += binom * (1 - t)**(n - j) * t**j * point_x
            y += binom * (1 - t)**(n - j) * t**j * point_y
        p = Point(round(x), round(y))
        if p not in points:
            p.debug = {
                "t": f"{t:.3f}",
                "x": f"{p.x:.3f}",
                "y": f"{p.y:.3f}",
            }
            points.append(p)
    return points
