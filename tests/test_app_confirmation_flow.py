import os
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from desktop_control_prototype import app
from desktop_control_prototype.intents import Intent


class AppConfirmationFlowTests(unittest.TestCase):
    def test_confirm_gesture_executes_pending_action_even_when_current_intent_differs(self):
        frame = object()
        cam = Mock()
        cam.get_frame.side_effect = [frame, frame]
        tracker = Mock()
        tracker.get_landmarks.return_value = {}
        controller = Mock()
        state_machine = Mock()
        state_machine.get_state.return_value = "IDLE"

        profile_intents = [
            Intent(gesture="Pinch", action="save_document", next_mode=None),
            Intent(gesture="Open_Palm", action="find", next_mode=None),
        ]
        executed_actions = []

        def capture_execute(_controller, _state_machine, intent):
            executed_actions.append(intent.action)

        fake_cv2 = SimpleNamespace(
            imshow=lambda *_args, **_kwargs: None,
            waitKey=lambda _delay: 0,
            destroyAllWindows=lambda: None,
        )

        with patch.dict(os.environ, {"MMDC_MAX_FRAMES": "2", "MMDC_HEADLESS": "0"}, clear=False), \
             patch.object(app, "Camera", return_value=cam), \
             patch.object(app, "Tracker", return_value=tracker), \
             patch.object(app, "DesktopController", return_value=controller), \
             patch.object(app, "StateMachine", return_value=state_machine), \
             patch.object(app, "detect_active_profile", return_value="Word"), \
             patch.object(app, "resolve_profile_intent", side_effect=profile_intents), \
             patch.object(app, "resolve_intent", return_value=Intent(gesture="None", action="no_op", next_mode=None)), \
             patch.object(app, "classify_pose", side_effect=["Pinch", "Open_Palm"]), \
             patch.object(app, "_execute_intent", side_effect=capture_execute), \
             patch.object(app, "draw_state", return_value=frame), \
             patch.object(app, "_save_frame", return_value=None), \
             patch.object(app, "MMDC_CONFIRM_REQUIRED", True), \
             patch.object(app, "CONFIRM_GESTURE", "Open_Palm"), \
             patch.object(app, "cv2", fake_cv2):
            app.main()

        self.assertEqual(executed_actions, ["no_op", "save_document"])


if __name__ == "__main__":
    unittest.main()
