import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self, max_hands=2):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

    # ---------------------------------------------------
    # RETURNS:
    # frame (with landmarks)
    # left_index (x, y) or None
    # right_index (x, y) or None
    # ---------------------------------------------------
    def get_index_positions(self, frame):

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        left_index = None
        right_index = None

        if results.multi_hand_landmarks and results.multi_handedness:

            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):

                label = handedness.classification[0].label

                # Index fingertip = landmark 8
                index_tip = hand_landmarks.landmark[8]
                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                if label == "Left":
                    left_index = (x, y)
                elif label == "Right":
                    right_index = (x, y)

                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame, left_index, right_index
