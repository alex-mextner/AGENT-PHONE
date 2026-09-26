from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepoCopyTests(unittest.TestCase):
    def test_readme_uses_canonical_name_and_links(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("# AGENT-PHONE", text)
        self.assertIn("## Concept renders", text)
        self.assertIn("https://agentos-bible.vercel.app/", text)
        self.assertIn("https://github.com/alex-mextner/sapio-state", text)
        self.assertIn("docs/ring-and-spatial-input.md", text)
        self.assertIn("docs/camera-strategy.md", text)

    def test_public_render_gallery_hides_implementation_tooling(self):
        text = (ROOT / "renders" / "README.md").read_text()
        self.assertTrue(text.startswith("# Concept renders"))
        self.assertNotIn("# Blender renders", text)

    def test_superpowers_workspace_is_ignored(self):
        text = (ROOT / ".gitignore").read_text()
        self.assertIn(".superpowers/", text)

    def test_gallery_publishes_new_render_set_not_rejected_baseline(self):
        text = (ROOT / "renders" / "README.md").read_text()
        for image in (
            "home-status.png",
            "chat-list-thread.png",
            "scale-comparison.png",
            "open-cuff-underside.png",
            "ring-spatial.png",
            "glasses-companion.png",
            "external-battery.png",
            "car-hud.png",
        ):
            self.assertIn(image, text)
        self.assertNotIn("hero-home.png", text)
        self.assertNotIn("tilted-chat.png", text)
        for rejected in (
            "hero-home.png",
            "tilted-chat.png",
            "remote-control.png",
            "side-profile.png",
            "screen-concept.blend",
        ):
            self.assertFalse((ROOT / "renders" / rejected).exists(), rejected)


if __name__ == "__main__":
    unittest.main()
