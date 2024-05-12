import pygame

g = 9.81

WIDTH = 1000
HEIGHT = 700
FPS = 60
DAMPING = 0.9


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Ball:
    def __init__(self, radius: float, color: Color, x: float, y: float, velocity_x: float, velocity_y: float):
        # x and y are the center coordinates of the ball
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update(self, dt: float):
        self.velocity_y += g
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    ball = Ball(100.0, Color(0, 100, 0), 300.0, 100.0, -50.0, 0.0)

    clock = pygame.time.Clock()

    running = True

    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball.update(dt)

        screen.fill((0, 0, 0))

        # Left Wall Collision

        if ball.x - ball.radius <= 0:
            ball.velocity_x = -ball.velocity_x * DAMPING
            ball.x = ball.radius

        # Right Wall Collision

        if ball.x + ball.radius >= WIDTH:
            ball.velocity_x = -ball.velocity_x * DAMPING
            ball.x = WIDTH - ball.radius

        # Floor Collision
        if ball.y + ball.radius >= HEIGHT:
            ball.velocity_y = -ball.velocity_y * DAMPING
            ball.y = HEIGHT - ball.radius

        # Ceiling Collision
        if ball.y - ball.radius <= 0:
            ball.velocity_y = -ball.velocity_y * DAMPING
            ball.y = ball.radius

        pygame.draw.circle(screen, (ball.color.r, ball.color.g, ball.color.b),
                           (int(ball.x), int(ball.y)), ball.radius)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
