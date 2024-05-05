import pygame as pgm
from bin.enemy import Enemy

#initialisasi
pgm.init()

#create clock
clock = pgm.time.Clock()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60

#creating window game
screen = pgm.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pgm.display.set_caption("TDEFENSE")

#load image
enemy_image = pgm.image.load('assets\images\monsters\enemy1.png').convert_alpha()

#creating groups
enemy_groups = pgm.sprite.Group()

waypoints = [
    (100, 100),
    (250, 250),
    (280, 180),
    (90, 200)
]

enemy = Enemy(waypoints, enemy_image)
enemy_groups.add(enemy)

#game loop
run = True
while run:

    # limits FPS to 60
    clock.tick(FPS) 

    #screen fill
    screen.fill("grey100")

    #enemy path
    pgm.draw.lines(screen, "grey0", False, waypoints)

    #update groups
    enemy_groups.update()


    #draw groups
    enemy_groups.draw(screen)

    #event handler
    for event in pgm.event.get():
            #quit program
        if event.type == pgm.QUIT:
            run = False

    #update display
    pgm.display.flip()

pgm.quit()
