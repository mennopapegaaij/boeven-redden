"""Het Arcade-venster van het spel."""

import arcade

from .instellingen import (
    BOEF_STRAAL,
    BOVENBALK_HOOGTE,
    LEVENSBALK_BREEDTE,
    LEVENSBALK_HOOGTE,
    MAX_BOEFEN_IN_AUTO,
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
        self._teken_obstakel_huizen()
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
        self._teken_gebouw(huis.x, huis.y, huis.breedte, huis.hoogte, arcade.color.YELLOW_GREEN)
        arcade.draw_text(
            "THUIS",
            huis.x,
            huis.y - 8,
            arcade.color.BLACK,
            12,
            bold=True,
            anchor_x="center",
        )

    def _teken_obstakel_huizen(self) -> None:
        """Teken de huizen waar je niet doorheen kunt rijden."""

        for huis in self.spel.obstakel_huizen:
            self._teken_gebouw(huis.x, huis.y, huis.breedte, huis.hoogte, arcade.color.LIGHT_GRAY)

    def _teken_gebouw(
        self,
        x: float,
        y: float,
        breedte: int,
        hoogte: int,
        kleur: tuple[int, int, int] | tuple[int, int, int, int],
    ) -> None:
        """Teken een huisje."""

        rect = arcade.XYWH(x, y, breedte, hoogte)
        arcade.draw_rect_filled(rect, kleur)
        arcade.draw_rect_outline(rect, arcade.color.DARK_GREEN, 3)
        arcade.draw_triangle_filled(
            x - breedte / 2 - 5,
            y + hoogte / 2,
            x + breedte / 2 + 5,
            y + hoogte / 2,
            x,
            y + hoogte / 2 + 35,
            arcade.color.BROWN,
        )
        arcade.draw_rect_filled(arcade.XYWH(x, y - 10, 18, 26), arcade.color.DARK_BROWN)
        arcade.draw_rect_filled(arcade.XYWH(x - breedte / 4, y + 5, 16, 16), arcade.color.SKY_BLUE)
        arcade.draw_rect_filled(arcade.XYWH(x + breedte / 4, y + 5, 16, 16), arcade.color.SKY_BLUE)

    def _teken_boefen(self) -> None:
        """Teken alle boefen."""

        for boef in self.spel.boefen:
            self._teken_boef(boef.x, boef.y)

    def _teken_boef(self, x: float, y: float) -> None:
        """Teken een boef met masker en gestreept shirt."""

        arcade.draw_ellipse_filled(x, y - 15, BOEF_STRAAL + 8, 10, (0, 0, 0, 80))

        # Hoofd
        arcade.draw_circle_filled(x, y + 12, 9, (255, 224, 189))
        arcade.draw_circle_outline(x, y + 12, 9, (120, 90, 70), 2)

        # Zwart masker
        arcade.draw_rect_filled(arcade.XYWH(x, y + 11, 18, 6), arcade.color.BLACK)
        arcade.draw_circle_filled(x - 4, y + 11, 1.2, arcade.color.WHITE)
        arcade.draw_circle_filled(x + 4, y + 11, 1.2, arcade.color.WHITE)

        # Gestreept boevenshirt
        arcade.draw_rect_filled(arcade.XYWH(x, y - 2, 18, 20), (35, 35, 35))
        arcade.draw_rect_filled(arcade.XYWH(x - 5, y - 2, 3, 20), arcade.color.WHITE)
        arcade.draw_rect_filled(arcade.XYWH(x, y - 2, 3, 20), arcade.color.WHITE)
        arcade.draw_rect_filled(arcade.XYWH(x + 5, y - 2, 3, 20), arcade.color.WHITE)

        # Armen
        arcade.draw_rect_filled(arcade.XYWH(x - 11, y - 3, 4, 14), (255, 224, 189))
        arcade.draw_rect_filled(arcade.XYWH(x + 11, y - 3, 4, 14), (255, 224, 189))

        # Benen
        arcade.draw_rect_filled(arcade.XYWH(x - 4, y - 17, 4, 12), arcade.color.DARK_BLUE)
        arcade.draw_rect_filled(arcade.XYWH(x + 4, y - 17, 4, 12), arcade.color.DARK_BLUE)

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
            f"Boef in auto: {self.spel.boefen_mee}/{MAX_BOEFEN_IN_AUTO}",
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
