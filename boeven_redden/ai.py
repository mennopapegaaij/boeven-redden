"""Hier staat hoe de politie beweegt.

Later kunnen we hier slimmere AI maken, zoals:
- om muren heen rijden
- wegen volgen
- elkaar ontwijken
"""

from .helpers import afstand_tussen
from .instellingen import POLITIE_START_SNELHEID
from .modellen import PolitieAuto, SpelerAuto


def bereken_politie_snelheid(score: int) -> float:
    """Geef de vaste snelheid van de politie terug."""

    return POLITIE_START_SNELHEID


def bereken_achtervolging_stap(
    politieauto: PolitieAuto,
    speler: SpelerAuto,
    snelheid: float,
) -> tuple[float, float]:
    """Bereken hoe ver een politieauto deze beurt wil rijden."""

    afstand = afstand_tussen(politieauto.x, politieauto.y, speler.x, speler.y)
    if afstand <= 1:
        return 0.0, 0.0

    dx = speler.x - politieauto.x
    dy = speler.y - politieauto.y
    return (dx / afstand) * snelheid, (dy / afstand) * snelheid
