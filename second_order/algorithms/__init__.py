from second_order.algorithms.circle import bresenham_circle
from second_order.algorithms.ellipse import bresenham_ellipse
from second_order.algorithms.hyperbola import bresenham_hyperbola
from second_order.algorithms.parabola import bresenham_parabola

algorithms = {
    "Parabola": bresenham_parabola,
    "Hyperbola": bresenham_hyperbola,
    "Circle": bresenham_circle,
    "Ellipse": bresenham_ellipse,
}
