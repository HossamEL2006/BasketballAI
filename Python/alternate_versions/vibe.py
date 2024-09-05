import pygame

pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

score = 0
text_surface = test_font.render(str(score), False, "White")

mouse_pos = pygame.Vector2()
player_pos = pygame.Vector2(540, 460)
ball_pos = pygame.Vector2(540, 260)

player_velocity = pygame.math.Vector2(0, 0)
ball_velocity = pygame.math.Vector2(0, 0)
gravity = pygame.math.Vector2(0, 0.3)
forceIntensity = 18.0

player_mass = 10
ball_mass = 8

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            direction = pygame.Vector2(mouse_pos - player_pos).normalize()
            player_velocity = direction * forceIntensity

    screen.fill("Black")

    player_pos += player_velocity
    ball_pos += ball_velocity
    player_velocity += gravity
    ball_velocity += gravity

    d = player_pos.distance_to(ball_pos)
    if d < 50:

        overlap = d - 50
        direct = ball_pos - player_pos
        direct.scale_to_length(overlap * 0.5)
        player_pos += direct
        ball_pos -= direct

        normal = (player_pos - ball_pos).normalize()
        relative_velocity = player_velocity - ball_velocity
        velocity_along_normal = relative_velocity.dot(normal)

        impulse = (2 * velocity_along_normal) / (player_mass + ball_mass)
        player_velocity -= impulse * ball_mass * normal * 0.8
        ball_velocity += impulse * player_mass * normal * 0.8

    if player_pos.x < 30:
        player_pos.x = 30
        player_velocity.x *= -0.8
    elif player_pos.x > 1050:
        player_pos.x = 1050
        player_velocity.x *= -0.8
    if player_pos.y > 690:
        player_pos.y = 690
        player_velocity.y *= -0.8
    elif player_pos.y < 30:
        player_pos.y = 30
        player_velocity.y *= -0.8

    if ball_pos.x < 20:
        ball_pos.x = 20
        ball_velocity.x *= -0.8
    elif ball_pos.x > 1060:
        ball_pos.x = 1060
        ball_velocity.x *= -0.8
    if ball_pos.y < 20:
        ball_pos.y = 20
        ball_velocity.y *= -0.8
    elif ball_pos.y > 740:
        player_pos = pygame.Vector2(540, 460)
        ball_pos = pygame.Vector2(540, 260)

        text_surface = test_font.render(str(score), False, "White")

        player_velocity = pygame.Vector2(0, 0)
        ball_velocity = pygame.Vector2(0, 0)
        gravity = pygame.Vector2(0, 0.3)
        forceIntensity = 15.0

    ball = pygame.draw.circle(screen, "Red", ball_pos, (20))
    player = pygame.draw.circle(screen, "Yellow", player_pos, (30))

    screen.blit(text_surface, (50, 50))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
