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
        self.nord, self.est, self.sud, self.ouest = \
        self.ouest, self.nord, self.est, self.sud
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
#V pour ville, P pour prairie, R pour route
tuile1 = Tuile("V","V","P","P")
tuile2 = Tuile("V","R","P","R")
tuile3 = Tuile("P","R","P","R")
tuile4 = Tuile("R","P","R","P")
tuile5 = Tuile("V","P","V","P")
tuile6 = Tuile("P","V","P","V")
tuile7 = Tuile("R","R","P","P")
tuile8 = Tuile("P","R","R","P")
tuile9 = Tuile("V","R","V","P")
tuile10 = Tuile("P","P","R","P")
pioche = [tuile1,tuile2,tuile3,tuile4,tuile5,tuile6,tuile7,tuile8,tuile9,tuile10]

random.shuffle(pioche)
plateau = Plateau()
plateau.placement(pioche.pop(),0,0)
while pioche :
    print(plateau.tuiles)
    tuile_joueur=pioche.pop()
    print("Voici votre tuile :",tuile_joueur.nord,tuile_joueur.est,tuile_joueur.sud,tuile_joueur.ouest)
    rotation = int(input("Tournez la tuile de 90°(1,2,3 fois) :"))
    for i in range(rotation) :
        tuile_joueur.tourner()
    x = int(input("Entrez une coordonnée x :"))
    y = int(input("Entrez une coordonnée y :"))
    if plateau.placement(tuile_joueur,x,y) :
        print("Tuile placée !")
    else :
        print("Placement non valide.")