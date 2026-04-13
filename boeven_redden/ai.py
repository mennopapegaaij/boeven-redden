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


def achtervolg_speler(politieauto: PolitieAuto, speler: SpelerAuto, snelheid: float) -> None:
    """Beweeg een politieauto recht op de speler af."""

    afstand = afstand_tussen(politieauto.x, politieauto.y, speler.x, speler.y)
    if afstand <= 1:
        return

    dx = speler.x - politieauto.x
    dy = speler.y - politieauto.y
    politieauto.x += (dx / afstand) * snelheid
    politieauto.y += (dy / afstand) * snelheid
