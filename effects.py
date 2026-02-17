import cv2
import math
import time
import numpy as np


# ==========================================================
# ENERGY ORB (Blue / Red / Purple) – CINEMATIC VERSION
# ==========================================================

def draw_energy_orb(frame, center, color,
                    alpha=1.0,
                    fusion=False,
                    scale=1):

    if center is None:
        return frame

    h, w = frame.shape[:2]

    # Create separate glow layer
    glow_layer = np.zeros((h, w, 3), dtype=np.uint8)

    t = time.time()
    radius = int(35 * scale + 6 * math.sin(t * 6))

    # ===============================
    # CORE DEPTH
    # ===============================
    if fusion:
        # Outer purple shell
        cv2.circle(glow_layer, center, radius, (160, 0, 255), -1)

        # Mid glow
        cv2.circle(glow_layer, center, int(radius * 0.65),
                   (220, 0, 255), -1)

        # Inner bright core
        cv2.circle(glow_layer, center, int(radius * 0.35),
                   (255, 255, 255), -1)
    else:
        # Normal orb
        cv2.circle(glow_layer, center, radius, color, -1)
        cv2.circle(glow_layer, center, int(radius * 0.4),
                   (255, 255, 255), -1)

    # ===============================
    # BLOOM (REAL GLOW)
    # ===============================
    glow_layer = cv2.GaussianBlur(glow_layer, (0, 0),
                                  sigmaX=18, sigmaY=18)

    frame = cv2.add(frame, glow_layer)

    # ===============================
    # ROTATING ENERGY PARTICLES
    # ===============================
    particle_count = 28 if fusion else 18
    orbit_radius = radius + 25

    for i in range(particle_count):
        angle = t * 2 + (2 * math.pi * i / particle_count)
        x = int(center[0] + orbit_radius * math.cos(angle))
        y = int(center[1] + orbit_radius * math.sin(angle))
        cv2.circle(frame, (x, y), 3, color, -1)

    # ===============================
    # DISTORTION RIPPLE
    # ===============================
    ripple = int(radius + 35 + 10 * math.sin(t * 4))
    cv2.circle(frame, center, ripple, color, 2)

    return frame


# ==========================================================
# CHROMATIC FLASH (Fusion Moment)
# ==========================================================

def chromatic_flash(frame):

    overlay = frame.copy()

    shift = 8

    blue_shift = np.roll(frame[:, :, 0], shift, axis=1)
    red_shift = np.roll(frame[:, :, 2], -shift, axis=1)

    overlay[:, :, 0] = blue_shift
    overlay[:, :, 2] = red_shift

    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    return frame


# ==========================================================
# SHOCKWAVE RIPPLE
# ==========================================================

def shockwave(frame, center, radius):

    if center is None:
        return frame

    overlay = frame.copy()

    cv2.circle(overlay, center, radius,
               (255, 0, 255), 3)

    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    return frame


# ==========================================================
# EXPLOSION EFFECT
# ==========================================================

def explosion(frame, center):

    if center is None:
        return frame

    for i in range(8):
        r = 40 + i * 25
        thickness = 2 if i < 4 else 1
        cv2.circle(frame, center, r,
                   (255, 0, 255), thickness)

    return frame
