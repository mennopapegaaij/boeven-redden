# 🚗 Boeven Redden!

Een Python-spel gemaakt met [Arcade 3](https://api.arcade.academy/).

## Hoe werkt het spel?
- Je rijdt als boef in een auto over de kaart (van bovenaf)
- Op de kaart staan andere boefen - rij er tegenaan om ze te redden
- Breng ze naar het huis op de kaart om punten te scoren
- Politieauto's achtervolgen jou en proberen jouw auto te slopen
- Je auto heeft een levensbalk - als die op nul is, is het game over
- Er staan nu ook huizen op de kaart waar je niet doorheen kunt rijden
- Er zijn wegen en op de weg rijdt jouw auto sneller
- De map is nu veel groter en het scherm schuift mee als je naar de rand rijdt
- Het spel gaat eindeloos door, maar er komt steeds meer politie!

## Starten
Zorg dat je Python 3 hebt, en installeer de benodigde pakketten:

```bash
pip install -r requirements.txt
```

Start het spel:
```bash
python spel.py
```

## Nieuwe mapstructuur
De code is nu opgesplitst in kleine bestanden:

- `spel.py` - start alleen het spel
- `boeven_redden/instellingen.py` - vaste getallen
- `boeven_redden/modellen.py` - simpele data-klassen
- `boeven_redden/wereld.py` - wereld en spawnplekken
- `boeven_redden/ai.py` - politie-AI
- `boeven_redden/spel_logica.py` - spelregels
- `boeven_redden/venster.py` - tekenen en toetsen

Dat maakt latere uitbreidingen makkelijker, zoals:
- muren en wegen
- slimmere politie
- botsende auto's

## Gemaakt door
Menno 🎮
