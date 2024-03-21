"""
Authors: Killian Nucci, Damien Touati
"""

import sys
from enums import PawnType
from pawn import Pawn


class BoardLoader():
    path: str
    width: int
    height: int
    pawns: list[list[Pawn]]
    sheeps: dict

    def __init__(self, path: str) -> None:
        self.path = path
        grid = self.load_board()
        self.setup_pawn(grid)
        self.width = len(grid[0])
        self.height = len(grid)

    def load_board(self) -> list:
        """
        Récupère la map et la met en liste
        """
        try:
            file = open(f"./maps/{self.path}", "r")
        except:
            print("This map doesn't exist")
            sys.exit(1)
        board = file.readlines()
        file.close()
        for i in range(len(board)):
            board[i] = board[i].rstrip('\n')
        return board

    def setup_pawn(self, grid: list[str]):
        """
        Initialisation des pions

        param grid: grille de jeu
        """
        self.pawns = []
        self.sheeps = {}
        for y in range(len(grid)):
            line = []
            for x in range(len(grid[0])):
                element = grid[y][x]
                pawn_type = PawnType.NONE
                if element == "S":
                    pawn_type = PawnType.SHEEP
                    self.sheeps[(x,y)]=Pawn((x, y), pawn_type)
                    line.append(Pawn((x, y), PawnType.NONE))
                    continue
                if element == "B":
                    pawn_type = PawnType.BUSH
                if element == "G":
                    pawn_type = PawnType.GRASS
                line.append(Pawn((x, y), pawn_type))
            self.pawns.append(line)