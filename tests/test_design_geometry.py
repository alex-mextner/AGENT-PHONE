import unittest

from blender.design_geometry import (
    DISPLAY_OUTER_MM,
    DISPLAY_ACTIVE_MM,
    WATCH_ULTRA_MM,
    WRIST_MODEL_MM,
    CUFF_GAP_MM,
    TILT_ANGLES_DEG,
    SCREEN_LONG_AXIS,
    BASE_FOOTPRINT_MM,
    CARRIER_FOOTPRINT_MM,
    visible_bezel_mm,
    validate_geometry,
)


class DesignGeometryTests(unittest.TestCase):
    def test_display_matches_two_watch_ultras_without_becoming_a_phone_slab(self):
        self.assertEqual(DISPLAY_OUTER_MM, (94.0, 45.0, 6.2))
        self.assertEqual(DISPLAY_ACTIVE_MM, (91.0, 42.0))
        self.assertEqual(WATCH_ULTRA_MM, (49.0, 44.0, 14.4))
        self.assertLessEqual(DISPLAY_OUTER_MM[0], WATCH_ULTRA_MM[0] * 2)
        self.assertLessEqual(DISPLAY_OUTER_MM[1], WATCH_ULTRA_MM[1] + 1.0)

    def test_long_axis_is_across_wrist_like_two_watch_ultras_side_by_side(self):
        self.assertEqual(SCREEN_LONG_AXIS, "across_wrist")

    def test_open_cuff_leaves_desk_contact_zone_free(self):
        self.assertGreaterEqual(CUFF_GAP_MM, 28.0)
        self.assertGreater(WRIST_MODEL_MM["width"], CUFF_GAP_MM)

    def test_cover_glass_is_nearly_borderless(self):
        left_right, short_ends = visible_bezel_mm()
        self.assertLessEqual(left_right, 1.5)
        self.assertLessEqual(short_ends, 1.5)

    def test_hidden_base_and_carrier_stay_visually_smaller_than_display(self):
        self.assertLessEqual(BASE_FOOTPRINT_MM[0], 64.0)
        self.assertLessEqual(BASE_FOOTPRINT_MM[1], 32.0)
        self.assertLessEqual(CARRIER_FOOTPRINT_MM[0], 70.0)
        self.assertLessEqual(CARRIER_FOOTPRINT_MM[1], 24.0)

    def test_tilt_states_cover_closed_reading_and_high_tilt(self):
        self.assertIn(0, TILT_ANGLES_DEG)
        self.assertIn(30, TILT_ANGLES_DEG)
        self.assertIn(55, TILT_ANGLES_DEG)

    def test_geometry_validator_has_no_errors(self):
        self.assertEqual(validate_geometry(), [])


if __name__ == "__main__":
    unittest.main()
