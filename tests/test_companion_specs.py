from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CompanionSpecTests(unittest.TestCase):
    def test_readme_links_critical_scenarios_and_names_core_companions(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("docs/critical-scenarios.md", text)
        self.assertIn("external endurance battery", text.lower())
        self.assertIn("car hud", text.lower())
        self.assertIn("bone-conduction", text.lower())

    def test_spec_covers_external_battery_glasses_audio_and_car_hud(self):
        text = (ROOT / "SPEC.md").read_text().lower()
        for phrase in (
            "underarm",
            "lower back",
            "bone-conduction",
            "gaze",
            "car hud",
            "silent articulation",
        ):
            self.assertIn(phrase, text)

    def test_critical_scenario_matrix_is_large_and_risk_aware(self):
        path = ROOT / "docs" / "critical-scenarios.md"
        self.assertTrue(path.exists())
        text = path.read_text()
        rows = [line for line in text.splitlines() if line.startswith("| ") and not line.startswith("| Scenario") and not line.startswith("| ---")]
        self.assertGreaterEqual(len(rows), 16)
        self.assertIn("Car HUD", text)
        self.assertIn("Industrial", text)
        self.assertIn("Healthcare", text)
        self.assertIn("Cycling", text)
        self.assertIn("New risk", text)
        self.assertIn("Screen-off", text)


if __name__ == "__main__":
    unittest.main()
