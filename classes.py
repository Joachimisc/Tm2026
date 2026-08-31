import affichage
import random

class Tuile :

    def __init__(self, nord, est, sud, ouest, numéro):
        self.nord = nord
        self.est = est
        self.sud = sud
        self.ouest = ouest
        self.numéro = numéro
        self.rotation = 0 

    def __repr__(self):
        return f"Tuile({self.nord},{self.est},{self.sud},{self.ouest})"

    def tourner(self):
        self.nord, self.est, self.sud, self.ouest = (self.ouest, self.nord, self.est, self.sud)
        self.rotation = (self.rotation + 90) % 360
        
class Plateau :

    def __init__(self):
        self.tuiles = {}

    def trouver_voisins(self, x, y):
        return {"nord": self.tuiles.get((x, y + 1)), "sud": self.tuiles.get((x, y - 1)), "est": self.tuiles.get((x + 1, y)), "ouest": self.tuiles.get((x - 1, y))}

    def validation(self, tuile, x, y):
        voisins = self.trouver_voisins(x, y)

        if (x, y) in self.tuiles:
            return False
        if (voisins["nord"] is None and voisins["sud"] is None and voisins["est"] is None and voisins["ouest"] is None):
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

    def fin_route(self, tuile):
        compteur = 0
        if tuile.nord == "R" :
            compteur += 1
        if tuile.est == "R" :
            compteur += 1
        if tuile.sud == "R" :
            compteur += 1
        if tuile.ouest == "R" :
            compteur += 1
        return compteur 

    #fonction récurssive pour compter le nombres de tuiles route sur lesquelles on peut se déplacer à partir d'une tuile donnée
    def compteur_route(self, x, y, direction, visites=None):
        if visites is None:
            visites = []
        if (x, y) in visites:
            return 0
        visites.append((x, y))
        points = 1
        tuile = self.tuiles[(x, y)]
        cote_entree = direction
        directions = {"nord": (0, 1),"sud": (0, -1),"est": (1, 0),"ouest": (-1, 0)}
        for cote in directions:
            if cote == cote_entree :
                continue
            dx = directions[cote][0]
            dy = directions[cote][1]
            if cote == "nord":
                type_cote = tuile.nord
                cote_voisin = "sud"
            elif cote == "sud": 
                type_cote = tuile.sud
                cote_voisin = "nord"
            elif cote == "est":
                type_cote = tuile.est
                cote_voisin = "ouest"
            else:
                type_cote = tuile.ouest
                cote_voisin = "est"

            if type_cote == "R":
                voisin = self.tuiles.get((x + dx, y + dy))
                if voisin :
                    if getattr (voisin, cote_voisin) == "R" :
                        points += self.compteur_route( x+dx, y+dy, cote_voisin, visites)

                    #if cote == "nord" and voisin.sud == "R" :
                        #points += self.compteur_route(x + dx,y + dy,visites)
                    #if cote == "est" and voisin.ouest == "R" :
                        #points += self.compteur_route(x + dx,y + dy,visites)
                    #if cote == "sud" and voisin.nord == "R" :
                        #points += self.compteur_route(x + dx,y + dy,visites)
                    #if cote == "ouest" and voisin.est == "R" :
                        #points += self.compteur_route(x + dx,y + dy,visites)

        return points

# fonction récurssive pour vérifier si une route est fermée  
    def route_fermee(self, x, y, direction, visites=None, depart=None):
        if visites is None:
            visites = set()
        if depart is None:
            depart = (x, y)
        if (x, y) in visites:
            return (x, y) == depart
        visites.add((x, y))
        tuile = self.tuiles.get((x, y))
        if tuile is None:
            return False
        if direction == "nord":
            nx, ny = x, y + 1
            cote = tuile.nord
            cote_voisin = "sud"
        elif direction == "sud":
            nx, ny = x, y - 1
            cote = tuile.sud
            cote_voisin = "nord"
        elif direction == "est":
            nx, ny = x + 1, y
            cote = tuile.est
            cote_voisin = "ouest"
        elif direction == "ouest":
            nx, ny = x - 1, y
            cote = tuile.ouest
            cote_voisin = "est"
        if cote != "R":
            return False
        voisin = self.tuiles.get((nx, ny))
        if voisin is None:
            return False
        if getattr(voisin, cote_voisin) != "R":
            return False
        return self.route_fermee(nx, ny, cote_voisin, visites, depart)
        
    #pas encore utile(le comptage des villes ne marche pas encore)
    def extremite_ville(self, tuile):
        compteur = 0
        if tuile.nord == "V":
            compteur += 1
        if tuile.est == "V":
            compteur += 1
        if tuile.sud == "V":
            compteur += 1
        if tuile.ouest == "V":
            compteur += 1

        return compteur

    #pareil
    def compteur_ville(self, x, y, visites=None):
        if visites is None:
            visites = []
        if (x, y) in visites:
            return 0
        visites.append((x, y))
        points = 0
        tuile = self.tuiles[(x, y)]

        if tuile.nord == "V":
            voisin = self.tuiles.get((x, y + 1))
            if voisin and voisin.sud == "V":
                points += self.compteur_ville(x, y + 1, visites)
        if tuile.sud == "V":
            voisin = self.tuiles.get((x, y - 1))
            if voisin and voisin.nord == "V":
                points += self.compteur_ville(x, y - 1, visites)
        if tuile.est == "V":
            voisin = self.tuiles.get((x + 1, y))
            if voisin and voisin.ouest == "V":
                points += self.compteur_ville(x + 1, y, visites)
        if tuile.ouest == "V":
            voisin = self.tuiles.get((x - 1, y))
            if voisin and voisin.est == "V":
                points += self.compteur_ville(x - 1, y, visites)

        return points

    #pareil 
    def vérifier_ville_fermee(self, x, y, visites=None):
        if visites is None:
            visites = []
        if (x, y) in visites:
            return True
        visites.append((x, y))
        tuile = self.tuiles[(x, y)]

        if self.extremite_ville(tuile) == 0:
            return False
        if tuile.nord == "V":
            voisin = self.tuiles.get((x, y + 1))
            if voisin is None or voisin.sud != "V":
                return False
            if not self.vérifier_ville_fermee(x, y + 1, visites):
                return False
        if tuile.sud == "V":
            voisin = self.tuiles.get((x, y - 1))
            if voisin is None or voisin.nord != "V":
                return False
            if not self.vérifier_ville_fermee(x, y - 1, visites):
                return False
        if tuile.est == "V":
            voisin = self.tuiles.get((x + 1, y))
            if voisin is None or voisin.ouest != "V":
                return False
            if not self.vérifier_ville_fermee(x + 1, y, visites):
                return False
        if tuile.ouest == "V":
            voisin = self.tuiles.get((x - 1, y))
            if voisin is None or voisin.est != "V":
                return False
            if not self.vérifier_ville_fermee(x - 1, y, visites):
                return False

        return True
class Joueur :
    def __init__(self, nom):
        self.nom = nom
        self.score = 0
    def __repr__(self):
        return f"Joueur({self.nom}, score={self.score})"

class Jeu :

    def __init__(self, joueurs, pioche, plateau):
        self.joueurs = joueurs
        self.pioche = pioche
        self.plateau = plateau
        self.index_joueur = 0
        self.tuile_actuelle = None
        self.partie_terminée = False

    def __repr__(self):
        return f"Jeu(joueurs={self.joueurs}, pioche={self.pioche})"
    
    def piocher_tuile(self):
        if self.pioche:
            self.tuile_actuelle = random.choice(self.pioche)
            self.pioche.remove(self.tuile_actuelle)
            return self.tuile_actuelle
        else:
            return None

    def nb_de_joueurs(self):
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
                if plateau.route_fermee(x, y):
                    points = plateau.compteur_route(x, y)
                    joueur.score = joueur.score + points
                    affichage.afficher_points(joueur, points)
                if plateau.vérifier_ville_fermee(x, y):
                    points = plateau.compteur_ville(x, y)
                    joueur.score += points * 2
                    affichage.afficher_points(joueur, points * 2)
                break
            else:
                affichage.afficher_placement_invalide()
        self.changer_joueur()

        return True
# fonction pour calculer le score d'un joueur après avoir placé une tuile de route (pas ville encore). on regarde de ou on vient
# et comment on peut continuer. On regarde dans quelles directions on peut aller (par exemple pour les carrefor)
    def calculer_score(self, x, y):
        joueur = self.joueurs[self.index_joueur]
        voisins = self.plateau.trouver_voisins(x, y)
        for direction, voisin in voisins.items():
            if voisin is None:
                continue
            if direction == "nord" and voisin.sud != "R":
                continue
            if direction == "sud" and voisin.nord != "R":
                continue
            if direction == "est" and voisin.ouest != "R":
                continue
            if direction == "ouest" and voisin.est != "R":
                continue
            if self.plateau.fin_route(self.plateau.tuiles[(x, y)]) >= 3:
                points = 1
                if direction == "nord":
                    points += self.plateau.compteur_route(x, y + 1, "sud")
                elif direction == "sud":
                    points += self.plateau.compteur_route(x, y - 1, "nord")
                elif direction == "est":
                    points += self.plateau.compteur_route(x + 1, y, "ouest")
                elif direction == "ouest":
                    points += self.plateau.compteur_route(x - 1, y, "est")

                joueur.score += points
                return points
                    
        if self.plateau.vérifier_ville_fermee(x, y):
            points = self.plateau.compteur_ville(x, y) * 2
            joueur.score += points
            return points
        return 0

    def changer_joueur(self):
        self.index_joueur = (self.index_joueur + 1)% len(self.joueurs)

    def jouer(self, plateau):
        random.shuffle(self.pioche)
        plateau.tuiles[(0, 0)] = self.pioche.pop(0)

        while self.pioche:
            continuer = self.jouer_tour(plateau)
            if not continuer:
                break
    # a completer et afficher une page quand le jeu est terminé
    def vérifier_victoire(self): 
        if self.joueurs[self.index_joueur].score >= 15:
            self.partie_terminée = True
            return True
        return False
        

    #affichage.afficher_fin()
    #affichage.afficher_classement(self.joueurs)