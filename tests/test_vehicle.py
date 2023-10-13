# --- Test ---
# python3 -m unittest : execute tous les tests
#   sachant qu'une class de test constitue une batterie de tests définies par chaque méthode.
# python3 -m unittest tests.test_vehicle : execute une seul batterie de tests définie par la classe
# python3 -m unittest tests.test_vehicle.TestVehicle.test_move : execute uniquement les test move()
# ------------------------------------------------------------------------------------------------------------------------------------------

import sys
sys.path.append('../Smart_road') 
import unittest
from src.clsVehicle import Vehicle

class TestVehicle(unittest.TestCase):
    def setUp(self):
        # Mise en place des conditions initiales pour les tests
        self.vehicle = Vehicle(speed=60, velocity=10, time=0, distance=0, safeDistance=5, route='s')

    def test_constructor(self):
        #Teste si le constructeur de Véhicule initialise correctement les attributs.
        self.assertEqual(self.vehicle.speed, 60)
        self.assertEqual(self.vehicle.velocity, 10)
        self.assertEqual(self.vehicle.time, 0)
        self.assertEqual(self.vehicle.distance, 0)
        self.assertEqual(self.vehicle.safeDistance, 5)
        self.assertEqual(self.vehicle.route, 's')

    def test_move(self):
        # Vérifiez que la méthode move met à jour correctement la distance
        self.vehicle.move(time=2)
        self.assertEqual(self.vehicle.distance, 20)

    def test_check_collision(self):
        # Testez la méthode check_collision pour vérifier qu'elle détecte correctement les collisions
        other_vehicle = Vehicle(speed=50, distance=100, route='s')
        self.assertTrue(self.vehicle.check_collision(other_vehicle))

    def test_maintain_safe_distance(self):
        # Testez la méthode maintain_safe_distance pour vérifier qu'elle maintient une distance de sécurité
        other_vehicle = Vehicle(speed=50, velocity=20, time=0, distance=110, safeDistance=5, route='s')
        self.vehicle.maintain_safe_distance(other_vehicle)
        self.assertEqual(self.vehicle.speed, 45)

if __name__ == '__main__':
    unittest.main()