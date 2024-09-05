import pygame
import numpy as np

BASKETBALL_RADIUS = 20
PLAYER_PUSH_POWER = 500
BALL_GRAVITY = 500


class Ball:
    def __init__(self, x, y, radius, game):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0, 0], dtype=float)
        self.acc = np.array([0, BALL_GRAVITY], dtype=float)
        self.radius = radius
        self.game = game

    def update(self):
        self.pos += self.vel * self.game.dt
        self.vel += self.acc * self.game.dt
        self.check_boundaries()

    def check_boundaries(self):
        if self.pos[0] + self.radius >= self.game.width:
            self.pos[0] = self.game.width - self.radius
            self.vel[0] *= -0.8
        if self.pos[0] - self.radius <= 0:
            self.pos[0] = self.radius
            self.vel[0] *= -0.8
        if self.pos[1] - self.radius <= 0:
            self.pos[1] = self.radius
            self.vel[1] *= -0.8

    def check_collision(self, player):
        distance = np.linalg.norm(self.pos - player.pos)
        if distance <= self.radius + player.radius:
            self.handle_collision(player)

    def handle_collision(self, player):
        direction = self.pos - player.pos
        direction = direction / np.linalg.norm(direction)  # Normalize the vector
        self.vel = direction * PLAYER_PUSH_POWER

    def draw(self, surface):
        pygame.draw.circle(
            surface, (255, 165, 0), (int(self.pos[0]), int(self.pos[1])), self.radius
        )
