VERT = "\033[32m"
ROUGE = "\033[31m"
RESET = "\033[0m"
import random




def creer_grille_liste(n):
    "crée une grille vide"
    return [[0 for _ in range(n)] for _ in range(n)]
    

import random

def ajouter_2_ou_4_aleatoire(grille):
    """
    Ajoute un 2 ou un 4 dans une case vide choisie aléatoirement dans la grille
    """
    chiffre = [2,4]
    apparition = random.choice(chiffre)
    cases_vides = []
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == 0:
                cases_vides.append((i, j))
    
    i, j= random.choice(cases_vides)
    grille[i][j] = apparition


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


def deplacer_a_gauche(ligne,score):
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
            score += ligne_sans_zero[i] * 2
            i += 2  
        else:
            resultat.append(ligne_sans_zero[i])
            i += 1
    
    while len(resultat) < len(ligne):
        resultat.append(0)
    
    return resultat,score


def deplacer_a_droite(ligne,score):
    """
    Déplace et combine les tuiles d'une ligne vers la droite.
    """
    ligne_inverse = ligne[::-1]
    ligne_deplacee,score= deplacer_a_gauche(ligne_inverse,score)
    return ligne_deplacee[::-1], score



def deplacer_haut(grille,score):
    """
    Déplace les tuiles de chaque colonne vers le haut.
    """
    taille = len(grille)
    for j in range(taille):
        colonne = []
        for i in range(taille):
            colonne.append(grille[i][j])
        colonne_deplacee,score = deplacer_a_gauche(colonne,score)
        for i in range(taille):
            grille[i][j] = colonne_deplacee[i]
    return grille, score

def deplacer_bas(grille,score):
    """
    Déplace les tuiles de chaque colonne vers le bas.
    """
    taille = len(grille)
    for j in range(taille):
        colonne = []
        for i in range(taille):
            colonne.append(grille[i][j])
        colonne_deplacee,score = deplacer_a_droite(colonne,score)
        for i in range(taille):
            grille[i][j] = colonne_deplacee[i]
    return grille, score



def deplacer(grille, direction, score):
    """
    Déplace toutes les lignes ou colonnes dans la direction spécifiée.
    Renvoie la grille modifiée et le score mis à jour.
    """
    if direction == 'q': 
        for i in range(len(grille)):
            grille[i], score = deplacer_a_gauche(grille[i], score)
    elif direction == 'd':
        for i in range(len(grille)):
            grille[i], score = deplacer_a_droite(grille[i], score)
    elif direction == 'z':
        grille, score = deplacer_haut(grille, score)
    elif direction == 's':
        grille, score = deplacer_bas(grille, score)
    return grille, score



def grille_est_pleine(grille):
    " Cette fonction renvoie le nombre de zero dans la grille"
    compteur = 0
    for element in grille:
        for chiffre in element:
            if chiffre == 0:
                compteur +=1
    return compteur

def mouvement_possible(grille):
    n = len(grille)
    for ligne in grille:
        if 0 in ligne:
            return True

    for i in range(n):
        for j in range(n - 1): 
            if grille[i][j] == grille[i][j + 1]:
                return True

    for j in range(n):
        for i in range(n - 1):  # Comparer avec la case du bas
            if grille[i][j] == grille[i + 1][j]:
                return True
    
    return False

def case_2048_existe(grille):
    for element in grille:
        if 2048 in element:
            return True
    return False



def jouer_2048():
    """
    Boucle principale pour jouer au 2048.
    """
    score = 0
    nb_carre = int(input("Vous voulez une grille de quelle taille ?:  "))
    grille = creer_grille_liste(nb_carre)
    ajouter_2_ou_4_aleatoire(grille)
    ajouter_2_ou_4_aleatoire(grille)

    print("Grille initiale :")
    print(convertir_grille_en_affichage(grille))
    
    while True:
        direction = choix_joueur()
        grille, score = deplacer(grille, direction,score)
        if case_2048_existe(grille):
            print(f"{VERT}Félicitations ! Vous avez atteint 2048 !{RESET}")
            break
        if not mouvement_possible(grille):
            print(f"{ROUGE}Perdu: aucun mouvement possible \n  Votre score est de {score}.{RESET}")
            break
        ajouter_2_ou_4_aleatoire(grille)

        print("Grille après le déplacement :")
        print(convertir_grille_en_affichage(grille))
        print(f"Votre score est de {score}")

jouer_2048()