def creer_grille_liste(n):
    "crée une grille vide"
    return [[' ' for _ in range(n)] for _ in range(n)]

import random

def ajouter_5_aleatoire(grille):
    """
    Ajoute un 5 dans une case vide (' ') choisie aléatoirement dans la grille,
    sans utiliser de liste en compréhension.
    """
    chiffre = [2,4]
    apparition = chiffre[random.randint(0,1)]
    cases_vides = []
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == ' ':
                cases_vides.append((i, j))
    

    
    
    i, j = random.choice(cases_vides)
    grille[i][j] = apparition


def convertir_grille_en_affichage(grille):
    """
    Convertit la grille logique (liste de listes) en une grille affichable (string).
    """
    n = len(grille)
    res = ''
    barre = '-' * (n * 5 + 1) + '\n'

    for ligne in grille:
        res += barre
        res += ''.join(f"| {val}  " if val != ' ' else "|    " for val in ligne) + '|\n'
    res += barre
    return res

grille = creer_grille_liste(4)
ajouter_5_aleatoire(grille)

grille_affichee = convertir_grille_en_affichage(grille)
print(grille_affichee)


#def creer_grille_vide(n):
    #res = ''
    #barre = '-' * n * 5 + '-' + '\n'
    #case = '|    ' *n + '|' +'\n'
    #for i in range(n):
        #res += barre
        #res += case 
    #res += barre
    #print(res)
#creer_grille_vide(5)



