from statistics import mean
import pygame
import numpy as np
from player import Player
from basketball import BasketBall
from AIs.simple_ai import simple_ai

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALLS_COLLISION_SLOWDOWN = 0.8

STATS_FONT = pygame.font.Font(None, 20)
SCORE_FONT = pygame.font.Font(None, 60)
# It's better to fix the delta time for AI training for a better consistency
# And to not allow the AI to use speedups and slowdowns as a glitch strategy


class Game:
    def __init__(self, fps=60):
        self.width = WIDTH
        self.height = HEIGHT

        # Initialize game objects
        self.player = Player(self.width // 2, self.height // 2, self)
        self.basketball = BasketBall(self.width // 2, 50, self)

        # Game Constants
        self.fps = fps
        self.dt = 1 / fps
        self.width = WIDTH

        # Score
        self.score = 0
        self.is_gameover = False

        self.moves_counter = 0

    def update(self):
        if self.check_collision():
            self.handle_collison()
            self.resolve_overlap()

        self.player.update()
        self.basketball.update()

        # speed = 1000 * self.dt / dt if dt else 0
        # self.speed.append(speed)
        # current_fps = 1000 / dt if dt else 0
        # self.current_fps.append(current_fps)
        #

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
        game_screen = pygame.Surface((WIDTH, HEIGHT))
        game_screen.fill((125, 125, 125))
        self.basketball.draw(game_screen)
        self.player.draw(game_screen)
        return game_screen

    def play_move(self, command):
        if command != "NO JUMP":
            x, y = map(float, command.split())
            self.player.push((x, y))
        self.update()
        self.moves_counter += 1

    def fetch_data(self):
        return [
            self.player.pos[0],
            self.player.pos[1],
            self.player.vel[0],
            self.player.vel[1],
            self.basketball.pos[0],
            self.basketball.pos[1],
            self.basketball.vel[0],
            self.basketball.vel[1],
        ]

    def gameover(self):
        self.is_gameover = True


def update_stats(real_dt, game_fps, fps_history, speed_history):
    real_fps = 1000 / real_dt
    fps_history.append(real_fps)
    speed = real_fps / game_fps
    speed_history.append(speed)

    capping_limit = 5 * real_fps
    if len(speed_history) > capping_limit:
        speed_history = speed_history[-max(int(capping_limit), 1) :]
        fps_history = fps_history[-max(int(capping_limit), 1) :]


def render_ui(game, speed_history, target_game_speed, fps_history):
    ui_canvas = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Render speed and FPS in smaller font
    ui_canvas.blit(
        STATS_FONT.render(f"Speed: {round(mean(speed_history) * 100)}%", True, "White"),
        (10, 10),
    )
    ui_canvas.blit(
        STATS_FONT.render(
            f"Target Speed: {round(target_game_speed * 100)}%", True, "White"
        ),
        (10, 30),
    )
    ui_canvas.blit(
        STATS_FONT.render(f"FPS: {round(mean(fps_history))}", True, "White"),
        (10, 50),
    )
    ui_canvas.blit(
        STATS_FONT.render(f"FPS Target: {game.fps}", True, "White"),
        (10, 70),
    )
    ui_canvas.blit(
        STATS_FONT.render(f"Frame Counter: {game.moves_counter}", True, "White"),
        (10, 90),
    )

    # Render score in larger font, centered at the top of the screen
    score_text = SCORE_FONT.render(str(game.score), True, "White")
    score_rect = score_text.get_rect(
        midtop=(game.width // 2, 10)
    )  # Centered at the top
    ui_canvas.blit(score_text, score_rect)

    return ui_canvas


def play(game, window, game_speed=1):
    clock = pygame.time.Clock()
    running = True
    speed_history = []
    fps_history = []
    while running:
        # CLOCK HANDELING
        real_dt = clock.tick(60 * game_speed)
        update_stats(real_dt, game.fps, fps_history, speed_history)

        # EVENT HANDELING
        was_mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                was_mouse_clicked = True

        # HUMAN CONTROLS
        mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float)
        if was_mouse_clicked:
            game.play_move(f"{mouse_pos[0]} {mouse_pos[1]}")
        else:
            game.play_move("NO JUMP")

        # RENDER
        window.blit(game.render_game(), (0, 0))
        window.blit(render_ui(game, speed_history, game_speed, fps_history), (0, 0))
        pygame.display.update()


def watch_ai_play(game, ai_script, window, game_speed=1):
    clock = pygame.time.Clock()
    running = True
    speed_history = []
    fps_history = []
    while running:
        # CLOCK HANDELING
        real_dt = clock.tick(60 * game_speed)
        update_stats(real_dt, game.fps, fps_history, speed_history)

        # EVENT HANDELING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # AI CONTROLS
        game.play_move(ai_script(game.fetch_data()))

        # RENDER
        window.blit(game.render_game(), (0, 0))
        window.blit(render_ui(game, speed_history, game_speed, fps_history), (0, 0))
        pygame.display.update()


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BasketBall AI")

    mode = "human"  # 'ai'

    if mode == "human":
        # Create a new game and play it with human controls
        new_game = Game()
        play(new_game, window, game_speed=1)
    elif mode == "ai":
        # Watch an AI play a new game based on ai_functino
        ai_function = simple_ai
        new_game = Game()
        watch_ai_play(new_game, ai_function, window)


if __name__ == "__main__":
    main()
