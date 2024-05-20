import unittest
from unittest.mock import patch, MagicMock
import pygame as pgm
from game import Game
from bin import globalvar as val

class TestGame(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()
    
    def test_clear_selection(self):
        tower = MagicMock()
        tower.selected = True
        self.game.tower_groups.add(tower)
        
        self.game.clear_selection()
        
        for tower in self.game.tower_groups:
            self.assertFalse(tower.selected)

    def test_select_tower(self):
        tower = MagicMock()
        tower.tile_x = 2
        tower.tile_y = 2
        self.game.tower_groups.add(tower)

        selected = self.game.select_tower((64, 64))  # 64/32 = 2, so (64, 64) maps to (2, 2)
        self.assertEqual(selected, tower)

    def test_create_buttons(self):
        self.game.create_buttons()
        self.assertIsNotNone(self.game.tower_button)
        self.assertIsNotNone(self.game.cancel_button)
        self.assertIsNotNone(self.game.upgrade_button)
        self.assertIsNotNone(self.game.change_button)
        self.assertIsNotNone(self.game.begin_button)
        self.assertIsNotNone(self.game.restart_button)
        self.assertIsNotNone(self.game.fforward_button)
    
    @patch('pygame.time.get_ticks')
    def test_check_game_outcome(self, mock_get_ticks):
        self.game.world.health = 0
        self.game.check_game_outcome()
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.game_outcome, -1)
        
        self.game.world.health = 10
        self.game.world.level = val.TOTAL_LEVELS + 1
        self.game.check_game_outcome()
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.game_outcome, 1)

    @patch('pygame.time.get_ticks')
    def test_reset_game(self, mock_get_ticks):
        mock_get_ticks.return_value = 1000
        self.game.reset_game()
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.level_started)
        self.assertFalse(self.game.placing_tower)
        self.assertIsNone(self.game.selected_tower)
        self.assertEqual(self.game.last_enemy_spawn, 1000)
        self.assertEqual(len(self.game.monster_groups), 0)
        self.assertEqual(len(self.game.tower_groups), 0)
        self.assertIsNotNone(self.game.world)

if __name__ == '__main__':
    unittest.main()
