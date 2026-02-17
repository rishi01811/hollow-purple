import cv2
import math
import random
import numpy as np


class Particle:
    def __init__(self, x, y, color, outward=False):

        self.x = x
        self.y = y
        self.color = color

        self.life = random.randint(25, 40)
        self.max_life = self.life

        angle = random.uniform(0, 2 * math.pi)

        if outward:
            speed = random.uniform(3, 6)
        else:
            speed = random.uniform(1, 3)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    # ---------------------------------------------------
    # UPDATE PARTICLE
    # ---------------------------------------------------
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    # ---------------------------------------------------
    # DRAW PARTICLE (soft fade)
    # ---------------------------------------------------
    def draw(self, frame):

        if self.life <= 0:
            return

        alpha = self.life / self.max_life
        size = max(1, int(4 * alpha))

        overlay = frame.copy()

        cv2.circle(
            overlay,
            (int(self.x), int(self.y)),
            size,
            self.color,
            -1
        )

        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # ---------------------------------------------------
    def is_dead(self):
        return self.life <= 0


class ParticleSystem:

    def __init__(self):
        self.particles = []

    # ---------------------------------------------------
    # EMIT PARTICLES
    # ---------------------------------------------------
    def emit(self, x, y, color, count=5, outward=False):

        for _ in range(count):
            self.particles.append(
                Particle(x, y, color, outward=outward)
            )

    # ---------------------------------------------------
    # UPDATE ALL PARTICLES
    # ---------------------------------------------------
    def update(self, frame):

        for p in self.particles[:]:
            p.update()
            p.draw(frame)

            if p.is_dead():
                self.particles.remove(p)
