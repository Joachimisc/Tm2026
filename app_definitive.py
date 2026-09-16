from nicegui import ui, app
import classes
import tuiles

app.add_static_files('/images', 'images')

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
        partie.plateau.tuiles[(0,0)] = tuiles.tuile_depart
        partie.pioche.remove(tuiles.tuile_depart)
        ui.navigate.to('/jeu')

    ui.button("Commencer", on_click=commencer)

def placer_tuile(x,y): 
    if partie.tuile_actuelle is None :
        ui.notify("Vous devez piocher une tuile avant de la placer.")
        return
    x_placement = x
    y_placement = y

    if partie.plateau.placement(partie.tuile_actuelle, x_placement, y_placement):
            points = partie.calculer_score(x_placement, y_placement)
            points_ville = 0
            if partie.plateau.extremite_ville(partie.plateau.tuiles[(x_placement, y_placement)]) > 0:
                if partie.plateau.vérifier_ville_fermee(x_placement, y_placement):
                    nombre_tuiles = partie.plateau.compteur_ville(x_placement, y_placement)
                    points_ville = nombre_tuiles * 2
                    joueur = partie.joueurs[partie.index_joueur]
                    joueur.score += points_ville
                    ui.notify(f"Ville terminée : {points_ville} points pour {partie.joueurs[partie.index_joueur]}!")
            if points > 0 :
                ui.notify(f"Vous avez gagné {points} points !")
                partie.tuile_actuelle = None
                joueur= partie.joueurs[partie.index_joueur]
                if joueur.score >= 15  :
                    ui.notify(f"{partie.joueurs[partie.index_joueur].nom} a gagné !!!")
                    afficher_joueur.refresh()
                    afficher_plateau.refresh()
                    return
            partie.tuile_actuelle = None
            partie.changer_joueur()
            afficher_joueur.refresh()
            afficher_plateau.refresh()
    else :
            ui.notify("Placement non valide.")

@ui.refreshable
def afficher_plateau():
    ui.label("Plateau :")

    with ui.grid(columns=13).style("gap: 0px;") :
        for y in range(6, -7, -1) :
            for x in range(-6, 7) :

                tuile = partie.plateau.tuiles.get((x,y))

                #with ui.card().style("width: 100px; height: 100px; border: 1px solid black; box-sizing : border-box;") :
                    #ui.label(f"{x},{y}")

                if tuile :
                    nom_image = f"{tuile.nord}{tuile.est}{tuile.sud}{tuile.ouest}.png"
                    ui.image(f"/images/{nom_image}").style("width: 100px; height: 100px; padding:0px;")
                else :
                    ui.button(f"{x},{y}", on_click=lambda x=x, y=y : placer_tuile(x,y)).style("width: 100px; height: 100px; border: 1px solid black; box-sizing : border-box;") 
                

@ui.refreshable
def afficher_joueur():
    joueur = partie.joueurs[partie.index_joueur]
    ui.label(f"Tour de {joueur.nom}")
    ui.label(f"Score de {partie.joueurs[0].nom}: {partie.joueurs[0].score}")
    ui.label(f"Score de {partie.joueurs[1].nom}: {partie.joueurs[1].score}")
    ui.label(f"Tuiles réstantes :{len(partie.pioche)}")
    if partie.tuile_actuelle :
        ui.label(f"Votre tuile : {partie.tuile_actuelle}")
        nom_image = f"{partie.tuile_actuelle.nord}{partie.tuile_actuelle.est}{partie.tuile_actuelle.sud}{partie.tuile_actuelle.ouest}.png"
        ui.image(f"/images/{nom_image}").style("width: 100px; height: 100px;")

@ui.page('/jeu')
def jeu():
    if partie is None:
        ui.label("Aucune partie en cours.")
        return
    ui.label("La partie a commencé !")
    #ui.image("/images/PPPP.png").style("width: 100px; height: 100px;")
    ui.separator()
    afficher_plateau()
    afficher_joueur()

    def piocher():
        if partie.tuile_actuelle is None:
            partie.piocher_tuile()
            afficher_joueur.refresh()
        else :
            ui.notify("Piochez d'abord une tuile.")
    ui.button("Piocher une tuile", on_click=piocher)

    def tourner_tuile():
        if partie.tuile_actuelle :
            partie.tuile_actuelle.tourner()
            afficher_joueur.refresh()
    ui.button("Tourner la tuile de 90° vers la droite", on_click=tourner_tuile)

        
ui.run()