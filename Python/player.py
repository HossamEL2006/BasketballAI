import pygame
import numpy as np

PLAYER_GRAVITY = 700
PLAYER_RADIUS = 30
PLAYER_PUSHBACK = 200
PLAYER_JUMP_FORCE = 700


class Player:
    def __init__(self, x, y, radius, game):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0, 0], dtype=float)
        self.acc = np.array([0, PLAYER_GRAVITY], dtype=float)
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

    def check_collision(self, basketball):
        distance = np.linalg.norm(self.pos - basketball.pos)
        if distance <= self.radius + basketball.radius:
            self.handle_collision(basketball)

    def handle_collision(self, basketball):
        direction = self.pos - basketball.pos
        direction = direction / np.linalg.norm(direction)  # Normalize the vector
        self.vel = -direction * PLAYER_PUSHBACK

    def push(self, target_pos):
        direction = target_pos - self.pos
        direction = direction / np.linalg.norm(direction)  # Normalize the vector
        self.vel = direction * PLAYER_JUMP_FORCE

    def draw(self, surface):
        pygame.draw.circle(
            surface, (0, 0, 255), (int(self.pos[0]), int(self.pos[1])), self.radius
        )
