"""Render a photorealistic-human proof for manual inspection."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bpy
from mathutils import Vector

from blender.human_asset import load_makehuman_wrist
from blender.scene_builder import build_product_scene, reset_scene
from blender.screen_concept import setup_world, setup_lighting


def look_at(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


reset_scene()
human = load_makehuman_wrist(profile="average", side="right")
# Place the watch slightly proximal to the anatomical wrist crease, as a real
# watch sits toward the elbow rather than directly on the hand joint.
human["object"].location.y += 0.055
built = build_product_scene(
    tilt_deg=22,
    texture="home",
    include_wrist_proxy=False,
    wrist_profile="average",
)
setup_world()
setup_lighting()

# Camera stays close enough that the rest of the body is naturally outside frame.
bpy.ops.object.camera_add(location=(0.135, -0.165, 0.095))
camera = bpy.context.object
camera.data.lens = 78
look_at(camera, (0.0, -0.008, 0.026))
bpy.context.scene.camera = camera

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(ROOT / "renders" / "previews" / "human-proof.png")
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.film_transparent = False
bpy.ops.render.render(write_still=True)
print("HUMAN_PROOF", scene.render.filepath)
