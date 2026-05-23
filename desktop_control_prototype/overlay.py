"""Overlay utilities to render mode and gesture info on frames."""
try:
    import cv2
except Exception:
    cv2 = None


HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
)


def draw_landmarks(frame, landmarks):
    if frame is None or not landmarks or cv2 is None:
        return frame

    h, w = frame.shape[:2]

    for x, y, _ in landmarks:
        px = int(x * w)
        py = int(y * h)
        cv2.circle(frame, (px, py), 4, (0, 255, 0), -1)

    for start, end in HAND_CONNECTIONS:
        try:
            ax, ay, _ = landmarks[start]
            bx, by, _ = landmarks[end]
        except (IndexError, TypeError):
            continue

        p1 = (int(ax * w), int(ay * h))
        p2 = (int(bx * w), int(by * h))
        cv2.line(frame, p1, p2, (0, 255, 0), 2)

    return frame


def draw_state(frame, state, gesture, profile=None, last_action=None, confirm_message=None):
    if frame is None:
        return None
    if cv2 is None:
        # OpenCV not available; return frame unchanged but log
        print("OpenCV not available; overlay skipped")
        return frame
    h, w = frame.shape[:2]
    # semi-transparent banner
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 48), (0, 0, 0), -1)
    alpha = 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    text = f"Mode: {state} | Gesture: {gesture}"
    if profile:
        text += f" | Profile: {profile}"
    if last_action:
        text += f" | Last: {last_action}"
    if confirm_message:
        cv2.putText(frame, confirm_message, (8, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 200), 2)
    cv2.putText(frame, text, (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return frame
