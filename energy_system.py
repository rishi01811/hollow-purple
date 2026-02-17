import math
import time
import cv2
from particle_system import ParticleSystem
from effects import draw_energy_orb


class EnergySystem:

    def __init__(self):
        self.blue_particles = ParticleSystem()
        self.red_particles = ParticleSystem()
        self.purple_particles = ParticleSystem()

    # ==========================================
    # IDLE STATE (Blue + Red Active)
    # ==========================================
    def update_idle(self, frame, left, right):

        if left:
            # Cinematic blue orb
            frame = draw_energy_orb(frame, left, (255, 0, 0))
            self.blue_particles.emit(left[0], left[1], (255, 0, 0), 4)

        if right:
            # Cinematic red orb
            frame = draw_energy_orb(frame, right, (0, 0, 255))
            self.red_particles.emit(right[0], right[1], (0, 0, 255), 4)

        self.blue_particles.update(frame)
        self.red_particles.update(frame)

        return frame

    # ==========================================
    # FUSION STATE (Purple Energy Swirl)
    # ==========================================
    def update_fusion(self, frame, center):

        if center is None:
            return frame

        # Cinematic purple orb (fusion mode)
        frame = draw_energy_orb(frame, center, (255, 0, 255), fusion=True)

        # Heavy purple particle emission
        self.purple_particles.emit(center[0], center[1], (255, 0, 255), 12)

        # Swirl force
        for p in self.purple_particles.particles:

            dx = p.x - center[0]
            dy = p.y - center[1]

            distance = math.hypot(dx, dy) + 0.001

            # perpendicular swirl force
            p.vx += -dy / distance * 0.4
            p.vy += dx / distance * 0.4

        self.purple_particles.update(frame)

        return frame

    # ==========================================
    # BLAST STATE (Expansion + Burst)
    # ==========================================
    def blast(self, frame, center, scale):

        if center is None:
            return frame

        # Expanding purple orb
        frame = draw_energy_orb(
            frame,
            center,
            (255, 0, 255),
            fusion=True,
            scale=scale
        )

        # Massive outward emission
        self.purple_particles.emit(
            center[0],
            center[1],
            (255, 0, 255),
            25,
            outward=True
        )

        self.purple_particles.update(frame)

        return frame
