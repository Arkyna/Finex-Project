from typing import Any
import pygame as pgm
import math
from .. import globalvar as val


class Tower(pgm.sprite.Sprite):
    def __init__(self, base_tower, sprite_sheets, tile_x, tile_y):
        pgm.sprite.Sprite.__init__(self)

        # variables
        self.upgrade_level = 1
        self.range = val.TOWER_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = val.TOWER_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_frame = pgm.time.get_ticks()
        self.selected = False
        self.target = None


        # position var
        self.tile_x = tile_x
        self.tile_y = tile_y

        # calculating center coordinates
        self.x = (self.tile_x + 0.5) * val.TILE_SIZE
        self.y = self.tile_y * val.TILE_SIZE

        # tower base image
        self.base_tower = base_tower
        self.base_rect = self.base_tower.get_rect()
        self.base_rect.center = (self.x, self.y)

        # animation frame variable
        self.sprite_sheets = sprite_sheets
        self.animation_frames = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pgm.time.get_ticks()

        # animation actual updator sprite
        self.angle = 90
        self.original_image = self.animation_frames[self.frame_index]
        self.image = pgm.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, (self.y - 30))

        #creating transparent circle showing range
        self.range_image = pgm.Surface((self.range * 2, self. range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pgm.draw.circle(self.range_image, "grey100",(self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        
    def load_images(self, sprite_sheet):
        # extracting image from sprite sheet
        size = sprite_sheet.get_height()
        animation_frames = []
        for x in range(val.ANIMATION_STEPS):
            temp_frames = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_frames.append(temp_frames)
        return animation_frames
    
    def update(self, monster_groups, world):
        #if target picked, play firing animation
        if self.target:
            self.play_animation()
        else:
        #search for new target once tower has cooled down
            if pgm.time.get_ticks() - self.last_frame > (self.cooldown / world.game_speed):
                self.pick_target(monster_groups)

    def pick_target(self, monster_groups):
        # finding enemy to target
        x_dist = 0
        y_dist = 0

        #check distance to each enemy that in range
        for monster in monster_groups:
            if monster.health > 0:
                x_dist = monster.pos[0] - self.x
                y_dist = monster.pos[1] - self.y
                dist = math.sqrt(x_dist **2 + y_dist ** 2)
                if dist < self.range:
                    self.target = monster
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.target.health -= val.DAMAGE
                    break
    
    def play_animation(self):
        #updating image
        self.original_image = self.animation_frames[self.frame_index]
        
        #checking if enough time has passed since last update
        if pgm.time.get_ticks() - self. update_time > val.ANIMATION_DELAY:
            self.update_time = pgm.time.get_ticks()
            self.frame_index += 1

            #check if the animation has finished and reset to idle state
            if self.frame_index >= len(self.animation_frames):
                self.frame_index = 0
                #record completed time and clear target so the cooldown can start
                self.last_frame = pgm.time.get_ticks()
                self.target = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = val.TOWER_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = val.TOWER_DATA[self.upgrade_level - 1].get("cooldown")

        #upgrade tower images
        self.animation_frames = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_frames[self.frame_index]

        #upgrade transparent circle showing range
        self.range_image = pgm.Surface((self.range * 2, self. range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pgm.draw.circle(self.range_image, "grey100",(self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        self.image = pgm.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, (self.y - 30))
        surface.blit(self.base_tower, self.base_rect)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
    