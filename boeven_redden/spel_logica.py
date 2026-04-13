"""Hier staan de spelregels.

Dit bestand weet:
- wat er beweegt
- wanneer je punten krijgt
- wanneer je schade krijgt

Het tekenen zit expres ergens anders. Zo kunnen we later
makkelijk muren, botsingen en slimmere AI toevoegen.
"""

from .ai import bereken_achtervolging_stap, bereken_politie_snelheid
from .helpers import afstand_tussen
from .instellingen import (
    AANTAL_BOEFEN,
    BOEF_STRAAL,
    MAX_BOEFEN_IN_AUTO,
    POLITIE_MIN_INTERVAL,
    POLITIE_START_INTERVAL,
    SCHADE_PAUZE,
    SPELER_SNELHEID,
    STATUS_GAME_OVER,
    STATUS_SPELEN,
)
from .modellen import Boef, Huis, InvoerStatus, PolitieAuto, SpelerAuto
from .wereld import (
    maak_boef,
    maak_huis,
    maak_obstakel_huizen,
    maak_politieauto,
    maak_speler,
    verplaats_auto_met_huizen,
)


class SpelLogica:
    """Houdt alle gegevens van een spelronde bij."""

    def __init__(self) -> None:
        self.nieuw_spel()

    def nieuw_spel(self) -> None:
        """Zet alles klaar voor een nieuwe ronde."""

        self.speler: SpelerAuto = maak_speler()
        self.huis: Huis = maak_huis()
        self.obstakel_huizen: list[Huis] = maak_obstakel_huizen()
        self.invoer = InvoerStatus()
        self.boefen: list[Boef] = []
        self.politieautos: list[PolitieAuto] = []
        self.boefen_mee = 0
        self.score = 0
        self.politie_timer = 0.0
        self.schade_timer = 0.0
        self.status = STATUS_SPELEN
        self.vul_boefen_aan()

    def update(self, delta_time: float) -> None:
        """Werk een klein stukje van het spel bij."""

        if self.status != STATUS_SPELEN:
            return

        self._beweeg_speler()
        self._update_schade_timer(delta_time)
        self._beweeg_politieautos()
        self._pak_boefen_op()
        self._lever_boefen_af()
        self._controleer_politiebotsingen()
        self._spawn_meer_politie(delta_time)
        self.vul_boefen_aan()

    def vul_boefen_aan(self) -> None:
        """Zorg dat er altijd genoeg boefen op de kaart staan."""

        while len(self.boefen) < AANTAL_BOEFEN:
            nieuwe_boef = maak_boef(
                self.speler,
                self.huis,
                self.obstakel_huizen,
                self.boefen,
            )
            if nieuwe_boef is None:
                break
            self.boefen.append(nieuwe_boef)

    def _beweeg_speler(self) -> None:
        """Verplaats de speler met de toetsen."""

        dx = 0.0
        dy = 0.0
        if self.invoer.omhoog:
            dy += SPELER_SNELHEID
        if self.invoer.omlaag:
            dy -= SPELER_SNELHEID
        if self.invoer.links:
            dx -= SPELER_SNELHEID
        if self.invoer.rechts:
            dx += SPELER_SNELHEID

        verplaats_auto_met_huizen(self.speler, dx, dy, self.obstakel_huizen)

    def _update_schade_timer(self, delta_time: float) -> None:
        """Laat de korte onkwetsbare tijd langzaam aflopen."""

        if self.schade_timer > 0:
            self.schade_timer -= delta_time

    def _beweeg_politieautos(self) -> None:
        """Laat alle politieautos richting de speler rijden."""

        snelheid = bereken_politie_snelheid(self.score)
        for politieauto in self.politieautos:
            dx, dy = bereken_achtervolging_stap(politieauto, self.speler, snelheid)
            verplaats_auto_met_huizen(politieauto, dx, dy, self.obstakel_huizen)

    def _pak_boefen_op(self) -> None:
        """Pak boefen op als de speler dichtbij komt."""

        boefen_over: list[Boef] = []
        raak_afstand = self.speler.breedte // 2 + BOEF_STRAAL

        for boef in self.boefen:
            afstand = afstand_tussen(self.speler.x, self.speler.y, boef.x, boef.y)
            kan_nog_meer_meenemen = self.boefen_mee < MAX_BOEFEN_IN_AUTO
            if afstand < raak_afstand and kan_nog_meer_meenemen:
                self.boefen_mee += 1
            else:
                boefen_over.append(boef)

        self.boefen = boefen_over

    def _lever_boefen_af(self) -> None:
        """Geef punten als je met boefen bij het huis komt."""

        afstand_huis = afstand_tussen(self.speler.x, self.speler.y, self.huis.x, self.huis.y)
        bereik_huis = self.huis.breedte // 2 + self.speler.breedte // 2
        if afstand_huis < bereik_huis and self.boefen_mee > 0:
            self.score += self.boefen_mee
            self.boefen_mee = 0

    def _controleer_politiebotsingen(self) -> None:
        """Geef schade als een politieauto je raakt."""

        if self.schade_timer > 0:
            return

        for politieauto in self.politieautos:
            raak_afstand = self.speler.breedte // 2 + politieauto.breedte // 2
            afstand = afstand_tussen(
                self.speler.x,
                self.speler.y,
                politieauto.x,
                politieauto.y,
            )
            if afstand < raak_afstand:
                self.speler.levens -= 1
                self.schade_timer = SCHADE_PAUZE
                if self.speler.levens <= 0:
                    self.status = STATUS_GAME_OVER
                break

    def _spawn_meer_politie(self, delta_time: float) -> None:
        """Laat steeds vaker nieuwe politieautos komen."""

        self.politie_timer += delta_time
        politie_interval = max(POLITIE_MIN_INTERVAL, POLITIE_START_INTERVAL - self.score * 0.4)

        if self.politie_timer >= politie_interval:
            self.politie_timer = 0.0
            huizen = [self.huis, *self.obstakel_huizen]
            self.politieautos.append(maak_politieauto(self.speler.x, self.speler.y, huizen))
