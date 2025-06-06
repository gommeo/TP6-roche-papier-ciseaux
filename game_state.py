"""
Oscar Gomme
class pour les game states
"""


from enum import Enum


class GameState(Enum):
    NOT_STARTED = 0
    ROUND_ACTIVE = 1
    ROUND_DONE = 2
    GAME_OVER = 3


class RoundWinner(Enum):
    ORDINATEUR = 0
    JOUEUR = 1
    EGALITE = 2
