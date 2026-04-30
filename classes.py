import random

class Tuile :
    def __init__(self,nord,est,sud,ouest):
        self.nord = nord
        self.est = est
        self.sud = sud
        self.ouest = ouest

    def __repr__(self):
        return f"Tuile({self.nord},{self.est},{self.sud},{self.ouest})"
    
    def tourner(self):
        self.nord, self.est, self.sud, self.ouest = self.ouest, self.nord, self.est, self.sud

class Plateau : 
    def __init__(self) :
        self.tuiles = {}

    def voisins(self, x, y):
        return {
            "nord": self.tuiles.get((x, y+1)),
            "sud": self.tuiles.get((x, y-1)),
            "est": self.tuiles.get((x+1, y)),
            "ouest": self.tuiles.get((x-1, y))
        }
    
    def validation(self,tuile,x,y) :
        voisins = self.voisins(x,y)
        if voisins["nord"] is None and voisins["sud"] is None and voisins["est"] is None and voisins["ouest"] is None:
            return False
        if (x,y) in self.tuiles:
            return False
        if voisins["nord"] and voisins["nord"].sud != tuile.nord:
            return False
        if voisins["sud"] and voisins["sud"].nord != tuile.sud:
            return False
        if voisins["est"] and voisins["est"].ouest != tuile.est:
            return False
        if voisins["ouest"] and voisins["ouest"].est != tuile.ouest:
            return False
        return True
    
    def placement(self,tuile,x,y) :
        if self.validation(tuile,x,y) :
            self.tuiles[(x,y)] = tuile
            return True
        return False 
class Joueur :

    def __init__(self,nom) :
        self.nom = nom
        self.score = 0
class Jeu :

    def __init__(self,joueurs,pioche) :
        self.joueurs = joueurs
        self.pioche = pioche
        self.index_joueur = 0

    def jouer_tour(self,plateau) :
        joueur = self.joueurs[self.index_joueur]
        print(f"Tour de {joueur.nom}")  
        if not self.pioche :
            return False
        print(plateau.tuiles)
        tuile_joueur = self.pioche.pop()
        print("Voici votre tuile :",tuile_joueur)
        rotation = int(input("Tournez la tuile de 90°(1,2,3 fois) :"))
        for i in range(rotation) :
            tuile_joueur.tourner()
        while True :
            x = int(input("Entrez une coordonnée x :"))
            y = int(input("Entrez une coordonnée y :"))
            if plateau.placement(tuile_joueur,x,y) :
                print("Tuile placée !")
                break
            else :
                print("Placement non valide, réessayez.")
        self.changer_joueur()
        return True
    
    def changer_joueur(self) :
        self.index_joueur = (self.index_joueur + 1)% len(self.joueurs)

    def deroulement_partie(self,plateau) :
        random.shuffle(self.pioche)
        plateau.tuiles[(0,0)] = self.pioche.pop()
        while self.pioche :
            continuer = self.jouer_tour(plateau)
            if not continuer :
                break
        print("Partie terminée !")