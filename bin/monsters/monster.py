import pygame as pgm
from pygame.math import Vector2
import math
from abc import ABC, abstractmethod
from .. import globalvar as val

class Monster(pgm.sprite.Sprite, ABC):
    def __init__(self, enemy_type, waypoints, images):
        super().__init__()
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = val.ENEMY_DATA.get(enemy_type)["health"]
        self.speed = val.ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pgm.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    # logics for following existing waypoints or path
    @abstractmethod
    def move(self, world):
        pass

    # rotating the images 
    @abstractmethod
    def rotate(self):
        pass

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += val.KILL_REWARD
            self.kill()
