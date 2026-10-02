import unittest

from blender.design_geometry import (
    BASE_FOOTPRINT_MM,
    CARRIER_FOOTPRINT_MM,
    COVER_GLASS_MM,
    CUFF_END_WIDTH_MM,
    CUFF_GAP_MM,
    CUFF_MID_WIDTH_MM,
    DISPLAY_ACTIVE_MM,
    DISPLAY_OUTER_MM,
    SCREEN_LONG_AXIS,
    TILT_ANGLES_DEG,
    WATCH_ULTRA_MM,
    WRIST_MODEL_MM,
    cuff_width_at_fraction,
    estimated_underside_opening_mm,
    validate_geometry,
    visible_bezel_mm,
)


class DesignGeometryTests(unittest.TestCase):
    def test_display_is_92_mm_max_and_runs_along_arm(self):
        self.assertEqual(DISPLAY_OUTER_MM, (92.0, 44.0, 6.6))
        self.assertEqual(COVER_GLASS_MM, (91.2, 43.2))
        self.assertEqual(DISPLAY_ACTIVE_MM, (89.8, 40.6))
        self.assertEqual(WATCH_ULTRA_MM, (49.0, 44.0, 14.4))
        self.assertEqual(SCREEN_LONG_AXIS, "along_arm")

    def test_open_cuff_is_broad_in_middle_and_tapers_at_both_ends(self):
        self.assertGreaterEqual(CUFF_MID_WIDTH_MM, 26.0)
        self.assertLessEqual(CUFF_MID_WIDTH_MM, 30.0)
        self.assertLessEqual(CUFF_END_WIDTH_MM, 14.0)
        self.assertAlmostEqual(cuff_width_at_fraction(0.0), CUFF_END_WIDTH_MM)
        self.assertAlmostEqual(cuff_width_at_fraction(1.0), CUFF_END_WIDTH_MM)
        self.assertGreater(cuff_width_at_fraction(0.5), CUFF_END_WIDTH_MM * 2.0)

    def test_open_cuff_leaves_a_real_hand_entry_gap(self):
        self.assertGreaterEqual(CUFF_GAP_MM, 48.0)
        self.assertGreaterEqual(estimated_underside_opening_mm("average"), 48.0)
        self.assertGreaterEqual(estimated_underside_opening_mm("slim"), 44.0)
        self.assertGreater(WRIST_MODEL_MM["width"], 50.0)

    def test_cover_glass_is_nearly_borderless(self):
        long_edge, short_end = visible_bezel_mm()
        self.assertLessEqual(long_edge, 1.7)
        self.assertLessEqual(short_end, 1.7)

    def test_hidden_base_and_carrier_fit_under_along_arm_display(self):
        self.assertLessEqual(BASE_FOOTPRINT_MM[0], DISPLAY_OUTER_MM[1])
        self.assertLess(BASE_FOOTPRINT_MM[1], DISPLAY_OUTER_MM[0])
        self.assertLessEqual(CARRIER_FOOTPRINT_MM[0], DISPLAY_OUTER_MM[1])
        self.assertLess(CARRIER_FOOTPRINT_MM[1], DISPLAY_OUTER_MM[0])
    def test_tilt_states_cover_closed_reading_and_high_tilt(self):
        self.assertIn(0, TILT_ANGLES_DEG)
        self.assertIn(30, TILT_ANGLES_DEG)
        self.assertIn(55, TILT_ANGLES_DEG)

    def test_geometry_validator_has_no_errors(self):
        self.assertEqual(validate_geometry(), [])


if __name__ == "__main__":
    unittest.main()
