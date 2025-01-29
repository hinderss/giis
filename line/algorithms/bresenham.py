from point import Point


def bresenham_algorithm(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        debug_info = {
            "sx": sx,
            "sy": sy,
            "dx": dx,
            "dy": dy,
            "error": err,
            "error2 > -dy": f"{2*err} > {-1*dy}",
            "error2 < dx": f"{2*err} < {dx}",
            "x": x1,
            "y": y1,
        }
        points.append(Point(x1, y1, debug=debug_info))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points
