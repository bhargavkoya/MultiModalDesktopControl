import unittest

from desktop_control_prototype.intents import classify_pose, resolve_intent
from desktop_control_prototype.state_machine import Mode, StateMachine


def _landmarks(index_tip=(0.5, 0.4), thumb_tip=(0.5, 0.5), middle_tip=(0.5, 0.6),
               ring_tip=(0.5, 0.6), pinky_tip=(0.5, 0.6), index_pip=(0.5, 0.5),
               middle_pip=(0.5, 0.5), ring_pip=(0.5, 0.5), pinky_pip=(0.5, 0.5)):
    points = [(0.0, 0.0, 0.0)] * 21
    points[4] = (*thumb_tip, 0.0)
    points[6] = (*index_pip, 0.0)
    points[8] = (*index_tip, 0.0)
    points[10] = (*middle_pip, 0.0)
    points[12] = (*middle_tip, 0.0)
    points[14] = (*ring_pip, 0.0)
    points[16] = (*ring_tip, 0.0)
    points[18] = (*pinky_pip, 0.0)
    points[20] = (*pinky_tip, 0.0)
    return points


class IntentTests(unittest.TestCase):
    def test_classify_pointing(self):
        self.assertEqual(classify_pose(_landmarks()), "Pointing")

    def test_classify_open_palm(self):
        self.assertEqual(
            classify_pose(_landmarks(
                index_tip=(0.5, 0.2),
                thumb_tip=(0.4, 0.4),
                middle_tip=(0.5, 0.2),
                ring_tip=(0.5, 0.2),
                pinky_tip=(0.5, 0.2),
                index_pip=(0.5, 0.4),
                middle_pip=(0.5, 0.4),
                ring_pip=(0.5, 0.4),
                pinky_pip=(0.5, 0.4),
            )),
            "Open_Palm",
        )

    def test_classify_closed_fist(self):
        self.assertEqual(
            classify_pose(_landmarks(
                index_tip=(0.5, 0.6),
                thumb_tip=(0.4, 0.6),
                middle_tip=(0.5, 0.6),
                ring_tip=(0.5, 0.6),
                pinky_tip=(0.5, 0.6),
                index_pip=(0.5, 0.4),
                middle_pip=(0.5, 0.4),
                ring_pip=(0.5, 0.4),
                pinky_pip=(0.5, 0.4),
            )),
            "Closed_Fist",
        )

    def test_resolve_pointer_mode(self):
        intent = resolve_intent(Mode.IDLE.name, "Pointing")
        self.assertEqual(intent.action, "enter_pointer_mode")
        self.assertEqual(intent.next_mode, Mode.POINTER.name)

    def test_resolve_pointer_pinch_mode(self):
        intent = resolve_intent(Mode.POINTER.name, "Pinch")
        self.assertEqual(intent.action, "pointer_pinch")

    def test_resolve_explorer_navigation_default(self):
        intent = resolve_intent(Mode.EXPLORER_NAV.name, "Open_Palm")
        self.assertEqual(intent.action, "navigate_down")

    def test_state_machine_transition_from_string(self):
        sm = StateMachine()
        sm.transition("POINTER")
        self.assertEqual(sm.get_state(), "POINTER")


if __name__ == "__main__":
    unittest.main()
