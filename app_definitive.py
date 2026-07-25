from nicegui import ui
import classes
import tuiles

plateau = classes.Plateau()

partie = None

@ui.page('/')
def accueil():
    nom1 = ui.input("Joueur 1")
    nom2 = ui.input("Joueur 2")

    def commencer():
        global partie
        joueurs = [classes.Joueur(nom1.value),classes.Joueur(nom2.value)]
        jeu = classes.Jeu(joueurs, tuiles.pioche)
        plateau.tuiles[(0,0)] = jeu.pioche.pop(0)
        partie = jeu
        ui.navigate.to('/jeu')

    ui.button("Commencer", on_click=commencer)

@ui.page('/jeu')
def jeu():
    if partie is None:
        ui.label("Aucune partie en cours.")
        return
    ui.label("La partie a commencé !")
    joueur = partie.joueurs[partie.index_joueur]
    ui.label(f"Tour de {joueur.nom}")
    ui.label(f"Score : {joueur.score}")
    ui.label(f"Tuiles restantes : {len(partie.pioche)}")

ui.run()