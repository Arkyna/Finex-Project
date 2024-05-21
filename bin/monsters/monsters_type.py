import pygame as pgm
from pygame.math import Vector2
import math
from .monster import Monster  # Import the abstract Monster class

class BasicMonster(Monster):
    def __init__(self, enemy_type, waypoints, images):
        super().__init__(enemy_type, waypoints, images)
        self.stunned = False
        self.stun_end_time = 0
        
    def move(self, world):
        if self.stunned and pgm.time.get_ticks() < self.stun_end_time:
            return  # Skip movement if stunned

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
        if self.target:
            dist = self.target - self.pos
            angle = math.degrees(math.atan2(-dist.y, dist.x))

            # Adjust angle to ensure natural left/right turning
            if -90 <= angle <= 90:  # Facing right
                self.angle = 0
            else:  # Facing left
                self.angle = 180

            # Flip the image if facing left
            if self.angle == 180:
                self.image = pgm.transform.flip(self.original_image, True, False)
            else:
                self.image = pgm.transform.rotate(self.original_image, self.angle)

            self.rect = self.image.get_rect()
            self.rect.center = self.pos


    def stun(self, duration: int) -> None:
        self.stunned = True
        self.stun_end_time = pgm.time.get_ticks() + duration

class FastMonster(Monster):
    def __init__(self, enemy_type, waypoints, images):
        super().__init__(enemy_type, waypoints, images)
        self.stunned = False
        self.stun_end_time = 0
        self.speed *= 1.3  # FastMonster walk faster
        

    def move(self, world):
        if self.stunned and pgm.time.get_ticks() < self.stun_end_time:
            return  # Skip movement if stunned
        
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
        if self.target:
            dist = self.target - self.pos
            angle = math.degrees(math.atan2(-dist.y, dist.x))

            # Adjust angle to ensure natural left/right turning
            if -90 <= angle <= 90:  # Facing right
                self.angle = 0
            else:  # Facing left
                self.angle = 180

            # Flip the image if facing left
            if self.angle == 180:
                self.image = pgm.transform.flip(self.original_image, True, False)
            else:
                self.image = pgm.transform.rotate(self.original_image, self.angle)

            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    def stun(self, duration: int) -> None:
        self.stunned = True
        self.stun_end_time = pgm.time.get_ticks() + duration

class BossMonster(Monster):
    def __init__(self, enemy_type, waypoints, images):
        super().__init__(enemy_type, waypoints, images)
        self.stunned = False
        self.stun_end_time = 0
        self.speed -= 1.2  # BossMonster walk slower
        self.health *= 3 # BossMonster got bigger health points

    def move(self, world):
        if self.stunned and pgm.time.get_ticks() < self.stun_end_time:
            return  # Skip movement if stunned

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
        if self.target:
            dist = self.target - self.pos
            angle = math.degrees(math.atan2(-dist.y, dist.x))

            # Adjust angle to ensure natural left/right turning
            if -90 <= angle <= 90:  # Facing right
                self.angle = 0
            else:  # Facing left
                self.angle = 180

            # Flip the image if facing left
            if self.angle == 180:
                self.image = pgm.transform.flip(self.original_image, True, False)
            else:
                self.image = pgm.transform.rotate(self.original_image, self.angle)

            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    def stun(self, duration: int) -> None:
        self.stunned = True
        self.stun_end_time = pgm.time.get_ticks() + duration

