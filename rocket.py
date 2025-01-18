import pygame
import numpy as np

class Rocket:
    def __init__(self, start_pos, speed=2.0):
        self.position = pygame.Vector2(start_pos)
        self.speed = speed
        self.direction = pygame.Vector2(0, -1)  # Initial direction
        self.active = False  # Start with the rocket stationary

    def update_position(self, time_step, width, height):
        if self.active:
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

    def checkHit(self, plane_pos):
        # Simple hit detection based on proximity
        return self.position.distance_to(plane_pos) < 8

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def draw(self, screen, color=(255, 0, 0), size=15):
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), size)

class KalmanFilter:
    def __init__(self, dt, u_x, u_y, std_acc, x_std_meas, y_std_meas):
        self.dt = dt
        self.u = np.matrix([[u_x], [u_y]])
        self.x = np.matrix([[0], [0], [0], [0]])
        self.A = np.matrix([[1, 0, dt, 0],
                            [0, 1, 0, dt],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])
        self.B = np.matrix([[(dt**2)/2, 0],
                            [0, (dt**2)/2],
                            [dt, 0],
                            [0, dt]])
        self.H = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0]])
        self.Q = np.matrix([[(dt**4)/4, 0, (dt**3)/2, 0],
                            [0, (dt**4)/4, 0, (dt**3)/2],
                            [(dt**3)/2, 0, dt**2, 0],
                            [0, (dt**3)/2, 0, dt**2]]) * std_acc**2
        self.R = np.matrix([[x_std_meas**2, 0],
                            [0, y_std_meas**2]])
        self.P = np.eye(self.A.shape[1])

    def predict(self):
        self.x = np.dot(self.A, self.x) + np.dot(self.B, self.u)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[0:2]

    def update(self, z):
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = np.round(self.x + np.dot(K, (z - np.dot(self.H, self.x))))
        I = np.eye(self.H.shape[1])
        self.P = (I - (K * self.H)) * self.P
        return self.x[0:2]