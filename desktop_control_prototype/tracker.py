"""Hand tracker wrapper with optional MediaPipe fallback."""
try:
    import mediapipe as mp
except Exception:
    mp = None

try:
    from mediapipe.python.solutions import hands as mp_hands
except Exception:
    mp_hands = None


class Tracker:
    def __init__(self):
        hands_factory = None
        if mp is not None and hasattr(mp, "solutions"):
            hands_factory = mp.solutions.hands.Hands
        elif mp_hands is not None:
            hands_factory = mp_hands.Hands

        if hands_factory is None:
            self.hands = None
            return

        self.hands = hands_factory(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def get_landmarks(self, frame):
        """Return a list of normalized landmark tuples or empty list.

        Landmarks are (x, y, z) normalized to [0,1] for x and y.
        """
        if self.hands is None or frame is None:
            return []
        image_rgb = frame[:, :, ::-1]
        results = self.hands.process(image_rgb)
        if not results.multi_hand_landmarks:
            return []
        hand = results.multi_hand_landmarks[0]
        # Convert to simple list of (x,y,z)
        return [(lm.x, lm.y, lm.z) for lm in hand.landmark]
