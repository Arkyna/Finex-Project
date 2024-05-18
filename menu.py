import pygame
from bin import button
from bin import globalvar as val
from game import Game
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

def main_menu():
    screen = pygame.display.set_mode((val.SCREEN_WIDTH + val.SIDE_PANEL, val.SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    # Game variables
    menu_state = "main"

    # Define fonts
    font = pygame.font.SysFont("arialblack", 40)

    # Define colours
    TEXT_COL = (255, 255, 255)

    # Load button images
    resume_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
    options_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
    quit_img = pygame.image.load("assets/images/main_menu/close_button.png").convert_alpha()
    video_img = pygame.image.load('assets/images/buttons/begin.png').convert_alpha()
    audio_img = pygame.image.load('assets/images/buttons/begin.png').convert_alpha()
    back_img = pygame.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
    wlcm_img = pygame.image.load('assets/images/main_menu/IRONY_TITLE_Large.png').convert_alpha()

    # Create button instances
    resume_button = button.Button(515, 300, resume_img, 1)
    options_button = button.Button(515, 450, options_img, 1)
    quit_button = button.Button(925, 100, quit_img, 1)
    video_button = button.Button(515, 250, video_img, 1)
    audio_button = button.Button(515, 400, audio_img, 1)
    back_button = button.Button(515, 550, back_img, 1)
    wlcm_button = button.Button(325, 100, wlcm_img, 1)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    # Game loop
    run = True
    while run:
        screen.fill((52, 78, 91))

        # Check menu state
        if menu_state == "main":
            wlcm_button.draw(screen)
            # Draw main menu buttons
            if resume_button.draw(screen):
                run = False  # Exit menu to start the game
            if options_button.draw(screen):
                menu_state = "options"
            if quit_button.draw(screen):
                pygame.quit()
                exit()

        if menu_state == "options":
            if video_button.draw(screen):
                print("Video Settings")
            if audio_button.draw(screen):
                print("Audio Settings")
            if back_button.draw(screen):
                menu_state = "main"

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    # Start the game after exiting the menu
    Game().run()
