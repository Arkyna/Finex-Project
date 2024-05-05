import pygame as pgm

class Tower(pgm.sprite.Sprite):
    def __init__(self, image, pos):
        pgm.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        