import unittest

from desktop_control_prototype.pointer_calibration import calibrate_pointer


class PointerCalibrationTests(unittest.TestCase):
    def test_clamps_values_into_calibration_range(self):
        x, y = calibrate_pointer(-1.0, 2.0)
        self.assertGreaterEqual(x, 0.0)
        self.assertLessEqual(x, 1.0)
        self.assertGreaterEqual(y, 0.0)
        self.assertLessEqual(y, 1.0)

    def test_maps_center_point(self):
        x, y = calibrate_pointer(0.5, 0.5)
        self.assertGreater(x, 0.4)
        self.assertLess(x, 0.6)
        self.assertGreater(y, 0.4)
        self.assertLess(y, 0.6)


if __name__ == "__main__":
    unittest.main()