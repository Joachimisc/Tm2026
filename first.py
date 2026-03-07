class Tuile :
    def __init__(self,nord,est,sud,ouest):
        self.nord = nord
        self.est = est
        self.sud = sud
        self.ouest = ouest
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
pioche = [tuile1,tuile2,tuile3,tuile4,tuile5,tuile6,tuile6,tuile7,tuile8,tuile9,tuile10]
