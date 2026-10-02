"""Physical placement checks for illustrative on-hand scenes, not comfort proof."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bpy
from mathutils import Vector
from blender.human_asset import joint_centers
from blender.scene_builder import reset_scene
from blender.screen_concept import build_scene

for name in ('home-status', 'ring-spatial', 'desk-clearance'):
    reset_scene()
    built, _ = build_scene(name)
    bpy.context.view_layer.update()
    human = built['human']['object']
    wrist = human.matrix_world @ Vector(joint_centers('right')['wrist'])
    assert wrist.y >= 0.052, (name, 'module extends beyond wrist crease', tuple(wrist))
    evaluated = human.evaluated_get(bpy.context.evaluated_depsgraph_get())
    hand = [evaluated.matrix_world @ v.co for v in evaluated.data.vertices]
    hand = [v for v in hand if wrist.y+0.035 < v.y < wrist.y+0.21 and abs(v.x) < 0.10 and abs(v.z) < 0.14]
    assert len(hand) > 100, (name, len(hand))
    floor = bpy.data.objects.get('Studio floor') or bpy.data.objects.get('Desk')
    top = max((floor.matrix_world @ Vector(c)).z for c in floor.bound_box)
    assert min(v.z for v in hand) >= top-0.0003, (name, 'hand intersects floor', min(v.z for v in hand), top)
    print('hand-fit:', name, 'wrist_mm', wrist.y*1000, 'table_clearance_mm', (min(v.z for v in hand)-top)*1000)
print('hand-fit-runtime: PASS')
