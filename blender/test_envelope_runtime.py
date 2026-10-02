"""Check evaluated module surfaces rather than trusting declared dimensions."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bpy
from blender.scene_builder import build_product_scene, reset_scene


def points(obj):
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return [evaluated.matrix_world @ v.co for v in evaluated.data.vertices]


reset_scene()
built = build_product_scene(tilt_deg=0, texture='home')
bpy.context.view_layer.update()
parts = [built['objects'][key] for key in ('display_frame', 'glass', 'ui')]
vertices = [v for obj in parts for v in points(obj)]
extents = [1000*(max(v[i] for v in vertices)-min(v[i] for v in vertices)) for i in range(3)]
assert all(abs(a-b) < 0.02 for a,b in zip(extents, (44,92,6.6))), extents
for key in ('display_frame', 'glass', 'ui'):
    obj = built['objects'][key]
    assert len(obj.data.vertices) >= 48, (key, len(obj.data.vertices))
print('evaluated-envelope: PASS', extents)
