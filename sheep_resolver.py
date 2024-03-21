"""
Authors: Killian Nucci, Damien Touati
"""

from enums import *
from pawn import Pawn

class SheepResolver():
    
    width: int
    height: int
    pawns: list[list]
    sheeps: dict
    sheeps_resolved: dict

    def __init__(self, width: int , height: int, pawns: Pawn, sheeps: Pawn):
        self.width = width
        self.height = height
        self.pawns = pawns
        self.sheeps = sheeps

    def resolve(self, commande: Commandes):
        """
        Va exécuter la bonne commande pour le déplacement et modifier les coordonnées des moutons en fonction des déplacement
        """
        self.sheeps_resolved = {}
        if commande == Commandes.UP:
            self.resolve_up()
        if commande == Commandes.DOWN:
            self.resolve_down()
        if commande == Commandes.LEFT:
            self.resolve_left()
        if commande == Commandes.RIGHT:
            self.resolve_right()
        self.resolve_sheep_grass()
        self.sheeps = self.sheeps_resolved.copy()
        

    def resolve_up(self):
        """
        Si déplacement en haut
        """
        for sheep in self.sheeps.values():
            self.resolve_v(sheep,-1)

    def resolve_down(self):
        """
        Si déplacement en bas
        """
        for sheep in self.sheeps.values():
            self.resolve_v(sheep,1)

    def resolve_left(self):
        """
        Si déplacement a gauche
        """
        for sheep in self.sheeps.values():
            self.resolve_h(sheep,-1)

    def resolve_right(self):
        """
        Si déplacement a droite
        """
        for sheep in self.sheeps.values():
                self.resolve_h(sheep,1)
 

    
    def resolve_v(self, sheep:Pawn, direction:int):
        """
        Pour déplacemenet horizontal

        :param sheep: mouton à déplacer
        :param direction: incrément pour la direction
        """
        if sheep == None or self.sheeps_resolved.get(sheep.position) != None:
            return
        sheep_x = sheep.position[0]
        sheep_y = sheep.position[1]
        current = sheep_y
        while (current+direction >= 0 and current+direction < self.height):
            current += direction
            current_pawn = self.pawns[current][sheep_x]
            other_sheep = self.is_sheep_here(sheep_x,current)
            if current_pawn.type == PawnType.BUSH:
                self.sheeps[sheep.position] = None
                sheep.position = (sheep_x,current_pawn.position[1]-direction)
                self.sheeps_resolved[sheep.position] = sheep
                return
            if other_sheep != None and other_sheep.position !=  sheep.position:
                self.resolve_v(other_sheep, direction)
                self.sheeps[sheep.position] = None
                sheep.position = (sheep_x,other_sheep.position[1]-direction)
                self.sheeps_resolved[sheep.position] = sheep
                return
    
        self.sheeps[sheep.position] = None
        sheep.position = (sheep_x,current)
        self.sheeps_resolved[sheep.position] = sheep

    def resolve_h(self, sheep:Pawn, direction:int):
        """
        Pour déplacemenet vertical

        :param sheep: mouton à déplacer
        :param direction: incrément pour la direction
        """
        if sheep == None or self.sheeps_resolved.get(sheep.position) != None:
            return
        sheep_x = sheep.position[0]
        sheep_y = sheep.position[1]
        current = sheep_x
        while (current+direction >= 0 and current+direction < self.width):
            current += direction
            current_pawn = self.pawns[sheep_y][current]
            other_sheep = self.is_sheep_here(current,sheep_y)
            if current_pawn.type == PawnType.BUSH:
                self.sheeps[sheep.position] = None
                sheep.position = (current_pawn.position[0]-direction,sheep_y)
                self.sheeps_resolved[sheep.position] = sheep
                return
            if other_sheep != None and other_sheep.position !=  sheep.position:
                self.resolve_h(other_sheep,direction)
                self.sheeps[sheep.position] = None
                sheep.position = (other_sheep.position[0]-direction,sheep_y)
                self.sheeps_resolved[sheep.position] = sheep
                return
        self.sheeps[sheep.position] = None
        sheep.position = (current,sheep_y)
        self.sheeps_resolved[sheep.position] = sheep
        
    def resolve_sheep_grass(self):
        """
        Regarde si un mouton est sur une case d'herbe
        """
        for col in self.pawns:
            for pawn in col:
                if pawn.type == PawnType.GRASS and self.sheeps_resolved.get(pawn.position) != None:
                    pawn.type = PawnType.SHEEP_GRASS
                if pawn.type == PawnType.SHEEP_GRASS and self.sheeps_resolved.get(pawn.position) == None:
                    pawn.type = PawnType.GRASS

    def is_sheep_here(self,x:int,y:int) -> Pawn:
        """
        regarde si il y a un mouton sur la case

        :param x: abscisse 
        :param y: ordonné

        :return: le mouton en question
        """
        if self.sheeps.get((x,y)) != None:
            return self.sheeps.get((x,y))
        return self.sheeps_resolved.get((x,y))

