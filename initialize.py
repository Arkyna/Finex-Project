import pygame as pgm
<<<<<<< HEAD
from bin.enemy import Enemy
=======
from enemy import Enemy
import math
>>>>>>> 19ededa6e5f5c8c0a0642d20a202b81fb21b5652

#initialisasi
pgm.init()

#create clock
clock = pgm.time.Clock()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60

#creating window game
screen = pgm.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pgm.display.set_caption("TDEFENSE")

#load image
enemy_image = pgm.image.load() 
enemy = Enemy((200, 300), enemy_image)

#game loop
run = True
while run:
    # limits FPS to 60
    clock.tick(FPS) 
    #event handler
    for event in pgm.event.get():
        if event.type == pgm.QUIT:
            run = False

pgm.quit()
