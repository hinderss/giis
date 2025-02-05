import math

from point import Point


def bresenham_parabola(x0, y0, a, b, c, x_limit, y_limit):
    points = []

    div = 0.5 / a
    x, y = 0, 0
    d_pre = 0.5 - a
    d_post = 1 - a * math.ceil(div) - 0.25 * a

    while x + x0 <= x_limit and y + y0 <= y_limit:
        points.append(Point(x + x0, y + y0, debug={"x": x + x0, "y": y + y0, "d_pre": f"{d_pre:.3f} < 0", "d_post": f"{d_post:.3f} >= 0"}))
        points.append(Point(-x + x0, y + y0, debug={"x": x + x0, "y": y + y0, "d_pre": f"{d_pre:.3f} < 0", "d_post": f"{d_post:.3f} >= 0"}))

        if x < div:
            tmp = -2 * a * x - 3 * a
            x += 1
            if d_pre < 0:
                y += 1
                d_pre += tmp + 1
            else:
                d_pre += tmp
        else:
            tmp = -2 * a * x - 2 * a + 1
            y += 1
            if d_post >= 0:
                x += 1
                d_post += tmp
            else:
                d_post += 1

    return points
