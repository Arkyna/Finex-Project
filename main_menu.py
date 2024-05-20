import pygame
from bin import button
from game import Game


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font(r"assets/font/MinecraftEvenings-lgvPd.ttf", 60)
        self.font = pygame.font.Font(r"assets/font/MinecraftBold-nMK1.otf", 50)
        self.small_font = pygame.font.Font(r"assets/font/MinecraftRegular-Bmg3.otf", 29)
        self.BLACK_TEXT_COL = (0, 0, 0)
        self.TEXT_COL = (0, 0, 0)
        self.load_images()
        self.create_buttons()

    def load_images(self):
        self.start_img = pygame.image.load('assets/images/buttons/play_button.png').convert_alpha()
        self.credit_img = pygame.image.load('assets/images/buttons/credit_button.png').convert_alpha()
        self.quit_img = pygame.image.load('assets/images/buttons/quit_button.png').convert_alpha()
        self.back_img = pygame.image.load('assets/images/buttons/back_button.png').convert_alpha()
        self.day_img = pygame.image.load('assets/images/buttons/day_button.png').convert_alpha()
        self.night_img = pygame.image.load('assets/images/buttons/night_button.png').convert_alpha()
        self.credit_bg_img = pygame.image.load('assets/images/gui/creddit_background.png').convert_alpha()
        self.background_img = pygame.image.load('assets/images/gui/background_main_menu.jpg').convert_alpha()

    def create_buttons(self):
        self.begin_button = button.Button(420, 300, self.start_img, 1)
        self.credit_button = button.Button(420, 400, self.credit_img, 1)
        self.quit_button = button.Button(420, 500, self.quit_img, 1)
        self.back_button = button.Button(420, 660, self.back_img, 1)
        self.day_button = button.Button(320, 400, self.day_img, 1)
        self.night_button = button.Button(520, 400, self.night_img, 1)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_additional_text(self):
        self.draw_text("SENTINEL SIEGE", self.title_font, self.TEXT_COL, 230, 30)
        self.draw_text("a Tower Defense Game", self.small_font, self.TEXT_COL, 310, 80)
        self.draw_text("Selamat Datang di sentinel siege!!", self.small_font, self.TEXT_COL, 250, 800)
        self.draw_text("Play untuk memulai permainan dan Quit untuk keluar ", self.small_font, self.TEXT_COL, 60, 830)

    def draw_credits(self):
        self.screen.blit(self.credit_bg_img, (51, 100))
        self.draw_text("Credits", self.font, self.BLACK_TEXT_COL, 300, 140)
        self.draw_text("Game Developer : OkSobatKoding", self.small_font, self.TEXT_COL, 180, 200)
        self.draw_text("Designer       : OkSobatKoding", self.small_font, self.TEXT_COL, 180, 240)
        self.draw_text("Special Thanks To", self.font, self.BLACK_TEXT_COL, 200, 280)
        self.draw_text("Music          : OpenGameArt", self.small_font, self.TEXT_COL, 180, 340)
        self.draw_text("GUI Assets     : KanekiZLF from Itch.io ", self.small_font, self.TEXT_COL, 180, 380)
        self.draw_text("Monster Assets : foozlecc from Itch.io ", self.small_font, self.TEXT_COL, 180, 420)
        self.draw_text("Tower Assets   : foozlecc from Itch.io ", self.small_font, self.TEXT_COL, 180, 460)
        self.draw_text("Map Assets     : foozlecc from Itch.io ", self.small_font, self.TEXT_COL, 180, 500)

    def draw_map_selection(self):
        self.draw_text("Select Map", self.font, self.TEXT_COL, 330, 300)
        if self.day_button.draw(self.screen):
            return "day"
        if self.night_button.draw(self.screen):
            return "night"
        if self.back_button.draw(self.screen):
            return "main"
        return "map_selection"

    def draw(self, menu_state):
        self.screen.fill((52, 78, 91))
        self.screen.blit(self.background_img, (0, 0))
        
        if menu_state == "main":
            self.draw_text("Main Menu", self.font, self.BLACK_TEXT_COL, 330, 200)
            self.draw_additional_text()
            if self.begin_button.draw(self.screen):
                return "map_selection"
            if self.credit_button.draw(self.screen):
                return "credit"
            if self.quit_button.draw(self.screen):
                return "quit"
        elif menu_state == "credit":
            self.draw_credits()
            if self.back_button.draw(self.screen):
                return "main"
        elif menu_state == "map_selection":
            return self.draw_map_selection()
        return menu_state


class GameApp:
    def __init__(self):
        pygame.init()
        # encapsulated
        self.__s_width = 960
        self.__s_height = 960
        self.screen = pygame.display.set_mode((self.__s_width, self.__s_height))
        pygame.display.set_caption("Sentinel SIEGE!!!!! now in 4k")
        self.menu = MainMenu(self.screen)
        self.game_paused = True
        self.menu_state = "main"
        self.map_choice = None
        self.run_game()

    def run_game(self):
        run = True
        while run:
            if self.game_paused:
                self.menu_state = self.menu.draw(self.menu_state)
                if self.menu_state in ["day", "night"]:
                    self.map_choice = self.menu_state
                    self.game_paused = False
                    game_instance = Game(self.map_choice)
                    game_instance.run()
                elif self.menu_state == "quit":
                    run = False

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
