"""
Authors: Killian Nucci, Damien Touati
"""

from fltk import *
from pawn import Pawn
from enums import *
from sheep_resolver import SheepResolver
import copy
import time

class Board():
    pawns: list[list]
    sheeps: dict
    commande = ["Up", "Down", "Left", "Right"]
    width: int
    height: int
    background_color = "#969999"
    cell_size_pixel = 100
    theme: str
    history = []

    def __init__(self, pawns_list: list[list[Pawn]], sheeps:list[Pawn],width: int, height: int, theme: str):
        self.pawns = pawns_list
        self.sheeps = sheeps
        self.width = width
        self.height = height
        self.theme = theme

    def width_pixel(self) -> int:
        """
        conversion longueur en pixel

        return: longueur pixel
        """
        return self.width*self.cell_size_pixel

    def height_pixel(self) -> int:
        """
        conversion hauteur en pixel

        return: hauteur pixel
        """
        return self.height*self.cell_size_pixel

    def play(self):
        """
        fonction principal qui va géré le jeu
        """
        cree_fenetre(self.width_pixel(), self.height_pixel())
        self.draw_board()
        while self.is_grass_left(): #and self.is_loose(): #A ne pas activer sur les grandes map car trop long entre chaque coup
            resolver = SheepResolver(self.width, self.height, self.pawns, self.sheeps)
            ev = attend_ev()
            tev = type_ev(ev)
            if tev == "Quitte":
                ferme_fenetre()
                break
            if tev == "Touche":
                commande = Board.get_command(touche(ev))
                if commande == Commandes.EXIT:
                    ferme_fenetre()
                    break
                elif commande == Commandes.SOLVER:
                    moves = self.solver()
                    print(moves)
                    if moves:
                        self.play_commands(resolver, moves)
                elif commande == Commandes.SOLVER_M:
                    print(self.solver_m(state = self.sheeps.keys()))
                elif commande == Commandes.UNDO:
                    self.undo()
                elif commande != None:
                    self.history.append((copy.deepcopy(self.pawns),copy.deepcopy(self.sheeps)))
                    resolver.resolve(commande)
                    self.pawns = resolver.pawns
                    self.sheeps = resolver.sheeps
            efface_tout()
            self.draw_board()
            mise_a_jour()
        if not self.is_grass_left():
            rectangle(self.width_pixel()*(1/8),self.height_pixel()*(2/5), self.width_pixel()*(7/8), self.height_pixel()*(3/5),couleur='black',remplissage='white')
            texte(self.width_pixel()/2,self.height_pixel()/2, "You win !!!!", couleur="green", ancrage="center")
            mise_a_jour()
            attend_ev()
        

    def draw_board(self):
        """
        fonction pour dessiner le plateau de jeu
        """
        x= 0
        y = 0
        rectangle(0, 0, self.width_pixel(), self.height_pixel(),
                  remplissage=self.background_color, epaisseur=0)
        for i in range(self.width):
            x = i*self.cell_size_pixel
            ligne(x, 0, x, self.height*self.cell_size_pixel)
        for i in range(self.height):
            y = i*self.cell_size_pixel
            ligne(0, y, self.width_pixel(), y)
        for col in self.pawns:
            for row in col:
                self.draw_pawn(row)
        for sheep in self.sheeps.values():
            if self.pawns[sheep.position[1]][sheep.position[0]].type != PawnType.SHEEP_GRASS:
                self.draw_pawn(sheep)

    def get_command(touche: str) -> Commandes:
        """
        fonction pour récupéré la commande faite par le joueur

        :return: une commande
        """
        if touche == "Up":
            return Commandes.UP
        if touche == "Down":
            return Commandes.DOWN
        if touche == "Left":
            return Commandes.LEFT
        if touche == "Right":
            return Commandes.RIGHT
        if touche == "Escape":
            return Commandes.EXIT
        if touche == "s":
            return Commandes.SOLVER
        if touche == "m":
            return Commandes.SOLVER_M
        if touche == "u":
            return Commandes.UNDO
        return None

    def draw_pawn(self, pawn: Pawn):
        """
        fonction pour dessiner les pions aux bons endroits

        param pawn: pion à dessiner
        """
        y = pawn.position[1]*self.cell_size_pixel + self.cell_size_pixel/2
        x = pawn.position[0]*self.cell_size_pixel + self.cell_size_pixel/2
        if pawn.type != PawnType.NONE:
            image(x, y, self.search_image(pawn.type))
        #texte(x-self.cell_size_pixel/2,y-self.cell_size_pixel/2,f'({pawn.position[0]},{pawn.position[1]})')
 
    def search_image(self, pawn_type: PawnType) -> str:
        """
        fonction pour trouver l'image correspondant au pion dessiner

        param pawn_type: type du pion
        return: chemin du fichier correspondant à l'image du pion à afficher
        """
        if pawn_type == pawn_type.GRASS:
            return f"./media/{self.theme}/grass.png"
        if pawn_type == pawn_type.SHEEP:
            return f"./media/{self.theme}/sheep.png"
        if pawn_type == pawn_type.BUSH:
            return f"./media/{self.theme}/bush.png"
        if pawn_type == pawn_type.SHEEP_GRASS:
            return f"./media/{self.theme}/sheep_grass.png"

    def is_grass_left(self) -> bool:
        """
        fonction qui va decider si une partie est gagnée ou non

        return: si partie est gagné ou non
        """
        for col in self.pawns:
            for row in col:
                if row.type == PawnType.GRASS:
                    return True
        return False

    def solver(self, visite = set()) -> list[str]:
        """
        cherche une solution pour la partie en cours

        :param visite: previous position
        :return: la solution
        """
        current_pawns = copy.deepcopy(self.pawns) #Utilisation du deepcopy, car .copy() ne copie seulement que la référence de l'objet et non l'objet en lui même
        current_sheeps = copy.deepcopy(self.sheeps)
        if not self.is_grass_left():
            return []
        if str(self.sheeps.keys()) in visite:
            return None
        else:
            visite.add(str(self.sheeps.keys()))
            for direction in self.commande:
                resolver = SheepResolver(self.width, self.height,copy.deepcopy(current_pawns), copy.deepcopy(current_sheeps))
                resolver.resolve(Board.get_command(direction))
                self.pawns = resolver.pawns
                self.sheeps = resolver.sheeps
                solution = self.solver(visite)
                if solution is not None:
                    return [direction]+solution
                self.pawns = current_pawns
                self.sheeps = current_sheeps
    
        
    def play_commands(self, resolver: SheepResolver,commandes: list[str]):
        """
        joue la solution du solver

        :param resolver: classe pour résoudre les déplacement des moutons
        :param commandes: la solution 
        """
        for commande in commandes:
            resolver.resolve(Board.get_command(commande))
            self.pawns = resolver.pawns
            self.sheeps = resolver.sheeps
            efface_tout()
            self.draw_board()
            mise_a_jour()
            time.sleep(.3)

    def is_loose(self) -> bool:
        """
        regarde si le joueur est dans une position perdante

        :return: bool
        """
        if self.solver() == None:
            rectangle(self.width_pixel()*(1/8),self.height_pixel()*(2/5), self.width_pixel()*(7/8), self.height_pixel()*(3/5),couleur='black',remplissage='white')
            texte(self.width_pixel()/2,self.height_pixel()/2, "You loose :(", couleur="red", ancrage="center")
            mise_a_jour()
            attend_ev()
            return False
        return True

    def undo(self):
        """
        retourne a la position précédente 
        """
        if len(self.history) >= 1:
            self.pawns = copy.deepcopy(self.history[-1][0])
            self.sheeps = copy.deepcopy(self.history[-1][1])
            self.history.pop(-1)


                




        
