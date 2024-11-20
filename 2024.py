def creer_grille_liste(n):
    "crée une grille vide"
    return [[' ' for _ in range(n)] for _ in range(n)]

import random

def ajouter_24_aleatoire(grille):
    """
    Ajoute un 5 dans une case vide (' ') choisie aléatoirement dans la grille,
    sans utiliser de liste en compréhension.
    """
    chiffre = [2,4]
    apparition1 = random.choice(chiffre)
    apparition2 = random.choice(chiffre)
    cases_vides = []
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == ' ':
                cases_vides.append((i, j))
    
    i, j= random.choice(cases_vides)
    grille[i][j] = apparition1
    cases_vides.remove((i,j))
    i,j = random.choice(cases_vides)
    grille[i][j] = apparition2


def convertir_grille_en_affichage(grille):
    """
    Convertit la grille logique (liste de listes) en une grille affichable (string).
    """
    n = len(grille)
    res = ''
    barre = '-' * (n * 5 + 1) + '\n'

    for ligne in grille:
        res += barre
        ligne_remplie = ""
        for valeur in ligne:
            if valeur != ' ':
                ligne_remplie += f"| {valeur}  "
            else:
                ligne_remplie += "|    "
        ligne_remplie += '|\n'
        res += ''.join(ligne_remplie)
    res += barre
    return res

n = int(input('Vous voulez une grille de combien'))
grille = creer_grille_liste(n)
ajouter_24_aleatoire(grille)

grille_affichee = convertir_grille_en_affichage(grille)
print(grille_affichee)

def choix_joueur():
    """
    Demande à l'utilisateur une direction et vérifie qu'elle est valide.
    """
    directions = {'z': "haut", 'q': "gauche", 's': "bas", 'd': "droite"}
    while True:
        choix = input("Choisissez une direction : z = haut, q = gauche, s = bas, d = droite\n")
        if choix in directions:
            return choix
        else:
            print("Choix invalide, veuillez essayer à nouveau.")


choix_joueur()



