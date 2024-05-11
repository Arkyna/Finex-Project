#Note : Menuny dah befungsi cuman gimana caranya buat nyatuin dengan initialize
import pygame
from bin import button
from bin import globalvar as val
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()


screen = pygame.display.set_mode((val.SCREEN_WIDTH + val.SIDE_PANEL, val.SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
resume_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
#butuh image button option
options_img = pygame.image.load("assets/images/buttons/begin.png").convert_alpha()
quit_img = pygame.image.load("assets/images/main_menu/close_button.png").convert_alpha()
#butuh image button video
video_img = pygame.image.load('assets/images/buttons/begin.png').convert_alpha()
#butuh image button audio
audio_img = pygame.image.load('assets/images/buttons/begin.png').convert_alpha()
back_img = pygame.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
#title
wlcm_img = pygame.image.load('assets/images/main_menu/IRONY_TITLE_Large.png').convert_alpha()

#create button instances
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

#game loop
run = True
while run:
#				R   G   B
  screen.fill((52, 78, 91))

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      wlcm_button.draw(screen)
      #draw pause screen buttons
      if resume_button.draw(screen):
        game_paused = False
      if options_button.draw(screen):
        menu_state = "options"
      if quit_button.draw(screen):
        run = False
    #check if the options menu is open
    if menu_state == "options":
      #draw the different options buttons
      if video_button.draw(screen):
        print("Video Settings")
      if audio_button.draw(screen):
        print("Audio Settings")
      if back_button.draw(screen):
        menu_state = "main"
  else:
    draw_text("Press SPACE to pause", font, TEXT_COL, 345, 420)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()