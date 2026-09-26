import unittest

from blender.render_plan import RENDER_PLAN
from blender.design_geometry import REQUIRED_LIFESTYLE_SCENES


class LifestyleRenderContractTests(unittest.TestCase):
    def test_every_lifestyle_scene_uses_real_human_not_validation_proxy(self):
        for name in REQUIRED_LIFESTYLE_SCENES:
            spec = RENDER_PLAN[name]
            self.assertFalse(spec["wrist_proxy"], name)
            self.assertIn(spec["human_profile"], {"average", "slim"}, name)

    def test_context_scenes_declare_their_physical_companions(self):
        expected = {
            "media-handoff": "tv",
            "ring-spatial": "ring-room",
            "glasses-companion": "glasses",
            "camera-companion": "camera-tile",
            "desk-clearance": "desk-laptop",
            "dive-concept": "dive-clasp",
            "external-battery": "external-battery",
            "car-hud": "car-hud",
        }
        for name, context in expected.items():
            self.assertEqual(RENDER_PLAN[name]["context"], context)

    def test_every_lifestyle_scene_has_human_offset_and_texture(self):
        for name in REQUIRED_LIFESTYLE_SCENES:
            spec = RENDER_PLAN[name]
            self.assertIsInstance(spec["human_offset_y_mm"], (int, float))
            self.assertGreater(spec["human_offset_y_mm"], 10)
            self.assertTrue(spec["texture"], name)


if __name__ == "__main__":
    unittest.main()
