import pygame as pgm
import json
from bin import globalvar as val
from bin.monster import Monster
from bin.world import World
from bin.button import Button
from bin.towers.tower import Tower

# initialisasi
pgm.init()

# create clock
clock = pgm.time.Clock()

# creating game window
screen = pgm.display.set_mode((val.SCREEN_WIDTH + val.SIDE_PANEL, val.SCREEN_HEIGHT))
pgm.display.set_caption(val.GAME_NAME)


# Game Variables
game_over = False
game_outcome = 0 # -1 = losing, 1 = Winning 
level_started = False
last_enemy_spawn = pgm.time.get_ticks()
placing_tower = False
selected_tower = None


# Load images
# map
map_image = pgm.image.load('assets/images/map/level1.png').convert_alpha()

# tower sprite sheet
tower_spritesheet = []
for x in range(1, val.TOWER_LEVELS + 1):
    tower_sheet = pgm.image.load(f'assets/images/towers/weapon_heavy_arrow_{x}.png').convert_alpha()
    tower_spritesheet.append(tower_sheet)

# tower sprite below tower sheet
base_tower = pgm.image.load(r'assets/images/towers/tower1.png').convert_alpha()

# individual tower image for mouse cursor
cursor_tower = pgm.image.load(r'assets/images/towers/tower1.png').convert_alpha()

# enemies
monster_images = {
    "weak": pgm.image.load('assets/images/monsters/enemy1.png').convert_alpha(),
    "medium": pgm.image.load('assets/images/monsters/enemy2.png').convert_alpha(),
    "strong": pgm.image.load('assets/images/monsters/enemy3.png').convert_alpha(),
    "elite": pgm.image.load('assets/images/monsters/enemy4.png').convert_alpha()
}

# buttons
buy_tower_image = pgm.image.load('assets/images/buttons/buy_button.png').convert_alpha()
cancel_button_image = pgm.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
upgrade_button_image = pgm.image.load('assets/images/buttons/upgrade.png').convert_alpha()# sidebar 
begin_image = pgm.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pgm.image.load('assets/images/buttons/restart.png').convert_alpha()
fforward_image = pgm.image.load('assets/images/buttons/fast_forward.png').convert_alpha()# sidebar 
sidebar_image = pgm.image.load('assets/images/gui/sidepanel.png').convert_alpha()
flat_back_image = pgm.image.load('assets/images/gui/flatbg_480x192.png').convert_alpha()

# load json data for monster path in levels
with open(r'bin/levels/level1.tmj') as file:
    world_data = json.load(file)

#load fonts for displaying text on the screen
text_font = pgm.font.SysFont("Consolas", 24, bold = True)
large_font = pgm.font.SysFont("Consolas", 36)

def display_data():
    screen.blit(sidebar_image,(val.SCREEN_WIDTH, 0))
    """ FOR HEALTH ICON DISPLAY """
    draw_text(str(world.health), text_font, "grey100", val.SCREEN_WIDTH + 20, 20)
    """ FOR MONEY ICON DISPLAY """
    draw_text(str(world.money), text_font, "grey100", val.SCREEN_WIDTH + 20, 50)
    """ FOR MONEY ICON DISPLAY """
    draw_text(str(world.level), text_font, "grey100", val.SCREEN_WIDTH + 20, 80)

#function to outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# audio disabled temporarily
# pgm.mixer.music.load(r"assets/audios/bgm2.mp3")
# pgm.mixer.music.play(-1)


# creating tower
def create_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // val.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // val.TILE_SIZE

    # calculating squential numbers of tile on level
    mouse_tile_num = (mouse_tile_y * val.COLS) + mouse_tile_x

    # checking tile if placeable
    if world.tile_map[mouse_tile_num] == 74:
        # checking the place is already occupied by tower
        space_is_free = True
        for tower in tower_groups:
            if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
                space_is_free = False
        # if free then place tower
        if space_is_free == True:
            new_tower = Tower(base_tower, tower_spritesheet, mouse_tile_x, mouse_tile_y)
            tower_groups.add(new_tower)
            # deduct cost of tower
            world.money -= val.BUY_COST


def select_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // val.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // val.TILE_SIZE
    for tower in tower_groups:
        if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
            return tower

def clear_selection():
    for tower in tower_groups:
        tower.selected = False

# create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# creating groups
monster_groups = pgm.sprite.Group()
tower_groups = pgm.sprite.Group()

# create button
tower_button = Button(val.SCREEN_WIDTH + 30, 120, buy_tower_image, True)
cancel_button = Button(val.SCREEN_WIDTH + 30, 240, cancel_button_image, True)
upgrade_button = Button(val.SCREEN_WIDTH + 30, 200, upgrade_button_image, True)
begin_button = Button(val.SCREEN_WIDTH + 30, 320, begin_image, True)
restart_button = Button(val.SCREEN_WIDTH + 30, 360, restart_image, True)
fforward_button = Button(val.SCREEN_WIDTH + 30, 400, fforward_image, False)

# game loop
run = True
while run:

    # limits FPS to 60
    clock.tick(val.FPS) 

    #########################
    # UPDATING SECTION
    #########################

    if game_over == False:
        #check if player has lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1
        #check if player has won
        if world.level > val.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1

        #update groups
        monster_groups.update(world)
        tower_groups.update(monster_groups, world)

        #highlit selected turret
        if selected_tower:
            selected_tower.selected = True

    #########################
    # DRAWING SECTION
    # MIND THE DRAW ORDER!!!
    #########################

    # screen fill ## LEGACY FILLER
    # screen.fill("grey100")

    #draw level
    world.draw(screen)

    #monster path
    pgm.draw.lines(screen, "grey0", False, world.waypoints)

    #draw groups
    monster_groups.draw(screen)
    # tower_groups.draw(screen) ## this is old syntax
    for tower in tower_groups:
        tower.draw(screen)
    
    display_data()

    if game_over == False:
        # cek if the level has been started or not
        if level_started == False:
            if begin_button.draw(screen):
                level_started = True
                #print(begin_button)
        else:
            #fast forward option
            world.game_speed = 1
            if fforward_button.draw(screen):
                world.game_speed = 2
            print(world.game_speed)
            # Spawn enemies
            if pgm.time.get_ticks() - last_enemy_spawn > val.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    monster = Monster(enemy_type, world.waypoints, monster_images)
                    monster_groups.add(monster)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pgm.time.get_ticks()

        #check if the wave is finished
        if world.check_level_complete() == True:
            world.money += val.LEVEL_COMPLETE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pgm.time.get_ticks()
            world.reset_level()
            world.process_enemies()

        #draw buttons
        #button for placing tower
        #for tower button show the cost
        draw_text(str(val.BUY_COST), text_font, "grey100", val.SCREEN_WIDTH + 160, 125)
        if tower_button.draw(screen):
            placing_tower = True
        # if placing then show the cancel button
        if placing_tower == True:
            # show cursor tower
            cursor_rect = cursor_tower.get_rect()
            cursor_pos = pgm.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= val.SCREEN_WIDTH:
                screen.blit(cursor_tower, cursor_rect)
            if cancel_button.draw(screen):
                placing_tower = False
                #print(tower_groups)
        # if a tower is selected, then show the upgrade buttons
        if selected_tower:
            # if a tower can be upgradede the nshow the upgrade buttons
            if selected_tower.upgrade_level < val.TOWER_LEVELS:
                if upgrade_button.draw(screen):
                    if world.money >= val.UPGRADE_COST :
                        selected_tower.upgrade()
                        world.money -= val.UPGRADE_COST
    else:
        screen.blit(flat_back_image,(240, 384))
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", 400, 400)
        elif game_outcome == 1:
            draw_text("YOU WIN?", large_font, "grey0", 400, 400)
        # restart the level
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_tower = False
            selected_tower = None
            last_enemy_spawn = pgm.time.get_ticks()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            #empty groups
            monster_groups.empty()
            tower_groups.empty()
            

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
           # clear selected tower
            selected_tower = False
            clear_selection()
            if placing_tower == True:
                # cek apakah uang cukup buat  beli tower
                if world.money >= val.BUY_COST:
                    create_tower(mouse_pos)
            else:
                selected_tower = select_tower(mouse_pos)
         
        
    #update display
    pgm.display.flip()

pgm.quit()
