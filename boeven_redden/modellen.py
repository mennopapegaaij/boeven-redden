"""Kleine bouwstenen van het spel."""

from dataclasses import dataclass


@dataclass
class Auto:
    """Een simpele auto met een plek en formaat."""

    x: float
    y: float
    breedte: int
    hoogte: int


@dataclass
class SpelerAuto(Auto):
    """De auto van de speler."""

    levens: int


@dataclass
class PolitieAuto(Auto):
    """Een politieauto die de speler achterna zit."""


@dataclass
class Boef:
    """Een boef die je kunt oppikken."""

    x: float
    y: float


@dataclass
class Huis:
    """De plek waar boefen thuis worden gebracht."""

    x: float
    y: float
    breedte: int
    hoogte: int


@dataclass
class Weg:
    """Een rechthoekig stuk weg."""

    x: float
    y: float
    breedte: int
    hoogte: int


@dataclass
class InvoerStatus:
    """Welke rijtoetsen nu zijn ingedrukt."""

    omhoog: bool = False
    omlaag: bool = False
    links: bool = False
    rechts: bool = False
