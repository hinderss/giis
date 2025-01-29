from point import Point


def bresenham_hyperbola(x0, y0, a, b, x_limit):
    points = []
    x = abs(a)
    y = 0
    a **= 2
    b **= 2
    d = b * (2 * x + 1) - a
    bx = x

    while x - bx <= x_limit:
        f1 = (d <= 0) or (2 * d - b * (2 * x + 1) <= 0)
        f2 = (d <= 0) or (2 * d - a * (2 * y + 1) > 0)

        points.append(Point(x0 - x, y0 - y, debug={"x": x0-x, "y": y0-y, "F1": f1, "F2": f2}))
        points.append(Point(x0 + x, y0 + y, debug={"x": x0-x, "y": y0-y, "F1": f1, "F2": f2}))
        points.append(Point(x0 + x, y0 - y, debug={"x": x0-x, "y": y0-y, "F1": f1, "F2": f2}))
        points.append(Point(x0 - x, y0 + y, debug={"x": x0-x, "y": y0-y, "F1": f1, "F2": f2}))

        x = x + 1 if f1 else x
        y = y + 1 if f2 else y

        d = d + b * (2 * x + 1) if f1 else d
        d = d - a * (2 * y - 1) if f2 else d

    return points
