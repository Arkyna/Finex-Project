import pygame as pgm

class Button():
    def __init__(self, x , y , image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pgm.mouse.get_pos()
        
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pgm.mouse.get_pressed()[0] == 1 and self.clicked == False :
                action = True
                # if button is a single click type then click to the True
                if self.single_click:
                    self.clicked = True

                    
        if pgm.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw buttoon on screen
        surface.blit(self.image, self.rect)

        return action

#testing coomit