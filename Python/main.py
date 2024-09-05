import pygame
import numpy as np
from player import Player, PLAYER_RADIUS
from ball import Ball, BASKETBALL_RADIUS

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
FIXED_DT = 1 / FPS # It's better to fix the delta time for AI training for a better consistency
                   # And to not allow the AI to use speedups and slowdowns as a glitch strategy


class Game:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BasketBall AI")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game objects
        self.player = Player(self.width // 2, self.height // 2, PLAYER_RADIUS, self)
        self.basketball = Ball(self.width // 2, 50, BASKETBALL_RADIUS, self)

        # Game Constants
        self.dt = FIXED_DT
        self.width = WIDTH

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float)
                self.player.push(mouse_pos)

    def update(self):
        self.basketball.check_collision(self.player)
        self.player.check_collision(self.basketball)

        self.player.update()
        self.basketball.update()

    def render(self):
        self.screen.fill((255, 255, 255))

        self.player.draw(self.screen)
        self.basketball.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
