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

reset_scene()
hero = create_camera("hero")
assert hero.location.y < -0.10, tuple(hero.location)
reset_scene()
context = create_camera("context")
assert context.location.y < -0.08, tuple(context.location)
reset_scene()
top = create_camera("top-ortho")
assert top.data.ortho_scale >= 0.20, top.data.ortho_scale
labels = add_scale_annotations()
for label in labels:
    mat = label.data.materials[0]
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    assert bsdf.inputs["Emission Strength"].default_value >= 1.0, label.name
print("renderer-runtime: PASS")
