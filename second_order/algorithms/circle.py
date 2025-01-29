from point import Point


def bresenham_circle(x0, y0, radius):
    x, y = 0, radius
    d = 3 - 2 * radius
    points = []

    def plot_circle_points(cx, cy, x, y, d=None):
        points.extend([
            Point(cx + x, cy + y, debug={"x": cx + x, "y": cy + y, "d": f"{d} < 0"}), Point(cx - x, cy + y, debug={"x": cx - x, "y": cy + y, "d": f"{d} < 0"}),
            Point(cx + x, cy - y, debug={"x": cx + x, "y": cy - y, "d": f"{d} < 0"}), Point(cx - x, cy - y, debug={"x": cx - x, "y": cy - y, "d": f"{d} < 0"}),
            Point(cx + y, cy + x, debug={"x": cx + y, "y": cy + x, "d": f"{d} < 0"}), Point(cx - y, cy + x, debug={"x": cx - y, "y": cy + x, "d": f"{d} < 0"}),
            Point(cx + y, cy - x, debug={"x": cx + y, "y": cy - x, "d": f"{d} < 0"}), Point(cx - y, cy - x, debug={"x": cx - y, "y": cy - x, "d": f"{d} < 0"}),
        ])

    plot_circle_points(x0, y0, x, y, d)

    while x < y:
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
        plot_circle_points(x0, y0, x, y, d)

    return points
