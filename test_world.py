import unittest
from unittest.mock import patch, MagicMock
import random

# Mocking the bin.globalvar module
class MockVal:
    HEALTH = 100
    MONEY = 50
    ENEMY_SPAWN_DATA = [
        {"enemy_type_1": 5, "enemy_type_2": 3},  # Level 1
        {"enemy_type_1": 7, "enemy_type_2": 2}   # Level 2
    ]

# Mocking the pygame module's Surface class for image
class MockSurface:
    def blit(self, source, dest):
        pass  # Mock implementation

import bin.globalvar as val

class World():
    def __init__(self, data, map_image):
        self.level = 1
        self.game_speed = 1
        self.health = val.HEALTH
        self.money = val.MONEY
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "layer1":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)
    
    def process_waypoints(self, data):
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        enemies = val.ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        return (self.killed_enemies + self.missed_enemies) == len(self.enemy_list)

    def reset_level(self):
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def draw(self, surface):
        surface.blit(self.image, (0, 0))


# Unit tests for World class
class TestWorld(unittest.TestCase):
    @patch('bin.globalvar', new=MockVal)
    def setUp(self):
        self.mock_data = {
            "layers": [
                {"name": "layer1", "data": [1, 2, 3, 4]},
                {"name": "waypoints", "objects": [{"polyline": [{"x": 1, "y": 2}, {"x": 3, "y": 4}]}]}
            ]
        }
        self.mock_image = MockSurface()
        self.world = World(self.mock_data, self.mock_image)

    def test_process_data(self):
        self.world.process_data()
        self.assertEqual(self.world.tile_map, [1, 2, 3, 4])
        self.assertEqual(self.world.waypoints, [(1, 2), (3, 4)])

    def test_process_waypoints(self):
        self.world.process_waypoints([{"x": 5, "y": 6}, {"x": 7, "y": 8}])
        self.assertEqual(self.world.waypoints, [(5, 6), (7, 8)])

    @patch('random.shuffle', lambda x: x)
    def test_process_enemies(self):
        self.world.process_enemies()
        expected_enemies = ['enemy_type_1'] * 5 + ['enemy_type_2'] * 3
        self.assertEqual(self.world.enemy_list, expected_enemies)

    def test_check_level_complete(self):
        self.world.killed_enemies = 5
        self.world.missed_enemies = 3
        self.world.process_enemies()
        self.assertTrue(self.world.check_level_complete())

    def test_reset_level(self):
        self.world.reset_level()
        self.assertEqual(self.world.enemy_list, [])
        self.assertEqual(self.world.spawned_enemies, 0)
        self.assertEqual(self.world.killed_enemies, 0)
        self.assertEqual(self.world.missed_enemies, 0)

    @patch.object(MockSurface, 'blit')
    def test_draw(self, mock_blit):
        self.world.draw(self.mock_image)
        mock_blit.assert_called_with(self.mock_image, (0, 0))

if __name__ == '__main__':
    unittest.main()
