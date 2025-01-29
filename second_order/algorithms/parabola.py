import math

from point import Point


def bresenham_parabola(x0, y0, a, b, c, x_limit, y_limit):
    points = []
    # x = 0
    # y = 0
    # d = 0
    #
    # while y < x_limit:
    #     points.append((x+x0, y+y0, BLACK))
    #     points.append((-x+x0, y+y0, BLACK))
    #     f1 = (d <= 0) or (2*(d-x)-1 <= 0)
    #     f2 = (d >= 0) or (2*d + 1 > 0)
    #
    #     x = x + 1 if f1 else x
    #     y = y + 1 if f2 else y
    #
    #     d = d + a*2*x + 1 if f1 else d
    #     d = d - 1 if f2 else d

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
