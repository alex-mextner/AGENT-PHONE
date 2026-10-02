import math
import unittest
from blender import design_geometry as geometry


class RoundedOutlineTests(unittest.TestCase):
    def test_rounded_outline_is_a_real_exact_size_perimeter(self):
        self.assertTrue(hasattr(geometry, 'rounded_outline'))
        points = geometry.rounded_outline(44, 92, 5, segments=12)
        self.assertGreaterEqual(len(points), 48)
        self.assertEqual(len(points), len(set(points)))
        for axis, extent in ((0, 44), (1, 92)):
            self.assertAlmostEqual(max(p[axis] for p in points) - min(p[axis] for p in points), extent)
        area = sum(a[0]*b[1] - b[0]*a[1] for a, b in zip(points, points[1:] + points[:1])) / 2
        self.assertGreater(area, 44*92 - 100)
        self.assertLess(area, 44*92)

    def test_invalid_dimensions_are_rejected(self):
        self.assertTrue(hasattr(geometry, 'rounded_outline'))
        for args in ((0, 92, 5), (44, -1, 5), (44, 92, 23), (44, 92, float('nan'))):
            with self.assertRaises(ValueError):
                geometry.rounded_outline(*args)


if __name__ == '__main__':
    unittest.main()
