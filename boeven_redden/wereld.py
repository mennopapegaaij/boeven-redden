"""Alles wat bij de spelwereld hoort.

Later kunnen hier ook wegen, muren en spawnplekken per level in komen.
"""

import random

from .helpers import afstand_tussen, klem
from .instellingen import (
    HUIS_BREEDTE,
    HUIS_DAK_HOOGTE,
    HUIS_DAK_OVERSTEEK,
    HUIS_HOOGTE,
    HUIS_X,
    HUIS_Y,
    BOEF_SPAWN_BREEDTE,
    BOEF_SPAWN_HOOGTE,
    BOEF_SPAWN_VER_BREEDTE,
    BOEF_SPAWN_VER_HOOGTE,
    MAX_LEVENS,
    OBSTAKEL_HUIZEN,
    POLITIE_BREEDTE,
    POLITIE_HOOGTE,
    SPELER_BREEDTE,
    SPELER_HOOGTE,
    VENSTER_BREEDTE,
    VENSTER_HOOGTE,
    WERELD_BREEDTE,
    WERELD_HOOGTE,
)
from .modellen import Auto, Boef, Huis, PolitieAuto, SpelerAuto


def maak_speler() -> SpelerAuto:
    """Maak de spelersauto in het midden van het scherm."""

    return SpelerAuto(
        x=float(HUIS_X + 170),
        y=float(HUIS_Y),
        breedte=SPELER_BREEDTE,
        hoogte=SPELER_HOOGTE,
        levens=MAX_LEVENS,
    )


def maak_huis() -> Huis:
    """Maak het huis op een vaste plek."""

    return Huis(x=HUIS_X, y=HUIS_Y, breedte=HUIS_BREEDTE, hoogte=HUIS_HOOGTE)


def maak_obstakel_huizen() -> list[Huis]:
    """Maak extra huizen waar auto's niet doorheen kunnen."""

    huizen: list[Huis] = []
    for x, y, breedte, hoogte in OBSTAKEL_HUIZEN:
        huis = Huis(x=x, y=y, breedte=breedte, hoogte=hoogte)
        links = huis.x - huis.breedte / 2 - HUIS_DAK_OVERSTEEK
        rechts = huis.x + huis.breedte / 2 + HUIS_DAK_OVERSTEEK
        onder = huis.y - huis.hoogte / 2
        boven = huis.y + huis.hoogte / 2 + HUIS_DAK_HOOGTE
        if links >= 0 and rechts <= WERELD_BREEDTE and onder >= 0 and boven <= WERELD_HOOGTE:
            huizen.append(huis)

    return huizen


def houd_auto_in_wereld(auto: Auto) -> None:
    """Laat een auto niet buiten het scherm rijden."""

    auto.x = klem(auto.x, auto.breedte // 2, WERELD_BREEDTE - auto.breedte // 2)
    auto.y = klem(auto.y, auto.hoogte // 2, WERELD_HOOGTE - auto.hoogte // 2)


def klem_camera_midden(camera_x: float, camera_y: float) -> tuple[float, float]:
    """Zorg dat het midden van de camera binnen de wereld blijft."""

    halve_breedte = VENSTER_BREEDTE / 2
    halve_hoogte = VENSTER_HOOGTE / 2
    return (
        klem(camera_x, halve_breedte, WERELD_BREEDTE - halve_breedte),
        klem(camera_y, halve_hoogte, WERELD_HOOGTE - halve_hoogte),
    )


def punt_is_in_huis(x: float, y: float, huis: Huis, marge: float = 0) -> bool:
    """Controleer of een punt in of te dicht bij een huis staat."""

    links = huis.x - huis.breedte / 2 - HUIS_DAK_OVERSTEEK - marge
    rechts = huis.x + huis.breedte / 2 + HUIS_DAK_OVERSTEEK + marge
    onder = huis.y - huis.hoogte / 2 - marge
    boven = huis.y + huis.hoogte / 2 + HUIS_DAK_HOOGTE + marge
    return links <= x <= rechts and onder <= y <= boven


def auto_raakt_huis(auto: Auto, huis: Huis) -> bool:
    """Controleer of een auto tegen een huis botst."""

    links_auto = auto.x - auto.breedte / 2
    rechts_auto = auto.x + auto.breedte / 2
    onder_auto = auto.y - auto.hoogte / 2
    boven_auto = auto.y + auto.hoogte / 2

    links_huis = huis.x - huis.breedte / 2 - HUIS_DAK_OVERSTEEK
    rechts_huis = huis.x + huis.breedte / 2 + HUIS_DAK_OVERSTEEK
    onder_huis = huis.y - huis.hoogte / 2
    boven_huis = huis.y + huis.hoogte / 2 + HUIS_DAK_HOOGTE

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

    zoekgebieden = (
        (BOEF_SPAWN_BREEDTE, BOEF_SPAWN_HOOGTE, 120),
        (BOEF_SPAWN_VER_BREEDTE, BOEF_SPAWN_VER_HOOGTE, 80),
        (WERELD_BREEDTE, WERELD_HOOGTE, 40),
    )

    for breedte, hoogte, pogingen in zoekgebieden:
        min_x = max(60, int(speler.x - breedte / 2))
        max_x = min(WERELD_BREEDTE - 60, int(speler.x + breedte / 2))
        min_y = max(60, int(speler.y - hoogte / 2))
        max_y = min(WERELD_HOOGTE - 60, int(speler.y + hoogte / 2))

        if min_x >= max_x or min_y >= max_y:
            continue

        for _ in range(pogingen):
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)

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


def maak_politieauto(rond_x: float, rond_y: float, huizen: list[Huis]) -> PolitieAuto:
    """Laat een politieauto net buiten het zicht van de speler beginnen."""

    halve_breedte = VENSTER_BREEDTE // 2
    halve_hoogte = VENSTER_HOOGTE // 2
    camera_x, camera_y = klem_camera_midden(rond_x, rond_y)
    zicht_links = camera_x - halve_breedte
    zicht_rechts = camera_x + halve_breedte
    zicht_onder = camera_y - halve_hoogte
    zicht_boven = camera_y + halve_hoogte

    for _ in range(200):
        geldige_kanten: list[int] = []
        if zicht_boven + 50 <= WERELD_HOOGTE - POLITIE_HOOGTE / 2:
            geldige_kanten.append(0)
        if zicht_rechts + 50 <= WERELD_BREEDTE - POLITIE_BREEDTE / 2:
            geldige_kanten.append(1)
        if zicht_onder - 50 >= POLITIE_HOOGTE / 2:
            geldige_kanten.append(2)
        if zicht_links - 50 >= POLITIE_BREEDTE / 2:
            geldige_kanten.append(3)

        kant = random.choice(geldige_kanten)
        if kant == 0:
            x = random.randint(int(zicht_links), int(zicht_rechts))
            y = zicht_boven + 50
        elif kant == 1:
            x = zicht_rechts + 50
            y = random.randint(int(zicht_onder), int(zicht_boven))
        elif kant == 2:
            x = random.randint(int(zicht_links), int(zicht_rechts))
            y = zicht_onder - 50
        else:
            x = zicht_links - 50
            y = random.randint(int(zicht_onder), int(zicht_boven))

        politieauto = PolitieAuto(
            x=float(klem(x, POLITIE_BREEDTE // 2, WERELD_BREEDTE - POLITIE_BREEDTE // 2)),
            y=float(klem(y, POLITIE_HOOGTE // 2, WERELD_HOOGTE - POLITIE_HOOGTE // 2)),
            breedte=POLITIE_BREEDTE,
            hoogte=POLITIE_HOOGTE,
        )

        if all(not auto_raakt_huis(politieauto, huis) for huis in huizen):
            return politieauto

    return PolitieAuto(
        x=float(klem(zicht_rechts + 50, POLITIE_BREEDTE // 2, WERELD_BREEDTE - POLITIE_BREEDTE // 2)),
        y=float(klem(camera_y, POLITIE_HOOGTE // 2, WERELD_HOOGTE - POLITIE_HOOGTE // 2)),
        breedte=POLITIE_BREEDTE,
        hoogte=POLITIE_HOOGTE,
    )
