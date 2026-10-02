"""Regression tests for the GH-4 final-review fix pass (C1-C3 already rebuilt).

Fast pytest/unittest checks (no Blender): wording truth, portable kit
references, renamed hinge metadata, and the evaluated closed-stack field.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class ReviewFixRegressions(unittest.TestCase):
    def test_spec_cuff_wording_broad_middle_not_root(self):
        spec = read("SPEC.md")
        self.assertIn("broad in the curved middle", spec)
        self.assertIn("about 12 mm", spec)
        self.assertNotIn("broad where it meets the module", spec)
        self.assertIn("middle of the long module sides", spec)

    def test_spec_states_evaluated_closed_stack(self):
        spec = read("SPEC.md")
        self.assertIn("14.8 mm above nominal proxy skin", spec)
        self.assertIn("closed_stack_mm", spec)

    def test_gallery_no_comfort_claim(self):
        gallery = read("renders/README.md")
        self.assertNotIn("comfortable reading angle", gallery)
        self.assertIn("comfort untested", gallery)
        self.assertIn("donning/retention unvalidated", gallery)

    def test_fit_kit_portable_and_safe_wording(self):
        kit = read("prototype/fit-kit/README.md")
        self.assertNotIn("/Users/ultra/.cache", kit)
        self.assertIn("Stop immediately on discomfort", kit)
        self.assertIn("simulated", kit.lower())
        self.assertIn("workflow comprehension", kit)
        self.assertIn("NOT recognition", kit)
        self.assertIn("dummy mass", kit.lower())
        self.assertIn("10 mm", kit)
        self.assertIn("module-envelope", kit)
        self.assertIn("dummies only", kit)
        self.assertIn("alterego", kit.lower())
        self.assertIn("echospeech", kit.lower())
        self.assertIn("doi", kit.lower())

    def test_hinge_metadata_renamed(self):
        src = read("blender/scene_builder.py")
        self.assertIn("nominal_hinge_offset_mm", src)
        self.assertNotIn("minimum_screen_clearance_mm", src)

    def test_validate_scene_reports_closed_stack(self):
        src = read("blender/validate_scene.py")
        self.assertIn("closed_stack_mm", src)
        self.assertIn("validate_closed_stack", src)
        self.assertIn("13-17 mm regression band", src)

    def test_collision_scope_limits_documented(self):
        doc = read("blender/README.md")
        self.assertIn("fully enclosed in another", doc)
        self.assertIn("not an exact edge-edge", doc.lower())


if __name__ == "__main__":
    unittest.main()
