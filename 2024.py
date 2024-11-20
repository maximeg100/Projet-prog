def creer_grille_liste(n):
    "crée une grille vide"
    return [[0 for _ in range(n)] for _ in range(n)]

import random

def ajouter_24_aleatoire(grille):
    """
    Ajoute un 2 ou un 4 dans une case vide choisie aléatoirement dans la grille
    """
    chiffre = [2,4]
    apparition1 = random.choice(chiffre)
    apparition2 = random.choice(chiffre)
    cases_vides = []
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == 0:
                cases_vides.append((i, j))
    
    i, j= random.choice(cases_vides)
    grille[i][j] = apparition1
    cases_vides.remove((i,j))
    i,j = random.choice(cases_vides)
    grille[i][j] = apparition2


def convertir_grille_en_affichage(grille):
    """
    Convertit la grille logique (liste de listes) en une grille affichable
    """
    n = len(grille)
    res = ''
    barre = '-' * (n * 5 + 1) + '\n'

    for ligne in grille:
        res += barre
        ligne_remplie = ""
        for valeur in ligne:
            if valeur != ' ':
                ligne_remplie += f"|{valeur:>4}" #pour pas que la grille change de largeur si c'est un nombre a deux chiffres ou +
            else:
                ligne_remplie += "|    "
        ligne_remplie += '|\n'
        res += ''.join(ligne_remplie)
    res += barre
    return res


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


def deplacer_a_gauche(ligne):
    """
    Déplace et combine les tuiles d'une ligne vers la gauche.
    """
    ligne_sans_zero = []
    for valeur in ligne:
        if valeur != 0:
            ligne_sans_zero.append(valeur)
    resultat = []
    i = 0
    while i < len(ligne_sans_zero):
        if i < len(ligne_sans_zero) - 1 and ligne_sans_zero[i] == ligne_sans_zero[i + 1]:
            resultat.append(ligne_sans_zero[i] * 2)
            i += 2  
        else:
            resultat.append(ligne_sans_zero[i])
            i += 1
    
    while len(resultat) < len(ligne):
        resultat.append(0)
    
    return resultat


def deplacer_a_droite(ligne):
    """
    Déplace et combine les tuiles d'une ligne vers la droite.
    """
    ligne_inverse = ligne[::-1]
    ligne_deplacee = deplacer_a_gauche(ligne_inverse)
    return ligne_deplacee[::-1]



def deplacer_haut(grille):
    """
    Déplace les tuiles de chaque colonne vers le haut.
    """
    taille = len(grille)
    for j in range(taille):
        colonne = []
        for i in range(taille):
            colonne.append(grille[i][j])
        colonne_deplacee = deplacer_a_gauche(colonne)
        for i in range(taille):
            grille[i][j] = colonne_deplacee[i]

def deplacer_bas(grille):
    """
    Déplace les tuiles de chaque colonne vers le bas.
    """
    taille = len(grille)
    for j in range(taille):
        colonne = []
        for i in range(taille):
            colonne.append(grille[i][j])
        colonne_deplacee = deplacer_a_droite(colonne)
        for i in range(taille):
            grille[i][j] = colonne_deplacee[i]



def deplacer(grille, direction):
    """
    Déplace toutes les lignes ou colonnes dans la direction spécifiée.
    direction peut être 'gauche', 'droite', 'haut', 'bas'.
    """
    if direction == 'gauche':
        for i in range(len(grille)):
            grille[i] = deplacer_a_gauche(grille[i])
    elif direction == 'droite':
        for i in range(len(grille)):
            grille[i] = deplacer_a_droite(grille[i])
    elif direction == 'haut':
        deplacer_haut(grille)
    elif direction == 'bas':
        deplacer_bas(grille)


nb_carré = int(input('Vous voulez une grille de combien ?'))
grille = creer_grille_liste(nb_carré)
ajouter_24_aleatoire(grille)
print(grille)


print("Grille initiale :")
print(convertir_grille_en_affichage(grille))

print("Déplacer à gauche :")
deplacer(grille, 'gauche')
print(convertir_grille_en_affichage(grille))

print("Déplacer à droite :")
deplacer(grille, 'droite')
print(convertir_grille_en_affichage(grille))

print("Déplacer vers le haut :")
deplacer(grille, 'haut')
print(convertir_grille_en_affichage(grille))

print("Déplacer vers le bas :")
deplacer(grille, 'bas')
print(convertir_grille_en_affichage(grille))
