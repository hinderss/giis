from convex_hull.algorithms.graham import graham_convex_hull
from convex_hull.algorithms.jarvis import jarvis_convex_hull

algorithms = {
    "Jarvis": jarvis_convex_hull,
    "Graham": graham_convex_hull,
}
