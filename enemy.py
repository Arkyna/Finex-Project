import pygame as pgm

class Enemy(pgm.sprite.Sprite):
    def __init__(self, pos, img):
        pgm.sprite.Sprite.__init__(self)
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = pos
 