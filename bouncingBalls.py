# Bouncing Balls Program
# Updated version: Bouncing balls within a complete circle with new balls on rebounds
import pygame
import numpy as np
import random

class Ball:
    def __init__(self, position, velocity):
        self.pos = np.array(position, dtype=np.float64)
        self.v = np.array(velocity, dtype=np.float64) 
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.rebounds = 0  # Count of rebounds

def create_random_ball():
    # Generate a random position inside the circle
    angle = random.uniform(0, 2 * np.pi)
    radius = random.uniform(0, CIRCLE_RADIUS - BALL_RADIUS)
    x = CIRCLE_CENTER[0] + radius * np.cos(angle)
    y = CIRCLE_CENTER[1] + radius * np.sin(angle)
    return Ball(position=[x, y], velocity=[random.uniform(-4, 4), random.uniform(-1, 1)])

pygame.init()
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

CIRCLE_CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=np.float64)
CIRCLE_RADIUS = 150
BALL_RADIUS = 5
ball_pos = np.array([WIDTH / 2, HEIGHT / 2 - 120], dtype=np.float64)
ball_vel = np.array([2, 3], dtype=np.float64)  # Example velocity
balls = [Ball(ball_pos, ball_vel)]

running = True
GRAVITY = 0.2

def draw_circle(window, center, radius):
    pygame.draw.circle(window, ORANGE, center.astype(int), radius, 3)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for ball in balls:
        # Update ball velocity due to gravity
        ball.v[1] += GRAVITY 
        ball.pos += ball.v
        
        # Check if the ball is out of bounds
        if ball.pos[1] > HEIGHT or ball.pos[0] < 0 or ball.pos[0] > WIDTH or ball.pos[1] < 0: 
            # Reset ball position to the center of the screen if it goes out of bounds
            ball.pos = np.array([WIDTH / 2, HEIGHT / 2 - 120], dtype=np.float64)
            ball.v = np.array([random.uniform(-4, 4), random.uniform(-1, 1)], dtype=np.float64)

        # Check collision with the circle
        dist = np.linalg.norm(ball.pos - CIRCLE_CENTER)
        if dist + BALL_RADIUS > CIRCLE_RADIUS:
            # Calculate the normal vector for reflection
            normal = (ball.pos - CIRCLE_CENTER) / np.linalg.norm(ball.pos - CIRCLE_CENTER)
            # Reflect the ball's velocity
            ball.v = ball.v - 2 * np.dot(ball.v, normal) * normal
            # Reposition the ball at the edge of the circle
            ball.pos = CIRCLE_CENTER + (CIRCLE_RADIUS - BALL_RADIUS) * normal
            
            # Increment the rebound count
            ball.rebounds += 1
            
            # Check if the ball has rebounded 4 times
            if ball.rebounds >= 4:
                balls.append(create_random_ball())  # Create a new ball
                ball.rebounds = 0  # Reset the rebound count

    window.fill(BLACK)
    draw_circle(window, CIRCLE_CENTER, CIRCLE_RADIUS)
    for ball in balls:
        pygame.draw.circle(window, ball.color, ball.pos.astype(int), BALL_RADIUS)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
