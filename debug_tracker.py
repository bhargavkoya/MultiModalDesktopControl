# debug_tracker.py
import sys
from pathlib import Path

try:
    import cv2
except Exception as e:
    print("OpenCV import error:", e)
    cv2 = None

mp = None
mp_hands = None
try:
    import mediapipe as mp
except Exception:
    mp = None

# Try multiple import paths for MediaPipe Hands
import importlib
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

print("mediapipe module found:", mp is not None)
print("mp_hands available:", bool(mp_hands))
if mp_hands:
    print("Using MediaPipe Hands from:", import_path_used)

# Try capturing a live frame
cap = cv2.VideoCapture(0) if cv2 else None
if cap is None or not cap.isOpened():
    print("Camera open failed. Try index 1: change VideoCapture(0) -> VideoCapture(1)")
    sys.exit(1)

ret, frame = cap.read()
cap.release()
if not ret or frame is None:
    print("Failed to capture frame from camera.")
    sys.exit(1)

if mp_hands is None:
    print("MediaPipe Hands not available via any import path.")
    sys.exit(1)

with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.3) as hands:
    img_rgb = frame[:, :, ::-1] if frame is not None else None
    res = hands.process(img_rgb)
    if not res or not getattr(res, "multi_hand_landmarks", None):
        print("No landmarks detected in live frame.")
        out = Path("screenshots")
        out.mkdir(exist_ok=True)
        p = out / "debug_failed.jpg"
        if cv2 and frame is not None:
            cv2.imwrite(str(p), frame)
            print("Saved sample to", p)
    else:
        lm = res.multi_hand_landmarks[0]
        print("Landmarks detected:", len(lm.landmark))
        for i, lmpt in enumerate(lm.landmark[:5]):
            print(f"lm[{i}]: x={lmpt.x:.3f} y={lmpt.y:.3f} z={lmpt.z:.3f}")
        if cv2:
            try:
                # drawing utils path may vary
                from mediapipe.python.solutions import drawing_utils as mp_drawing
            except Exception:
                try:
                    import mediapipe as mp
                    mp_drawing = mp.solutions.drawing_utils
                except Exception:
                    mp_drawing = None

            if mp_drawing:
                annotated = frame.copy()
                try:
                    mp_drawing.draw_landmarks(annotated, lm, mp_hands.HAND_CONNECTIONS)
                    cv2.imshow("debug landmarks", annotated)
                    cv2.waitKey(3000)
                    cv2.destroyAllWindows()
                except Exception as e:
                    print("Could not draw landmarks preview:", e)
            else:
                print("Drawing utilities not available; skipping preview.")
