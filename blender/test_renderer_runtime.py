"""Blender-runtime regression check for renderer configuration."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bpy
from blender.screen_concept import configure_render

scene = configure_render(preview=True)
assert scene.render.engine == "BLENDER_EEVEE", scene.render.engine
assert (scene.render.resolution_x, scene.render.resolution_y) == (1000, 760)
print("renderer-runtime: PASS")
