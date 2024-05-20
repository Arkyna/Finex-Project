import unittest
from unittest.mock import patch, MagicMock
import pygame as pgm
import sys
import os

# Ensure the root directory is in the sys.path for imports to work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game import Game  # Import the Game class from game.py
from bin import globalvar as val  # Import the global variables

class TestGameInitialization(unittest.TestCase):
    @patch('game.pgm.image.load')
    def test_load_assets(self, mock_load):
        # Create a fake surface to be returned by the mock
        mock_load.return_value = MagicMock(spec=pgm.Surface)
        
        game = Game()
        game.load_assets()

        # Check if image.load was called with the correct file paths
        mock_load.assert_any_call('assets/images/map/level1.png')
        mock_load.assert_any_call('assets/images/towers/basic_tower_1.png')
        mock_load.assert_any_call('assets/images/towers/electric_tower_1.png')
        # Add more assertions for other images as needed

        # Check if the loaded images are assigned to the correct attributes
        self.assertIsNotNone(game.map_image)
        self.assertEqual(len(game.basic_tower_spritesheet), val.TOWER_LEVELS)
        self.assertEqual(len(game.electric_tower_spritesheet), val.TOWER_LEVELS)

    def test_initial_game_variables(self):
        game = Game()
        game.setup_game_variables()

        self.assertFalse(game.game_over)
        self.assertEqual(game.game_outcome, 0)
        self.assertFalse(game.level_started)
        self.assertIsInstance(game.last_enemy_spawn, int)
        self.assertFalse(game.placing_tower)
        self.assertIsNone(game.selected_tower)
        self.assertIsInstance(game.monster_groups, pgm.sprite.Group)
        self.assertIsInstance(game.tower_groups, pgm.sprite.Group)

if __name__ == '__main__':
    unittest.main()
