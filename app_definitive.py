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
        plateau = classes.Plateau()
        jeu = classes.Jeu(joueurs, tuiles.pioche, plateau)
        partie = jeu
        partie.plateau.tuiles[(0,0)] = partie.pioche.pop(0)
        ui.navigate.to('/jeu')

    ui.button("Commencer", on_click=commencer)

@ui.refreshable
def afficher_plateau():
    ui.label("Plateau :")
    for position, tuile in partie.plateau.tuiles.items():
        ui.label(f"{position} : {tuile}")

@ui.refreshable
def afficher_joueur():
    joueur = partie.joueurs[partie.index_joueur]
    ui.label(f"Tour de {joueur.nom}")
    ui.label(f"Score : {joueur.score}")
    ui.label(f"Tuiles réstantes :{len(partie.pioche)}")
    if partie.tuile_actuelle :
        ui.label(f"Votre tuile : {partie.tuile_actuelle}")

@ui.page('/jeu')
def jeu():
    if partie is None:
        ui.label("Aucune partie en cours.")
        return
    ui.label("La partie a commencé !")
    ui.label(f"Tuiles restantes : {len(partie.pioche)}")
    ui.separator()
    afficher_plateau()
    afficher_joueur()
    def piocher():
        partie.piocher_tuile()
        afficher_joueur.refresh()
    ui.button("Piocher une tuile", on_click=piocher)
    def tourner_tuile():
        if partie.tuile_actuelle :
            partie.tuile_actuelle.tourner()
            afficher_joueur.refresh()
    ui.button("Tourner la tuile de 90° vers la droite", on_click=tourner_tuile)
ui.run()