import cv2
import math
import time
import numpy as np
from energy_system import EnergySystem
from hand_tracking import HandTracker
from effects import draw_energy_orb, shockwave, explosion, chromatic_flash



TOUCH_THRESHOLD = 25


def main():

    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    energy = EnergySystem()

    state = "IDLE"

    fusion_center = None
    locked_center = None
    blast_scale = 1
    impact_timer = 0
    shockwave_radius = 0

    previous_frame = None

    print("Press ESC to quit")

    while True:

        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        # ================= MOTION TRAIL =================
        if previous_frame is not None:
            frame = cv2.addWeighted(frame, 0.88, previous_frame, 0.12, 0)

        previous_frame = frame.copy()

        frame, left, right = tracker.get_index_positions(frame)

        distance = 999
        if left and right:
            distance = math.hypot(left[0] - right[0], left[1] - right[1])

        # ================= STATE MACHINE =================

        if state == "IDLE":

            frame = energy.update_idle(frame, left, right)

            if left and right and distance < TOUCH_THRESHOLD:
                frame = chromatic_flash(frame)

                # White impact flash
                flash = np.full_like(frame, 255)
                frame = cv2.addWeighted(frame, 0.4, flash, 0.6, 0)

                fusion_center = left
                state = "FUSION_IMPACT"
                impact_timer = 0
                shockwave_radius = 0

        # ================================================
        elif state == "FUSION_IMPACT":

            impact_timer += 1

            # Micro shake
            shake_x = int(math.sin(time.time() * 90) * 5)
            shake_y = int(math.cos(time.time() * 85) * 5)

            h, w = frame.shape[:2]
            M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
            frame = cv2.warpAffine(frame, M, (w, h))

            frame = energy.update_fusion(frame, fusion_center)

            shockwave_radius += 10
            frame = shockwave(frame, fusion_center, shockwave_radius)

            if impact_timer > 12:
                state = "FUSED"

        # ================================================
        elif state == "FUSED":

            if left:
                fusion_center = left

            frame = energy.update_fusion(frame, fusion_center)

            # If left hand removed → lock position and blast
            if left is None and fusion_center:
                locked_center = fusion_center
                blast_scale = 1
                state = "BLASTING"

        # ================================================
        elif state == "BLASTING":

            blast_scale += 0.35

            # HEAVY SHAKE
            shake_x = int(math.sin(time.time() * 60) * 10)
            shake_y = int(math.cos(time.time() * 55) * 10)

            h, w = frame.shape[:2]
            M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
            frame = cv2.warpAffine(frame, M, (w, h))

            # Forward rush illusion (center zoom growth)
            if locked_center:
                frame = energy.blast(frame, locked_center, blast_scale)

                frame = shockwave(
                    frame,
                    locked_center,
                    int(150 * blast_scale)
                )

            # Peak explosion moment
            if blast_scale > 3:

                if locked_center:
                    frame = explosion(frame, locked_center)

                # Reset everything cleanly
                state = "IDLE"
                fusion_center = None
                locked_center = None
                blast_scale = 1

        # =================================================

        cv2.imshow("Hollow Purple Engine", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
