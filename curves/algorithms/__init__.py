from curves.algorithms.b_spline import b_spline
from curves.algorithms.bezier import bezier_curve
from curves.algorithms.hermite import hermite_curve

algorithms = {
    "Hermite": hermite_curve,
    "Bezier": bezier_curve,
    "B-spline": b_spline,
}
