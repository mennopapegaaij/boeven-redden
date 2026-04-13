"""Het Arcade-venster van het spel."""

import arcade

from .instellingen import (
    BOEF_STRAAL,
    BOVENBALK_HOOGTE,
    LEVENSBALK_BREEDTE,
    LEVENSBALK_HOOGTE,
    MAX_LEVENS,
    STATUS_GAME_OVER,
    VENSTER_BREEDTE,
    VENSTER_HOOGTE,
    VENSTER_TITEL,
)
from .spel_logica import SpelLogica


class BoevenReddenVenster(arcade.Window):
    """Het hoofdvenster waarin je speelt."""

    def __init__(self) -> None:
        super().__init__(VENSTER_BREEDTE, VENSTER_HOOGTE, VENSTER_TITEL)
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.spel = SpelLogica()

    def on_update(self, delta_time: float) -> None:
        """Werk de spelregels bij."""

        self.spel.update(delta_time)

    def on_draw(self) -> None:
        """Teken alles op het scherm."""

        self.clear()
        self._teken_huis()
        self._teken_boefen()
        self._teken_politieautos()
        self._teken_speler()
        self._teken_hud()

        if self.spel.status == STATUS_GAME_OVER:
            self._teken_game_over()

    def _teken_huis(self) -> None:
        """Teken het huis."""

        huis = self.spel.huis
        rect = arcade.XYWH(huis.x, huis.y, huis.breedte, huis.hoogte)
        arcade.draw_rect_filled(rect, arcade.color.YELLOW_GREEN)
        arcade.draw_rect_outline(rect, arcade.color.DARK_GREEN, 3)
        arcade.draw_triangle_filled(
            huis.x - 45,
            huis.y + 40,
            huis.x + 45,
            huis.y + 40,
            huis.x,
            huis.y + 75,
            arcade.color.BROWN,
        )
        arcade.draw_text(
            "THUIS",
            huis.x,
            huis.y - 8,
            arcade.color.BLACK,
            12,
            bold=True,
            anchor_x="center",
        )

    def _teken_boefen(self) -> None:
        """Teken alle boefen."""

        for boef in self.spel.boefen:
            arcade.draw_circle_filled(boef.x, boef.y, BOEF_STRAAL, arcade.color.ORANGE)
            arcade.draw_circle_outline(boef.x, boef.y, BOEF_STRAAL, (180, 80, 0), 2)
            arcade.draw_text(
                "B",
                boef.x,
                boef.y - 6,
                arcade.color.BLACK,
                12,
                bold=True,
                anchor_x="center",
            )

    def _teken_politieautos(self) -> None:
        """Teken alle politieautos."""

        for politieauto in self.spel.politieautos:
            auto_rect = arcade.XYWH(
                politieauto.x,
                politieauto.y,
                politieauto.breedte,
                politieauto.hoogte,
            )
            licht_rect = arcade.XYWH(politieauto.x, politieauto.y + politieauto.hoogte // 2 - 4, 14, 8)
            arcade.draw_rect_filled(auto_rect, arcade.color.RED)
            arcade.draw_rect_filled(licht_rect, arcade.color.BLUE)
            arcade.draw_text(
                "P",
                politieauto.x,
                politieauto.y - 7,
                arcade.color.WHITE,
                12,
                bold=True,
                anchor_x="center",
            )

    def _teken_speler(self) -> None:
        """Teken de auto van de speler."""

        speler = self.spel.speler
        zichtbaar = self.spel.schade_timer <= 0 or int(self.spel.schade_timer * 6) % 2 == 0
        if not zichtbaar:
            return

        auto_rect = arcade.XYWH(speler.x, speler.y, speler.breedte, speler.hoogte)
        voorruit_rect = arcade.XYWH(speler.x, speler.y + 8, 20, 12)
        arcade.draw_rect_filled(auto_rect, arcade.color.BLUE)
        arcade.draw_rect_filled(voorruit_rect, (173, 216, 230))
        arcade.draw_text(
            "J",
            speler.x,
            speler.y - 9,
            arcade.color.WHITE,
            12,
            bold=True,
            anchor_x="center",
        )

    def _teken_hud(self) -> None:
        """Teken score, boefen en levens."""

        arcade.draw_rect_filled(
            arcade.XYWH(VENSTER_BREEDTE // 2, VENSTER_HOOGTE - 18, VENSTER_BREEDTE, BOVENBALK_HOOGTE),
            (0, 0, 0, 180),
        )

        arcade.draw_text(
            f"Score: {self.spel.score}",
            10,
            VENSTER_HOOGTE - 28,
            arcade.color.WHITE,
            16,
            bold=True,
        )

        arcade.draw_text(
            f"Boefen bij je: {self.spel.boefen_mee}",
            VENSTER_BREEDTE // 2,
            VENSTER_HOOGTE - 28,
            arcade.color.ORANGE,
            16,
            bold=True,
            anchor_x="center",
        )

        balk_x = VENSTER_BREEDTE - LEVENSBALK_BREEDTE - 10
        balk_y = VENSTER_HOOGTE - 24
        arcade.draw_rect_filled(
            arcade.XYWH(balk_x + LEVENSBALK_BREEDTE // 2, balk_y, LEVENSBALK_BREEDTE, LEVENSBALK_HOOGTE),
            arcade.color.DARK_RED,
        )

        gevuld = int((self.spel.speler.levens / MAX_LEVENS) * LEVENSBALK_BREEDTE)
        if gevuld > 0:
            kleur = arcade.color.GREEN if self.spel.speler.levens > 2 else (220, 80, 0)
            arcade.draw_rect_filled(
                arcade.XYWH(balk_x + gevuld // 2, balk_y, gevuld, LEVENSBALK_HOOGTE),
                kleur,
            )

        arcade.draw_text("Auto:", balk_x - 44, balk_y - 8, arcade.color.WHITE, 11)

    def _teken_game_over(self) -> None:
        """Teken het game over scherm."""

        arcade.draw_rect_filled(
            arcade.XYWH(VENSTER_BREEDTE // 2, VENSTER_HOOGTE // 2, VENSTER_BREEDTE, VENSTER_HOOGTE),
            (0, 0, 0, 190),
        )
        arcade.draw_text(
            "GAME OVER!",
            VENSTER_BREEDTE // 2,
            VENSTER_HOOGTE // 2 + 90,
            arcade.color.RED,
            60,
            bold=True,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Je hebt {self.spel.score} boefen thuisgebracht!",
            VENSTER_BREEDTE // 2,
            VENSTER_HOOGTE // 2 + 20,
            arcade.color.WHITE,
            26,
            anchor_x="center",
        )
        arcade.draw_text(
            "Druk op ENTER om opnieuw te spelen",
            VENSTER_BREEDTE // 2,
            VENSTER_HOOGTE // 2 - 60,
            arcade.color.YELLOW,
            20,
            anchor_x="center",
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Onthoud welke toets is ingedrukt."""

        if self.spel.status == STATUS_GAME_OVER:
            if key == arcade.key.ENTER:
                self.spel.nieuw_spel()
            return

        if key in (arcade.key.UP, arcade.key.W):
            self.spel.invoer.omhoog = True
        if key in (arcade.key.DOWN, arcade.key.S):
            self.spel.invoer.omlaag = True
        if key in (arcade.key.LEFT, arcade.key.A):
            self.spel.invoer.links = True
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.spel.invoer.rechts = True

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Verwijder een toets uit de invoer."""

        if key in (arcade.key.UP, arcade.key.W):
            self.spel.invoer.omhoog = False
        if key in (arcade.key.DOWN, arcade.key.S):
            self.spel.invoer.omlaag = False
        if key in (arcade.key.LEFT, arcade.key.A):
            self.spel.invoer.links = False
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.spel.invoer.rechts = False


def main() -> None:
    """Start het spelvenster."""

    BoevenReddenVenster()
    arcade.run()
