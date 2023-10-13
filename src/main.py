
import sys, pygame, random, cProfile
from render_windows import render_windows 
from clsVehicle import Vehicle
from clsIntersection import Intersection

def main():    
    # Initialisation de Pygame
    pygame.init()

    # Création de la fenêtre
    largeur_fenetre = 1600
    hauteur_fenetre = largeur_fenetre / 2
    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    pygame.display.set_caption("Projet Zone01 :                                                                                     Smart Road                                                             Tony Quedeville 06/09/2024")
    
    # Création de l'horloge (cadence de jeu)
    clock = pygame.time.Clock()
    tps_add_v = 0
    

    # Créer une instance d'intersection
    intersection = Intersection()
    render_windows(fenetre) # Appel de la fonction d'affichage de l'intersection
    
    # Boucle principale
    running = True
    while running:
        temps_actuel = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                running = False
            
            elif event.type == pygame.KEYDOWN:
                create_vehicle = False
                
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN: 
                    provenance = 'Nord'
                    create_vehicle = True
                elif event.key == pygame.K_UP: 
                    provenance = 'Sud'
                    create_vehicle = True
                elif event.key == pygame.K_LEFT: 
                    provenance = 'Est'
                    create_vehicle = True
                elif event.key == pygame.K_RIGHT: 
                    provenance = 'Ouest'
                    create_vehicle = True
                elif event.key == pygame.K_r or event.key == pygame.K_R: 
                    provenance = random.choice(['Nord', 'Sud', 'Est', 'Ouest'])
                    create_vehicle = True
        
                if create_vehicle:
                    voie_aleatoire = ['Right', 'Straight', 'Left']
                    if intersection.nb_vehicule_R >= 5 : voie_aleatoire.remove('Right')
                    if intersection.nb_vehicule_S >= 5 : voie_aleatoire.remove('Straight')
                    if intersection.nb_vehicule_L >= 5 : voie_aleatoire.remove('Left')
                    if len(voie_aleatoire) > 0:
                        new_vehicle = Vehicle(  intersection = intersection,
                                            # voie=random.choice(['Straight']), 
                                            # voie=random.choice(['Left']), 
                                            voie=random.choice(voie_aleatoire), 
                                            provenance=provenance,
                                        )
                        create_vehicle = False
                        if tps_add_v + 200 < temps_actuel and len(intersection.vehicles) <= 10 : 
                            intersection.add_vehicle(new_vehicle)
                        tps_add_v = temps_actuel
        
        render_windows(fenetre)

        for vehicle in intersection.vehicles:            
            if vehicle.move(temps_passe):
                intersection.remove_vehicle(vehicle)
            else:
                vehicle.render_info_vehicle(fenetre, intersection)
            vehicle.render_vehicles(fenetre)
        
        intersection.render_stat(fenetre)
        pygame.display.flip() # Met à jour l'affichage
        
        temps_passe = pygame.time.get_ticks() - temps_actuel
        
        # Limiter la boucle à x FPS (cadence de jeu)
        clock.tick_busy_loop(10)
    
    pygame.quit()
    sys.exit()
    


if __name__ == "__main__":
    main()
    # cProfile.run("main()", sort='cumulative')