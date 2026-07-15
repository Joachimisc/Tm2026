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
        partie = classes.Partie(joueurs, tuiles.pioche)
        ui.navigate.to('/jeu')

    ui.button("Commencer", on_click=commencer)
    
ui.run()