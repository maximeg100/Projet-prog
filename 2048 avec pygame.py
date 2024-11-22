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
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

SCREEN_SIZE = 600
GRID_SIZE = 4
TILE_SIZE = SCREEN_SIZE // GRID_SIZE
FONT = pygame.font.Font(None, 50)


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
        for i in range(n - 1):
            if grille[i][j] == grille[i + 1][j]:
                return True
    
    return False

def case_2048_existe(grille):
    for element in grille:
        if 2048 in element:
            return True
    return False

def dessiner_grille(screen, grille, score):
    screen.fill(LIGHT_GRAY)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            valeur = grille[i][j]
            x = j * TILE_SIZE
            y = i * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, TILE_COLORS[valeur], rect)
            if valeur != 0:
                couleur_texte = BLACK if valeur < 128 else WHITE
                texte = FONT.render(str(valeur), True, couleur_texte)
                texte_rect = texte.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(texte, texte_rect)
    
    texte_score = FONT.render(f"Score: {score}", True, GRAY)
    screen.blit(texte_score, (10, SCREEN_SIZE - 50))
    pygame.display.flip()


def jouer_2048_pygame():
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("2048")
    grille = creer_grille_liste(GRID_SIZE)
    score = 0
    ajouter_2_ou_4_aleatoire(grille)
    ajouter_2_ou_4_aleatoire(grille)
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
                    ajouter_2_ou_4_aleatoire(grille)
                    if not mouvement_possible(grille):
                        print(f"{ROUGE}Perdu: aucun mouvement possible{RESET}")
                        running = False
                    elif case_2048_existe(grille):
                        print(f"{VERT}Felicitations vous avez atteint 2048 !{RESET}")
                        running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    jouer_2048_pygame()