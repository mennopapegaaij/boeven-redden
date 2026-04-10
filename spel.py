"""
Boeven Redden!
==============
Jij rijdt als boef in een auto.
Rij over andere boefen om ze op te pikken.
Breng ze naar het HUIS om punten te scoren!
Maar pas op: politieauto's proberen jou te rammen.

Besturing:
  Pijltoetsen of WASD  =  rijden
  ENTER                =  opnieuw spelen (na game over)
"""

import arcade
import random
import math

# -----------------------------------------------
# Instellingen van het scherm
# -----------------------------------------------
VENSTER_BREEDTE = 900
VENSTER_HOOGTE = 700
VENSTER_TITEL = "Boeven Redden!"

# -----------------------------------------------
# Instellingen van de spelersauto
# -----------------------------------------------
SPELER_SNELHEID = 4        # pixels per frame
SPELER_BREEDTE = 28
SPELER_HOOGTE = 44
MAX_LEVENS = 5             # hoeveel keer mag je geraakt worden

# -----------------------------------------------
# Instellingen van de politieauto's
# -----------------------------------------------
POLITIE_BREEDTE = 26
POLITIE_HOOGTE = 40
POLITIE_START_SNELHEID = 2.0   # beginsnelheid
POLITIE_MAX_SNELHEID = 5.5     # maximale snelheid
POLITIE_START_INTERVAL = 12.0  # seconden tussen nieuwe politieauto's
POLITIE_MIN_INTERVAL = 3.0     # zo snel spawn je ze minimaal

# -----------------------------------------------
# Instellingen van de boefen
# -----------------------------------------------
BOEF_STRAAL = 14
AANTAL_BOEFEN = 8  # hoeveel boefen staan er tegelijk op de kaart

# -----------------------------------------------
# Het huis (waar je de boefen naartoe brengt)
# -----------------------------------------------
HUIS_X = 100
HUIS_Y = 100
HUIS_BREEDTE = 80
HUIS_HOOGTE = 80

# -----------------------------------------------
# Spelstatus
# -----------------------------------------------
STATUS_SPELEN = "spelen"
STATUS_GAME_OVER = "game_over"

# Hoe lang ben je onkwetsbaar na een botsing?
SCHADE_PAUZE = 1.5  # seconden


class BoevenRedden(arcade.Window):
    """Het hoofdvenster van het spel."""

    def __init__(self):
        # Maak het venster aan
        super().__init__(VENSTER_BREEDTE, VENSTER_HOOGTE, VENSTER_TITEL)
        arcade.set_background_color(arcade.color.DARK_GREEN)
        # Begin meteen met het spel
        self.setup()

    def setup(self):
        """Zet alles klaar voor een nieuwe ronde."""

        # Positie en eigenschappen van de speler
        self.speler_x = float(VENSTER_BREEDTE // 2)
        self.speler_y = float(VENSTER_HOOGTE // 2)
        self.speler_levens = MAX_LEVENS
        self.boefen_mee = 0    # hoeveel boefen heb je opgepikt?
        self.score = 0

        # Welke toetsen worden ingedrukt? (True = ingedrukt)
        self.toets_omhoog = False
        self.toets_omlaag = False
        self.toets_links = False
        self.toets_rechts = False

        # Boefen op de kaart: elk item is een (x, y) paar
        self.boefen = []
        for _ in range(AANTAL_BOEFEN):
            self.voeg_boef_toe()

        # Politieauto's: elk item is een woordenboek met x en y
        self.politie = []

        # Timers
        self.politie_timer = 0.0   # telt af tot de volgende politieauto
        self.schade_timer = 0.0    # telt af na een botsing (onkwetsbaar)

        # Spelstatus
        self.status = STATUS_SPELEN

    # --------------------------------------------------
    # Hulpfuncties
    # --------------------------------------------------

    def voeg_boef_toe(self):
        """Voeg een boef toe op een willekeurige plek, ver van het huis."""
        for _ in range(200):  # probeer maximaal 200 keer
            x = random.randint(60, VENSTER_BREEDTE - 60)
            y = random.randint(60, VENSTER_HOOGTE - 60)
            # Zet hem niet te dicht bij het huis
            ver_van_huis = math.hypot(x - HUIS_X, y - HUIS_Y) > 110
            # Zet hem niet te dicht bij de speler
            ver_van_speler = math.hypot(x - self.speler_x, y - self.speler_y) > 90
            if ver_van_huis and ver_van_speler:
                self.boefen.append((x, y))
                return

    def spawn_politie(self):
        """Laat een nieuwe politieauto aan de rand van het scherm verschijnen."""
        kant = random.randint(0, 3)
        if kant == 0:    # bovenkant
            x = random.randint(0, VENSTER_BREEDTE)
            y = VENSTER_HOOGTE + 30
        elif kant == 1:  # rechterkant
            x = VENSTER_BREEDTE + 30
            y = random.randint(0, VENSTER_HOOGTE)
        elif kant == 2:  # onderkant
            x = random.randint(0, VENSTER_BREEDTE)
            y = -30
        else:            # linkerkant
            x = -30
            y = random.randint(0, VENSTER_HOOGTE)
        self.politie.append({'x': float(x), 'y': float(y)})

    # --------------------------------------------------
    # Spellogica (wordt 60x per seconde uitgevoerd)
    # --------------------------------------------------

    def on_update(self, delta_time):
        """Bewerk het spel: beweeg alles, controleer botsingen."""
        if self.status != STATUS_SPELEN:
            return

        # --- Beweeg de speler op basis van ingedrukte toetsen ---
        if self.toets_omhoog:
            self.speler_y += SPELER_SNELHEID
        if self.toets_omlaag:
            self.speler_y -= SPELER_SNELHEID
        if self.toets_links:
            self.speler_x -= SPELER_SNELHEID
        if self.toets_rechts:
            self.speler_x += SPELER_SNELHEID

        # Blijf binnen de randen van het scherm
        self.speler_x = max(SPELER_BREEDTE // 2,
                            min(VENSTER_BREEDTE - SPELER_BREEDTE // 2, self.speler_x))
        self.speler_y = max(SPELER_HOOGTE // 2,
                            min(VENSTER_HOOGTE - SPELER_HOOGTE // 2, self.speler_y))

        # --- Schade timer: telt omlaag, zodat je niet steeds schade krijgt ---
        if self.schade_timer > 0:
            self.schade_timer -= delta_time

        # --- Beweeg elke politieauto richting de speler ---
        # Hoe hoger je score, hoe sneller de politie!
        politie_snelheid = min(
            POLITIE_START_SNELHEID + self.score * 0.15,
            POLITIE_MAX_SNELHEID
        )
        for p in self.politie:
            dx = self.speler_x - p['x']
            dy = self.speler_y - p['y']
            afstand = math.hypot(dx, dy)
            if afstand > 1:
                p['x'] += (dx / afstand) * politie_snelheid
                p['y'] += (dy / afstand) * politie_snelheid

        # --- Controleer of de speler een boef aanraakt ---
        boefen_over = []
        for boef in self.boefen:
            afstand = math.hypot(self.speler_x - boef[0], self.speler_y - boef[1])
            # Raak je de boef? Dan pak je hem op!
            if afstand < SPELER_BREEDTE // 2 + BOEF_STRAAL:
                self.boefen_mee += 1
            else:
                boefen_over.append(boef)
        self.boefen = boefen_over

        # Als alle boefen opgepikt zijn, zet nieuwe boefen neer
        if len(self.boefen) == 0:
            for _ in range(AANTAL_BOEFEN):
                self.voeg_boef_toe()

        # --- Controleer of de speler bij het huis is met boefen ---
        afstand_huis = math.hypot(self.speler_x - HUIS_X, self.speler_y - HUIS_Y)
        bereik_huis = HUIS_BREEDTE // 2 + SPELER_BREEDTE // 2
        if afstand_huis < bereik_huis and self.boefen_mee > 0:
            # Lever alle boefen af en verdien punten!
            self.score += self.boefen_mee
            self.boefen_mee = 0

        # --- Controleer of politie de speler ramt ---
        if self.schade_timer <= 0:
            for p in self.politie:
                afstand = math.hypot(self.speler_x - p['x'], self.speler_y - p['y'])
                raak_breedte = SPELER_BREEDTE // 2 + POLITIE_BREEDTE // 2
                if afstand < raak_breedte:
                    self.speler_levens -= 1
                    self.schade_timer = SCHADE_PAUZE  # even onkwetsbaar
                    if self.speler_levens <= 0:
                        self.status = STATUS_GAME_OVER
                    break  # maar één botsing per moment

        # --- Laat periodiek nieuwe politieauto's verschijnen ---
        self.politie_timer += delta_time
        # Hoe meer score, hoe sneller er politie bijkomt
        politie_interval = max(
            POLITIE_MIN_INTERVAL,
            POLITIE_START_INTERVAL - self.score * 0.4
        )
        if self.politie_timer >= politie_interval:
            self.politie_timer = 0.0
            self.spawn_politie()

    # --------------------------------------------------
    # Tekenen (wordt 60x per seconde uitgevoerd)
    # --------------------------------------------------

    def on_draw(self):
        """Teken alles op het scherm."""
        self.clear()

        # Teken altijd de spelwereld
        self._teken_wereld()

        # Als het game over is, teken het game over scherm erbovenop
        if self.status == STATUS_GAME_OVER:
            self._teken_game_over()

    def _teken_wereld(self):
        """Teken de kaart, boefen, politie en de speler."""

        # --- Teken het huis ---
        arcade.draw_rectangle_filled(HUIS_X, HUIS_Y, HUIS_BREEDTE, HUIS_HOOGTE,
                                     arcade.color.YELLOW_GREEN)
        arcade.draw_rectangle_outline(HUIS_X, HUIS_Y, HUIS_BREEDTE, HUIS_HOOGTE,
                                      arcade.color.DARK_GREEN, 3)
        # Dak van het huis (driehoek)
        arcade.draw_triangle_filled(
            HUIS_X - 45, HUIS_Y + 40,
            HUIS_X + 45, HUIS_Y + 40,
            HUIS_X, HUIS_Y + 75,
            arcade.color.BROWN
        )
        arcade.draw_text("THUIS", HUIS_X, HUIS_Y - 8,
                         arcade.color.BLACK, 12, bold=True, anchor_x="center")

        # --- Teken de boefen (oranje cirkels met een B) ---
        for boef in self.boefen:
            arcade.draw_circle_filled(boef[0], boef[1], BOEF_STRAAL, arcade.color.ORANGE)
            arcade.draw_circle_outline(boef[0], boef[1], BOEF_STRAAL, (180, 80, 0), 2)
            arcade.draw_text("B", boef[0], boef[1] - 6,
                             arcade.color.BLACK, 12, bold=True, anchor_x="center")

        # --- Teken de politieauto's (rode rechthoeken) ---
        for p in self.politie:
            # Carrosserie
            arcade.draw_rectangle_filled(p['x'], p['y'], POLITIE_BREEDTE, POLITIE_HOOGTE,
                                         arcade.color.RED)
            # Zwaailicht (blauw blokje bovenop)
            arcade.draw_rectangle_filled(p['x'], p['y'] + POLITIE_HOOGTE // 2 - 4,
                                         14, 8, arcade.color.BLUE)
            arcade.draw_text("P", p['x'], p['y'] - 7,
                             arcade.color.WHITE, 12, bold=True, anchor_x="center")

        # --- Teken de spelersauto (blauwe rechthoek) ---
        # Knippert als je net geraakt bent (onkwetsbaar effect)
        zichtbaar = self.schade_timer <= 0 or int(self.schade_timer * 6) % 2 == 0
        if zichtbaar:
            arcade.draw_rectangle_filled(self.speler_x, self.speler_y,
                                         SPELER_BREEDTE, SPELER_HOOGTE,
                                         arcade.color.BLUE)
            # Voorruit
            arcade.draw_rectangle_filled(self.speler_x, self.speler_y + 8,
                                         20, 12, (173, 216, 230))
            arcade.draw_text("J", self.speler_x, self.speler_y - 9,
                             arcade.color.WHITE, 12, bold=True, anchor_x="center")

        # --- Teken de HUD (score, boefen mee, levensbalk) ---
        self._teken_hud()

    def _teken_hud(self):
        """Teken de informatiebalk bovenaan het scherm."""

        # Donkere achtergrond voor de balk
        arcade.draw_rectangle_filled(VENSTER_BREEDTE // 2, VENSTER_HOOGTE - 18,
                                     VENSTER_BREEDTE, 36, (0, 0, 0, 180))

        # Score (links)
        arcade.draw_text(f"Score: {self.score}", 10, VENSTER_HOOGTE - 28,
                         arcade.color.WHITE, 16, bold=True)

        # Hoeveel boefen heb je bij je? (midden)
        arcade.draw_text(f"Boefen bij je: {self.boefen_mee}",
                         VENSTER_BREEDTE // 2, VENSTER_HOOGTE - 28,
                         arcade.color.ORANGE, 16, bold=True, anchor_x="center")

        # Levensbalk (rechts)
        balk_breedte = 160
        balk_hoogte = 16
        balk_x = VENSTER_BREEDTE - balk_breedte - 10
        balk_y = VENSTER_HOOGTE - 24

        # Achtergrond van de levensbalk (donkerrood)
        arcade.draw_rectangle_filled(balk_x + balk_breedte // 2, balk_y,
                                     balk_breedte, balk_hoogte, arcade.color.DARK_RED)

        # Gevuld gedeelte van de levensbalk (groen of rood als laag)
        gevuld = int((self.speler_levens / MAX_LEVENS) * balk_breedte)
        if gevuld > 0:
            kleur = arcade.color.GREEN if self.speler_levens > 2 else (220, 80, 0)
            arcade.draw_rectangle_filled(balk_x + gevuld // 2, balk_y,
                                         gevuld, balk_hoogte, kleur)

        arcade.draw_text("Auto:", balk_x - 44, balk_y - 8,
                         arcade.color.WHITE, 11)

    def _teken_game_over(self):
        """Teken het game over scherm."""

        # Donkere overlay over het spel
        arcade.draw_rectangle_filled(VENSTER_BREEDTE // 2, VENSTER_HOOGTE // 2,
                                     VENSTER_BREEDTE, VENSTER_HOOGTE, (0, 0, 0, 190))

        # Grote tekst: GAME OVER
        arcade.draw_text("GAME OVER!",
                         VENSTER_BREEDTE // 2, VENSTER_HOOGTE // 2 + 90,
                         arcade.color.RED, 60, bold=True, anchor_x="center")

        # Hoeveel boefen heb je gered?
        arcade.draw_text(f"Je hebt {self.score} boefen thuisgebracht!",
                         VENSTER_BREEDTE // 2, VENSTER_HOOGTE // 2 + 20,
                         arcade.color.WHITE, 26, anchor_x="center")

        # Instructie om opnieuw te spelen
        arcade.draw_text("Druk op ENTER om opnieuw te spelen",
                         VENSTER_BREEDTE // 2, VENSTER_HOOGTE // 2 - 60,
                         arcade.color.YELLOW, 20, anchor_x="center")

    # --------------------------------------------------
    # Toetsen
    # --------------------------------------------------

    def on_key_press(self, key, modifiers):
        """Wordt aangeroepen als je een toets indrukt."""

        # Op game over scherm: ENTER = opnieuw beginnen
        if self.status == STATUS_GAME_OVER:
            if key == arcade.key.ENTER:
                self.setup()
            return

        # Rijden
        if key in (arcade.key.UP, arcade.key.W):
            self.toets_omhoog = True
        if key in (arcade.key.DOWN, arcade.key.S):
            self.toets_omlaag = True
        if key in (arcade.key.LEFT, arcade.key.A):
            self.toets_links = True
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.toets_rechts = True

    def on_key_release(self, key, modifiers):
        """Wordt aangeroepen als je een toets loslaat."""
        if key in (arcade.key.UP, arcade.key.W):
            self.toets_omhoog = False
        if key in (arcade.key.DOWN, arcade.key.S):
            self.toets_omlaag = False
        if key in (arcade.key.LEFT, arcade.key.A):
            self.toets_links = False
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.toets_rechts = False


# -----------------------------------------------
# Start het spel
# -----------------------------------------------
def main():
    """Maak het spelvenster aan en start de game loop."""
    BoevenRedden()
    arcade.run()


if __name__ == "__main__":
    main()
