"""Prototype entrypoint: smoke test capture + overlay draw."""
from desktop_control_prototype.camera import Camera
from desktop_control_prototype.tracker import Tracker
from desktop_control_prototype.overlay import draw_state
from desktop_control_prototype.state_machine import StateMachine
from desktop_control_prototype.gestures import interpret
import os
try:
    import cv2
except Exception:
    cv2 = None


def main():
    cam = Camera()
    frame = cam.get_frame()
    if frame is None:
        print("No frame captured; exiting.")
        return
    tracker = Tracker()
    landmarks = tracker.get_landmarks(frame)
    gesture = interpret(landmarks)
    sm = StateMachine()
    state = sm.get_state()
    out = draw_state(frame, state, gesture, last_action=None)
    out_path = "/tmp/mmdc_sample.jpg"
    if cv2 is not None:
        cv2.imwrite(out_path, out)
        print(f"Captured frame saved to: {out_path}")
    else:
        print("OpenCV not available; captured frame not saved.")


if __name__ == "__main__":
    main()
