import classes
import tuiles

plateau = classes.Plateau()
joueur1 = classes.Joueur("Joachim")
joueur2 = classes.Joueur("Livio")

jeu = classes.Jeu([joueur1,joueur2],tuiles.pioche)
jeu.deroulement_partie(plateau)