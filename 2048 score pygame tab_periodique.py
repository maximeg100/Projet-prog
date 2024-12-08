VERT = "\033[32m"
ROUGE = "\033[31m"
RESET = "\033[0m"
import random
import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (119, 110, 101)
LIGHT_GRAY = (187, 173, 160)
elements_periodiques = {
    "H": {"fusion": "He", "couleur": (238, 228, 218)},
    "He": {"fusion": "Li", "couleur": (237, 224, 200)},
    "Li": {"fusion": "Be", "couleur": (242, 177, 121)},
    "Be": {"fusion": "C", "couleur": (245, 149, 99)},
    "C": {"fusion": "N", "couleur": (246, 124, 95)},
    "N": {"fusion": "O", "couleur": (246, 94, 59)},
    "O": {"fusion": "F", "couleur": (237, 207, 114)},
    "F": {"fusion": "Ne", "couleur": (237, 204, 97)},
    "Ne": {"fusion": "Na", "couleur": (237, 200, 80)},
    "Na": {"fusion": "Mg", "couleur": (237, 197, 63)},
    "Mg": {"fusion": "Al", "couleur": (237, 194, 46)},
}

SCREEN_SIZE = 600
GRID_SIZE = 4
TILE_SIZE = SCREEN_SIZE // GRID_SIZE 
FONT = pygame.font.Font(None, 50)


def creer_grille_liste(n):
    "crée une grille carrée de n sur n avec des 0"
    return [[0 for _ in range(n)] for _ in range(n)]


def ajouter_element_aleatoire(grille):
    "Ajoute un 2 ou un 4 dans une case vide choisie aléatoirement dans la grille"
    if nombre_cases_vides(grille) == 0:
        return

    cases_vides = []
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == 0:
                cases_vides.append((i, j))
    
    i, j = random.choice(cases_vides)
    grille[i][j] = random.choice(['H', 'He'])

def cherche_meilleure_case(grille):
    "cherche la meilleure case et renvoie l'element"
    meilleure_case = None
    max_valeur = 0
    for ligne in grille:
        for element in ligne:
            if element != 0 and element in elements_periodiques:
                valeur_numerique = obtenir_valeur_numerique(element)
                if valeur_numerique > max_valeur:
                    max_valeur = valeur_numerique
                    meilleure_case = element
    return meilleure_case

def obtenir_valeur_numerique(element):
    "convertit un élément chimique en sa valeur numérique"
    valeurs_numeriques = {
        "H": 2, "He": 4, "Li": 8, "Be": 16, "C": 32,
        "N": 64, "O": 128, "F": 256, "Ne": 512, "Na": 1024, "Mg": 2048}
    return valeurs_numeriques.get(element, 0)

def deplacer_a_gauche(ligne,score):
    "Déplace les tuiles de chaque colonne vers la gauche et les combine si elles sont égales, calcule le score"
    ligne_sans_zero = []
    for valeur in ligne:
        if valeur != 0:
            ligne_sans_zero.append(valeur)
    resultat = []
    i = 0
    while i < len(ligne_sans_zero):
        if i < len(ligne_sans_zero) - 1 and ligne_sans_zero[i] == ligne_sans_zero[i + 1] and ligne_sans_zero[i] in elements_periodiques:
            fusion_element = elements_periodiques[ligne_sans_zero[i]]['fusion']
            resultat.append(fusion_element)
            valeur_fusion = obtenir_valeur_numerique(fusion_element)
            score += valeur_fusion
            i += 2  
        else:
            resultat.append(ligne_sans_zero[i])
            i += 1
    
    while len(resultat) < len(ligne):
        resultat.append(0)
    
    return resultat,score


def deplacer_a_droite(ligne,score):
    "Déplace les tuiles de chaque colonne vers la droite et les combine si elles sont égales, calcule le score"
    ligne_inverse = ligne[::-1]
    ligne_deplacee,score= deplacer_a_gauche(ligne_inverse,score)
    return ligne_deplacee[::-1], score



def deplacer_haut(grille,score):
    "Déplace les tuiles de chaque colonne vers le haut et les combine si elles sont égales, calcule le score"
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
    "Déplace les tuiles de chaque colonne vers le bas et les combine si elles sont égales, calcule le score"
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
    """Déplace toutes les lignes ou colonnes de la grille dans une direction direction
    et calcule le score"""
    if direction == 'gauche': 
        for i in range(len(grille)):
            grille[i], score = deplacer_a_gauche(grille[i], score)
    elif direction == 'droite':
        for i in range(len(grille)):
            grille[i], score = deplacer_a_droite(grille[i], score)
    elif direction == 'haut':
        grille, score = deplacer_haut(grille, score)
    elif direction == 'bas':
        grille, score = deplacer_bas(grille, score)
    return grille, score

def nombre_cases_vides(grille):
    compteur = 0
    for ligne in grille:
        for element in ligne:
            if element == 0:
                compteur += 1
    return compteur


def mouvement_possible(grille):
    "renvoie true si on peut encore bouger"
    n = len(grille)
    for ligne in grille:
        if 0 in ligne:
            return True

    for i in range(n):
        for j in range(n - 1): 
            if grille[i][j] == grille[i][j + 1]:
                return True

    for j in range(n):
        for i in range(n - 1):
            if grille[i][j] == grille[i + 1][j]:
                return True
    
    return False

def case_2048_existe(grille):
    "renvoie true si il y a un 2048 dans une grille"
    for element in grille:
        if 32 in element:
            return True
    return False

def dessiner_grille(screen, grille, score):
    "dessine la grille sur pygame en la mettant à jour"
    screen.fill(LIGHT_GRAY)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            valeur = grille[i][j]
            x = j * TILE_SIZE
            y = i * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE-3, TILE_SIZE -3)
            couleur = (elements_periodiques[valeur]['couleur'] if valeur in elements_periodiques else (205,193,180))
            pygame.draw.rect(screen, couleur, rect)
            if valeur != 0:
                font = pygame.font.Font(None, obtenir_taille_police(valeur))
                texte = font.render(str(valeur), True, BLACK)
                texte_rect = texte.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(texte, texte_rect)
    
    texte_score = FONT.render(f"Score: {score}", True, GRAY)
    screen.blit(texte_score, (10, SCREEN_SIZE - 50))
    pygame.display.flip()

def obtenir_taille_police(valeur):
    if valeur == 0:
        return 0  
    num_digits = len(str(valeur))
    return TILE_SIZE // (num_digits + 1) + 15


def jouer_2048_pygame():
    "fonction main"
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("2048")
    grille = creer_grille_liste(GRID_SIZE)
    score = 0
    ajouter_element_aleatoire(grille)
    ajouter_element_aleatoire(grille)
    dessiner_grille(screen, grille, score)
    
    running = True

    while running:
        dessiner_grille(screen, grille, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                direction = None
                if event.key == pygame.K_LEFT:
                    direction = 'gauche'
                elif event.key == pygame.K_RIGHT:
                    direction = 'droite'
                elif event.key == pygame.K_UP:
                    direction = 'haut'
                elif event.key == pygame.K_DOWN:
                    direction = 'bas'
                if direction:
                    grille, score = deplacer(grille, direction, score)
                    if not mouvement_possible(grille):
                        print(f"{ROUGE}{'-'*13}Perdu{'-'*13}\n{' '*5}Votre score est de {score}{' '*5}\n  Votre meilleur case était {cherche_meilleure_case(grille)}{RESET}")
                        running = False
                        break
                    else:
                        ajouter_element_aleatoire(grille)
                    if case_2048_existe(grille):
                        print(f"{VERT}Felicitations vous avez atteint 2048 !{RESET}")
                        running = False
                    

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    jouer_2048_pygame()