import unittest
import pygame
from main import MainMenu, GameApp

class TestMainMenu(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((100, 100))  # Create a small screen for testing
        self.menu = MainMenu(self.screen)

    def test_button_clicks(self):
        # Simulate button clicks and check if the correct actions are returned
        self.assertEqual(self.menu.draw("main"), "main")  # Main menu should stay
        self.assertEqual(self.menu.draw("credit"), "main")  # Back button should return to main menu
        self.assertEqual(self.menu.draw("map_selection"), "map_selection")  # No action on map selection screen

    def tearDown(self):
        pygame.quit()

class TestGameApp(unittest.TestCase):
    def test_game_run(self):
        # Simply test if the game can be run without errors
        GameApp()

if __name__ == "__main__":
    unittest.main()
