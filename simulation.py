# simulation.py
import pygame
import sys
import numpy as np
from plane import Plane
from rocket import Rocket, KalmanFilter

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1600, 1200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Plane and Rocket Game")

# Initialize the plane and rocket
plane = Plane(start_pos=(WIDTH // 2, HEIGHT // 2))
rocket = Rocket(start_pos=(WIDTH // 4, HEIGHT // 4))

# Initialize Kalman filter for rocket tracking
kalman_filter = KalmanFilter(dt=1.0/FPS , u_x=0, u_y=0, std_acc=1, x_std_meas=1, y_std_meas=1)

# Direction map for numpad keys
DIRECTION_MAP = {
    pygame.K_KP1: pygame.Vector2(-1, 1),   # Southwest
    pygame.K_KP2: pygame.Vector2(0, 1),    # South
    pygame.K_KP3: pygame.Vector2(1, 1),    # Southeast
    pygame.K_KP4: pygame.Vector2(-1, 0),   # West
    pygame.K_KP6: pygame.Vector2(1, 0),    # East
    pygame.K_KP7: pygame.Vector2(-1, -1),  # Northwest
    pygame.K_KP8: pygame.Vector2(0, -1),   # North
    pygame.K_KP9: pygame.Vector2(1, -1),   # Northeast
}

# Main game loop
clock = pygame.time.Clock()
running = True
rocket_active = False  # Track rocket activation status

time_step = 1.0   # Continuous time step

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()

    for key, direction in DIRECTION_MAP.items():
        if keys[key]:
            plane.set_direction(direction)

    if keys[pygame.K_KP_PLUS]:
        plane.increase_speed()
    if keys[pygame.K_KP_MINUS]:
        plane.decrease_speed()

    # Start rocket motion with spacebar
    if keys[pygame.K_SPACE]:
        rocket.activate()
    mOldPlanePosition = plane.position#our siulation radar tracks the object 1 tick before
    # Update plane position
    plane.update_position(time_step, WIDTH, HEIGHT)

    # Rocket updates using Kalman filter prediction and update if active
    if rocket.active:
        predicted_position = kalman_filter.predict()
        rocket.position.x, rocket.position.y = predicted_position[0, 0], predicted_position[1, 0]
        measurement = np.array([[mOldPlanePosition.x], [mOldPlanePosition.y]])
        kalman_filter.update(measurement)

    # Check for hit
    if rocket.checkHit(plane.position):
        print("Rocket hit the plane!")
        rocket.deactivate()

    # Draw the plane and rocket
    plane.draw(screen)
    rocket.draw(screen)

    # Display velocity, direction, and rocket state in the top-right corner
    font = pygame.font.SysFont(None, 24)
    velocity_text = font.render(f"Plane Speed: {plane.speed:.2f}", True, BLACK)
    direction_text = font.render(f"Plane Direction: ({plane.direction.x:.2f}, {plane.direction.y:.2f})", True, BLACK)
    rocket_text = font.render(f"Rocket Position: ({rocket.position.x:.2f}, {rocket.position.y:.2f})", True, BLACK)
    status_text = font.render("Rocket Active: Yes" if rocket.active else "Rocket Active: No", True, BLACK)

    screen.blit(velocity_text, (WIDTH - 250, 10))
    screen.blit(direction_text, (WIDTH - 250, 40))
    screen.blit(rocket_text, (WIDTH - 250, 70))
    screen.blit(status_text, (WIDTH - 250, 100))

    # Refresh screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
