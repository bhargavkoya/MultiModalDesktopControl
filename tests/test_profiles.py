import unittest

from desktop_control_prototype.app_profiles import detect_active_profile, resolve_profile_intent
from desktop_control_prototype.state_machine import Mode


class ProfileTests(unittest.TestCase):
    def test_detect_explorer_profile(self):
        self.assertEqual(detect_active_profile("File Explorer"), "Explorer")

    def test_detect_word_profile(self):
        self.assertEqual(detect_active_profile("Microsoft Word - Document1"), "Word")

    def test_detect_generic_profile(self):
        self.assertEqual(detect_active_profile("Terminal"), "Generic")

    def test_resolve_explorer_profile_intent(self):
        intent = resolve_profile_intent("Explorer", Mode.EXPLORER_NAV.name, "Pinch")
        self.assertIsNotNone(intent)
        self.assertEqual(intent.action, "open_selected_item")

    def test_resolve_word_profile_intent(self):
        intent = resolve_profile_intent("Word", Mode.APP_CONTROL.name, "Pinch")
        self.assertIsNotNone(intent)
        self.assertEqual(intent.action, "save_document")
        intent = resolve_profile_intent("Word", Mode.APP_CONTROL.name, "Open_Palm")
        self.assertIsNotNone(intent)
        self.assertEqual(intent.action, "find")
        intent = resolve_profile_intent("Word", Mode.APP_CONTROL.name, "Pointing")
        self.assertIsNotNone(intent)
        self.assertEqual(intent.action, "select_all")
        intent = resolve_profile_intent("Word", Mode.APP_CONTROL.name, "Closed_Fist")
        self.assertIsNotNone(intent)
        self.assertEqual(intent.action, "bold")


if __name__ == "__main__":
    unittest.main()