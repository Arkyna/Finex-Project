from abc import ABC, abstractmethod
from typing import Any, List
import pygame as pgm
import math
from .. import globalvar as val

class Tower(pgm.sprite.Sprite, ABC):
    def __init__(self, base_tower, sprite_sheets, tile_x, tile_y):
        super().__init__()
        self.upgrade_level = 1
        self.range = val.TOWER_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = val.TOWER_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_frame = pgm.time.get_ticks()
        self.selected = False
        self.target = None

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = (self.tile_x + 0.5) * val.TILE_SIZE
        self.y = self.tile_y * val.TILE_SIZE

        self.base_tower = base_tower
        self.base_rect = self.base_tower.get_rect()
        self.base_rect.center = (self.x, self.y)

        self.sprite_sheets = sprite_sheets
        self.animation_frames = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pgm.time.get_ticks()

        self.angle = 90
        self.original_image = self.animation_frames[self.frame_index]
        self.image = pgm.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, (self.y - 30))

        self.range_image = pgm.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pgm.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    @abstractmethod
    def load_images(self, sprite_sheet) -> List[Any]:
        pass

    @abstractmethod
    def update(self, monster_groups: pgm.sprite.Group, world: Any) -> None:
        pass

    @abstractmethod
    def pick_target(self, monster_groups: pgm.sprite.Group) -> None:
        pass

    @abstractmethod
    def play_animation(self) -> None:
        pass

    @abstractmethod
    def upgrade(self) -> None:
        pass

    def draw(self, surface: pgm.Surface) -> None:
        self.image = pgm.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, (self.y - 30))
        surface.blit(self.base_tower, self.base_rect)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
