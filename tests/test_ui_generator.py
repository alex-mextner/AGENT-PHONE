from pathlib import Path
import tempfile
import unittest

from PIL import Image

import blender.generate_ui as ui


class UIGeneratorTests(unittest.TestCase):
    def test_required_texture_set_and_canvas_size(self):
        required = {
            "home", "chat", "marketplace", "split", "remote",
            "blind-input", "research", "handoff", "navigation", "camera",
        }
        self.assertEqual(set(ui.REQUIRED_TEXTURES), required)
        self.assertEqual(ui.CANVAS_SIZE, (1400, 660))

    def test_generate_all_creates_every_texture(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            ui.generate_all(out)
            for name in ui.REQUIRED_TEXTURES:
                path = out / f"{name}.png"
                self.assertTrue(path.exists(), name)
                with Image.open(path) as image:
                    self.assertEqual(image.size, ui.CANVAS_SIZE)

    def test_chat_is_two_pane_not_single_empty_thread(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            ui.generate_all(out)
            im = Image.open(out / "chat.png").convert("RGB")
            # Divider between compact chat list and open thread.
            self.assertGreater(sum(im.getpixel((430, 220))) // 3, 30)
            # A selected-chat card in the left pane and message bubble in right.
            self.assertGreater(sum(im.getpixel((220, 220))) // 3, 15)
            self.assertGreater(sum(im.getpixel((960, 350))) // 3, 18)

    def test_blind_input_keeps_at_least_92_percent_pixels_near_black(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            ui.generate_all(out)
            im = Image.open(out / "blind-input.png").convert("RGB")
            pixels = list(im.get_flattened_data())
            near_black = sum(1 for r, g, b in pixels if max(r, g, b) < 24)
            self.assertGreaterEqual(near_black / len(pixels), 0.92)


if __name__ == "__main__":
    unittest.main()
