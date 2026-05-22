import unittest
from time import time

from desktop_control_prototype.confirm_manager import ConfirmManager


class ConfirmManagerTests(unittest.TestCase):
    def test_confirmation_required_flow(self):
        cm = ConfirmManager(required=True, timeout=1.0)
        now = 100.0
        res = cm.request("save_document", now)
        self.assertEqual(res, "pending")
        # repeat within timeout
        res = cm.request("save_document", now + 0.5)
        self.assertEqual(res, "confirmed")
        # gesture-based confirm should also work when pending
        res = cm.request("go_back", now + 2.0)
        self.assertEqual(res, "pending")
        self.assertTrue(cm.confirm_with_gesture("Open_Palm", now + 2.1))

    def test_gesture_confirm_requires_matching_gesture_and_non_expired_pending(self):
        cm = ConfirmManager(required=True, timeout=1.0, confirm_gesture="Open_Palm")
        now = 300.0
        self.assertEqual(cm.request("save_document", now), "pending")
        self.assertFalse(cm.confirm_with_gesture("Pinch", now + 0.1))
        self.assertEqual(cm.pending_action, "save_document")
        self.assertFalse(cm.confirm_with_gesture("Open_Palm", now + 1.2))
        self.assertIsNone(cm.pending_action)

    def test_expired_pending(self):
        cm = ConfirmManager(required=True, timeout=1.0)
        now = 200.0
        res = cm.request("go_back", now)
        self.assertEqual(res, "pending")
        # expire
        cm.cancel_if_expired(now + 2.0)
        res = cm.request("go_back", now + 2.1)
        self.assertEqual(res, "pending")

    def test_not_required(self):
        cm = ConfirmManager(required=False, timeout=1.0)
        res = cm.request("save_document", 0.0)
        self.assertEqual(res, "confirmed")


if __name__ == "__main__":
    unittest.main()
