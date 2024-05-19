import pygame
from bin import button
from bin import globalvar as val
from game import Game
import os

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arialblack", 40)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.TEXT_COL = (255, 255, 255)
        self.BLACK_TEXT_COL = (0, 0, 0)
        self.load_images()
        self.create_buttons()

    def load_images(self):
        self.resume_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
        self.credit_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
        self.quit_img = pygame.image.load("assets/images/main_menu/close_button.png").convert_alpha()
        self.back_img = pygame.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
        self.wlcm_img = pygame.image.load('assets/images/main_menu/IRONY_TITLE_Large.png').convert_alpha()

    def create_buttons(self):
        self.resume_button = button.Button(515, 300, self.resume_img, 1)
        self.credit_button = button.Button(515, 450, self.credit_img, 1)
        self.quit_button = button.Button(925, 100, self.quit_img, 1)
        self.back_button = button.Button(515, 550, self.back_img, 1)
        self.wlcm_button = button.Button(325, 100, self.wlcm_img, 1)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_additional_text(self):
        self.draw_text("Selamat Datang di sentinel siege!!", self.small_font, self.TEXT_COL, 100, 30)
        self.draw_text("Pilih opsi di bawah untuk memulai atau keluar.", self.small_font, self.TEXT_COL, 100, 60)

    def draw(self, menu_state):
        self.screen.fill((52, 78, 91))
        if menu_state == "main":
            self.wlcm_button.draw(self.screen)
            self.draw_text("Main Menu", self.font, self.BLACK_TEXT_COL, 460, 120)
            self.draw_additional_text()
            if self.resume_button.draw(self.screen):
                return "resume"
            if self.credit_button.draw(self.screen):
                return "credit"
            if self.quit_button.draw(self.screen):
                return "quit"
        elif menu_state == "credit":
            if self.back_button.draw(self.screen):
                return "main"
        return menu_state

class GameApp:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        pygame.init()
        self.screen = pygame.display.set_mode((val.SCREEN_WIDTH + val.SIDE_PANEL, val.SCREEN_HEIGHT))
        pygame.display.set_caption("Main Menu")
        self.menu = MainMenu(self.screen)
        self.game_paused = False
        self.menu_state = "main"
        self.run_game()

    def run_game(self):
        run = True
        while run:
            if self.game_paused:
                self.menu_state = self.menu.draw(self.menu_state)
                if self.menu_state == "resume":
                    self.game_paused = False
                    game_instance = Game()
                    game_instance.run()
                elif self.menu_state == "quit":
                    run = False
            else:
                self.menu.draw_text("Tekan SPACE untuk jeda", self.menu.font, self.menu.TEXT_COL, 345, 420)
                self.game_paused = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_paused = True
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    GameApp()
