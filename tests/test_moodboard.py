from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MoodboardTests(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "docs" / "moodboard.md"

    def test_required_categories_and_user_reference(self):
        text = self.path.read_text() if self.path.exists() else ""
        required = [
            "Film & game wrist computers",
            "Real wearables",
            "Open cuffs & tilting displays",
            "Flexible / emissive displays",
            "Rings & spatial control",
            "Glasses",
            "Detachable cameras",
        ]
        for heading in required:
            self.assertIn(heading, text)
        self.assertIn("https://novate.ru/blogs/240711/18254/", text)

    def test_every_reference_card_has_keep_avoid_why(self):
        text = self.path.read_text() if self.path.exists() else ""
        cards = re.findall(r"^### REF-[^\n]+\n(.*?)(?=^### REF-|\Z)", text, re.M | re.S)
        self.assertGreaterEqual(len(cards), 12)
        for card in cards:
            self.assertIn("**KEEP:**", card)
            self.assertIn("**AVOID:**", card)
            self.assertIn("**WHY:**", card)
            self.assertRegex(card, r"\*\*Source:\*\* https?://")

    def test_at_least_eight_cards_have_external_visual_previews(self):
        text = self.path.read_text() if self.path.exists() else ""
        previews = re.findall(r"!\[[^\]]*\]\(https?://[^)]+\)", text)
        self.assertGreaterEqual(len(previews), 8)

    def test_references_page_links_moodboard(self):
        text = (ROOT / "docs" / "references.md").read_text()
        self.assertIn("moodboard.md", text)


if __name__ == "__main__":
    unittest.main()
