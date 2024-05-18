import os
import pygame as pgm
import json
from bin import globalvar as val
from bin.monster import Monster
from bin.world import World
from bin.button import Button
from bin.towers.tower1 import FirstTower

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Game:
    def __init__(self):
        pgm.init()
        self.clock = pgm.time.Clock()
        self.screen = pgm.display.set_mode((val.SCREEN_WIDTH + val.SIDE_PANEL, val.SCREEN_HEIGHT))
        pgm.display.set_caption(val.GAME_NAME)
        self.load_assets()
        self.load_world()
        self.setup_game_variables()
        self.run()

    def load_assets(self):
        self.map_image = pgm.image.load('assets/images/map/level1.png').convert_alpha()
        self.tower_spritesheet = [pgm.image.load(f'assets/images/towers/weapon_heavy_arrow_{x}.png').convert_alpha() for x in range(1, val.TOWER_LEVELS + 1)]
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
        self.begin_image = pgm.image.load('assets/images/buttons/begin.png').convert_alpha()
        self.restart_image = pgm.image.load('assets/images/buttons/restart.png').convert_alpha()
        self.fforward_image = pgm.image.load('assets/images/buttons/fast_forward.png').convert_alpha()
        self.sidebar_image = pgm.image.load('assets/images/gui/sidepanel.png').convert_alpha()
        self.flat_back_image = pgm.image.load('assets/images/gui/flatbg_480x192.png').convert_alpha()
        self.text_font = pgm.font.SysFont("Consolas", 24, bold=True)
        self.large_font = pgm.font.SysFont("Consolas", 36)

    def load_world(self):
        with open('bin/levels/level1.tmj') as file:
            world_data = json.load(file)
        self.world = World(world_data, self.map_image)
        self.world.process_data()
        self.world.process_enemies()

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

    def create_buttons(self):
        self.tower_button = Button(val.SCREEN_WIDTH + 30, 120, self.buy_tower_image, True)
        self.cancel_button = Button(val.SCREEN_WIDTH + 30, 240, self.cancel_button_image, True)
        self.upgrade_button = Button(val.SCREEN_WIDTH + 30, 200, self.upgrade_button_image, True)
        self.begin_button = Button(val.SCREEN_WIDTH + 30, 320, self.begin_image, True)
        self.restart_button = Button(val.SCREEN_WIDTH + 30, 360, self.restart_image, True)
        self.fforward_button = Button(val.SCREEN_WIDTH + 30, 400, self.fforward_image, False)

    def run(self):
        while True:
            self.clock.tick(val.FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pgm.event.get():
            if event.type == pgm.QUIT:
                pgm.quit()
                exit()

            if event.type == pgm.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(pgm.mouse.get_pos())

    def handle_mouse_click(self, mouse_pos):
        if mouse_pos[0] < val.SCREEN_WIDTH and mouse_pos[1] < val.SCREEN_HEIGHT:
            self.selected_tower = False
            self.clear_selection()
            if self.placing_tower:
                if self.world.money >= val.BUY_COST:
                    self.create_tower(mouse_pos)
            else:
                self.selected_tower = self.select_tower(mouse_pos)

    def create_tower(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // val.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // val.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * val.COLS) + mouse_tile_x
        if self.world.tile_map[mouse_tile_num] == 74:
            if not any((mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y) for tower in self.tower_groups):
                new_tower = FirstTower(self.base_tower, self.tower_spritesheet, mouse_tile_x, mouse_tile_y)
                self.tower_groups.add(new_tower)
                self.world.money -= val.BUY_COST

    def select_tower(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // val.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // val.TILE_SIZE
        for tower in self.tower_groups:
            if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
                return tower

    def clear_selection(self):
        for tower in self.tower_groups:
            tower.selected = False

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
                        monster = Monster(enemy_type, self.world.waypoints, self.monster_images)
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

    def check_game_outcome(self):
        if self.world.health <= 0:
            self.game_over = True
            self.game_outcome = -1
        if self.world.level > val.TOTAL_LEVELS:
            self.game_over = True
            self.game_outcome = 1

    def draw(self):
        self.world.draw(self.screen)
        pgm.draw.lines(self.screen, "grey0", False, self.world.waypoints)
        self.monster_groups.draw(self.screen)
        for tower in self.tower_groups:
            tower.draw(self.screen)
        self.display_data()

        if not self.game_over:
            if not self.level_started:
                if self.begin_button.draw(self.screen):
                    self.level_started = True
            self.draw_buttons()
        else:
            self.screen.blit(self.flat_back_image, (240, 384))
            self.draw_game_over()
            if self.restart_button.draw(self.screen):
                self.reset_game()

        pgm.display.flip()

    def draw_buttons(self):
        self.draw_text(str(val.BUY_COST), self.text_font, "grey100", val.SCREEN_WIDTH + 160, 125)
        if self.tower_button.draw(self.screen):
            self.placing_tower = True
        if self.placing_tower:
            cursor_rect = self.cursor_tower.get_rect()
            cursor_pos = pgm.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= val.SCREEN_WIDTH:
                self.screen.blit(self.cursor_tower, cursor_rect)
            if self.cancel_button.draw(self.screen):
                self.placing_tower = False
        if self.selected_tower and self.selected_tower.upgrade_level < val.TOWER_LEVELS:
            if self.upgrade_button.draw(self.screen):
                if self.world.money >= val.UPGRADE_COST:
                    self.selected_tower.upgrade()
                    self.world.money -= val.UPGRADE_COST
        if self.level_started:
                self.fforward_button.draw(self.screen)

    def draw_game_over(self):
        self.draw_text("GAME OVER" if self.game_outcome == -1 else "YOU WIN?", self.large_font, "grey0", 400, 400)

    def reset_game(self):
        self.game_over = False
        self.level_started = False
        self.placing_tower = False
        self.selected_tower = None
        self.last_enemy_spawn = pgm.time.get_ticks()
        self.load_world()
        self.monster_groups.empty()
        self.tower_groups.empty()

    def display_data(self):
        self.screen.blit(self.sidebar_image, (val.SCREEN_WIDTH, 0))
        self.draw_text(str(self.world.health), self.text_font, "grey100", val.SCREEN_WIDTH + 20, 20)
        self.draw_text(str(self.world.money), self.text_font, "grey100", val.SCREEN_WIDTH + 20, 50)
        self.draw_text(str(self.world.level), self.text_font, "grey100", val.SCREEN_WIDTH + 20, 80)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

if __name__ == "__main__":
    Game()
