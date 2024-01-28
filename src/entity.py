import random

from pygame import Vector2
import pygame


class Entity:
    def __init__(self,
                 pos: tuple = (0, 0), velocity: tuple = (0, 0), size: int = 32, mass: int = 1,
                 color: tuple = (255, 255, 255)):
        self.pos = Vector2(pos)
        self.velocity = Vector2(velocity)
        self.size = size
        self.mass = mass
        self.color = color
        self.friction = 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.size / 2)
        self.draw_velocity_vector(surface)

    def draw_velocity_vector(self, surface):
        second_point = (self.pos + self.velocity * 12)
        pygame.draw.line(surface, (255, 255, 255), self.pos, second_point)
        pygame.draw.circle(surface, (255, 0, 0), second_point, self.size / 8)

    def clamp_pos(self, min_x, min_y, max_x, max_y):
        if (self.pos.x <= min_x + self.size / 2 or
                self.pos.x >= max_x - self.size / 2 or
                self.pos.y <= min_y + self.size / 2 or
                self.pos.y >= max_y - self.size / 2):
            self.velocity = Vector2(0, 0)
            self.pos.x = max(min_x + self.size / 2, min(self.pos.x, max_x - self.size / 2))
            self.pos.y = max(min_y + self.size / 2, min(self.pos.y, max_y - self.size / 2))

    def move(self, dx=0, dy=0):
        move = Vector2(dx, dy)
        self.velocity *= self.friction
        if move.length() != 0:
            self.velocity += move.normalize()
        self.pos += self.velocity
