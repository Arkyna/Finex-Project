import pygame
from bin import button
from bin import globalvar as val
from game import Game
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

screen = pygame.display.set_mode((val.SCREEN_WIDTH + val.SIDE_PANEL, val.SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# game variables
game_paused = False
menu_state = "main"

# define fonts
font = pygame.font.SysFont("arialblack", 40)
small_font = pygame.font.SysFont("arial", 20)  # Font baru untuk teks tambahan

# define colours
TEXT_COL = (255, 255, 255)  # White color for text
BLACK_TEXT_COL = (0, 0, 0)  # Red color for better visibility

# load button images
resume_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
credit_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
quit_img = pygame.image.load("assets/images/main_menu/close_button.png").convert_alpha()
back_img = pygame.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
wlcm_img = pygame.image.load('assets/images/main_menu/IRONY_TITLE_Large.png').convert_alpha()

# create button instances
resume_button = button.Button(515, 300, resume_img, 1)
credit_button = button.Button(515, 450, credit_img, 1)
quit_button = button.Button(925, 100, quit_img, 1)
back_button = button.Button(515, 550, back_img, 1)
wlcm_button = button.Button(325, 100, wlcm_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Teks tambahan di menu utama
def draw_additional_text():
    draw_text("Selamat Datang di sentinel siege!!", small_font, TEXT_COL, 100, 30)
    draw_text("Pilih opsi di bawah untuk memulai atau keluar.", small_font, TEXT_COL, 100, 60)

# game loop
run = True
while run:
    screen.fill((52, 78, 91))

    # check if game is paused
    if game_paused:
        # check menu state
        if menu_state == "main":
            wlcm_button.draw(screen)  # Menggambar wlcm_img terlebih dahulu
            draw_text("Main Menu", font, BLACK_TEXT_COL, 460, 120)  # Menambahkan teks "Main Menu" di atas wlcm_img dengan warna HITAM LEGAM AMBATUKAM
            draw_additional_text()  # Memanggil fungsi untuk menampilkan teks tambahan
            # draw pause screen buttons
            if resume_button.draw(screen):
                game_paused = False
                game_instance = Game()
                game_instance.run()  # Memastikan game dijalankan
            if credit_button.draw(screen):
                menu_state = "credit"
            if quit_button.draw(screen):
                run = False
        # check if the options menu is open
        if menu_state == "credit":
            # draw the different options buttons
            if back_button.draw(screen):
                menu_state = "main"
    else:
        draw_text("Tekan SPACE untuk jeda", font, TEXT_COL, 345, 420)
        game_paused = True  # Menambahkan ini agar game langsung masuk ke menu utama

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()