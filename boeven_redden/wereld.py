"""Alles wat bij de spelwereld hoort.

Later kunnen hier ook wegen, muren en spawnplekken per level in komen.
"""

import random

from .helpers import afstand_tussen, klem
from .instellingen import (
    HUIS_BREEDTE,
    HUIS_HOOGTE,
    HUIS_X,
    HUIS_Y,
    MAX_LEVENS,
    POLITIE_BREEDTE,
    POLITIE_HOOGTE,
    SPELER_BREEDTE,
    SPELER_HOOGTE,
    VENSTER_BREEDTE,
    VENSTER_HOOGTE,
)
from .modellen import Auto, Boef, Huis, PolitieAuto, SpelerAuto


def maak_speler() -> SpelerAuto:
    """Maak de spelersauto in het midden van het scherm."""

    return SpelerAuto(
        x=float(VENSTER_BREEDTE // 2),
        y=float(VENSTER_HOOGTE // 2),
        breedte=SPELER_BREEDTE,
        hoogte=SPELER_HOOGTE,
        levens=MAX_LEVENS,
    )


def maak_huis() -> Huis:
    """Maak het huis op een vaste plek."""

    return Huis(x=HUIS_X, y=HUIS_Y, breedte=HUIS_BREEDTE, hoogte=HUIS_HOOGTE)


def houd_auto_in_wereld(auto: Auto) -> None:
    """Laat een auto niet buiten het scherm rijden."""

    auto.x = klem(auto.x, auto.breedte // 2, VENSTER_BREEDTE - auto.breedte // 2)
    auto.y = klem(auto.y, auto.hoogte // 2, VENSTER_HOOGTE - auto.hoogte // 2)


def maak_boef(speler: SpelerAuto, huis: Huis, bestaande_boefen: list[Boef]) -> Boef | None:
    """Zoek een nette plek voor een nieuwe boef."""

    for _ in range(200):
        x = random.randint(60, VENSTER_BREEDTE - 60)
        y = random.randint(60, VENSTER_HOOGTE - 60)

        ver_van_huis = afstand_tussen(x, y, huis.x, huis.y) > 110
        ver_van_speler = afstand_tussen(x, y, speler.x, speler.y) > 90
        ver_van_andere_boef = all(
            afstand_tussen(x, y, boef.x, boef.y) > 40 for boef in bestaande_boefen
        )

        if ver_van_huis and ver_van_speler and ver_van_andere_boef:
            return Boef(x=float(x), y=float(y))

    return None


def maak_politieauto() -> PolitieAuto:
    """Laat een politieauto aan de rand van het scherm beginnen."""

    kant = random.randint(0, 3)
    if kant == 0:
        x = random.randint(0, VENSTER_BREEDTE)
        y = VENSTER_HOOGTE + 30
    elif kant == 1:
        x = VENSTER_BREEDTE + 30
        y = random.randint(0, VENSTER_HOOGTE)
    elif kant == 2:
        x = random.randint(0, VENSTER_BREEDTE)
        y = -30
    else:
        x = -30
        y = random.randint(0, VENSTER_HOOGTE)

    return PolitieAuto(
        x=float(x),
        y=float(y),
        breedte=POLITIE_BREEDTE,
        hoogte=POLITIE_HOOGTE,
    )
