# --- Outils de visualisation ---

# ------------------------------------------------------------------------------------------------------------------------------------------

import pygame, math

# Trace un rectangle 
def Rectangle(fenetre, position, dimensions, couleurs, bordure):
    x, y = position
    larg, haut = dimensions
    couleur_debut, couleur_fin = couleurs 
    border_size, border_color = bordure
    
    # pygame.draw.rect(fenetre, couleur_debut, (x, y, larg, haut))
    
    surface = pygame.Surface(dimensions, pygame.SRCALPHA)
    
    # Remplir la surface avec le dégradé
    y_rectangle = 0
    for i in range(haut):
        r = int(couleur_debut[0] + (couleur_fin[0] - couleur_debut[0]) * (i / haut))
        g = int(couleur_debut[1] + (couleur_fin[1] - couleur_debut[1]) * (i / haut))
        b = int(couleur_debut[2] + (couleur_fin[2] - couleur_debut[2]) * (i / haut))
        a = int(couleur_debut[3] + (couleur_fin[3] - couleur_debut[3]) * (i / haut))
        pygame.draw.rect(surface, (r, g, b, a), pygame.Rect(0, y_rectangle, larg, 1))
        y_rectangle += 1
    fenetre.blit(surface, position)
    
    pygame.draw.line(fenetre, border_color, (x, y), (x + larg, y), border_size)
    pygame.draw.line(fenetre, border_color, (x, y + haut), (x + larg, y + haut), border_size)
    pygame.draw.line(fenetre, border_color, (x, y), (x, y + haut), border_size)
    pygame.draw.line(fenetre, border_color, (x + larg, y), (x + larg, y + haut), border_size)


# Trace un arc de cercle
def Arc_circle(fenetre, position, radius, angles, color, border_size=0):
    x, y = position
    start, end = angles
    
    # Convertir les angles en radians
    angle_start = math.radians(start)
    angle_end = math.radians(end)    
    
    pygame.draw.arc(fenetre, color, (x, y, radius, radius), angle_start, angle_end, border_size)


# Affiche un texte
def Texte(fenetre, texte, position, police, taille, couleurs):
    x, y = position
    color, back_color = couleurs 
    
    font = pygame.font.Font(police, taille)
    if back_color != None:
        text_b = font.render(texte, True, back_color)
        fenetre.blit(text_b, (x+2, y+2))
    text = font.render(texte, True, color)
    fenetre.blit(text, (x, y))
    

#  Affiche une ligne en pointillé
def Discontinute_ligne(fenetre, position, longueur, points, direction, color, border_size):
    x, y = position
    trait, interval = points
    
    if direction == 'bas':
        for i in range(y, longueur, interval): 
            pygame.draw.line(fenetre, color, (x, i), (x, i + trait), border_size)