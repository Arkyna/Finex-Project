import pygame as pgm
from pygame.math import Vector2
import math

class Enemy(pgm.sprite.Sprite):
    def __init__(self, waypoints, image):
        pgm.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 1.5
        self.angle = 0
        self.original_image = image
        self.image = pgm.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def update(self):
        self.move()
        self.rotate()

    def move(self):
        #defining target waypoint
        if self.target_waypoint < len(self.waypoints):     
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #enemy reached the end of the path
            self.kill()

        #calculating distance to target
        dist = self.movement.length()

        #check if remaining distance is greater than the enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        #calculating distance to the next waypoint
        dist = self.target - self.pos
        #using distance to calculate angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        #rotating image and updating rectangle
        self.image = pgm.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos