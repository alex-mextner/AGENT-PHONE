import unittest

from blender.design_geometry import REQUIRED_LIFESTYLE_SCENES, REQUIRED_MECHANICAL_SCENES
from blender.scene_manifest import SCENES, scene_names


class SceneManifestTests(unittest.TestCase):
    def test_all_required_scenes_are_declared(self):
        names = set(scene_names())
        self.assertTrue(set(REQUIRED_MECHANICAL_SCENES).issubset(names))
        self.assertTrue(set(REQUIRED_LIFESTYLE_SCENES).issubset(names))

    def test_every_scene_keeps_along_arm_orientation_and_open_cuff(self):
        for name, spec in SCENES.items():
            self.assertEqual(spec["screen_long_axis"], "along_arm", name)
            self.assertEqual(spec["cuff"], "open", name)

    def test_scale_comparison_contains_watch_reference(self):
        comparison = SCENES["scale-comparison"]
        self.assertTrue(comparison["watch_reference"])
        self.assertEqual(comparison["render_kind"], "technical")

    def test_tilt_scenes_use_expected_angles(self):
        self.assertEqual(SCENES["closed-side"]["tilt_deg"], 0)
        self.assertEqual(SCENES["tilt-30"]["tilt_deg"], 30)
        self.assertEqual(SCENES["tilt-55"]["tilt_deg"], 55)

    def test_lifestyle_scenes_map_to_existing_ui_textures(self):
        textured = {
            name: spec["texture"]
            for name, spec in SCENES.items()
            if spec.get("texture")
        }
        self.assertEqual(textured["chat-list-thread"], "chat")
        self.assertEqual(textured["home-status"], "home")
        self.assertEqual(textured["media-handoff"], "handoff")
        self.assertEqual(textured["outdoor-navigation"], "navigation")


if __name__ == "__main__":
    unittest.main()
