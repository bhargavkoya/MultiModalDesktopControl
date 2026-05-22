"""Overlay utilities to render mode and gesture info on frames."""
try:
    import cv2
except Exception:
    cv2 = None


def draw_state(frame, state, gesture, last_action=None):
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
    if last_action:
        text += f" | Last: {last_action}"
    cv2.putText(frame, text, (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return frame
