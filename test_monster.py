import unittest
from unittest.mock import Mock, patch
import pygame as pgm
from pygame.math import Vector2
from bin.monsters.monster import Monster

# Mock the global variables and constants
mock_val = Mock()
mock_val.ENEMY_DATA = {
    'weak': {'health': 10, 'speed': 1},
    'medium': {'health': 15, 'speed': 2},
    'strong': {'health': 20, 'speed': 3},
    'elite': {'health': 30, 'speed': 4}
}
mock_val.KILL_REWARD = 100

# A concrete subclass of Monster for testing purposes
class TestMonster(Monster):
    def move(self, world):
        pass
    
    def rotate(self):
        pass

class TestMonsterClass(unittest.TestCase):
    
    @patch('bin.monsters.monster.val', mock_val)
    def setUp(self):
        # Initialize Pygame (necessary for creating surfaces)
        pgm.init()

        self.enemy_type = 'weak'
        self.waypoints = [(0, 0), (10, 10)]
        
        # Create a small surface to use as the image
        self.test_surface = pgm.Surface((10, 10))
        self.images = {self.enemy_type: self.test_surface}
        
        # Creating a TestMonster instance
        self.monster = TestMonster(self.enemy_type, self.waypoints, self.images)
        
        # Mocking the world object
        self.mock_world = Mock()
        self.mock_world.killed_enemies = 0
        self.mock_world.money = 0

    def test_initialization(self):
        self.assertEqual(self.monster.health, 10)
        self.assertEqual(self.monster.speed, 1)
        self.assertEqual(self.monster.pos, Vector2(0, 0))
        self.assertEqual(self.monster.target_waypoint, 1)

    def test_update(self):
        with patch.object(self.monster, 'move') as mock_move, \
             patch.object(self.monster, 'rotate') as mock_rotate, \
             patch.object(self.monster, 'check_alive') as mock_check_alive:
            
            self.monster.update(self.mock_world)
            
            mock_move.assert_called_once_with(self.mock_world)
            mock_rotate.assert_called_once()
            mock_check_alive.assert_called_once_with(self.mock_world)

    def test_check_alive(self):
        self.monster.health = 0
        self.monster.check_alive(self.mock_world)
        
        self.assertEqual(self.mock_world.killed_enemies, 1)
        self.assertEqual(self.mock_world.money, 100)
        self.assertTrue(self.monster not in pgm.sprite.Sprite.groups(self.monster))

if __name__ == '__main__':
    unittest.main()
