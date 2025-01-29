from point import Point


def bresenham_ellipse(x0, y0, rx, ry):
    points = []

    def plot_ellipse_points(cx, cy, x, y, d=None, string=None):
        points.extend([
            Point(cx + x, cy + y, debug={"x": cx + x, "y": cy + y, "d2": f"{d} {string}"}), Point(cx - x, cy + y, debug={"x": cx - x, "y": cy + y, "d2": f"{d} {string}"}),
            Point(cx + x, cy - y, debug={"x": cx + x, "y": cy - y, "d2": f"{d} {string}"}), Point(cx - x, cy - y, debug={"x": cx - x, "y": cy - y, "d2": f"{d} {string}"})
        ])

    x, y = 0, ry
    rx2, ry2 = rx ** 2, ry ** 2
    tworx2, twory2 = 2 * rx2, 2 * ry2
    px, py = 0, tworx2 * y

    # Region 1
    d1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    while px < py:
        plot_ellipse_points(x0, y0, x, y, d1, "< 0")
        x += 1
        px += twory2
        if d1 < 0:
            d1 += ry2 + px
        else:
            y -= 1
            py -= tworx2
            d1 += ry2 + px - py

    # Region 2
    d2 = (ry2 * (x + 0.5) ** 2) + (rx2 * (y - 1) ** 2) - (rx2 * ry2)
    while y >= 0:
        plot_ellipse_points(x0, y0, x, y, d2, "> 0")
        y -= 1
        py -= tworx2
        if d2 > 0:
            d2 += rx2 - py
        else:
            x += 1
            px += twory2
            d2 += rx2 - py + px

    return points
