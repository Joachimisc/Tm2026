import affichage

class Tuile :

    def __init__(self, nord, est, sud, ouest):
        self.nord = nord
        self.est = est
        self.sud = sud
        self.ouest = ouest

    def __repr__(self):
        return f"Tuile({self.nord},{self.est},{self.sud},{self.ouest})"

    def tourner(self):
        self.nord, self.est, self.sud, self.ouest = (
            self.ouest,
            self.nord,
            self.est,
            self.sud
        )

class Plateau :

    def __init__(self):
        self.tuiles = {}

    def voisins(self, x, y):
        return {
            "nord": self.tuiles.get((x, y + 1)),
            "sud": self.tuiles.get((x, y - 1)),
            "est": self.tuiles.get((x + 1, y)),
            "ouest": self.tuiles.get((x - 1, y))
        }

    def validation(self, tuile, x, y):
        voisins = self.voisins(x, y)

        if (x, y) in self.tuiles:
            return False
        if (voisins["nord"] is None and
            voisins["sud"] is None and
            voisins["est"] is None and
            voisins["ouest"] is None):
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

    def placement(self, tuile, x, y):
        if self.validation(tuile, x, y):

            self.tuiles[(x, y)] = tuile
            return True
        return False

class Joueur :
    def __init__(self, nom):
        self.nom = nom
        self.score = 0
    def __repr__(self):
        return f"Joueur({self.nom}, score={self.score})"

class Jeu :

    def __init__(self, joueurs, pioche):
        self.joueurs = joueurs
        self.pioche = pioche
        self.index_joueur = 0

    def __repr__(self):
        return f"Jeu(joueurs={self.joueurs}, pioche={self.pioche})"

    def nombre_de_joueurs(self):
        return len(self.joueurs)
    
    def jouer_tour(self, plateau):
        if not self.pioche:
            return False
        joueur = self.joueurs[self.index_joueur]
        affichage.afficher_tour(joueur)
        affichage.afficher_plateau(plateau)
        tuile_joueur = self.pioche.pop()
        affichage.afficher_tuile(tuile_joueur)
        rotation = affichage.demander_rotation()

        for i in range(rotation):
            tuile_joueur.tourner()

        while True:
            x, y = affichage.demander_coordonnees()
            if plateau.placement(tuile_joueur, x, y):
                affichage.afficher_tuile_placee()
                break
            else:
                affichage.afficher_placement_invalide()
        self.changer_joueur()

        return True

    def changer_joueur(self):
        self.index_joueur = (self.index_joueur + 1)% len(self.joueurs)

    def deroulement_jeu(self, plateau):
        plateau.tuiles[(0, 0)] = self.pioche.pop(0)

        while self.pioche:
            continuer = self.jouer_tour(plateau)
            if not continuer:
                break

        affichage.afficher_fin()