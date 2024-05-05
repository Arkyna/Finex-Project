import pygame as pgm

class Button():
    def __init__(self, x , y , image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        # get mouse position
        pos = pgm.mouse.get_pos()
        

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pgm.mouse.get_pressed()[0] == 1:
                pass

        # draw buttoon on screen
        surface.blid(self.image, self.rect)

#testing coomit