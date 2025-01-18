import pygame

class Plane:
    def __init__(self, start_pos, speed=2.0):
        self.position = pygame.Vector2(start_pos)
        self.speed = speed
        self.direction = pygame.Vector2(0, -1)  # Initial direction: north
        self.acceleration_step = 0.5
        self.max_speed = 10
        self.min_speed = 0.5

    def update_position(self, time_step, width, height):
        # Forward Euler update for position
        self.position += self.direction * self.speed * time_step

        # Handle screen boundaries
        if self.position.x < 0:
            self.position.x = width
        elif self.position.x > width:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = height
        elif self.position.y > height:
            self.position.y = 0

    def set_direction(self, new_direction):
        # Allow for smooth and continuous directional change
        if new_direction.length() > 0:
            self.direction = (self.direction + new_direction * 0.1).normalize()

    def increase_speed(self):
        self.speed = min(self.speed + self.acceleration_step, self.max_speed)

    def decrease_speed(self):
        self.speed = max(self.speed - self.acceleration_step, self.min_speed)

    def draw(self, screen, color=(0, 128, 255), size=20):
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), size)
