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

@ui.refreshable
def afficher_plateau():
    ui.label("Plateau :")

    with ui.grid(columns=11).style("gap: 0px;") :
        for y in range(5, -6, -1) :
            for x in range(-5, 6) :

                tuile = partie.plateau.tuiles.get((x,y))

                #with ui.card().style("width: 100px; height: 100px; border: 1px solid black; box-sizing : border-box;") :
                    #ui.label(f"{x},{y}")

                if tuile :
                    nom_image = f"{tuile.nord}{tuile.est}{tuile.sud}{tuile.ouest}.png"
                    ui.image(f"/images/{nom_image}").style("width: 100px; height: 100px; padding:0px;")
                else :
                    with ui.card().style("width: 100px; height: 100px; border: 1px solid black; box-sizing : border-box;") :
                        ui.label(f"{x},{y}")
                

                

            

    #for position, tuile in partie.plateau.tuiles.items():
        #nom_image = f"{tuile.nord}{tuile.est}{tuile.sud}{tuile.ouest}.png"
        #ui.image(f"/images/{nom_image}").style("width: 100px; height: 100px;")

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
    x = ui.number("coordonnée x", value = 0)
    y = ui.number("coordonnée y", value = 0) 

    def placer_tuile(): 
        if partie.tuile_actuelle is None :
            ui.notify("Vous devez piocher une tuile avant de la placer.")
            return
        x_placement = int(x.value)
        y_placement = int(y.value)

        if partie.plateau.placement(partie.tuile_actuelle, x_placement, y_placement):
            points = partie.calculer_score(x_placement, y_placement)
            if points > 0 :
                ui.notify(f"Vous avez gagné {points} points !")
                partie.tuile_actuelle = None
                joueur= partie.joueurs[partie.index_joueur]
                if joueur.score >= 3:
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
    ui.button("Placer la tuile", on_click=placer_tuile)


        
ui.run()