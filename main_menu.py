import pygame
from bin import button
from bin import globalvar as val
from game import Game

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/font/buddychampion.ttf", 72)
        self.small_font = pygame.font.Font("assets/font/buddychampionital.ttf", 40)
        self.TEXT_COL = (0, 0, 0)
        self.BLACK_TEXT_COL = (0, 0, 0)
        self.load_images()
        self.create_buttons()

    def load_images(self):
        self.resume_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
        self.credit_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
        self.quit_img = pygame.image.load("assets/images/main_menu/close_button.png").convert_alpha()
        self.back_img = pygame.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
        self.wlcm_img = pygame.image.load('assets/images/main_menu/IRONY_TITLE_Large.png').convert_alpha()
        self.credit_bg_img = pygame.image.load('assets/images/main_menu/UI_board_Large_parchment.png').convert_alpha()

    def create_buttons(self):
        self.resume_button = button.Button(515, 300, self.resume_img, 1)
        self.credit_button = button.Button(515, 450, self.credit_img, 1)
        self.quit_button = button.Button(925, 100, self.quit_img, 1)
        self.back_button = button.Button(515, 660, self.back_img, 1)
        self.wlcm_button = button.Button(325, 100, self.wlcm_img, 1)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_additional_text(self):
        self.draw_text("Selamat Datang di sentinel siege!!", self.small_font, self.TEXT_COL, 100, 30)
        self.draw_text("Pilih opsi di bawah untuk memulai atau keluar.", self.small_font, self.TEXT_COL, 100, 60)

    def draw_credits(self):
        self.screen.blit(self.credit_bg_img, (150, 100))  # Adjust the position as needed
        self.draw_text("Credits", self.font, self.BLACK_TEXT_COL, 490, 140)
        self.draw_text("Game Developer: OkSobatKoding", self.small_font, self.TEXT_COL, 180, 200)
        self.draw_text("Designer: OkSobatKoding", self.small_font, self.TEXT_COL, 180, 240)
        self.draw_text("Special Thanks To", self.font, self.BLACK_TEXT_COL, 330, 280)
        self.draw_text("Music: OpenGameArt", self.small_font, self.TEXT_COL, 180, 340)
        self.draw_text("GUI Assets: KanekiZLF from Itch.io ", self.small_font, self.TEXT_COL, 180, 380)
        self.draw_text("Monster Assets: foozlecc from Itch.io ", self.small_font, self.TEXT_COL, 180, 420)
        self.draw_text("Tower Assets: foozlecc from Itch.io ", self.small_font, self.TEXT_COL, 180, 460)
        self.draw_text("Map Assets: foozlecc from Itch.io ", self.small_font, self.TEXT_COL, 180, 500)

    def draw(self, menu_state):
        self.screen.fill((52, 78, 91))
        if menu_state == "main":
            self.wlcm_button.draw(self.screen)
            self.draw_text("Main Menu", self.font, self.BLACK_TEXT_COL, 430, 120)
            self.draw_additional_text()
            if self.resume_button.draw(self.screen):
                return "resume"
            if self.credit_button.draw(self.screen):
                return "credit"
            if self.quit_button.draw(self.screen):
                return "quit"
        elif menu_state == "credit":
            self.draw_credits()
            if self.back_button.draw(self.screen):
                return "main"
        return menu_state
class GameApp:
    def __init__(self):
        pygame.init()
        self._s_width = 960
        self._s_height = 960
        self.screen = pygame.display.set_mode((self._s_width , self._s_height))
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
