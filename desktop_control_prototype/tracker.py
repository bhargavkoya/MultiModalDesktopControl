"""Hand tracker wrapper with robust MediaPipe import fallbacks."""
import importlib
import logging

_LOG = logging.getLogger(__name__)

mp = None
mp_hands = None
import_path_used = None
try:
    import mediapipe as mp
except Exception:
    mp = None

# Try several common import paths where MediaPipe may expose Hands
for candidate in (
    "mediapipe.solutions.hands",
    "mediapipe.python.solutions.hands",
    "mediapipe.python.solutions",
    "mediapipe.solutions",
):
    try:
        mod = importlib.import_module(candidate)
        if hasattr(mod, "Hands"):
            mp_hands = mod
            import_path_used = candidate
            break
        # some modules expose .hands attribute instead
        if hasattr(mod, "hands") and hasattr(mod.hands, "Hands"):
            mp_hands = mod.hands
            import_path_used = candidate + ".hands"
            break
    except Exception:
        continue

if mp_hands is None and mp is not None:
    try:
        if hasattr(mp, "solutions") and hasattr(mp.solutions, "hands"):
            mp_hands = mp.solutions.hands
            import_path_used = "mediapipe.solutions.hands (via mediapipe)"
    except Exception:
        mp_hands = None

if mp_hands:
    _LOG.info("Using MediaPipe Hands from: %s", import_path_used)
else:
    _LOG.info("MediaPipe Hands not available; hand tracking disabled")


class Tracker:
    def __init__(self):
        hands_factory = None
        if mp_hands is not None and hasattr(mp_hands, "Hands"):
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
        try:
            image_rgb = frame[:, :, ::-1]
        except Exception:
            return []
        try:
            results = self.hands.process(image_rgb)
        except Exception as e:
            _LOG.exception("MediaPipe processing error: %s", e)
            return []
        if not results or not getattr(results, "multi_hand_landmarks", None):
            return []
        hand = results.multi_hand_landmarks[0]
        # Convert to simple list of (x,y,z)
        return [(lm.x, lm.y, lm.z) for lm in hand.landmark]
