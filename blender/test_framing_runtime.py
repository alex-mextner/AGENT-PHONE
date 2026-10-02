"""Camera regression: the real product and finger landmarks must stay in frame."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from blender import screen_concept as renderer
from blender.scene_builder import reset_scene
assert hasattr(renderer, 'fit_scene_camera'), 'geometry-aware framing is missing'
for name in ('scale-comparison','tilt-55','home-status','ring-spatial','desk-clearance'):
    reset_scene()
    built, _ = renderer.build_scene(name)
    scene = renderer.configure_render(True)
    renderer.fit_scene_camera(built)
    bpy.context.view_layer.update()
    points = [obj.matrix_world @ Vector(c) for obj in built['objects'].values() for c in obj.bound_box]
    if built['human']:
        points += [built['human']['anchors_world']['index_tip']]
    projected = [world_to_camera_view(scene, scene.camera, p) for p in points]
    bounds = (min(p.x for p in projected),max(p.x for p in projected),min(p.y for p in projected),max(p.y for p in projected))
    assert bounds[0] >= .039 and bounds[1] <= .961 and bounds[2] >= .039 and bounds[3] <= .961, (name,bounds)
    assert all(p.z > 0 for p in projected), name
    print('camera-frame:',name,[round(v,3) for v in bounds])
print('framing-runtime: PASS')
