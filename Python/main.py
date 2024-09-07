from statistics import mean
import pygame
import numpy as np
from player import Player
from ball import BasketBall

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS_TARGET = 60
BALLS_COLLISION_SLOWDOWN = 0.8
FIXED_DT = 1 / FPS_TARGET
STATS_FONT = pygame.font.Font(None, 20)
SCORE_FONT = pygame.font.Font(None, 60)
# It's better to fix the delta time for AI training for a better consistency
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
        self.player = Player(self.width // 2, self.height // 2, self)
        self.basketball = BasketBall(self.width // 2, 50, self)

        # Game Constants
        self.dt = FIXED_DT
        self.width = WIDTH

        # Stats
        self.speed = []
        self.current_fps = []
        self.frame_counter = 0

        # Score
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float)
                self.player.push(mouse_pos)

    def update(self, dt):
        if self.check_collision():
            self.handle_collison()
            self.resolve_overlap()

        self.player.update()
        self.basketball.update()

        speed = 1000 * FIXED_DT / dt if dt else 0
        self.speed.append(speed)
        current_fps = 1000 / dt if dt else 0
        self.current_fps.append(current_fps)
        if len(self.speed) > current_fps:
            self.speed = self.speed[-max(int(current_fps), 1):]
            self.current_fps = self.current_fps[-max(int(current_fps), 1):]

    def check_collision(self):
        distance = np.linalg.norm(self.player.pos - self.basketball.pos)
        if distance <= self.player.radius + self.basketball.radius:
            return True

    def resolve_overlap(self):
        # Calculate the distance vector and magnitude
        distance_vector = self.player.pos - self.basketball.pos
        distance = np.linalg.norm(distance_vector)

        # Calculate the overlap (if any)
        overlap = (self.player.radius + self.basketball.radius) - distance

        # Normalize the distance vector to get the direction of push
        direction = distance_vector / distance

        # Push both balls apart by half of the overlap
        self.player.pos += direction * (overlap / 2)
        self.basketball.pos -= direction * (overlap / 2)

    def handle_collison(self):
        # Use the Elastic Collision formula to calculate the new velocity vectors
        m1 = self.player.mass
        m2 = self.basketball.mass
        x1 = self.player.pos
        x2 = self.basketball.pos
        v1 = self.player.vel
        v2 = self.basketball.vel
        new_player_vel = (
            v1
            - (2 * m2 / (m1 + m2))
            * (v1 - v2).dot(x1 - x2)
            * (x1 - x2)
            / np.linalg.norm(x1 - x2) ** 2
        ) * BALLS_COLLISION_SLOWDOWN
        new_ball_vel = (
            v2
            - (2 * m1 / (m1 + m2))
            * (v2 - v1).dot(x2 - x1)
            * (x2 - x1)
            / np.linalg.norm(x2 - x1) ** 2
        ) * BALLS_COLLISION_SLOWDOWN
        self.player.vel = new_player_vel
        self.basketball.vel = new_ball_vel

    def render_game(self):
        self.screen.fill((125, 125, 125))
        self.basketball.draw(self.screen)
        self.player.draw(self.screen)

    def render_ui(self):
        # Render speed and FPS in smaller font
        self.screen.blit(
            STATS_FONT.render(
                f"Speed: {round(mean(self.speed) * 100)}%", True, "White"
            ),
            (10, 10),
        )
        self.screen.blit(
            STATS_FONT.render(f"FPS: {round(mean(self.current_fps))}", True, "White"),
            (10, 30),
        )
        self.screen.blit(
            STATS_FONT.render(f"FPS Target: {FPS_TARGET}", True, "White"),
            (10, 50),
        )
        self.screen.blit(
            STATS_FONT.render(f"Frame Counter: {self.frame_counter}", True, "White"),
            (10, 70),
        )

        # Render score in larger font, centered at the top of the screen
        score_text = SCORE_FONT.render(str(self.score), True, "White")
        score_rect = score_text.get_rect(
            midtop=(self.width // 2, 10)
        )  # Centered at the top
        self.screen.blit(score_text, score_rect)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS_TARGET)
            self.handle_events()
            self.update(dt)
            self.render_game()
            self.render_ui()
            pygame.display.update()
            self.frame_counter += 1

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
