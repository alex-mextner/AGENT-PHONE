from pathlib import Path
import tempfile
import unittest

from blender import human_asset


ROOT = Path(__file__).resolve().parents[1]


class HumanAssetTests(unittest.TestCase):
    def test_metadata_documents_source_license_and_local_cache(self):
        meta = human_asset.HUMAN_ASSET_METADATA
        self.assertIn("makehumancommunity", meta["source_url"])
        self.assertEqual(meta["license"], "CC0-1.0")
        self.assertIn("LICENSE", meta["license_url"].upper())
        self.assertEqual(meta["redistribution"], "download-on-demand")
        self.assertTrue(meta["base_obj"].endswith("base.obj"))
        self.assertTrue(meta["skin_zip"].endswith(".zip"))

    def test_missing_asset_fails_clearly(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "base.obj"
            with self.assertRaisesRegex(FileNotFoundError, "fetch_human_asset"):
                human_asset.require_asset(missing)

    def test_profiles_are_explicit_not_silent_scale_guesses(self):
        self.assertIn("average", human_asset.WRIST_PROFILES)
        self.assertIn("slim", human_asset.WRIST_PROFILES)
        self.assertGreater(human_asset.WRIST_PROFILES["average"]["wrist_width_mm"], 50)
        self.assertLess(human_asset.WRIST_PROFILES["slim"]["wrist_width_mm"],
                        human_asset.WRIST_PROFILES["average"]["wrist_width_mm"])

    def test_asset_readme_names_license_and_cache_policy(self):
        text = (ROOT / "assets" / "human" / "README.md").read_text()
        self.assertIn("CC0", text)
        self.assertIn("MakeHuman", text)
        self.assertIn("download-on-demand", text)
        self.assertIn("assets/human/cache", text)


if __name__ == "__main__":
    unittest.main()
