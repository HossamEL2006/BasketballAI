from math import sqrt
import pygame


pygame.init()
clock = pygame.time.Clock()


class Ball:
    def __init__(self, x, y, width, surface):
        self.position = pygame.Vector2(x, y)
        self.gravity = 1
        self.speed = pygame.Vector2(0, 0)
        self.width = width
        self.surface = surface
        self.last_speed = self.speed
        self.color = pygame.Color(255, 0, 0)

    def update(self):
        self.position += self.speed
        self.speed.y += self.gravity
        self.speed.x *= 0.98
        self.touch_contour()
        self.last_speed = self.speed

    def draw(self):
        pygame.draw.circle(
            self.surface,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.width,
        )

    def touch_contour(self):
        if self.position.x + self.width > self.surface.get_width():
            self.position.x = self.surface.get_width() - self.width
            self.speed.x = -self.last_speed.x * 0.8
        elif self.position.x - self.width < 0:
            self.position.x = self.width
            self.speed.x = -self.last_speed.x * 0.8

        if self.position.y + self.width > self.surface.get_height():
            self.position.y = self.surface.get_height() - self.width
            self.speed.y = -self.last_speed.y * 0.6
            if abs(self.speed.y) < 2.6:
                self.speed.y = 0
            if abs(self.speed.x) < 0.1:
                self.speed.x = 0
        elif self.position.y - self.width < 0:
            self.position.y = self.width
            self.speed.y = -self.last_speed.y * 0.6


class BasketBall(Ball):
    def __init__(self, x, y, width, surface):
        super().__init__(x, y, width, surface)


class Player(Ball):
    def __init__(self, x, y, width, surface, ball):
        super().__init__(x, y, width, surface)
        self.color = pygame.Color(0, 255, 0)
        self.ball = ball

    # def update(self):
    #     # last_speed = self.position
    #     # mouse_x, mouse_y = pygame.mouse.get_pos()
    #     # self.position = pygame.Vector2(mouse_x, mouse_y)
    #     self.__s
    #     self.collision_entre_ball()

    def update(self):
        super().update()
        self.collision_entre_ball()

    def collision_entre_ball(self):
        v1 = self.position
        v2 = self.ball.position
        m1 = 10
        m2 = 5

        if v1.distance_to(v2) < self.width + self.ball.width - 2:
            normal = (v1 - v2).normalize()
            relative_velocity = self.speed - self.ball.speed
            velocity_along_normal = relative_velocity.dot(normal)

            if velocity_along_normal > 0:
                return

            impulse = (2 * velocity_along_normal) / (m1 + m2)
            self.speed -= impulse * m2 * normal
            self.ball.speed += impulse * m1 * normal


def main():
    surface = pygame.display.set_mode((640, 480))
    basketball = BasketBall(320, 240, 50, surface)
    player = Player(200, 100, 50, surface, basketball)

    loop = True

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    basketball.speed.y = -10
                if event.key == pygame.K_LEFT:
                    basketball.speed.x = -10
                if event.key == pygame.K_RIGHT:
                    basketball.speed.x = 10

                if event.key == pygame.K_z:
                    player.speed.y = -10
                if event.key == pygame.K_q:
                    player.speed.x = -10
                if event.key == pygame.K_d:
                    player.speed.x = 10

        surface.fill(pygame.Color(255, 255, 255))
        basketball.update()
        player.update()
        basketball.draw()
        player.draw()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
