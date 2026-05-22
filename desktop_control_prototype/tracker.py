"""Hand tracker wrapper with optional MediaPipe fallback."""
try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except Exception:
    mp = None
    HAS_MEDIAPIPE = False


class Tracker:
    def __init__(self):
        if HAS_MEDIAPIPE:
            self.hands = mp.solutions.hands.Hands(static_image_mode=False,
                                                  max_num_hands=1,
                                                  min_detection_confidence=0.5,
                                                  min_tracking_confidence=0.5)
        else:
            self.hands = None

    def get_landmarks(self, frame):
        """Return a list of normalized landmark tuples or empty list.

        Landmarks are (x, y, z) normalized to [0,1] for x and y.
        """
        if not HAS_MEDIAPIPE or frame is None:
            return []
        image_rgb = frame[:, :, ::-1]
        results = self.hands.process(image_rgb)
        if not results.multi_hand_landmarks:
            return []
        hand = results.multi_hand_landmarks[0]
        # Convert to simple list of (x,y,z)
        return [(lm.x, lm.y, lm.z) for lm in hand.landmark]
