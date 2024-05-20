from typing import Any, List
import pygame as pgm
import math
from .. import globalvar as val
from .tower import Tower  # Import the base Tower class

class DefaultTower(Tower):
    def load_images(self, sprite_sheet) -> List[Any]:
        size = sprite_sheet.get_height()
        animation_frames = []
        for x in range(val.ANIMATION_STEPS):
            temp_frame = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_frames.append(temp_frame)
        return animation_frames

    def update(self, monster_groups: pgm.sprite.Group, world: Any) -> None:
        if self.target:
            self.play_animation()
        else:
            if pgm.time.get_ticks() - self.last_frame > (self.cooldown / world.game_speed):
                self.pick_target(monster_groups)

    def pick_target(self, monster_groups: pgm.sprite.Group) -> None:
        for monster in monster_groups:
            if monster.health > 0:
                x_dist = monster.pos[0] - self.x
                y_dist = monster.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = monster
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.target.health -= val.DAMAGE
                    break

    def play_animation(self) -> None:
        self.original_image = self.animation_frames[self.frame_index]
        if pgm.time.get_ticks() - self.update_time > val.ANIMATION_DELAY:
            self.update_time = pgm.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_frames):
                self.frame_index = 0
                self.last_frame = pgm.time.get_ticks()
                self.target = None
    
    

    def upgrade(self) -> None:
        self.upgrade_level += 1
        self.range = val.TOWER_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = val.TOWER_DATA[self.upgrade_level - 1].get("cooldown")

        self.animation_frames = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_frames[self.frame_index]

        self.range_image = pgm.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pgm.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

class ElectricTower(Tower):
    def load_images(self, sprite_sheet) -> List[Any]:
        self.stun_duration = 500  # Duration in milliseconds
        size = sprite_sheet.get_height()
        animation_frames = []
        for x in range(16):
            temp_frame = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_frames.append(temp_frame)
        return animation_frames

    def update(self, monster_groups: pgm.sprite.Group, world: Any) -> None:
        if self.target:
            self.play_animation()
        else:
            if pgm.time.get_ticks() - self.last_frame > (self.cooldown / world.game_speed):
                self.pick_target(monster_groups)

    def pick_target(self, monster_groups: pgm.sprite.Group) -> None:
        for monster in monster_groups:
            if monster.health > 0:
                x_dist = monster.pos[0] - self.x
                y_dist = monster.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = monster
                    # disabling the rotation of the tower
                    # self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.apply_stun(monster)  # Apply the stun effect
                    self.target.health -= val.DAMAGE
                    break

    def apply_stun(self, monster) -> None:
        monster.stun(self.stun_duration)               

    def play_animation(self) -> None:
        self.original_image = self.animation_frames[self.frame_index]
        if pgm.time.get_ticks() - self.update_time > val.ANIMATION_DELAY:
            self.update_time = pgm.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_frames):
                self.frame_index = 0
                self.last_frame = pgm.time.get_ticks()
                self.target = None

    def upgrade(self) -> None:
        self.upgrade_level += 1
        self.range = val.TOWER_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = val.TOWER_DATA[self.upgrade_level - 1].get("cooldown")

        self.animation_frames = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_frames[self.frame_index]

        self.range_image = pgm.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pgm.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def setup_range_image(self) -> None:
        self.range_image = pgm.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pgm.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def initialize_from_tower(self, tower):
        self.upgrade_level = tower.upgrade_level
        self.range = tower.range
        self.cooldown = tower.cooldown
        self.animation_frames = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_frames[0]
        self.setup_range_image()


