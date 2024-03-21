"""
Authors: Killian Nucci, Damien Touati
"""

from enum import Enum
class Commandes(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    EXIT = 5
    SOLVER = 6
    SOLVER_M = 7
    UNDO = 8

class PawnType(Enum):
    SHEEP = 1
    BUSH = 2
    GRASS = 3
    NONE = 4
    SHEEP_GRASS = 5