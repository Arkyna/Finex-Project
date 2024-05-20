import pygame as pgm
import json
from bin import globalvar as val
from bin.monsters.monsters_type import BasicMonster, FastMonster, BossMonster
from bin.world import World
from bin.button import Button
from bin.towers.towers_type import DefaultTower, ElectricTower

# The whole game initialization
class Game:
    def __init__(self, map_choice):
        # initialize them pygame modules
        pgm.init()
        # store the map choice
        self.map_choice = map_choice
        # create a clock for the frame rate and time management
        self.clock = pgm.time.Clock()
        # set the game window title
        self.screen = pgm.display.set_mode((val.SCREEN_WIDTH, val.SCREEN_HEIGHT))
        pgm.display.set_caption(val.GAME_NAME)
        # load the assets needed for the game
        self.load_assets()
        # load the game world
        self.load_world()
        # set up the initial game variables
        self.setup_game_variables()
        # calling or starting the main loop of the game 
    
    def start_game(self):
        self.run()

    # Load the images and assets
    def load_assets(self):
        if self.map_choice == 'day':
            self.map_image = pgm.image.load('assets/images/map/level1.png').convert_alpha()
        else:
            self.map_image = pgm.image.load('assets/images/map/map_1_night_vers.png').convert_alpha()

        # self.map_image = pgm.image.load('assets/images/map/level1.png').convert_alpha()
        self.basic_tower_spritesheet = [pgm.image.load(f'assets/images/towers/basic_tower_{x}.png').convert_alpha() for x in range(1, val.TOWER_LEVELS + 1)]
        self.electric_tower_spritesheet = [pgm.image.load(f'assets/images/towers/electric_tower_{x}.png').convert_alpha() for x in range(1, val.TOWER_LEVELS + 1)]
        self.base_tower = pgm.image.load(r'assets/images/towers/ABC_tower.png').convert_alpha()
        self.cursor_tower = pgm.image.load(r'assets/images/towers/cursor_tower.png').convert_alpha()
        self.monster_images = {
            "weak": pgm.image.load(r'assets/images/monsters/enemy1.png').convert_alpha(),
            "medium": pgm.image.load(r'assets/images/monsters/enemy2.png').convert_alpha(),
            "strong": pgm.image.load(r'assets/images/monsters/enemy3.png').convert_alpha(),
            "elite": pgm.image.load(r'assets/images/monsters/enemy4.png').convert_alpha()
        }
        self.buy_tower_image = pgm.image.load('assets/images/buttons/buy_button.png').convert_alpha()
        self.cancel_button_image = pgm.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
        self.upgrade_button_image = pgm.image.load('assets/images/buttons/upgrade.png').convert_alpha()
        self.change_button_image = pgm.image.load('assets/images/buttons/change_button.png').convert_alpha()
        self.begin_image = pgm.image.load('assets/images/buttons/begin.png').convert_alpha()
        self.restart_image = pgm.image.load('assets/images/buttons/restart.png').convert_alpha()
        self.fforward_image = pgm.image.load('assets/images/buttons/fast_forward.png').convert_alpha()

        # side bar selection
        if self.map_choice == 'day':
            self.sidebar_image = pgm.image.load('assets/images/gui/sidepanel.png').convert_alpha()
        else:
            self.sidebar_image = pgm.image.load('assets/images/gui/side_nightversion.png').convert_alpha()

        self.flat_back_image = pgm.image.load('assets/images/gui/flatbg_480x192.png').convert_alpha()
        self.large_font = pgm.font.Font(r"assets\font\MinecraftBold-nMK1.otf", 36)
        self.text_font = pgm.font.Font(r"assets\font\MinecraftRegular-Bmg3.otf", 24)

    # loading the world 
    def load_world(self):
        # this JSON consist of world data, that contains path of the level, and we load it first
        with open('bin/levels/level1.tmj') as file:
            world_data = json.load(file)
        # creating world object with the loaded world/level image
        self.world = World(world_data, self.map_image)
        # process the world data from the JSON that extracted in world.py
        self.world.process_data()
        # load and process the enemies into the level
        self.world.process_enemies()

    # set up the initial game variables
    def setup_game_variables(self):
        self.game_over = False
        self.game_outcome = 0  # -1 = losing, 1 = Winning
        self.level_started = False
        self.last_enemy_spawn = pgm.time.get_ticks()
        self.placing_tower = False
        self.selected_tower = None
        self.monster_groups = pgm.sprite.Group()
        self.tower_groups = pgm.sprite.Group()
        self.create_buttons()

    # creating the buttons here and draw it on other methods
    def create_buttons(self):
        self.tower_button = Button(990, 120, self.buy_tower_image, True)
        self.cancel_button = Button(990, 240, self.cancel_button_image, True)
        self.upgrade_button = Button(990, 180, self.upgrade_button_image, True)
        self.change_button = Button(990, 240, self.change_button_image, True)
        self.begin_button = Button(990, 320, self.begin_image, True)
        self.restart_button = Button(990, 360, self.restart_image, True)
        self.fforward_button = Button(990, 400, self.fforward_image, False)

        '''dynammically reposition the buttons using the widht of the screen and calculate it from that numbers
        examples *formula = (screen widht) - (screen width-position)* for the button position it should automaitcally reposition itself
        this is just a random trivia'''

    # the main game loop
    def run(self):
        while True:
            # frame limiter
            self.clock.tick(val.FPS)
            # handle events
            self.handle_events()
            # updating the game logics for each frame
            self.update()
            # draw the elements on the screen
            self.draw()

    # events handlers/controller
    def handle_events(self):
        for event in pgm.event.get():
            if event.type == pgm.QUIT:
                # quitting the game if the windows is closed
                pgm.quit()
                exit()

             # handle the left mouse button click
            if event.type == pgm.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(pgm.mouse.get_pos())
    
    # handling the logic if the mouse is clicked, and determine if the tower is selected or to place a tower
    def handle_mouse_click(self, mouse_pos):
        if mouse_pos[0] < 960 and mouse_pos[1] < val.SCREEN_HEIGHT:
            self.selected_tower = False
            self.clear_selection()
            if self.placing_tower:
                if self.world.money >= val.BUY_COST:
                    self.create_tower(mouse_pos)
            else:
                self.selected_tower = self.select_tower(mouse_pos)

    # creating a new tower based on the mouse position and check if the money is enough/valid
    def create_tower(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // val.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // val.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * val.COLS) + mouse_tile_x
        if self.world.tile_map[mouse_tile_num] == 74:
            if not any((mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y) for tower in self.tower_groups):
                # Tower types
                default_tower = DefaultTower(self.base_tower, self.basic_tower_spritesheet, mouse_tile_x, mouse_tile_y)
                self.tower_groups.add(default_tower)
                self.world.money -= val.BUY_COST
    
    # select an existing tower
    def select_tower(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // val.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // val.TILE_SIZE
        for tower in self.tower_groups:
            if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
                return tower

    # clear selected tower
    def clear_selection(self):
        for tower in self.tower_groups:
            tower.selected = False

    # updating the whole game for each loop
    def update(self):
        if not self.game_over:
            self.check_game_outcome()
            self.monster_groups.update(self.world)
            self.tower_groups.update(self.monster_groups, self.world)
            if self.selected_tower:
                self.selected_tower.selected = True
            if self.level_started:
                self.world.game_speed = 1
                if self.fforward_button.draw(self.screen):
                    self.world.game_speed = 2
                if pgm.time.get_ticks() - self.last_enemy_spawn > val.SPAWN_COOLDOWN:
                    if self.world.spawned_enemies < len(self.world.enemy_list):
                        enemy_type = self.world.enemy_list[self.world.spawned_enemies]
                        monster = self.create_monster(enemy_type, self.world.waypoints)
                        self.monster_groups.add(monster)
                        self.world.spawned_enemies += 1
                        self.last_enemy_spawn = pgm.time.get_ticks()
                if self.world.check_level_complete():
                    self.world.money += val.LEVEL_COMPLETE_REWARD
                    self.world.level += 1
                    self.level_started = False
                    self.last_enemy_spawn = pgm.time.get_ticks()
                    self.world.reset_level()
                    self.world.process_enemies()
    
    # draw monsters variants or types
    def create_monster(self, enemy_type, waypoints):
        if enemy_type == "weak":
            return BasicMonster("weak", waypoints, self.monster_images)
        elif enemy_type == "medium":
            return FastMonster("medium", waypoints, self.monster_images)
        elif enemy_type == "strong":
            return BossMonster("strong", waypoints, self.monster_images)
    
    # checking the variables of the game state to determine the game over
    def check_game_outcome(self):
        if self.world.health <= 0:
            self.game_over = True
            self.game_outcome = -1
        if self.world.level > val.TOTAL_LEVELS:
            self.game_over = True
            self.game_outcome = 1

    # draw all the elements into the screen
    def draw(self):
        self.world.draw(self.screen)
        # level path uncomment to enable the path drawing
        #pgm.draw.lines(self.screen, "grey0", False, self.world.waypoints)
        # draw the monsters
        self.monster_groups.draw(self.screen)
        # draw each tower that in tower_group
        for tower in self.tower_groups:
            tower.draw(self.screen)
        # display the game's data, such as money, base health, and level
        self.display_data()

        # draw the begin button if the game haven't started
        if not self.game_over:
            if not self.level_started:
                if self.begin_button.draw(self.screen):
                    self.level_started = True
            self.draw_buttons()
        else:
            # calling the game over screen, and resetting the level as the reset button is pressed, as the reset button is drawn on the screen
            self.screen.blit(self.flat_back_image, (240, 384))
            self.draw_game_over()
            # reset the game if the restart button is pressed
            if self.restart_button.draw(self.screen):
                self.reset_game()

        pgm.display.flip()

    # draw dat interactive buttons on the screen
    def draw_buttons(self):
        self.draw_text(str(val.BUY_COST), self.text_font, "grey100", 1120, 125)
        if self.tower_button.draw(self.screen):
            self.placing_tower = True
        if self.placing_tower:
            cursor_rect = self.cursor_tower.get_rect()
            cursor_pos = pgm.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= 960:
                self.screen.blit(self.cursor_tower, cursor_rect)
            if self.cancel_button.draw(self.screen):
                self.placing_tower = False
        if self.selected_tower:
            if self.selected_tower.upgrade_level < val.TOWER_LEVELS:
            # upgrade button and logics
                if self.upgrade_button.draw(self.screen):
                    if self.world.money >= val.UPGRADE_COST:
                        self.selected_tower.upgrade()
                        self.world.money -= val.UPGRADE_COST
                if isinstance(self.selected_tower, DefaultTower):
                    if self.change_button.draw(self.screen):
                        if self.world.money >= 10:
                            self.change_tower_element(self.selected_tower)
                            self.world.money -= 10
        if self.level_started:
                self.fforward_button.draw(self.screen)
    
    # changing the tower element into electric
    def change_tower_element(self, tower):
        electric_tower = ElectricTower(self.base_tower, self.electric_tower_spritesheet, tower.tile_x, tower.tile_y)
        electric_tower.initialize_from_tower(tower)
        self.tower_groups.remove(tower)
        self.tower_groups.add(electric_tower)
        self.selected_tower = electric_tower

    # draw the game over and victory messages on the screen
    def draw_game_over(self):
        self.draw_text("GAME OVER" if self.game_outcome == -1 else "YOU WIN?", self.large_font, "grey0", 400, 400)

    # reset the game state
    def reset_game(self):
        self.game_over = False
        self.level_started = False
        self.placing_tower = False
        self.selected_tower = None
        self.last_enemy_spawn = pgm.time.get_ticks()
        self.load_world()
        self.monster_groups.empty()
        self.tower_groups.empty()

    # display the data of game such as healt, money, and current level
    def display_data(self):
        self.screen.blit(self.sidebar_image, (960, 0))
        self.draw_text(str("Health  : "), self.text_font, "grey100", 980, 20)
        self.draw_text(str(self.world.health), self.text_font, "grey100", 1090, 20)
        self.draw_text(str("Money   : "), self.text_font, "grey100", 980, 50)
        self.draw_text(str(self.world.money), self.text_font, "grey100", 1090, 50)
        self.draw_text(str("Level   : "), self.text_font, "grey100", 980, 80)
        self.draw_text(str(self.world.level), self.text_font, "grey100", 1090, 80)

    # text drawing
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

# uncomment the line below for running the game directly from this file
if __name__ == "__main__":
    Game("Malam")

''' 
OOP that have been applied on this game:

Classes and Objects can be found at this same file,
Inheritance, Encapsulation and polymorphism can be found at monster_type.py,
Abstraction can be found at tower.py and monster.py,
another Encapsulation can be found at main_menu.py the screen variable is well encapsulated

'''