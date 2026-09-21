from nicegui import ui, app
import classes
import tuiles

app.add_static_files('/images', 'images')

partie = None
zone_pion = None

@ui.page('/')
def accueil():
    nom1 = ui.input("Joueur 1")
    nom2 = ui.input("Joueur 2")

    def commencer():
        global partie
        joueurs = [classes.Joueur(nom1.value),classes.Joueur(nom2.value)]
        joueurs[0].couleur = "red"
        joueurs[1].couleur = "blue"
        plateau = classes.Plateau()
        jeu = classes.Jeu(joueurs, tuiles.pioche, plateau)
        partie = jeu
        partie.plateau.tuiles[(0,0)] = tuiles.tuile_depart
        partie.pioche.remove(tuiles.tuile_depart)
        ui.navigate.to('/jeu')

    ui.button("Commencer", on_click=commencer)

def poser_pion_route(tuile, joueur):
    joueur.pions -= 1
    tuile.pion_route = joueur
    continuer_tour()

def poser_pion_ville(tuile, joueur):
    joueur.pions -= 1
    tuile.pion_ville = joueur
    continuer_tour()

def placer_pion(x,y) :
    tuile = partie.plateau.tuiles[(x, y)]
    joueur = partie.joueurs[partie.index_joueur]

    zone_pion.clear()
    with zone_pion :
        ui.label("Sur quelle partie voulez-vous poser votre pion ?")
        with ui.row():
            if "R" in [tuile.nord, tuile.est, tuile.sud, tuile.ouest]:
                ui.button("Route", on_click=lambda: poser_pion_route(tuile, joueur))
            if "V" in [tuile.nord, tuile.est, tuile.sud, tuile.ouest]:
                ui.button("Ville", on_click=lambda: poser_pion_ville(tuile, joueur))

def continuer_tour() :
    partie.tuile_actuelle = None
    partie.changer_joueur()
    afficher_joueur.refresh()
    afficher_plateau.refresh()

def demander_pion(x,y) :
    joueur = partie.joueurs[partie.index_joueur]
    if joueur.pions == 0:
        continuer_tour()
        return
    zone_pion.clear()
    with zone_pion :
        ui.notify("Tuile placée ! Voulez-vous placer un pion ?")
        with ui.row() :
            ui.button("Oui", on_click=lambda : placer_pion(x,y))
            ui.button("Non", on_click=lambda : continuer_tour())

def position_pion(tuile, type_zone):
    positions = {"nord": (50, 15),"est": (85, 50),"sud": (50, 85),"ouest": (15, 50)}
    points = []
    for direction, position in positions.items():
        if getattr(tuile, direction) == type_zone:
            points.append(position)
    if not points:
        return 50, 50
    x = sum(p[0] for p in points) / len(points)
    y = sum(p[1] for p in points) / len(points)

    return x, y

def placer_tuile(x,y): 
    if partie.tuile_actuelle is None :
        ui.notify("Vous devez piocher une tuile avant de la placer.")
        return
    x_placement = x
    y_placement = y

    if partie.plateau.placement(partie.tuile_actuelle, x_placement, y_placement):
            afficher_plateau.refresh()
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
                
            joueur= partie.joueurs[partie.index_joueur]
            if joueur.score >= 15:
                    ui.navigate.to('/victoire')
                    return
                
            demander_pion(x_placement, y_placement)
    else :
            ui.notify("Placement non valide.")

@ui.refreshable
def afficher_plateau():
    ui.label("Plateau :")

    with ui.grid(columns=17).style("gap: 0px;") :
        for y in range(8, -9, -1) :
            for x in range(-8, 9) :

                tuile = partie.plateau.tuiles.get((x,y))

                #with ui.card().style("width: 100px; height: 100px; border: 1px solid black; box-sizing : border-box;") :
                    #ui.label(f"{x},{y}")

                if tuile :
                    nom_image = f"{tuile.nord}{tuile.est}{tuile.sud}{tuile.ouest}.png"
                    with ui.element("div").style("position: relative; width: 100px; height: 100px;"):
                        ui.image(f"/images/{nom_image}").style("width: 100px; height: 100px; padding:0px;")
                        if tuile.pion_route:
                            x_pion, y_pion = position_pion(tuile, "R")
                            ui.label("●").style(
                                f"position: absolute; left: {x_pion}%; top: {y_pion}%; "
                                f"transform: translate(-50%, -50%); "
                                f"font-size: 30px; color: {tuile.pion_route.couleur};"
                            )
                        if tuile.pion_ville:
                            x_pion,y_pion = position_pion(tuile, "V")
                            ui.label("●").style(
                                f"position: absolute; left: {x_pion}%; top: {y_pion}%; "
                                f"transform: translate(-50%, -50%); "
                                f"font-size: 30px; color: {tuile.pion_ville.couleur};"
                            )
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

@ui.page('/victoire')
def victoire():
    joueur = partie.joueurs[partie.index_joueur]

    ui.label("🏆 VICTOIRE !").style("font-size: 40px; font-weight: bold;")
    ui.label(f"{joueur.nom} a gagné !").style("font-size: 30px;")
    ui.label(f"Score : {joueur.score} points").style("font-size: 24px;")

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
    global zone_pion
    zone_pion = ui.column()

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