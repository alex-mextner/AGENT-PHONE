import unittest

from blender.render_plan import RENDER_PLAN


class RenderPlanTests(unittest.TestCase):
    def test_required_mechanical_scenes_have_explicit_cameras(self):
        expected = {
            "scale-comparison": "top-ortho",
            "closed-side": "side-ortho",
            "tilt-30": "side-ortho",
            "tilt-55": "side-ortho",
            "open-cuff-underside": "underside",
            "mechanism-exploded": "exploded",
            "detached-module": "hero",
        }
        for name, camera in expected.items():
            self.assertIn(name, RENDER_PLAN)
            self.assertEqual(RENDER_PLAN[name]["camera"], camera)

    def test_scale_comparison_is_orthographic_and_has_reference(self):
        scene = RENDER_PLAN["scale-comparison"]
        self.assertTrue(scene["orthographic"])
        self.assertTrue(scene["watch_reference"])
        self.assertEqual(scene["texture"], None)

    def test_preview_dimensions_are_consistent(self):
        for name, scene in RENDER_PLAN.items():
            self.assertEqual(scene["preview_resolution"], (1000, 760), name)
            self.assertEqual(scene["final_resolution"], (1800, 1368), name)

    def test_technical_views_do_not_occlude_the_subject(self):
        self.assertFalse(RENDER_PLAN["open-cuff-underside"]["ground"])
        self.assertFalse(RENDER_PLAN["open-cuff-underside"]["wrist_proxy"])
        self.assertFalse(RENDER_PLAN["mechanism-exploded"]["wrist_proxy"])
        self.assertFalse(RENDER_PLAN["detached-module"]["wrist_proxy"])
        self.assertTrue(RENDER_PLAN["tilt-55"]["wrist_proxy"])


if __name__ == "__main__":
    unittest.main()
