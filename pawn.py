"""
Authors: Killian Nucci, Damien Touati
"""

from enums import PawnType


class Pawn():
    position: tuple
    type: PawnType

    def __init__(self, position: tuple[int, int], type: PawnType):
        self.position = position
        self.type = type


