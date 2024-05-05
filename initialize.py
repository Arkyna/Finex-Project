import pygame as pgm
import json
from bin import globalvar as val
from bin.enemy import Enemy
from bin.world import World
from bin.button import Button
from bin.tower import Tower

#initialisasi
pgm.init()

#create clock
clock = pgm.time.Clock()

#creating window game
screen = pgm.display.set_mode((val.SCREEN_WIDTH + val.SIDE_PANEL, val.SCREEN_HEIGHT))
pgm.display.set_caption("TDEFENSE")

#Load image
#map
map_image = pgm.image.load(r'assets\images\map\level1.png').convert_alpha()

#individual tower image for mouse cursor
cursor_tower = pgm.image.load(r'assets\images\towers\tower1.png').convert_alpha()

#enemies
enemy_image = pgm.image.load(r'assets\images\monsters\enemy2.png').convert_alpha()

# buttons
buy_turret_image = pgm.image.load(r'assets\images\buttons\buy_button.png').convert_alpha()
cancel_button_image = pgm.image.load(r'assets\images\buttons\cancel_button.png').convert_alpha()

#sidebar 
sidebar_image = pgm.image.load(r'assets\images\gui\sidepanel.png').convert_alpha()

#load json data for level
with open('bin\levels\level1.tmj') as file:
    world_data = json.load(file)

#creating tower
def create_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // val.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // val.TILE_SIZE

    #calculating squential numbers of tile on level
    mouse_tile_num = (mouse_tile_y * val.COLS) + mouse_tile_x

    #checking tile if place able
    if world.tile_map[mouse_tile_num] == 74:
        #checking the place is already occupied by tower
        space_is_free = True
        for tower in tower_groups:
            if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
                space_is_free = False
        #if free then place tower
        if space_is_free == True:
            new_tower = Tower(cursor_tower, mouse_tile_x, mouse_tile_y)
            tower_groups.add(new_tower)

#create world
world = World(world_data, map_image)
world.process_data()

#creating groups
enemy_groups = pgm.sprite.Group()
tower_groups = pgm.sprite.Group()



enemy = Enemy(world.waypoints, enemy_image)
enemy_groups.add(enemy)

# create button
turret_button = Button(val.SCREEN_WIDTH + 30, 120, buy_turret_image)
cancel_button = Button(val.SCREEN_WIDTH + 30, 180, cancel_button_image)

#game loop
run = True
while run:

    # limits FPS to 60
    clock.tick(val.FPS) 

     #########################
    # UPDATING SECTION
    #########################

    #update groups
    enemy_groups.update()

    #########################
    # DRAWING SECTION
    #########################

    #screen fill
    screen.fill("grey100")

    #draw level
    world.draw(screen)

    #enemy path
    pgm.draw.lines(screen, "grey0", False, world.waypoints)

    #draw groups
    enemy_groups.draw(screen)
    tower_groups.draw(screen)

    #draw sidebar
    screen.blit(sidebar_image,(960, 0))

    #draw buttons
    #button for placing turret
    turret_button.draw(screen)
    cancel_button.draw(screen)

    print(tower_groups)

    #event handler
    for event in pgm.event.get():
            #quit program
        if event.type == pgm.QUIT:
            run = False

    #mouse click
    if event.type == pgm.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = pgm.mouse.get_pos()

        #check if the mouse on the game
        if mouse_pos[0] < val.SCREEN_WIDTH and mouse_pos[1] < val.SCREEN_HEIGHT:
            create_tower(mouse_pos)
         
        
    #update display
    pgm.display.flip()

pgm.quit()
