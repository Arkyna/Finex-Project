import pygame as pgm
import json
from bin import globalvar as val
from bin.enemy import Enemy
from bin.world import World
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
enemy_image = pgm.image.load(r'assets\images\monsters\enemy1.png').convert_alpha()

#load json data for level
with open('bin\levels\level1.tmj') as file:
    world_data = json.load(file)

#creating tower
def create_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // val.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // val.TILE_SIZE

    #calculating squential numbers of tile on level
    mouse_tile_num = (mouse_tile_y * val.COLS) + mouse_tile_x

    #checking tile if grass
    if world.tile_map[mouse_tile_num] == 39:
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

#game loop
run = True
while run:

    # limits FPS to 60
    clock.tick(val.FPS) 

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
    tower_groups.draw(screen)

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
