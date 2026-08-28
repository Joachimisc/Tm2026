import random

# =========================
# CLASSE TUILE
# =========================

class Tuile:
    def __init__(self, nord, est, sud, ouest):
        self.nord = nord
        self.est = est
        self.sud = sud
        self.ouest = ouest

    def __repr__(self):
        return f"Tuile(N:{self.nord}, E:{self.est}, S:{self.sud}, O:{self.ouest})"

    def tourner(self):
        self.nord, self.est, self.sud, self.ouest = self.ouest, self.nord, self.est, self.sud


# =========================
# CLASSE PLATEAU
# =========================

class Plateau:
    def __init__(self):
        self.tuiles = {}

    def voisins(self, x, y):
        return {
            "nord": self.tuiles.get((x, y+1)),
            "sud": self.tuiles.get((x, y-1)),
            "est": self.tuiles.get((x+1, y)),
            "ouest": self.tuiles.get((x-1, y))
        }

    def validation(self, tuile, x, y):
        voisins = self.voisins(x, y)

        if (x, y) in self.tuiles:
            return False

        if all(v is None for v in voisins.values()):
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

    def placement_possible(self, tuile):
        for (x, y) in self.tuiles.keys():
            positions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

            for nx, ny in positions:
                copie = Tuile(tuile.nord, tuile.est, tuile.sud, tuile.ouest)

                for i in range(4):
                    if self.validation(copie, nx, ny):
                        return True
                    copie.tourner()
        return False

    def afficher(self):
        print("\n===== PLATEAU =====")
        for coord, tuile in self.tuiles.items():
            print(coord, ":", tuile)
        print("===================\n")


# =========================
# CLASSE JOUEUR
# =========================

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.score = 0


# =========================
# CLASSE JEU
# =========================

class Jeu:
    def __init__(self, joueurs, pioche):
        self.joueurs = joueurs
        self.pioche = pioche
        self.index_joueur = 0

    def changer_joueur(self):
        self.index_joueur = (self.index_joueur + 1) % len(self.joueurs)

    def jouer_tour(self, plateau):
        joueur = self.joueurs[self.index_joueur]
        print("===================================")
        print("Tour de", joueur.nom)
        print("Score :", joueur.score)
        print("===================================")

        if not self.pioche:
            return False

        plateau.afficher()

        tuile_joueur = self.pioche.pop()
        print("Votre tuile :", tuile_joueur)

        if not plateau.placement_possible(tuile_joueur):
            print("Aucun placement possible pour cette tuile.")
            self.changer_joueur()
            return True

        while True:
            try:
                rotation = int(input("Tourner la tuile de 90° (0,1,2,3 fois) : "))
                if rotation in [0,1,2,3]:
                    break
            except:
                pass
            print("Entrée invalide.")

        for i in range(rotation):
            tuile_joueur.tourner()

        print("Tuile après rotation :", tuile_joueur)

        while True:
            try:
                x = int(input("Coordonnée x : "))
                y = int(input("Coordonnée y : "))
            except:
                print("Entrez des nombres.")
                continue

            if plateau.placement(tuile_joueur, x, y):
                print("Tuile placée avec succès !")
                joueur.score += 1
                break
            else:
                print("Placement non valide, recommencez.")

        self.changer_joueur()
        return True

    def deroulement_partie(self, plateau):
        random.shuffle(self.pioche)

        tuile_depart = self.pioche.pop()
        plateau.tuiles[(0, 0)] = tuile_depart

        print("===== TUILE DE DEPART =====")
        print(tuile_depart)

        while self.pioche:
            continuer = self.jouer_tour(plateau)
            if not continuer:
                break

        print("\n========= PARTIE TERMINEE =========")
        for joueur in self.joueurs:
            print(joueur.nom, ":", joueur.score, "points")

        gagnant = max(self.joueurs, key=lambda j: j.score)
        print("Le gagnant est", gagnant.nom, "!")


# =========================
# CREATION DES TUILES
# =========================

pioche = [
    Tuile("ville", "route", "ville", "route"),
    Tuile("route", "ville", "route", "ville"),
    Tuile("champ", "route", "champ", "route"),
    Tuile("ville", "ville", "route", "route"),
    Tuile("route", "champ", "route", "champ"),
    Tuile("champ", "ville", "champ", "ville"),
    Tuile("ville", "route", "champ", "route"),
    Tuile("route", "route", "ville", "ville"),
    Tuile("champ", "champ", "route", "route"),
    Tuile("ville", "champ", "ville", "champ")
]

# =========================
# CREATION DES JOUEURS
# =========================

joueurs = [
    Joueur("Alice"),
    Joueur("Bob")
]

# =========================
# LANCEMENT DE LA PARTIE
# =========================

plateau = Plateau()
jeu = Jeu(joueurs, pioche)
jeu.deroulement_partie(plateau)