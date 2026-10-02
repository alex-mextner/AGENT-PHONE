"""Blender-runtime regression check for renderer configuration."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bpy
from blender.scene_builder import reset_scene
from blender.screen_concept import configure_render, create_camera, add_scale_annotations

scene = configure_render(preview=True)
assert scene.render.engine == "BLENDER_EEVEE", scene.render.engine
assert (scene.render.resolution_x, scene.render.resolution_y) == (1000, 760)

final_scene = configure_render(preview=False)
assert final_scene.render.engine == "CYCLES", final_scene.render.engine
assert final_scene.cycles.samples >= 64, final_scene.cycles.samples
assert final_scene.cycles.use_denoising
assert (final_scene.render.resolution_x, final_scene.render.resolution_y) == (1800, 1368)

reset_scene()
hero = create_camera("hero")
assert hero.location.y < -0.24, tuple(hero.location)
assert hero.location.length > 0.34, tuple(hero.location)
assert hero.data.lens <= 72
reset_scene()
context = create_camera("context")
assert context.location.y < -0.30, tuple(context.location)
assert context.location.length > 0.45, tuple(context.location)
assert context.data.lens <= 58
reset_scene()
tilt = create_camera("tilt-tech")
assert tilt.location.length > 0.35, tuple(tilt.location)
assert tilt.data.lens <= 72
reset_scene()
top = create_camera("top-ortho")
assert top.data.ortho_scale >= 0.20, top.data.ortho_scale
labels = add_scale_annotations()
for label in labels:
    mat = label.data.materials[0]
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    assert bsdf.inputs["Emission Strength"].default_value >= 1.0, label.name
print("renderer-runtime: PASS")
