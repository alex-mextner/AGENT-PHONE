"""Blender-runtime contract for the v3 along-arm product geometry."""

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from blender.scene_builder import build_product_scene, reset_scene


def mm_dims(obj):
    return tuple(round(v * 1000.0, 1) for v in obj.dimensions)


reset_scene()
built = build_product_scene(
    tilt_deg=0,
    texture="home",
    include_wrist_proxy=True,
    watch_reference=True,
)
objects = built["objects"]

assert mm_dims(objects["display_frame"]) == (44.0, 92.0, 5.7), mm_dims(objects["display_frame"])
assert built["metadata"]["screen_long_axis"] == "along_arm"
assert built["metadata"]["underside_gap_mm"] >= 48.0

watch_bodies = [
    obj for obj in objects.values()
    if obj.name.startswith("Apple Watch Ultra size reference")
]
assert len(watch_bodies) == 1, [obj.name for obj in watch_bodies]

ui = objects["ui"]
assert math.isclose(abs(ui.rotation_euler.z), math.pi / 2, abs_tol=1e-4), tuple(ui.rotation_euler)

left = objects["cuff_left"]
right = objects["cuff_right"]
assert 0.026 <= left.dimensions.y <= 0.030, tuple(left.dimensions)
assert 0.026 <= right.dimensions.y <= 0.030, tuple(right.dimensions)
assert all(poly.use_smooth for poly in left.data.polygons)
assert all(poly.use_smooth for poly in right.data.polygons)
base = objects["base"]
base_bottom = base.location.z - base.dimensions.z/2
base_top = base.location.z + base.dimensions.z/2
for cuff in (left, right):
    roots = [cuff.matrix_world @ v.co for v in list(cuff.data.vertices)[:4]]
    assert all(base_bottom <= v.z <= base_top for v in roots), (cuff.name, [v.z for v in roots], base_bottom, base_top)
    assert all(abs(v.x) < base.dimensions.x/2 for v in roots), cuff.name

carrier = objects["carrier"]
pivot = built["pivot"]
carrier_rear_y = carrier.location.y - carrier.dimensions.y / 2
assert abs(pivot.location.y - carrier_rear_y) <= 0.0015, (pivot.location.y, carrier_rear_y)

frame = objects["display_frame"]
assert abs(frame.matrix_world.translation.y) <= 0.0015, tuple(frame.matrix_world.translation)

print("geometry-runtime: PASS", mm_dims(objects["display_frame"]), built["metadata"])
