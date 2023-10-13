# --- Visualisation de simulation ---

# ------------------------------------------------------------------------------------------------------------------------------------------

import pygame
from graphic_tools.graph_tools import * # Rectangle, Arc_circle, Segment, Texte

# Couleurs
# https://htmlcolorcodes.com/fr/
blanc = (255, 255, 255)
gris_fonce = (44, 44, 44)
gris = (117, 117, 117)
gris_clair = (156, 156, 156)
noir = (0, 0, 0)
rouge = (255, 0, 0)
vert = (0, 255, 0)
bleu = (0, 0, 255)
jaune = (255, 255, 0)

def render_windows(fenetre):
    largeur_fenetre, hauteur_fenetre = fenetre.get_size()
    
    # Efface l'écran
    fenetre.fill(blanc)
    
    # Appel aux fonctions de rendu de composants
    render_information_panel(fenetre, (0,0), (int(largeur_fenetre / 3), hauteur_fenetre))
    render_intersection(fenetre, (largeur_fenetre // 4, 0), hauteur_fenetre)
    render_stat_panel(fenetre, ((largeur_fenetre // 4)*3, 0), (largeur_fenetre // 4, hauteur_fenetre))
    
    return False


# Paneau d'informations véhicules
def render_information_panel(fenetre, position, panel_size):
    x,y = position
    
    # Fond 
    couleur_debut = (150, 150, 150, 255)  # Gris clair
    couleur_fin = (70, 70, 70, 255)    # Gris foncé
    Rectangle(fenetre, position, panel_size, (couleur_debut, couleur_fin), (1, noir))
    
    # Titre
    Texte(fenetre, "Véhicules :", (x+130, y+8), None, 36, (noir, blanc))
    
    # Légende    
    size_police = 24
    lig = size_police + 4
    col = 46
    marge = 5
    Rectangle(fenetre, (x+marge, y+lig+10), (390,lig), (couleur_fin, couleur_debut), (1, noir))
    
    Texte(fenetre, "N°", (x+marge*2, y+lig+marge+10), None, size_police, (blanc, noir))    
    Texte(fenetre, "vitesse", (x+col*1.1, y+lig+marge+10), None, size_police, (blanc, noir))
    pygame.draw.line(fenetre, gris_clair, (x+col*1.1-marge-2, y+lig+marge+7), (x+col*1.1-marge-2, y+lig+marge+lig+3), 1)
    pygame.draw.line(fenetre, gris_fonce, (x+col*1.1-marge-1, y+lig+marge+7), (x+col*1.1-marge-1, y+lig+marge+lig+3), 1)    
    Texte(fenetre, "temps", (x+col*2.6, y+lig+marge+10), None, size_police, (blanc, noir))
    pygame.draw.line(fenetre, gris_clair, (x+col*2.6-marge-2, y+lig+marge+7), (x+col*2.6-marge-2, y+lig+marge+lig+3), 1)
    pygame.draw.line(fenetre, gris_fonce, (x+col*2.6-marge-1, y+lig+marge+7), (x+col*2.6-marge-1, y+lig+marge+lig+3), 1)
    Texte(fenetre, "dist.", (x+col*4, y+lig+marge+10), None, size_police, (blanc, noir))
    pygame.draw.line(fenetre, gris_clair, (x+col*4-marge-2, y+lig+marge+7), (x+col*4-marge-2, y+lig+marge+lig+3), 1)
    pygame.draw.line(fenetre, gris_fonce, (x+col*4-marge-1, y+lig+marge+7), (x+col*4-marge-1, y+lig+marge+lig+3), 1)
    Texte(fenetre, "crois.", (x+col*5.3, y+lig+marge+10), None, size_police, (blanc, noir))
    pygame.draw.line(fenetre, gris_clair, (x+col*5.3-marge-2, y+lig+marge+7), (x+col*5.3-marge-2, y+lig+marge+lig+3), 1)
    pygame.draw.line(fenetre, gris_fonce, (x+col*5.3-marge-1, y+lig+marge+7), (x+col*5.3-marge-1, y+lig+marge+lig+3), 1)
    Texte(fenetre, "ap.", (x+col*7, y+lig+marge+10), None, size_police, (blanc, noir))
    pygame.draw.line(fenetre, gris_clair, (x+col*7-marge-2, y+lig+marge+7), (x+col*7-marge-2, y+lig+marge+lig+3), 1)
    pygame.draw.line(fenetre, gris_fonce, (x+col*7-marge-1, y+lig+marge+7), (x+col*7-marge-1, y+lig+marge+lig+3), 1)
    
    # Nombre de vehicules par voie
    Rectangle(fenetre, (x+marge, y+lig*26), (390,lig*2+marge*2), (couleur_fin, couleur_debut), (1, noir))
    Texte(fenetre, "Nombre de vehicules par voie :", (x+marge*2, y+lig*26+marge*2), None, size_police, (blanc, noir))

# Panneau des statistiques
def render_stat_panel(fenetre, position, panel_size):  
    x,y = position
    
    # Couleurs
    couleur_debut = (150, 150, 150, 255) # Gris clair
    couleur_fin = (70, 70, 70, 255) # Gris foncé
    couleur_sombre = (20, 20, 20, 255) # Gris sombre
    
    # Fond
    Rectangle(fenetre, position, panel_size, (couleur_debut, couleur_fin), (1, noir))
    
    # Titre
    Texte(fenetre, "Statistiques :", (x+120, y+8), None, 36, (noir, blanc))
    
    # Mise en forme des resultats
    size_police = 24
    lig = size_police + 4
    col = 46
    marge = 5
    
    # Nombres de véhicules total
    Rectangle(fenetre, (x+marge, y+lig+10), (390,size_police), (couleur_fin, couleur_debut), (1, noir))
    
    # Collisions
    Rectangle(fenetre, (x+marge, y+lig*2+10), (390,lig*10), (couleur_fin, couleur_debut), (1, noir))
    Texte(fenetre, "Collisions S1-S4 : ", (x+marge*2, y+lig*2+10+marge), None, size_police, (blanc, noir))
    Texte(fenetre, "Collisions S2-L5 : ", (x+marge*2, y+lig*3+10+marge), None, size_police, (blanc, noir))
    Texte(fenetre, "Collisions S3-L1 : ", (x+marge*2, y+lig*4+10+marge), None, size_police, (blanc, noir))
    Texte(fenetre, "Collisions S4-S1 : ", (x+marge*2, y+lig*5+10+marge), None, size_police, (blanc, noir))
    Texte(fenetre, "Collisions L1-S3 : ", (x+marge*2, y+lig*6+10+marge), None, size_police, (blanc, noir))
    Texte(fenetre, "Collisions L2-L3 : ", (x+marge*2, y+lig*7+10+marge), None, size_police, (blanc, noir))
    Texte(fenetre, "Collisions L3-L2 : ", (x+marge*2, y+lig*8+10+marge), None, size_police, (blanc, noir))
    Texte(fenetre, "Collisions L2-L4 : ", (x+marge*2, y+lig*9+10+marge), None, size_police, (blanc, noir))            
    Texte(fenetre, "Collisions L4-L2 : ", (x+marge*2, y+lig*10+10+marge), None, size_police, (blanc, noir))            
    Texte(fenetre, "Collisions L5-S2 : ", (x+marge*2, y+lig*11+10+marge), None, size_police, (blanc, noir))
    
    Rectangle(fenetre, (x+marge+200, y+lig*6+10), (90,lig*1), (couleur_fin, couleur_sombre), (1, noir))
    Texte(fenetre, "Total : ", (x+marge*2+200, y+lig*6+10+marge), None, size_police, (blanc, noir))
    
    # Graph temps moyen vehicules
    Rectangle(fenetre, (x+marge, y+lig*13), (390,lig*5+marge*2), (couleur_fin, couleur_debut), (1, noir))
    Texte(fenetre, "Temps moyen :", (x+marge*2, y+lig*13+marge*2), None, size_police, (blanc, noir))
    
    # Temps mini et maxi des vehicules
    Rectangle(fenetre, (x+marge, y+lig*19), (390,lig*4+marge*2), (couleur_fin, couleur_debut), (1, noir))
    Texte(fenetre, "Temps minimum et maximum :", (x+marge*2, y+lig*19+marge*2), None, size_police, (blanc, noir))
    
    # Vitesse mini et maxi des vehicules
    Rectangle(fenetre, (x+marge, y+lig*24), (390,lig*2+marge*2), (couleur_fin, couleur_debut), (1, noir))
    Texte(fenetre, "Vitesse minimum et maximum :", (x+marge*2, y+lig*24+marge*2), None, size_police, (blanc, noir))


# Visuel de l'intersection
def render_intersection(fenetre, position, size_intersection):
    x,y = position
    
    # Fond 
    couleur_debut = (100, 100, 100, 255)  # Gris foncé
    couleur_fin = (50, 50, 50, 255)  # Noir
    Rectangle(fenetre, (x,y), (size_intersection, size_intersection), (couleur_debut, couleur_fin), (1, noir))
    
    # Rond point
    radius = 20
    # pygame.draw.circle(fenetre, gris, (x+size_intersection//2, y+size_intersection//2), radius)
    Arc_circle(fenetre, (x+size_intersection//2-radius, y+size_intersection//2-radius), radius*2, (0, 360), gris, 1)
    # Point de rotation
    testx = x + size_intersection // 2
    testy = size_intersection // 2
    pygame.draw.line(fenetre, blanc, (testx, testy), (testx, testy), 1)
    
    # Routes 
    long_voie = size_intersection//2-radius
    larg_voie = 40
    
    # Route nord  
    Road(fenetre, (x-1, y), size_intersection, (long_voie, larg_voie), 'Nord')  
    Road(fenetre, (x-1, y), size_intersection, (long_voie, larg_voie), 'Sud')  
    Road(fenetre, (x-1, y), size_intersection, (long_voie, larg_voie), 'Est')  
    Road(fenetre, (x-1, y), size_intersection, (long_voie, larg_voie), 'Ouest')  


# Trajet d'une route
def Road(fenetre, position, taille, longueur, direction='Nord'):
    x,y = position
    long_voie, larg_voie = longueur
    epaisseur = 1
    
    # Pointillé
    trait = 15
    
    road_surface = pygame.Surface((taille+taille//2, taille), pygame.SRCALPHA)
    
    # pygame.draw.line(road_surface, gris_fonce, (x+long_voie, y), (x+long_voie, taille), epaisseur)  
    Discontinute_ligne(road_surface, (x+long_voie-larg_voie, y), taille, (trait, trait*3), 'bas', gris, epaisseur)
    Discontinute_ligne(road_surface, (x+long_voie-larg_voie*2, y), taille, (trait, trait*3), 'bas', gris, epaisseur)
    
    pygame.draw.line(road_surface, blanc, (x+taille//2-larg_voie//2, y), (x+taille//2-larg_voie//2, long_voie-larg_voie*3), epaisseur)
    pygame.draw.line(road_surface, blanc, (x+taille//2+larg_voie//2, y), (x+taille//2+larg_voie//2, long_voie-larg_voie*3), epaisseur)
    pygame.draw.line(road_surface, blanc, (x+taille//2-larg_voie//2, long_voie-larg_voie*3), (x+taille//2+larg_voie//2, long_voie-larg_voie*3), epaisseur)
    
    # Right
    Texte(road_surface, 'R', (x+long_voie-larg_voie*3+14, y+5), None, 24, (blanc, noir))
    pygame.draw.line(road_surface, blanc, (x+long_voie-larg_voie*3, y), (x+long_voie-larg_voie*3, long_voie-larg_voie*3), epaisseur)
    pygame.draw.line(road_surface, blanc, (x+long_voie-larg_voie*3, long_voie-larg_voie*3), (x, long_voie-larg_voie*3), epaisseur)
    
    # Straigth
    Texte(road_surface, 'S', (x+long_voie-larg_voie*2+14, y+5), None, 24, (blanc, noir))
    
    # Left
    Texte(road_surface, 'L', (x+long_voie-larg_voie+14, y+5), None, 24, (blanc, noir))
    
    couleur_bleu_f = (112, 194, 185, 255)  
    couleur_bleu_d = (31, 90, 84, 255)

    couleur_vert_f = (120, 179, 101, 255)  
    couleur_vert_d = (33, 84, 25, 255)

    couleur_jaune_f = (172, 126, 202, 255)  
    couleur_jaune_d = (60, 25, 82, 255)

    couleur_mauve_f = (218, 171, 70, 255)  
    couleur_mauve_d = (91, 71, 26 , 255)
    
    rotated_rect = road_surface.get_rect()
    if direction == 'Nord':
        Texte(road_surface, "Nord", (x+200, y+20), None, 26, (couleur_bleu_f, noir))
    elif direction == 'Sud':
        Texte(road_surface, "Sud", (x+200, y+20), None, 26, (couleur_vert_f, noir))
        road_surface = pygame.transform.rotate(road_surface, 180)
        rotated_rect.center = (x//2 + taille , y + taille//2 )
    elif direction == 'Est':
        Texte(road_surface, "Est", (x+200, y+20), None, 26, (couleur_jaune_f, noir))
        road_surface = pygame.transform.rotate(road_surface, -90)
        rotated_rect.center = (x + 600 + 1 , y)
    elif direction == 'Ouest':
        Texte(road_surface, "Ouest", (x+200, y+20), None, 26, (couleur_mauve_f, noir))
        road_surface = pygame.transform.rotate(road_surface, 90)
        rotated_rect.center = (x + 600 , y + taille//2)

    # Dessinez la route sur la fenêtre principale
    fenetre.blit(road_surface, rotated_rect.topleft)


