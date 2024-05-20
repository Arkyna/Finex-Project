import pygame as pgm
from bin import globalvar as val

class GameTest:
    def __init__(self):
        # Initialize pygame
        pgm.init()
        self.screen = pgm.display.set_mode((val.SCREEN_WIDTH, val.SCREEN_HEIGHT))
        pgm.display.set_caption(val.GAME_NAME)
        self.load_assets()

    def load_assets(self):
        self.large_font = pgm.font.Font(r"assets/font/MinecraftBold-nMK1.otf", 36)
        self.text_font = pgm.font.Font(r"assets/font/MinecraftRegular-Bmg3.otf", 24)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def test_draw_text(self):
        # Fill the screen with a color (white) for better visibility
        self.screen.fill((255, 255, 255))
        
        # Test drawing text
        self.draw_text("Test Text", self.text_font, (0, 0, 0), 100, 100)
        
        # Update display
        pgm.display.flip()
        
        # Keep the window open for a few seconds to see the result
        pgm.time.wait(3000)

# Run the test
if __name__ == "__main__":
    val.SCREEN_WIDTH = 1200  # Ensure these values are set
    val.SCREEN_HEIGHT = 800
    val.GAME_NAME = "Game Test"
    
    game_test = GameTest()
    game_test.test_draw_text()
    
    # Quit pygame
    pgm.quit()
