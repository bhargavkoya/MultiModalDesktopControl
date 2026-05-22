"""Camera utilities with safe fallbacks."""
import os

try:
    import cv2
except Exception:
    cv2 = None


class Camera:
    def __init__(self, device=0):
        self.device = device

    def get_frame(self):
        """Capture a single frame and return it (BGR numpy array) or None."""
        if cv2 is None:
            print("OpenCV not installed; camera unavailable.")
            return None
        cap = cv2.VideoCapture(self.device)
        if not cap.isOpened():
            print("Unable to open camera device.")
            return None
        ret, frame = cap.read()
        cap.release()
        if not ret:
            print("Failed to read frame from camera.")
            return None
        return frame
