"""Kleine helper-functies voor rekenen."""

import math


def afstand_tussen(x1: float, y1: float, x2: float, y2: float) -> float:
    """Meet de afstand tussen twee punten."""

    return math.hypot(x2 - x1, y2 - y1)


def klem(getal: float, minimum: float, maximum: float) -> float:
    """Zorg dat een getal binnen twee grenzen blijft."""

    return max(minimum, min(maximum, getal))
