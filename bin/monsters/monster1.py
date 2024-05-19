import pygame as pgm
from pygame.math import Vector2
import math
from .monster import Monster  # Import the abstract Monster class
from .. import globalvar as val

class BasicMonster(Monster):
    def __init__(self, enemy_type, waypoints, images):
        super().__init__(enemy_type, waypoints, images)
        
    def move(self, world):
        if self.target_waypoint < len(self.waypoints):     
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
            world.health -= 1
            world.missed_enemies += 1

        dist = self.movement.length()

        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        self.image = pgm.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
