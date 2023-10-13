# --- Class ---

# ------------------------------------------------------------------------------------------------------------------------------------------

import pygame
from graphic_tools.graph_tools import Rectangle, Texte

class Intersection:
    def __init__(self):
        self.vehicles_datas = []
        self.vehicles = []
        self.nb_vehicule_R = 0
        self.nb_vehicule_S = 0
        self.nb_vehicule_L = 0
        self.croisement_S = [229, 269, 359, 399]
        self.croisement_L = [229, 269, 359, 434, 514]
        self.collisions = {
            'S1-S4': 0,
            'S2-L5': 0,
            'S3-L1': 0,
            'S4-S1': 0,
            'L1-S3': 0,
            'L2-L3': 0,
            'L3-L2': 0,
            'L2-L4': 0,
            'L4-L2': 0,
            'L5-S2': 0
        }
        self.provenances = ["Nord", "Ouest", "Sud", "Est"]
        self.nbCollisions = 0


    def getVehicleIndexById(self, id):
        for index, v in enumerate(self.vehicles):
            if v.id is id:
                return index
        return -1  # Retourne -1 si le véhicule n'est pas trouvé dans la liste


    # Ajouter un véhicule à l'intersection
    def add_vehicle(self, vehicle):        
        self.vehicles.append(vehicle)
        self.vehicles_datas.append(vehicle)
        if vehicle.voie == 'Right': self.nb_vehicule_R +=1
        if vehicle.voie == 'Straight': self.nb_vehicule_S +=1
        if vehicle.voie == 'Left': self.nb_vehicule_L +=1
        
        if len(self.vehicles) > 1:
            for i,v in enumerate(self.vehicles):
                # Si le vehicule précédent est trop prét on autorise pas la création du suivant en le supprimant
                if vehicle.id > v.id and vehicle.provenance == v.provenance and vehicle.voie == v.voie:
                    if v.safeDistance - v.distance >= 0:
                        self.vehicles.remove(vehicle)
                        self.vehicles_datas.remove(vehicle)


    # Retirer un véhicule de l'intersection
    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)
        if vehicle.voie == 'Right': self.nb_vehicule_R -=1
        if vehicle.voie == 'Straight': self.nb_vehicule_S -=1
        if vehicle.voie == 'Left': self.nb_vehicule_L -=1


# --- Visuel ---
    # Mettre à jour l'état de l'intersection
    def update_state(self, time):
        for vehicle in self.vehicles:
            vehicle.move(time)
            # Gérer les collisions et les distances de sécurité
            for other_vehicle in self.vehicles:
                if vehicle != other_vehicle and vehicle.check_collision(other_vehicle):
                    vehicle.maintain_safe_distance(other_vehicle)


    # Paneau des statistiques
    def render_stat(self, fenetre):  
        largeur_fenetre, hauteur_fenetre = fenetre.get_size()
        position = ((largeur_fenetre // 4)*3, 0)      
        x,y = position
        panel_size = (largeur_fenetre // 4, hauteur_fenetre)
        
        # couleur
        blanc = (255, 255, 255)
        noir = (0, 0, 0)
        rouge = (255, 70, 70)
        jaune = (255, 255, 0)
        couleur_debut = (150, 150, 150, 255) # Gris clair
        couleur_fin = (70, 70, 70, 255) # Gris foncé
        
        # Mise en forme des resultats
        size_police = 24
        lig = size_police + 4
        col = 46
        marge = 5
        
        # Nombres de véhicules total
        Texte(fenetre, "Nb Vehicules : ", (x+marge*2, y+lig+10+marge), None, size_police, (blanc, noir))
        Texte(fenetre, str(len(self.vehicles_datas)), (x+marge*2+120, y+lig+10+marge), None, size_police, (jaune, noir))
        
        # Collisions
        Texte(fenetre, str(self.nbCollisions), (x+marge*2+250, y+lig*6+10+marge), None, size_police, (rouge, noir))
        
        if self.collisions['S1-S4'] != 0:
            Texte(fenetre, str(self.collisions['S1-S4']), (x+marge*2+140, y+lig*2+10+marge), None, size_police, (jaune, noir))
        
        if self.collisions['S2-L5'] != 0:
            Texte(fenetre, str(self.collisions['S2-L5']), (x+marge*2+140, y+lig*3+10+marge), None, size_police, (jaune, noir))

        if self.collisions['S3-L1'] != 0:
            Texte(fenetre, str(self.collisions['S3-L1']), (x+marge*2+140, y+lig*4+10+marge), None, size_police, (jaune, noir))

        if self.collisions['S4-S1'] != 0:
            Texte(fenetre, str(self.collisions['S4-S1']), (x+marge*2+140, y+lig*5+10+marge), None, size_police, (jaune, noir))

        if self.collisions['L1-S3'] != 0:
            Texte(fenetre, str(self.collisions['L1-S3']), (x+marge*2+140, y+lig*6+10+marge), None, size_police, (jaune, noir))

        if self.collisions['L2-L3'] != 0:
            Texte(fenetre, str(self.collisions['L2-L3']), (x+marge*2+140, y+lig*7+10+marge), None, size_police, (jaune, noir))

        if self.collisions['L3-L2'] != 0:
            Texte(fenetre, str(self.collisions['L3-L2']), (x+marge*2+140, y+lig*8+10+marge), None, size_police, (jaune, noir))

        if self.collisions['L2-L4'] != 0:
            Texte(fenetre, str(self.collisions['L2-L4']), (x+marge*2+140, y+lig*9+10+marge), None, size_police, (jaune, noir))
            
        if self.collisions['L4-L2'] != 0:
            Texte(fenetre, str(self.collisions['L4-L2']), (x+marge*2+140, y+lig*10+10+marge), None, size_police, (jaune, noir))

        if self.collisions['L5-S2'] != 0:
            Texte(fenetre, str(self.collisions['L5-S2']), (x+marge*2+140, y+lig*11+10+marge), None, size_police, (jaune, noir))

        #  Couleurs graphique
        couleur_bleu_f = (112, 194, 185, 255)  
        couleur_bleu_d = (31, 90, 84, 255)
        
        couleur_vert_f = (120, 179, 101, 255)  
        couleur_vert_d = (33, 84, 25, 255)

        couleur_mauve_f = (172, 126, 202, 255)  
        couleur_mauve_d = (60, 25, 82, 255)

        couleur_jaune_f = (218, 171, 70, 255)  
        couleur_jaune_d = (255, 255, 26 , 255)

        couleur_blanc_d = (200, 200, 200 , 255)         
        
        # Graph temps vehicules
        tps_moy = 0
        
        tps_min_R = 0
        tps_max_R = 0
        tps_moy_R = 0
        v_R = 0
        
        tps_min_S = 0
        tps_max_S = 0
        tps_moy_S = 0
        v_S = 0
        
        tps_min_L = 0
        tps_max_L = 0
        tps_moy_L = 0
        v_L = 0
        
        vit_min = 0
        vit_max = 0
        
        if len(self.vehicles_datas) > 0:
            for i,v in enumerate(self.vehicles_datas):                
                tps_moy = tps_moy + v.time
                if v.velocity <= vit_min or vit_min == 0: vit_min = round(v.velocity, 2)
                if v.velocity >= vit_max : vit_max = round(v.velocity, 2)
                
                if v.voie == "Right":
                    v_R +=1
                    tps_moy_R = tps_moy_R + v.time
                    if v.time <= tps_min_R or tps_min_R == 0: tps_min_R = round(v.time, 2)
                    if v.time >= tps_max_R: tps_max_R = round(v.time, 2)
                elif v.voie == "Straight":
                    v_S +=1
                    tps_moy_S = tps_moy_S + v.time
                    if v.time <= tps_min_S or tps_min_S == 0: tps_min_S = round(v.time, 2)
                    if v.time >= tps_max_S: tps_max_S = round(v.time, 2)
                elif v.voie == "Left":
                    v_L +=1
                    tps_moy_L = tps_moy_L + v.time
                    if v.time <= tps_min_L or tps_min_L == 0: tps_min_L = round(v.time, 2)
                    if v.time >= tps_max_L: tps_max_L = round(v.time, 2)
            
            if v_R > 0 : tps_moy_R = round(tps_moy_R / v_R, 2)
            if v_S > 0 : tps_moy_S = round(tps_moy_S / v_S, 2)
            if v_L > 0 : tps_moy_L = round(tps_moy_L / v_L, 2)
            tps_moy = round(tps_moy / len(self.vehicles_datas), 2)
                    
        Texte(fenetre, "Right: ", (x+marge*2, y+lig*14+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(v_R), (x+marge*2+74, y+lig*14+marge*2), None, size_police, (jaune, noir))
        Rectangle(fenetre, (x+marge*2+110, y+lig*14+marge), (tps_moy_R*60, lig-2), (couleur_bleu_d, couleur_blanc_d), (1, noir))
        Texte(fenetre, str(tps_moy_R), (x+marge*2+114, y+lig*14+marge*2), None, size_police, (jaune, noir))
        
        Texte(fenetre, "Straight: ", (x+marge*2, y+lig*15+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(v_S), (x+marge*2+74, y+lig*15+marge*2), None, size_police, (jaune, noir))
        Rectangle(fenetre, (x+marge*2+110, y+lig*15+marge), (tps_moy_S*60, lig-2), (couleur_vert_d, couleur_blanc_d), (1, noir))
        Texte(fenetre, str(tps_moy_S), (x+marge*2+114, y+lig*15+marge*2), None, size_police, (jaune, noir))
        
        Texte(fenetre, "Left: ", (x+marge*2, y+lig*16+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(v_L), (x+marge*2+74, y+lig*16+marge*2), None, size_police, (jaune, noir))
        Rectangle(fenetre, (x+marge*2+110, y+lig*16+marge), (tps_moy_L*60, lig-2), (couleur_mauve_d, couleur_blanc_d), (1, noir))
        Texte(fenetre, str(tps_moy_L), (x+marge*2+114, y+lig*16+marge*2), None, size_police, (jaune, noir))
        
        Texte(fenetre, "Total: ", (x+marge*2, y+lig*17+marge*2), None, size_police, (jaune, noir))
        Texte(fenetre, str(len(self.vehicles_datas)), (x+marge*2+74, y+lig*17+marge*2), None, size_police, (jaune, noir))
        Rectangle(fenetre, (x+marge*2+110, y+lig*17+marge), (tps_moy*60, lig-2), (couleur_jaune_f, couleur_jaune_d), (1, noir))
        Texte(fenetre, str(tps_moy), (x+marge*2+114, y+lig*17+marge*2), None, size_police, (blanc, noir))
        
        # Temps mini et maxi des vehicules
        Texte(fenetre, "Tps Right ", (x+marge*2, y+lig*20+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, "mini : ", (x+marge*2+120, y+lig*20+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(tps_min_R), (x+marge*2+170, y+lig*20+marge*2), None, size_police, (jaune, noir))
        Texte(fenetre, "maxi : ", (x+marge*2+240, y+lig*20+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(tps_max_R), (x+marge*2+300, y+lig*20+marge*2), None, size_police, (jaune, noir))
        
        Texte(fenetre, "Tps Straight ", (x+marge*2, y+lig*21+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, "mini : ", (x+marge*2+120, y+lig*21+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(tps_min_S), (x+marge*2+170, y+lig*21+marge*2), None, size_police, (jaune, noir))
        Texte(fenetre, "maxi : ", (x+marge*2+240, y+lig*21+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(tps_max_S), (x+marge*2+300, y+lig*21+marge*2), None, size_police, (jaune, noir))
        
        Texte(fenetre, "Tps Left ", (x+marge*2, y+lig*22+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, "mini : ", (x+marge*2+120, y+lig*22+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(tps_min_L), (x+marge*2+170, y+lig*22+marge*2), None, size_police, (jaune, noir))
        Texte(fenetre, "maxi : ", (x+marge*2+240, y+lig*22+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(tps_max_L), (x+marge*2+300, y+lig*22+marge*2), None, size_police, (jaune, noir))
        
        # Vitesse mini et maxi des vehicules
        Texte(fenetre, "Vitesse ", (x+marge*2, y+lig*25+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, "mini : ", (x+marge*2+120, y+lig*25+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(vit_min), (x+marge*2+170, y+lig*25+marge*2), None, size_police, (jaune, noir))
        Texte(fenetre, "maxi : ", (x+marge*2+240, y+lig*25+marge*2), None, size_police, (blanc, noir))
        Texte(fenetre, str(vit_max), (x+marge*2+300, y+lig*25+marge*2), None, size_police, (jaune, noir))
