"""Prototype entrypoint: smoke test capture + overlay draw."""
from desktop_control_prototype.camera import Camera
from desktop_control_prototype.config import ACTION_COOLDOWN_SECONDS, POINTER_SMOOTHING
from desktop_control_prototype.desktop_controller import DesktopController
from desktop_control_prototype.app_profiles import detect_active_profile, resolve_profile_intent
from desktop_control_prototype.intents import Intent, classify_pose, resolve_intent
from desktop_control_prototype.pointer_calibration import calibrate_pointer
from desktop_control_prototype.command_adapter import parse_command
from desktop_control_prototype.confirm_manager import ConfirmManager
from desktop_control_prototype.config import MMDC_CONFIRM_REQUIRED, CONFIRM_TIMEOUT
from desktop_control_prototype.pointer_interactions import PointerGestureState, advance_pointer_gesture
from desktop_control_prototype.tracker import Tracker
from desktop_control_prototype.overlay import draw_state
from desktop_control_prototype.state_machine import StateMachine
import os
import time
try:
    import cv2
except Exception:
    cv2 = None


def _execute_intent(controller, state_machine, intent):
    if intent.next_mode is not None:
        state_machine.transition(intent.next_mode)

    if intent.action == "click":
        controller.click()
    elif intent.action == "enter_navigation_mode":
        controller.open_explorer()
    elif intent.action == "open_selected_item":
        controller.open_selected()
    elif intent.action == "pause":
        controller.pause()
    elif intent.action == "resume":
        controller.resume()
    elif intent.action == "navigate_down":
        controller.navigate_down()
    elif intent.action == "navigate_up":
        controller.navigate_up()
    elif intent.action == "go_back":
        controller.go_back()
    elif intent.action == "focus_address_bar":
        controller.focus_address_bar()
    elif intent.action == "save_document":
        controller.save_document()
    elif intent.action == "find":
        controller.find()
    elif intent.action == "select_all":
        controller.select_all()
    elif intent.action == "bold":
        controller.bold()
    elif intent.action == "pointer_pinch":
        pass
    elif intent.action == "drag_tap":
        controller.mouse_down()
        controller.mouse_up()


def _is_throttled_action(action):
    return action in {
        "click",
        "open_selected_item",
        "navigate_down",
        "navigate_up",
        "go_back",
        "focus_address_bar",
        "save_document",
        "find",
        "select_all",
        "bold",
        "pointer_pinch",
        "drag_tap",
    }


def _is_sensitive_action(action: str) -> bool:
    return action in {
        "open_explorer",
        "open_selected_item",
        "save_document",
        "go_back",
    }


def _update_pointer(controller, landmarks, smoothed_pointer):
    if not landmarks:
        return smoothed_pointer

    try:
        index_tip = landmarks[8]
    except (IndexError, TypeError):
        return smoothed_pointer

    x_norm, y_norm = calibrate_pointer(index_tip[0], index_tip[1])

    if smoothed_pointer is None:
        smoothed_pointer = (x_norm, y_norm)
    else:
        prev_x, prev_y = smoothed_pointer
        smoothed_pointer = (
            (POINTER_SMOOTHING * prev_x) + ((1 - POINTER_SMOOTHING) * x_norm),
            (POINTER_SMOOTHING * prev_y) + ((1 - POINTER_SMOOTHING) * y_norm),
        )

    controller.move_pointer_normalized(*smoothed_pointer, duration=0)
    return smoothed_pointer


def _normalized_to_screen(controller, normalized_point):
    width, height = controller.screen_size()
    x = max(0, min(width - 1, int(normalized_point[0] * width)))
    y = max(0, min(height - 1, int(normalized_point[1] * height)))
    return x, y


def _save_frame(frame, project_root, filename="mmdc_sample.jpg"):
    screenshots_dir = os.path.join(project_root, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    out_path = os.path.join(screenshots_dir, filename)
    if cv2 is not None:
        cv2.imwrite(out_path, frame)
        return out_path
    return None


def main():
    max_frames = int(os.environ.get("MMDC_MAX_FRAMES", "1"))
    headless = os.environ.get("MMDC_HEADLESS", "0") == "1"
    cam = Camera()
    tracker = Tracker()
    controller = DesktopController()
    sm = StateMachine()
    confirm_manager = ConfirmManager(required=MMDC_CONFIRM_REQUIRED, timeout=CONFIRM_TIMEOUT)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    last_intent = "idle"
    last_gesture = "None"
    last_profile = "Generic"
    saved_path = None
    smoothed_pointer = None
    last_action_at = 0.0
    pointer_gesture_state = PointerGestureState()

    for _ in range(max_frames):
        frame = cam.get_frame()
        if frame is None:
            print("No frame captured; exiting.")
            return

        landmarks = tracker.get_landmarks(frame)
        gesture = classify_pose(landmarks)
        # Support an offline command input via env var for testing or text input
        cmd_text = os.environ.get("MMDC_COMMAND", "").strip()
        if cmd_text:
            cmd_intent = parse_command(cmd_text, sm.get_state())
            if cmd_intent:
                _execute_intent(controller, sm, cmd_intent)
            # clear the command so it doesn't re-run
            try:
                del os.environ["MMDC_COMMAND"]
            except Exception:
                os.environ["MMDC_COMMAND"] = ""
        active_profile = detect_active_profile()
        profile_intent = resolve_profile_intent(active_profile, sm.get_state(), gesture)
        intent = profile_intent or resolve_intent(sm.get_state(), gesture)

        current_state = sm.get_state()
        now = time.time()

        if current_state == "POINTER" and gesture == "Pointing":
            smoothed_pointer = _update_pointer(controller, landmarks, smoothed_pointer)
            intent = Intent(gesture=gesture, action="move_pointer", next_mode=None)

        elif current_state == "POINTER" and gesture == "Pinch":
            smoothed_pointer = _update_pointer(controller, landmarks, smoothed_pointer)
            pointer_action = advance_pointer_gesture(pointer_gesture_state, gesture, now)
            if pointer_action == "drag_start":
                controller.mouse_down()
                intent = Intent(gesture=gesture, action="pointer_drag_start", next_mode=None)
            elif pointer_action == "drag_update":
                if smoothed_pointer is not None:
                    controller.drag_to(*_normalized_to_screen(controller, smoothed_pointer), duration=0)
                intent = Intent(gesture=gesture, action="pointer_dragging", next_mode=None)
            elif pointer_action == "hold_pending":
                intent = Intent(gesture=gesture, action="pointer_hold", next_mode=None)
            else:
                intent = Intent(gesture=gesture, action=pointer_action or "pointer_pinch", next_mode=None)

        elif pointer_gesture_state.pinch_started_at is not None:
            pointer_action = advance_pointer_gesture(pointer_gesture_state, gesture, now)
            if pointer_action == "drag_end":
                controller.mouse_up()
            elif pointer_action == "drag_tap":
                pass
            if pointer_action:
                intent = Intent(gesture=gesture, action=pointer_action, next_mode=None)

        if _is_throttled_action(intent.action) and now - last_action_at < ACTION_COOLDOWN_SECONDS:
            intent = Intent(gesture=intent.gesture, action="no_op", next_mode=intent.next_mode)

        # Confirmation gating for sensitive actions
        confirm_message = None
        if intent.action and _is_sensitive_action(intent.action):
            confirm_result = confirm_manager.request(intent.action, now)
            if confirm_result == "pending":
                confirm_message = f"Confirm: repeat '{intent.action}' to execute"
                intent = Intent(gesture=intent.gesture, action="no_op", next_mode=intent.next_mode)
            else:
                # confirmed, proceed normally
                pass

        _execute_intent(controller, sm, intent)

        if _is_throttled_action(intent.action) and intent.action != "move_pointer" and intent.action != "no_op":
            last_action_at = now

        out = draw_state(frame, sm.get_state(), gesture, profile=active_profile, last_action=intent.action, confirm_message=confirm_message)
        saved_path = _save_frame(out, project_root)

        last_intent = intent.action
        last_gesture = gesture
        last_profile = active_profile

        if headless or cv2 is None:
            break

        try:
            cv2.imshow("MMDC Prototype", out)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
        except Exception:
            break

        time.sleep(0.01)

    if saved_path:
        print(f"Captured frame saved to: {saved_path}")
    print(f"State: {sm.get_state()} | Profile: {last_profile} | Gesture: {last_gesture} | Intent: {last_intent}")
    if cv2 is not None and not headless:
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass


if __name__ == "__main__":
    main()
