from statistics import mean
import pygame
import numpy as np
from player import Player
from basketball import BasketBall
from bots.simple_bot import simple_bot
from point_collider import PointCollider
from box_collider import BoxCollider

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

        self.points = []
        self.points.extend(BoxCollider(0, 110, 6, 90, gap=5).generate_point_colliders())
        self.points.append(PointCollider(8, 171))
        self.points.append(PointCollider(11, 171))
        self.points.append(PointCollider(13, 173))
        self.points.append(PointCollider(14, 176))
        self.points.append(PointCollider(14, 179))
        self.points.append(PointCollider(14, 181))
        self.points.append(PointCollider(16, 184))
        self.points.append(PointCollider(16, 188))
        self.points.append(PointCollider(17, 191))
        self.points.append(PointCollider(18, 194))
        self.points.append(PointCollider(18, 197))
        self.points.append(PointCollider(18, 201))
        self.points.append(PointCollider(19, 204))
        self.points.append(PointCollider(20, 209))
        self.points.append(PointCollider(20, 212))
        self.points.append(PointCollider(21, 216))
        self.points.append(PointCollider(21, 220))
        self.points.append(PointCollider(21, 223))
        self.points.append(PointCollider(21, 226))
        self.points.append(PointCollider(21, 230))
        self.points.append(PointCollider(11, 168))
        self.points.append(PointCollider(12, 164))
        self.points.append(PointCollider(8, 164))
        self.points.append(PointCollider(74, 172))
        self.points.append(PointCollider(74, 168))
        self.points.append(PointCollider(74, 164))
        self.points.append(PointCollider(77, 164))
        self.points.append(PointCollider(79, 164))
        self.points.append(PointCollider(79, 168))
        self.points.append(PointCollider(79, 172))
        self.points.append(PointCollider(76, 172))
        self.points.append(PointCollider(72, 174))
        self.points.append(PointCollider(72, 176))
        self.points.append(PointCollider(72, 179))
        self.points.append(PointCollider(71, 183))
        self.points.append(PointCollider(69, 186))
        self.points.append(PointCollider(70, 188))
        self.points.append(PointCollider(69, 191))
        self.points.append(PointCollider(68, 195))
        self.points.append(PointCollider(68, 199))
        self.points.append(PointCollider(67, 202))
        self.points.append(PointCollider(67, 206))
        self.points.append(PointCollider(66, 209))
        self.points.append(PointCollider(66, 213))
        self.points.append(PointCollider(66, 217))
        self.points.append(PointCollider(66, 221))
        self.points.append(PointCollider(65, 225))
        self.points.append(PointCollider(65, 228))
        self.points.append(PointCollider(65, 223))

    def update(self):
        # Update position & velocities
        self.player.update()
        self.basketball.update()

        # Collision Handeling: Player <--> ColliderPoint
        # Find the closest collider point and compute collisions #!(NOT OPTIMISED)
        collided_points = []
        collided_points_distances = []

        for i in self.points:
            status, d = i.check_collision(self.player)
            if status:
                collided_points.append(i)
                collided_points_distances.append(d)

        if collided_points:
            closest_collided_point = collided_points[
                collided_points_distances.index(min(collided_points_distances))
            ]
            closest_collided_point.handle_collision(self.player)
            closest_collided_point.resolve_overlap(self.player)

        # Collision Handeling: BasketBall <--> ColliderPoint
        # Find the closest collider point and compute collisions #!(NOT OPTIMISED)
        collided_points = []
        collided_points_distances = []

        for i in self.points:
            status, d = i.check_collision(self.basketball)
            if status:
                collided_points.append(i)
                collided_points_distances.append(d)

        if collided_points:
            closest_collided_point = collided_points[
                collided_points_distances.index(min(collided_points_distances))
            ]
            closest_collided_point.handle_collision(self.basketball)
            closest_collided_point.resolve_overlap(self.basketball)

        # Collision Handeling: Player <--> BasketBall
        if self.check_collision():
            self.handle_collison()
            self.resolve_overlap()

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


def render_game(game):
    game_screen = pygame.Surface((WIDTH, HEIGHT))
    game_screen.fill((125, 125, 125))
    game.basketball.draw(game_screen)
    game.player.draw(game_screen)
    game_screen.blit(pygame.transform.scale_by(pygame.image.load("basket.png"), .1), (-10, 100))
    for i in game.points:
        i.draw(game_screen)
    return game_screen


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
        real_dt = clock.tick(game.fps * game_speed)
        update_stats(real_dt, game.fps, fps_history, speed_history)

        # EVENT HANDELING
        was_mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    was_mouse_clicked = True
                else:
                    x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    print(f"self.points.append(PointCollider{(x, y)})")
                    game.points.append(PointCollider(x, y))

        # HUMAN CONTROLS
        mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float)
        if was_mouse_clicked:
            game.play_move(f"{mouse_pos[0]} {mouse_pos[1]}")
        else:
            game.play_move("NO JUMP")

        # RENDER
        window.blit(render_game(game), (0, 0))
        window.blit(render_ui(game, speed_history, game_speed, fps_history), (0, 0))
        pygame.display.update()


def watch_bot_play(game, ai_script, window, game_speed=1):
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

        # BOT CONTROLS
        game.play_move(ai_script(game.fetch_data()))

        # RENDER
        window.blit(render_game(game), (0, 0))
        window.blit(render_ui(game, speed_history, game_speed, fps_history), (0, 0))
        pygame.display.update()


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BasketBall AI")

    mode = "human"  # 'human' or 'bot'

    if mode == "human":
        # Create a new game and play it with human controls
        new_game = Game(fps=60)
        play(new_game, window, game_speed=1)
    elif mode == "bot":
        # Watch an AI play a new game based on ai_functino
        ai_function = simple_bot
        new_game = Game()
        watch_bot_play(new_game, ai_function, window, game_speed=1)


if __name__ == "__main__":
    main()
