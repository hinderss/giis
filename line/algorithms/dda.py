from point import Point


def dda_algorithm(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps

    x, y = x1, y1
    for step in range(steps + 1):
        debug_info = {
            "dx": dx,
            "dy": dy,
            "steps": steps,
            "x_increment": x_increment,
            "y_increment": y_increment,
            "step": step,
            "x": x,
            "y": y,
        }
        points.append(Point(round(x), round(y), debug=debug_info))
        x += x_increment
        y += y_increment

    return points
