import pygame as pgm
from . import globalvar as val


class Tower(pgm.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y):
        pgm.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y

        #calculating center coordinates
        self.x = self.tile_x * val.TILE_SIZE
        self.y = self.tile_y * val.TILE_SIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        