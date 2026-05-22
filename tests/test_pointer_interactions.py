import unittest

from desktop_control_prototype.pointer_interactions import PointerGestureState, advance_pointer_gesture


class PointerInteractionTests(unittest.TestCase):
    def test_short_pinch_resolves_to_click_on_release(self):
        state = PointerGestureState()
        self.assertEqual(advance_pointer_gesture(state, "Pinch", 0.0), "hold_pending")
        self.assertEqual(advance_pointer_gesture(state, "Open_Palm", 0.1), "click")

    def test_long_pinch_resolves_to_drag_start_then_end(self):
        state = PointerGestureState()
        self.assertEqual(advance_pointer_gesture(state, "Pinch", 0.0), "hold_pending")
        self.assertEqual(advance_pointer_gesture(state, "Pinch", 0.4), "drag_start")
        self.assertEqual(advance_pointer_gesture(state, "Pinch", 0.5), "drag_update")
        self.assertEqual(advance_pointer_gesture(state, "Open_Palm", 0.6), "drag_end")


if __name__ == "__main__":
    unittest.main()