import pygame as pgm
import json
from bin.enemy import Enemy
from bin.world import World

#initialisasi
pgm.init()

#create clock
clock = pgm.time.Clock()

ROWS = 15
COLS = 15
TILE_SIZE = 64
SCREEN_WIDTH = TILE_SIZE*COLS
SCREEN_HEIGHT = TILE_SIZE*ROWS
FPS = 60

#creating window game
screen = pgm.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pgm.display.set_caption("TDEFENSE")

#load image
#map
map_image = pgm.image.load('assets\images\map\level_1.png').convert_alpha()

#enemies
enemy_image = pgm.image.load('assets\images\monsters\enemy1.png').convert_alpha()

#load json data for level
with open('bin\levels\_cord.tmj') as file:
    world_data = json.load(file)

#create world
world = World(world_data, map_image)
world.process_data()

#creating groups
enemy_groups = pgm.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_groups.add(enemy)

#game loop
run = True
while run:

    # limits FPS to 60
    clock.tick(FPS) 

    #screen fill
    screen.fill("grey100")

    #draw level
    world.draw(screen)

    #enemy path
    pgm.draw.lines(screen, "grey0", False, world.waypoints)

    #update groups
    enemy_groups.update()


    #draw groups
    enemy_groups.draw(screen)

    #event handler
    for event in pgm.event.get():
            #quit program
        if event.type == pgm.QUIT:
            run = False

    #update display
    pgm.display.flip()

pgm.quit()
