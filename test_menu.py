# experimental

import unittest
import pygame
from main_menu import MainMenu

class TestMainMenu(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.menu = MainMenu(self.screen)

    def test_buttons_displayed_correctly(self):
        # Draw buttons
        self.menu.draw("main")

        # Check if buttons are displayed
        self.assertIsNotNone(self.menu.begin_button)
        self.assertIsNotNone(self.menu.credit_button)
        self.assertIsNotNone(self.menu.quit_button)

if __name__ == "__main__":
    unittest.main()

    
