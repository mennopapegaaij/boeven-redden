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
    OBSTAKEL_HUIZEN,
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


def maak_obstakel_huizen() -> list[Huis]:
    """Maak extra huizen waar auto's niet doorheen kunnen."""

    return [
        Huis(x=x, y=y, breedte=breedte, hoogte=hoogte)
        for x, y, breedte, hoogte in OBSTAKEL_HUIZEN
    ]


def houd_auto_in_wereld(auto: Auto) -> None:
    """Laat een auto niet buiten het scherm rijden."""

    auto.x = klem(auto.x, auto.breedte // 2, VENSTER_BREEDTE - auto.breedte // 2)
    auto.y = klem(auto.y, auto.hoogte // 2, VENSTER_HOOGTE - auto.hoogte // 2)


def punt_is_in_huis(x: float, y: float, huis: Huis, marge: float = 0) -> bool:
    """Controleer of een punt in of te dicht bij een huis staat."""

    links = huis.x - huis.breedte / 2 - marge
    rechts = huis.x + huis.breedte / 2 + marge
    onder = huis.y - huis.hoogte / 2 - marge
    boven = huis.y + huis.hoogte / 2 + marge
    return links <= x <= rechts and onder <= y <= boven


def auto_raakt_huis(auto: Auto, huis: Huis) -> bool:
    """Controleer of een auto tegen een huis botst."""

    links_auto = auto.x - auto.breedte / 2
    rechts_auto = auto.x + auto.breedte / 2
    onder_auto = auto.y - auto.hoogte / 2
    boven_auto = auto.y + auto.hoogte / 2

    links_huis = huis.x - huis.breedte / 2
    rechts_huis = huis.x + huis.breedte / 2
    onder_huis = huis.y - huis.hoogte / 2
    boven_huis = huis.y + huis.hoogte / 2

    return (
        links_auto < rechts_huis
        and rechts_auto > links_huis
        and onder_auto < boven_huis
        and boven_auto > onder_huis
    )


def verplaats_auto_met_huizen(auto: Auto, dx: float, dy: float, huizen: list[Huis]) -> None:
    """Beweeg een auto, maar stop als er een huis in de weg staat."""

    oude_x = auto.x
    auto.x += dx
    houd_auto_in_wereld(auto)
    if any(auto_raakt_huis(auto, huis) for huis in huizen):
        auto.x = oude_x

    oude_y = auto.y
    auto.y += dy
    houd_auto_in_wereld(auto)
    if any(auto_raakt_huis(auto, huis) for huis in huizen):
        auto.y = oude_y


def maak_boef(
    speler: SpelerAuto,
    huis: Huis,
    obstakel_huizen: list[Huis],
    bestaande_boefen: list[Boef],
) -> Boef | None:
    """Zoek een nette plek voor een nieuwe boef."""

    for _ in range(200):
        x = random.randint(60, VENSTER_BREEDTE - 60)
        y = random.randint(60, VENSTER_HOOGTE - 60)

        ver_van_huis = afstand_tussen(x, y, huis.x, huis.y) > 110
        ver_van_speler = afstand_tussen(x, y, speler.x, speler.y) > 90
        niet_in_obstakel_huis = all(
            not punt_is_in_huis(x, y, obstakel_huis, marge=20)
            for obstakel_huis in obstakel_huizen
        )
        ver_van_andere_boef = all(
            afstand_tussen(x, y, boef.x, boef.y) > 40 for boef in bestaande_boefen
        )

        if ver_van_huis and ver_van_speler and niet_in_obstakel_huis and ver_van_andere_boef:
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
