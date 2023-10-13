# --- Class ---

# ------------------------------------------------------------------------------------------------------------------------------------------

from ast import And
from operator import truediv
import pygame
from graphic_tools.graph_tools import Rectangle, Texte, Arc_circle

class Vehicle:
    def __init__(self, intersection, voie, provenance):
        self.intersection = intersection
        self.id = len(intersection.vehicles_datas) + 1
        self.velocity = 0                   # vitesse instantanée (pixel/ms)
        self.velocityMax = 0                # vitesse maximum atteinte (pixel/ms)
        self.velocityMin = 0                # vitesse minimum atteinte (pixel/ms)
        self.fast = 250                     # rapports de vitesse rapide 
        self.med = 150                      # rapports de vitesse modérée 
        self.slow = 25                      # rapports de vitesse lente
        self.stop = 0                       # freinage
        self.speed = self.fast              # vitesse de consigne (pixel/ms)
        self.time = 0                       # temps écoulé depuis l'entrée dans l'intersection (ms)
        self.distance = 0                   # distance parcourue depuis l'entrée dans l'intersection (pixel)
        self.larg = 30                      # largeur du vehicule
        self.long = 40                      # longueur du vehicule
        self.safeDistance = self.long * 2   # distance de sécurité (pixel)
        self.voie = voie                    # voie (L,S,R) Left:gauche, Straight:centre, Rigth:droite. determine la direction à suivre
        self.provenance = provenance        # Nord, Ouest, Sud, Est
        self.croisement_ap = []             # Croisements dont le vehicule s'approche à l'instant T
        self.croisement = []                # Croisements dans lequel le vehicule se trouve à l'instant T
        self.collision = ''                 # Collision du vehicule
        
        # Parametres visuels
        self.position = (0, 0)                          # position graphique (pixel) correspond à l'arrière du vehicule
        self.rotate = (0)                               # rotation graphique (pixel) tourne le vehicule lorsqu'il prend le virage (Left ou Right)
        
        self.id_info = len(intersection.vehicles) + 1   # position graphique (pixel)
        if self.voie == 'Left':
            self.position = (344, 30)                   # position graphique (pixel)
        elif self.voie == 'Straight':
            self.position = (304, 30)                   # position graphique (pixel)
        elif self.voie == 'Right':
            self.position = (264, 30)                   # position graphique (pixel)
        
        if self.provenance == "Nord":            
            self.couleur_v_f = (112, 194, 185, 255)  
            self.couleur_v_d = (31, 90, 84, 255)
        elif self.provenance == "Sud":            
            self.couleur_v_f = (120, 179, 101, 255)  
            self.couleur_v_d = (33, 84, 25, 255)
        elif self.provenance == "Est":            
            self.couleur_v_f = (172, 126, 202, 255)  
            self.couleur_v_d = (60, 25, 82, 255)
        elif self.provenance == "Ouest":            
            self.couleur_v_f = (218, 171, 70, 255)  
            self.couleur_v_d = (91, 71, 26 , 255)


    # Vérifier si le véhicule se trouve dans un croisement (collision potentielle)
    def check_croisement(self):
        cr = ''
        if self.voie == 'Straight':
            croisements = self.intersection.croisement_S
            voie = 'S'
        if self.voie == 'Left':
            croisements = self.intersection.croisement_L
            voie = 'L'

        croisements_occupes = []
        croisements_approche = []

        if self.voie != 'Right':
            for i, dist in enumerate(croisements): # Test sur l'avant du vehicule
                cr = voie + str(i+1)
                if dist <= self.distance < dist + 40:
                    croisements_occupes.append({
                                                "id": self.id,
                                                "cr": cr
                                                })
                elif dist <= self.distance + self.long < dist + 40:
                    croisements_approche.append({
                                                "id": self.id,
                                                "cr": cr,
                                                "rl": 1
                                                })
                elif dist <= self.distance + self.long*2 < dist + 40:
                    croisements_approche.append({
                                                "id": self.id,
                                                "cr": cr,
                                                "rl": 2
                                                })
                elif dist <= self.distance + self.long*3 < dist + 40:
                    croisements_approche.append({
                                                "id": self.id,
                                                "cr": cr,
                                                "rl": 3
                                                })
                    break
            
            for i, dist in enumerate(croisements): # Test sur l'arrière du vehicule
                cr = voie + str(i+1)
                if dist <= self.distance - self.long < dist + 40:
                    croisements_occupes.append({
                                                "id": self.id,
                                                "cr": cr
                                                })
                elif dist <= self.distance < dist + 40:
                    croisements_approche.append({
                                                "id": self.id,
                                                "cr": cr,
                                                "rl": 0
                                                })
                else:
                    self.speed = self.fast
                    break
            
            self.croisement = croisements_occupes
            self.croisement_ap = croisements_approche


    # Maintien une distance de sécurité par rapport à un autre véhicule
    def maintain_safe_distance(self):
        for i,v in enumerate(self.intersection.vehicles):
            if self.provenance == v.provenance and self.voie == v.voie and self.id > v.id:
                if self.distance + self.long*3 - v.distance >= 0:
                    self.speed = self.med // 2
                if self.distance + self.long*2 - v.distance >= 0:
                    self.speed = self.med
                if self.distance + self.long - v.distance >= 0:
                    self.speed = self.slow


    # Vérifier s'il y a une collision avec un autre véhicule
    def check_collision(self):
        ip = 0 # index de provenances ["Nord", "Ouest", "Sud", "Est"]
        for index, p in enumerate(self.intersection.provenances):
            if self.provenance == p:
                ip = index
                break
        
        for index, v in enumerate(self.intersection.vehicles):
            # ip+1 = v viens de la droite. ip+2 = v viens d'en face. ip+3 = v viens de la gauche.
            if self.voie == 'Straight':
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)                            
                            if scr["cr"] == 'S1' and vcr["cr"] == 'S4':
                                if self.collision == '':
                                    self.collision = 'S1-S4'
                                    self.intersection.collisions['S1-S4'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True
                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+1
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la droite (ip+1)
                            if scr["cr"] == 'S4' and vcr["cr"] == 'S1':
                                if self.collision == '':
                                    self.collision = 'S4-S1'
                                    self.intersection.collisions['S4-S1'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True
                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'S2' and vcr["cr"] == 'L5':
                                v.speed = v.stop
                                if self.collision == '':
                                    self.collision = 'S2-L5'
                                    self.intersection.collisions['S2-L5'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True
                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+1
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la droite (ip+1)
                            if scr["cr"] == 'S3' and vcr["cr"] == 'L1':
                                if self.collision == '':
                                    self.collision = 'S3-L1'
                                    self.intersection.collisions['S3-L1'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True
            
            if self.voie == 'Left':
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)
                            if scr["cr"] == 'L1' and vcr["cr"] == 'S3':
                                if self.collision == '':
                                    self.collision = 'L1-S3'
                                    self.intersection.collisions['L1-S3'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True

                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)
                            if scr["cr"] == 'L2' and vcr["cr"] == 'L3':
                                if self.collision == '':
                                    self.collision = 'L2-L3'
                                    self.intersection.collisions['L2-L3'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True

                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+1
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la droite (ip+1)
                            if scr["cr"] == 'L3' and vcr["cr"] == 'L2':
                                if self.collision == '':
                                    self.collision = 'L3-L2'
                                    self.intersection.collisions['L3-L2'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True

                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L2' and vcr["cr"] == 'L4':
                                if self.collision == '':
                                    self.collision = 'L2-L4'
                                    self.intersection.collisions['L2-L4'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True
                                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L4' and vcr["cr"] == 'L2':
                                if self.collision == '':
                                    self.collision = 'L4-L2'
                                    self.intersection.collisions['L4-L2'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True
                                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L4' and vcr["cr"] == 'L2':
                                if self.collision == '':
                                    self.collision = 'L4-L2'
                                    self.intersection.collisions['L4-L2'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True

                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L5' and vcr["cr"] == 'S2':
                                if self.collision == '':
                                    self.collision = 'L5-S2'
                                    self.intersection.collisions['L5-S2'] += 1
                                    self.intersection.remove_vehicle(v)
                                    return True
        return False


    # Ralentir à proximité d'un autre véhicule dans un croisement
    def proxi_crois(self):
        ip = 0 # index de provenances ["Nord", "Ouest", "Sud", "Est"]
        for index, p in enumerate(self.intersection.provenances):
            if self.provenance == p:
                ip = index
                break
        
        for index, v in enumerate(self.intersection.vehicles):            
            # ip+1 = v viens de la droite. ip+2 = v viens d'en face. ip+3 = v viens de la gauche.
            if self.voie == 'Straight':
                for i, scr in enumerate(self.croisement):                            
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)                            
                            if scr["cr"] == 'S1' and vcr["cr"] == 'S4' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break
                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+1
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la droite (ip+1)                            
                            if scr["cr"] == 'S4' and vcr["cr"] == 'S1' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break
                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'S2' and vcr["cr"] == 'L5' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break
                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+1
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la droite (ip+1)
                            if scr["cr"] == 'S3' and vcr["cr"] == 'L1' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break

            
            if self.voie == 'Left':
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)
                            if scr["cr"] == 'L1' and vcr["cr"] == 'S3' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break

                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)
                            if scr["cr"] == 'L2' and vcr["cr"] == 'L3' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break

                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+1
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la droite (ip+1)
                            if scr["cr"] == 'L3' and vcr["cr"] == 'L2' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break

                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L4' and vcr["cr"] == 'L2' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break
                
                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L2' and vcr["cr"] == 'L4' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break

                for i, scr in enumerate(self.croisement):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L5' and vcr["cr"] == 'S2' and scr["id"] != vcr["id"]:
                                self.speed = self.fast
                                v.speed = self.slow
                                break


    # Ralentir 1 des 2 vehicules à proximité d'un croisement
    def proxi(self):
        ip = 0 # index de provenances ["Nord", "Ouest", "Sud", "Est"]
        for index, p in enumerate(self.intersection.provenances):
            if self.provenance == p:
                ip = index
                break
        
        for index, v in enumerate(self.intersection.vehicles):            
            # ip+1 = v viens de la droite. ip+2 = v viens d'en face. ip+3 = v viens de la gauche.
            if self.voie == 'Straight':
                for i, scr in enumerate(self.croisement_ap):                            
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)                            
                            if scr["cr"] == 'S1' and vcr["cr"] == 'S4' and scr["id"] != vcr["id"]:
                                # v.speed = self.fast
                                if vcr["rl"] == 3 :
                                    self.speed = self.med
                                elif vcr["rl"] == 2 :
                                    self.speed = self.med//2
                                elif vcr["rl"] == 1 :
                                    self.speed = self.slow
                                break

                for i, scr in enumerate(self.croisement_ap):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'S2' and vcr["cr"] == 'L5' and scr["id"] != vcr["id"]:
                                # v.speed = self.fast
                                if vcr["rl"] == 3 :
                                    self.speed = self.med
                                elif vcr["rl"] == 2 :
                                    self.speed = self.med//2
                                elif vcr["rl"] == 1 :
                                    self.speed = self.slow
                                break

            if self.voie == 'Left':
                for i, scr in enumerate(self.croisement_ap):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)
                            if scr["cr"] == 'L1' and vcr["cr"] == 'S3' and scr["id"] != vcr["id"]:
                                # v.speed = self.fast
                                if vcr["rl"] == 3 :
                                    self.speed = self.med
                                elif vcr["rl"] == 2 :
                                    self.speed = self.med//2
                                elif vcr["rl"] == 1 :
                                    self.speed = self.slow
                                break
                
                for i, scr in enumerate(self.croisement_ap):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+3
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens de la gauche (ip+3)
                            if scr["cr"] == 'L2' and vcr["cr"] == 'L3' and scr["id"] != vcr["id"]:
                                # v.speed = self.fast
                                if vcr["rl"] == 3 :
                                    self.speed = self.med
                                elif vcr["rl"] == 2 :
                                    self.speed = self.med//2
                                elif vcr["rl"] == 1 :
                                    self.speed = self.slow
                                break
                
                for i, scr in enumerate(self.croisement_ap):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L2' and vcr["cr"] == 'L4' and scr["id"] != vcr["id"]:
                                # v.speed = self.fast
                                if vcr["rl"] == 3 :
                                    self.speed = self.med
                                elif vcr["rl"] == 2 :
                                    self.speed = self.med//2
                                elif vcr["rl"] == 1 :
                                    self.speed = self.slow
                                break
                
                # for i, scr in enumerate(self.croisement_ap):
                #     for i, vcr in enumerate(v.croisement_ap):
                #         i = ip+2
                #         if i >= 4: i = i-4
                #         if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                #             if scr["cr"] == 'L4' and vcr["cr"] == 'L2' and scr["id"] != vcr["id"]:
                #                 self.speed = self.fast
                #                 v.speed = self.slow
                #                 break
                
                for i, scr in enumerate(self.croisement_ap):
                    for i, vcr in enumerate(v.croisement_ap):
                        i = ip+2
                        if i >= 4: i = i-4
                        if v.provenance == self.intersection.provenances[i]: # si v viens d'en face (ip+2)
                            if scr["cr"] == 'L5' and vcr["cr"] == 'S2' and scr["id"] != vcr["id"]:
                                # v.speed = self.fast
                                if vcr["rl"] == 3 :
                                    self.speed = self.med
                                elif vcr["rl"] == 2 :
                                    self.speed = self.med//2
                                elif vcr["rl"] == 1 :
                                    self.speed = self.slow
                                break


    # Calculer la nouvelle position en fonction de la vitesse et du temps
    def move(self, time):
        dist_left_rotate = 424    # distance à laquelle le vehicule tourne à gauche
        dist_right_rotate = 264   # distance à laquelle le vehicule tourne à droite
        
        x,y = self.position
        self.time += round(time / 1000, 2)
        self.distance += int(self.speed * time / 1000)
        self.velocity = int(self.speed * time / 1000)
        
        if self.voie == 'Left':
            if self.distance >= dist_left_rotate - self.long*1 and self.rotate < 90:
                self.rotate += 15
                if self.rotate > 90: self.rotate = 90
                
            if y >= dist_left_rotate:
                self.position = (x + self.velocity, dist_left_rotate)
            else:
                self.position = (x, y + self.velocity)

        elif self.voie == 'Right':
            if self.distance >= dist_right_rotate - self.long and self.rotate > -90:
                self.rotate -= 30
                if self.rotate < -90: self.rotate = -90
            
            if y >= dist_right_rotate:
                self.position = (x - self.velocity, dist_right_rotate)
            else:
                self.position = (x, y + self.velocity)
        
        else:
            self.position = (x, y + self.velocity)
        
        # Test si collision
        self.check_croisement()
        if self.croisement != '':
            if self.check_collision():
                self.intersection.remove_vehicle(self)
                self.intersection.nbCollisions += 1

        # Test si distance de securité atteinte
        self.proxi_crois()
        self.proxi()
        self.maintain_safe_distance()
        
        # Sortie du vehicule de l'intersection
        if self.voie == "Right" and self.distance >= 550:
            return True
        elif self.voie == "Straight" and self.distance >= 760:
            return True
        elif self.voie == "Left" and self.distance >= 840:
            return True
        else:
            return False


    # Paneau d'informations
    def render_info_vehicle(self, fenetre, intersection):
        size_police = 24
        lig = size_police + 4
        col = 46
        marge = 5
        x,y = marge, lig + 40 - (intersection.getVehicleIndexById(self.id)) * -size_police
        
        #  Couleurs
        blanc = (255, 255, 255)
        gris_fonce = (44, 44, 44)
        noir = (0, 0, 0)
        rouge = (200, 0, 0)
        jaune = (255, 255, 0)
        vert = (0, 255, 0)
        
        # Fond 
        Rectangle(fenetre, (x,y), (390,size_police+lig), (self.couleur_v_d, self.couleur_v_f), (1, noir))
        
        # Titre
        Texte(fenetre, str(self.id), (x+marge, y+marge), None, size_police, (blanc, noir))        
        
        Texte(fenetre, str(self.velocity), (x+col*1.2, y+marge), None, size_police, (blanc, noir))
        pygame.draw.line(fenetre, self.couleur_v_f, (x+col*1.2-marge*3-2, y+2), (x+col*1.2-marge*3-2, y+size_police), 1)
        pygame.draw.line(fenetre, self.couleur_v_d, (x+col*1.2-marge*3-1, y+2), (x+col*1.2-marge*3-1, y+size_police), 1)  
        
        Texte(fenetre, "{:.2f}".format(self.time), (x+col*2.6, y+marge), None, size_police, (blanc, noir))
        pygame.draw.line(fenetre, self.couleur_v_f, (x+col*2.6-marge*2-2, y+2), (x+col*2.6-marge*2-2, y+size_police), 1)
        pygame.draw.line(fenetre, self.couleur_v_d, (x+col*2.6-marge*2-1, y+2), (x+col*2.6-marge*2-1, y+size_police), 1)
        
        Texte(fenetre, str(self.distance), (x+col*4, y+marge), None, size_police, (blanc, noir))
        pygame.draw.line(fenetre, self.couleur_v_f, (x+col*4-marge*2-2, y+2), (x+col*4-marge*2-2, y+size_police), 1)
        pygame.draw.line(fenetre, self.couleur_v_d, (x+col*4-marge*2-1, y+2), (x+col*4-marge*2-1, y+size_police), 1)
        
        if self.croisement != []:
            cr = self.croisement[0]["cr"]
            if len(self.croisement) > 1:
                cr = cr + " " + self.croisement[1]["cr"]
            Texte(fenetre, cr, (x+col*5.3, y+marge), None, size_police, (jaune, noir))
        pygame.draw.line(fenetre, self.couleur_v_f, (x+col*5.3-marge*2-2, y+2), (x+col*5.3-marge*2-2, y+size_police), 1)
        pygame.draw.line(fenetre, self.couleur_v_d, (x+col*5.3-marge*2-1, y+2), (x+col*5.3-marge*2-1, y+size_police), 1)
        
        if self.croisement_ap != []:
            ap = self.croisement_ap[0]["cr"]
            if len(self.croisement_ap) > 1:
                ap = ap + " " + self.croisement_ap[1]["cr"]
            Texte(fenetre, ap, (x+col*6.8+marge, y+marge), None, size_police, (vert, noir))
        pygame.draw.line(fenetre, self.couleur_v_f, (x+col*6.8-2, y+2), (x+col*6.8-2, y+size_police), 1)
        pygame.draw.line(fenetre, self.couleur_v_d, (x+col*6.8-1, y+2), (x+col*6.8-1, y+size_police), 1)
        
        Texte(fenetre, "Route : " + self.provenance, (x+marge*2, y+lig), None, size_police, (gris_fonce, self.couleur_v_f))
        Texte(fenetre, "Voie : " + self.voie, (x+col*3+marge*2, y+lig), None, size_police, (gris_fonce, self.couleur_v_f))
        Texte(fenetre, "Securité : " + str(self.safeDistance), (x+col*6+marge, y+lig), None, size_police, (gris_fonce, self.couleur_v_f))
        
        # Nombre de vehicules par voie
        y = lig + 40
        Texte(fenetre, "Right : ", (x+marge*2, y+lig*25), None, size_police, (blanc, noir))
        Texte(fenetre, str(self.intersection.nb_vehicule_R), (x+marge*2+56, y+lig*25), None, size_police, (jaune, noir))
        Texte(fenetre, "Straight : ", (x+marge*2+120, y+lig*25), None, size_police, (blanc, noir))
        Texte(fenetre, str(self.intersection.nb_vehicule_S), (x+marge*2+200, y+lig*25), None, size_police, (jaune, noir))
        Texte(fenetre, "Left : ", (x+marge*2+280, y+lig*25), None, size_police, (blanc, noir))
        Texte(fenetre, str(self.intersection.nb_vehicule_L), (x+marge*2+326, y+lig*25), None, size_police, (jaune, noir))


    # Visuel pour un véhicule
    def render_vehicles(self, fenetre):
        x,y = self.position
        largeur_fenetre, hauteur_fenetre = fenetre.get_size()
        
        #  Couleurs
        blanc = (255, 255, 255)
        noir = (0, 0, 0)
        rouge = (255, 0, 0)
        
        road_surface = pygame.Surface((hauteur_fenetre , hauteur_fenetre), pygame.SRCALPHA)
        
        # Vehicule
        vehicle_surface = pygame.Surface((self.larg , self.long), pygame.SRCALPHA)
        Rectangle(vehicle_surface, (0,0), (self.larg, self.long), (self.couleur_v_d, self.couleur_v_f), (1, noir))
        Texte(vehicle_surface, str(self.id), (4,13), None, 20, (blanc, noir))
        if self.collision != '':
            Arc_circle(vehicle_surface, (7,20), 15, (0, 360), rouge, 4)
        
        vehicle_surface_rect = vehicle_surface.get_rect()
        if self.voie == 'Right':
            vehicle_surface_rect.center = (self.long, self.larg)
        if self.voie == 'Left':
            vehicle_surface_rect.center = (self.long, 0)
        vehicle_surface = pygame.transform.rotate(vehicle_surface, self.rotate)
        
        road_surface.blit(vehicle_surface, (x,y))
        
        # Surface représentant la route
        rotated_rect = road_surface.get_rect()
        rotated_rect.center = (hauteur_fenetre , hauteur_fenetre//2)
        if self.provenance == 'Sud':
            road_surface = pygame.transform.rotate(road_surface, 180)
        elif self.provenance == 'Est':
            road_surface = pygame.transform.rotate(road_surface, -90)
        elif self.provenance == 'Ouest':
            road_surface = pygame.transform.rotate(road_surface, 90)

        # Dessinez la route sur la fenêtre principale
        fenetre.blit(road_surface, rotated_rect.topleft)
