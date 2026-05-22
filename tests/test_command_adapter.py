import unittest

from desktop_control_prototype.command_adapter import parse_command
from desktop_control_prototype.state_machine import Mode


class CommandAdapterTests(unittest.TestCase):
    def test_parse_open_explorer(self):
        intent = parse_command("Open Explorer")
        self.assertIsNotNone(intent)
        self.assertEqual(intent.action, "enter_navigation_mode")

    def test_parse_pointer_mode(self):
        intent = parse_command("pointer mode")
        self.assertIsNotNone(intent)
        self.assertEqual(intent.action, "enter_pointer_mode")

    def test_parse_save_and_find(self):
        self.assertEqual(parse_command("save").action, "save_document")
        self.assertEqual(parse_command("find").action, "find")

    def test_unknown_command(self):
        self.assertIsNone(parse_command("do something weird"))


if __name__ == "__main__":
    unittest.main()
