# NOT YET IMPLEMENTED nor Valid

import unittest
from unittest.mock import patch, MagicMock
import pygame as pgm
from game import Game  # Adjust this import to match the location of Game class
from bin import globalvar as val
from bin.world import World

class TestGame(unittest.TestCase):

    @patch('game.pgm.display.set_mode')
    @patch('game.pgm.font.Font')
    @patch('game.pgm.image.load')
    @patch('game.World')
    def setUp(self, MockWorld, mock_load, mock_font, mock_set_mode):
        # Mocking World object creation
        mock_world_instance = MockWorld.return_value
        mock_world_instance.process_data = MagicMock()
        mock_world_instance.process_enemies = MagicMock()
        mock_world_instance.reset_level = MagicMock()

        self.game = Game('day')

    def test_initialization(self):
        self.assertIsInstance(self.game, Game)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.level_started)
        self.assertIsNotNone(self.game.map_image)
        self.assertIsNotNone(self.game.sidebar_image)

    def test_load_assets(self):
        self.game.load_assets()
        self.assertIsNotNone(self.game.map_image)
        self.assertIsNotNone(self.game.basic_tower_spritesheet)
        self.assertIsNotNone(self.game.electric_tower_spritesheet)
        self.assertIsNotNone(self.game.base_tower)
        self.assertIsNotNone(self.game.cursor_tower)
        self.assertIsNotNone(self.game.monster_images)
        self.assertIsNotNone(self.game.buy_tower_image)
        self.assertIsNotNone(self.game.cancel_button_image)
        self.assertIsNotNone(self.game.upgrade_button_image)
        self.assertIsNotNone(self.game.change_button_image)
        self.assertIsNotNone(self.game.begin_image)
        self.assertIsNotNone(self.game.restart_image)
        self.assertIsNotNone(self.game.fforward_image)
        self.assertIsNotNone(self.game.quit_img)
        self.assertIsNotNone(self.game.sidebar_image)
        self.assertIsNotNone(self.game.flat_back_image)
        self.assertIsNotNone(self.game.large_font)
        self.assertIsNotNone(self.game.text_font)

    def test_load_world(self):
        self.game.load_world()
        self.assertIsInstance(self.game.world, World)

    def test_setup_game_variables(self):
        self.game.setup_game_variables()
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.game_outcome, 0)
        self.assertFalse(self.game.level_started)
        self.assertIsInstance(self.game.monster_groups, pgm.sprite.Group)
        self.assertIsInstance(self.game.tower_groups, pgm.sprite.Group)

    @patch('game.pgm.event.get')
    def test_handle_events_quit(self, mock_event_get):
        mock_event_get.return_value = [pgm.event.Event(pgm.QUIT)]
        with patch('game.pgm.quit') as mock_pgm_quit, patch('builtins.exit') as mock_exit:
            self.game.handle_events()
            mock_pgm_quit.assert_called_once()
            mock_exit.assert_called_once()

    @patch('game.pgm.event.get')
    @patch('game.pgm.mouse.get_pos')
    def test_handle_events_mouse_click(self, mock_mouse_get_pos, mock_event_get):
        mock_mouse_get_pos.return_value = (100, 100)
        mock_event_get.return_value = [pgm.event.Event(pgm.MOUSEBUTTONDOWN, button=1)]
        self.game.handle_events()
        self.assertFalse(self.game.selected_tower)
    
    def test_handle_mouse_click(self):
        self.game.placing_tower