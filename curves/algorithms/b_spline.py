from point import Point


def b_spline(control_points: list[tuple[int, int]], degree: int = 3, num_points: int = 1000) -> list[Point]:
    n = len(control_points) - 1
    m = n + degree + 1

    knots = [0] * (degree + 1) + list(range(1, m - 2 * degree)) + [m - 2 * degree] * (degree + 1)

    def basis_function(i, k, t):
        if k == 0:
            return 1 if knots[i] <= t < knots[i + 1] else 0
        c1 = (t - knots[i]) / (knots[i + k] - knots[i]) * basis_function(i, k - 1, t) if knots[i + k] != knots[i] else 0
        c2 = (knots[i + k + 1] - t) / (knots[i + k + 1] - knots[i + 1]) * basis_function(i + 1, k - 1, t) if knots[i + k + 1] != knots[i + 1] else 0
        return c1 + c2

    points = []
    for i in range(num_points):
        t = knots[degree] + (knots[-degree - 1] - knots[degree]) * i / (num_points - 1)
        x, y = 0, 0
        for j in range(n + 1):
            b = basis_function(j, degree, t)
            point_x, point_y = control_points[j]
            x += point_x * b
            y += point_y * b
        p = Point(round(x), round(y))
        if p not in points and p != Point(0, 0):
            p.debug = {
                "t": f"{t:.3f}",
                "x": f"{p.x:.3f}",
                "y": f"{p.y:.3f}",
            }
            points.append(p)

    return points[1:]
