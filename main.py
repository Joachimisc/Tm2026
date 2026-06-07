import classes
import tuiles
import affichage

plateau = classes.Plateau()

noms = affichage.creation_joueurs()
joueurs = []
for nom in noms:
    joueurs.append(classes.Joueur(nom))


jeu = classes.Jeu(joueurs,tuiles.pioche)
jeu.deroulement_jeu(plateau)
