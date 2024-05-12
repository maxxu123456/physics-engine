import pygame
import numpy as np
import random
from math import sqrt

"""
Author: Max Xu
Enjoy!
"""
g = 9.81

WIDTH = 1000
HEIGHT = 700
FPS = 60
DAMPING = 0.9


def dist(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def generate_random_balls(n):
    balls = []
    max_radius = 50
    min_radius = 10
    min_velocity = -120
    max_velocity = 120
    area_to_mass_factor = 5

    for _ in range(n):
        radius = None
        color = None
        mass = None
        x = None
        y = None

        # Always generate non overlapping ball
        valid = False
        while not valid:
            radius = random.randint(min_radius, max_radius)
            color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # Mass is proportional to radius squared, so we multiply an arbitrary factor to r^2
            mass = area_to_mass_factor * (radius ** 2)

            x = random.uniform(radius, WIDTH - radius)
            y = random.uniform(radius, HEIGHT - radius)

            # Check for Overlap
            overlap_found = False
            for ball in balls:
                if dist(x, y, ball.x, ball.y) <= radius + ball.radius:
                    overlap_found = True
                    break

            if not overlap_found:
                valid = True

        velocity_x = random.uniform(min_velocity, max_velocity)
        velocity_y = random.uniform(min_velocity, max_velocity)

        ball = Ball(radius, color, mass, x, y, velocity_x, velocity_y)
        balls.append(ball)

    return balls


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Ball:
    def __init__(self, radius: float, color: Color, mass: float, x: float, y: float, velocity_x: float,
                 velocity_y: float):
        # x and y are the center coordinates of the ball
        self.radius = radius
        self.color = color
        self.mass = mass
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

    ball1 = Ball(100.0, Color(0, 100, 0), 1, 100.0, 150.0, -50.0, 0.0)
    ball2 = Ball(100.0, Color(20, 40, 29), 10, 400, 200, 60, 0)

    balls = generate_random_balls(10)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Colliding Ball Engine")
    running = True

    while running:
        # stored the pairs of balls that collisison have been resolve for
        pairs_resolved = []
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for i in range(len(balls)):
            ball = balls[i]
            ball.update(dt)

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

            # Check Every Pair of Balls for a Collision
            for j in range(i + 1, len(balls)):
                other_ball = balls[j]
                if other_ball != ball and dist(ball.x, ball.y, other_ball.x,
                                               other_ball.y) <= ball.radius + other_ball.radius:
                    print("Collision Occurring")
                    # Calculate the vector from one ball to the other
                    norm_vec = np.array([other_ball.x - ball.x, other_ball.y - ball.y])
                    # Calculate the magnitude of the vector
                    mag = np.linalg.norm(norm_vec)
                    # Calculate the unit normal vector
                    unit_norm_vec = norm_vec / mag
                    # Calculate the unit tangent vector
                    unit_tangent_vec = np.array([-unit_norm_vec[1], unit_norm_vec[0]])

                    # Decompose the velocities into normal and tangential components
                    v1n = np.dot([ball.velocity_x, ball.velocity_y], unit_norm_vec)
                    v1t = np.dot([ball.velocity_x, ball.velocity_y], unit_tangent_vec)
                    v2n = np.dot([other_ball.velocity_x, other_ball.velocity_y], unit_norm_vec)
                    v2t = np.dot([other_ball.velocity_x, other_ball.velocity_y], unit_tangent_vec)

                    # Calculate new normal velocities after collision
                    v1n_prime = (v1n * (ball.mass - other_ball.mass) + 2 * other_ball.mass * v2n) / (
                            ball.mass + other_ball.mass)
                    v2n_prime = (v2n * (other_ball.mass - ball.mass) + 2 * ball.mass * v1n) / (
                            ball.mass + other_ball.mass)

                    # Convert scalar normal and tangential velocities into vectors
                    v1n_prime_vec = v1n_prime * unit_norm_vec
                    v1t_prime_vec = v1t * unit_tangent_vec
                    v2n_prime_vec = v2n_prime * unit_norm_vec
                    v2t_prime_vec = v2t * unit_tangent_vec

                    # Update velocities
                    ball.velocity_x, ball.velocity_y = v1n_prime_vec + v1t_prime_vec
                    other_ball.velocity_x, other_ball.velocity_y = v2n_prime_vec + v2t_prime_vec

                    # Position correction to avoid overlapping
                    overlap = 0.5 * (
                            ball.radius + other_ball.radius - mag + 1)
                    ball.x -= overlap * unit_norm_vec[0]
                    ball.y -= overlap * unit_norm_vec[1]
                    other_ball.x += overlap * unit_norm_vec[0]
                    other_ball.y += overlap * unit_norm_vec[1]

            pygame.draw.circle(screen, (ball.color.r, ball.color.g, ball.color.b),
                               (int(ball.x), int(ball.y)), ball.radius)
        text = font.render(f'Number of Balls: {len(balls)}, Gravity: {g:.2f}, Damping: {DAMPING:.2f}', True,
                           (255, 255, 255))
        screen.blit(text, (50, 50))
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
