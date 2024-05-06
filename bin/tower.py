from typing import Any
import pygame as pgm
from . import globalvar as val


class Tower(pgm.sprite.Sprite):
    def __init__(self, base_tower, sprite_sheet, tile_x, tile_y):
        pgm.sprite.Sprite.__init__(self)
        #cooldown counter
        self.cooldown = 1500
        self.last_frame = pgm.time.get_ticks()

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

        # animation var
        self.sprite_sheet = sprite_sheet
        self.animation_frames = self.load_images()
        self.frame_index = 0
        self.update_time = pgm.time.get_ticks()

        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        
    def load_images(self):
        # extracting image from sprite sheet
        size = self.sprite_sheet.get_height()
        animation_frames = []
        for x in range(val.ANIMATION_STEPS):
            temp_frames = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_frames.append(temp_frames)
        return animation_frames
    
    def update(self):
        #search for new target once tower has cooled down
        if pgm.time.get_ticks() - self.last_frame > self.cooldown:
            self.play_animation()
    
    def play_animation(self):
        #updating image
        self.image = self.animation_frames[self.frame_index]
        
        #checking if enough time has passed since last update
        if pgm.time.get_ticks() - self. update_time > val.ANIMATION_DELAY:
            self.update_time = pgm.time.get_ticks()
            self.frame_index += 1

            #check if the animation has finished and reset to idle state
            if self.frame_index >= len(self.animation_frames):
                self.frame_index = 0
                #record completed time and clear target so the cooldown can start
                self.last_frame = pgm.time.get_ticks()