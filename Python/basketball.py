import pygame
import numpy as np


class BasketBall:
    mass = 1
    gravity = 500
    radius = 20
    wall_collision_slowdown = 0.5

    def __init__(self, x, y, game):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0, 0], dtype=float)
        self.acc = np.array([0, BasketBall.gravity], dtype=float)
        self.game = game

    def update(self):
        self.pos += self.vel * self.game.dt
        self.vel += self.acc * self.game.dt
        self.check_boundaries()

    def check_boundaries(self):
        if self.pos[0] + BasketBall.radius >= self.game.width:
            self.pos[0] = self.game.width - BasketBall.radius
            self.vel[0] *= -BasketBall.wall_collision_slowdown
        if self.pos[0] - BasketBall.radius <= 0:
            self.pos[0] = BasketBall.radius
            self.vel[0] *= -BasketBall.wall_collision_slowdown
        if self.pos[1] - BasketBall.radius <= 0:
            self.pos[1] = BasketBall.radius
            self.vel[1] *= -BasketBall.wall_collision_slowdown

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (255, 165, 0),
            (int(self.pos[0]), int(self.pos[1])),
            BasketBall.radius,
        )
