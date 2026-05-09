import classes
import tuiles
import affichage

plateau = classes.Plateau()
joueurs = affichage.creation_joueurs()

jeu = classes.Jeu(joueurs,tuiles.pioche)
jeu.deroulement_jeu(plateau)