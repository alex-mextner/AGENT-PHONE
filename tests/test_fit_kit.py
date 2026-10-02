import importlib
import tempfile
import unittest
from collections import Counter
from pathlib import Path


class FitKitTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('blender.fit_kit'))
        return importlib.import_module('blender.fit_kit')

    def test_dummy_meshes_are_exact_size_closed_and_non_degenerate(self):
        kit = self.module()
        for height in (6.6, 10.0, 14.0):
            vertices, faces = kit.dummy_mesh(height)
            extents = [max(v[i] for v in vertices)-min(v[i] for v in vertices) for i in range(3)]
            self.assertEqual(extents, [92.0, 44.0, height])
            edges = Counter(tuple(sorted((f[i],f[(i+1)%3]))) for f in faces for i in range(3))
            self.assertTrue(all(n == 2 for n in edges.values()))
            self.assertTrue(all(kit.triangle_area(vertices, f) > 0 for f in faces))

    def test_kit_contains_print_scale_and_empty_not_fabricated_diary(self):
        with tempfile.TemporaryDirectory() as folder:
            self.module().generate_kit(Path(folder))
            self.assertEqual(len(list(Path(folder).glob('*.stl'))), 4)
            self.assertIn('mm', (Path(folder)/'template-1to1.svg').read_text())
            self.assertEqual(len((Path(folder)/'wear-diary.csv').read_text().splitlines()), 1)
