def creation_joueurs():

    joueurs = []

    nombre_joueurs = int(input("Nombre de joueurs : "))

    for i in range(nombre_joueurs):
        nom = input(f"Nom du joueur {i+1} : ")
        joueurs.append(nom)

    return joueurs

def afficher_tour(joueur):
    print(f"\nTour de {joueur}")

def afficher_plateau(plateau):
    print(plateau.tuiles)

def afficher_tuile(tuile):
    print("Voici votre tuile :", tuile)

def demander_rotation():
    return int(input("Tournez la tuile de 90° (0,1,2,3 fois) : "))

def demander_coordonnees():
    x = int(input("Entrez une coordonnée x : "))
    y = int(input("Entrez une coordonnée y : "))
    return x, y

def afficher_placement_invalide():
    print("Placement non valide, réessayez.")

def afficher_tuile_placee():
    print("Tuile placée !")

def afficher_fin():
    print("Partie terminée !")