"""Render the measured AGENT-PHONE concept.

Examples:
  Blender --background --python blender/screen_concept.py -- --preview --technical-only
  Blender --background --python blender/screen_concept.py -- --preview --scene scale-comparison
"""

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from blender.framing import fit_scene_camera
from blender.context_props import add_context
from blender.human_asset import load_makehuman_wrist
from blender.render_plan import RENDER_PLAN
from blender.scene_manifest import SCENES
from blender.scene_builder import (
    build_product_scene,
    material,
    reset_scene,
    rounded_box,
)

OUT = ROOT / "renders"
PREVIEW_OUT = OUT / "previews"


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--technical-only", action="store_true")
    parser.add_argument("--scene")
    parser.add_argument("--save-blend", action="store_true")
    return parser.parse_args(argv)


def look_at(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


def setup_world():
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.16, 0.18, 0.21, 1)
    bg.inputs["Strength"].default_value = 0.5


def add_area(name, location, energy, size, color, target=(0, 0, 0.025)):
    bpy.ops.object.light_add(type="AREA", location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = energy
    light.data.shape = "DISK"
    light.data.size = size
    light.data.color = color
    look_at(light, target)
    return light


def setup_lighting():
    add_area("Key", (0.20, 0.25, 0.35), 7.0, 0.32, (1.0, 0.94, 0.87))
    add_area("Fill", (-0.20, -0.10, 0.18), 2.0, 0.24, (0.83, 0.90, 1.0))
    add_area("Rim", (0.15, -0.20, 0.32), 5.0, 0.28, (0.88, 0.93, 1.0))


def setup_ground():
    ground_mat = material("Studio floor", (0.19, 0.20, 0.22), roughness=0.7)
    return rounded_box(
        "Studio floor",
        (0, 0, -0.038),
        (0.34, 0.40, 0.006),
        ground_mat,
        bevel=0.006,
    )


def create_camera(camera_kind):
    if camera_kind == "top-ortho":
        location, target, lens = (0, -0.020, 0.24), (0, -0.020, 0.025), 70
        ortho_scale = 0.230
    elif camera_kind == "tilt-tech":
        location, target, lens = (0.27, -0.27, 0.18), (0, 0.006, 0.020), 68
        ortho_scale = None
    elif camera_kind == "underside-wide":
        location, target, lens = (0.20, -0.20, -0.18), (0, 0, 0.006), 72
        ortho_scale = None
    elif camera_kind == "exploded":
        location, target, lens = (0.19, 0.22, 0.20), (0, 0.005, 0.055), 70
        ortho_scale = None
    elif camera_kind == "desk":
        location, target, lens = (0.19, -0.14, 0.075), (0, -0.005, 0.010), 72
        ortho_scale = None
    elif camera_kind == "context":
        location, target, lens = (0.33, -0.38, 0.22), (0, 0.095, 0.060), 55
        ortho_scale = None
    else:
        location, target, lens = (0.24, -0.29, 0.16), (0, 0.012, 0.030), 68
        ortho_scale = None

    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    camera.name = f"Camera {camera_kind}"
    camera.data.lens = lens
    if ortho_scale:
        camera.data.type = "ORTHO"
        camera.data.ortho_scale = ortho_scale
    look_at(camera, target)
    bpy.context.scene.camera = camera
    return camera


def add_label(text, location, size=0.0055, align="CENTER"):
    bpy.ops.object.text_add(location=location)
    obj = bpy.context.object
    obj.name = "Scale label"
    obj.data.body = text
    obj.data.align_x = align
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.00005
    label_mat = material("Label", (0.82, 0.86, 0.92), roughness=0.32)
    bsdf = label_mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Emission Color"].default_value = (0.82, 0.86, 0.92, 1.0)
    bsdf.inputs["Emission Strength"].default_value = 4.0
    obj.data.materials.append(label_mat)
    return obj


def add_scale_annotations():
    # Top-orthographic labels lie flat in XY, facing +Z by default.
    device = add_label("AGENT-PHONE   92 × 44 mm", (0.020, 0.064, 0.080), size=0.0052)
    watch = add_label("WATCH ULTRA   49 × 44 mm", (-0.064, -0.034, 0.080), size=0.0046)
    return device, watch


def build_scene(name):
    manifest = SCENES[name]
    plan = RENDER_PLAN[name]
    technical = plan["camera"] in {"top-ortho", "tilt-tech", "underside-wide", "exploded"} or name == "detached-module"

    human_profile = plan.get("human_profile")
    human = None
    if human_profile:
        human = load_makehuman_wrist(profile=human_profile, side="right")
        offset_y = plan.get("human_offset_y_mm", 55.0) / 1000.0
        human["object"].location.y += offset_y
        for anchor in human["anchors_world"].values():
            anchor.y += offset_y

    built = build_product_scene(
        tilt_deg=manifest.get("tilt_deg", 18),
        texture=manifest.get("texture"),
        include_wrist_proxy=plan.get("wrist_proxy", True),
        wrist_profile=human_profile or "average",
        watch_reference=plan.get("watch_reference", False),
        exploded=(name == "mechanism-exploded"),
        detached=(name == "detached-module"),
    )
    built["human"] = human
    anchors = human["anchors_world"] if human else None
    built["context_objects"] = add_context(plan.get("context"), anchors=anchors, skin=human["object"] if human else None)

    setup_world()
    setup_lighting()
    if plan.get("ground", True):
        setup_ground()
    create_camera(plan["camera"])
    if name == "scale-comparison":
        add_scale_annotations()
    return built, technical


def configure_render(preview):
    scene = bpy.context.scene
    res = (1000, 760) if preview else (1800, 1368)
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.compression = 32
    scene.render.use_file_extension = True
    if preview:
        scene.render.engine = "BLENDER_EEVEE"
    else:
        scene.render.engine = "CYCLES"
        scene.cycles.samples = 64
        scene.cycles.use_denoising = True
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = -0.35
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "MILLIMETERS"
    return scene


def render_one(name, preview=True):
    reset_scene()
    built, _ = build_scene(name)
    scene = configure_render(preview)
    fit_scene_camera(built)
    directory = PREVIEW_OUT if preview else OUT
    if preview:
        directory = PREVIEW_OUT / ("technical" if SCENES[name]["render_kind"] == "technical" else "lifestyle")
    directory.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(directory / f"{name}.png")
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {name}: {scene.render.filepath}")
    return scene.render.filepath


def main():
    args = parse_args()
    if args.scene:
        names = [args.scene]
    elif args.technical_only:
        names = [name for name, spec in SCENES.items() if spec["render_kind"] == "technical"]
    else:
        names = list(RENDER_PLAN)

    for name in names:
        if name not in RENDER_PLAN:
            raise SystemExit(f"Unknown render scene: {name}")
        render_one(name, preview=args.preview)

    if args.save_blend:
        # Keep the device/hand master inspectable with textures packed, not a
        # checkpoint of whichever companion happened to render last.
        reset_scene()
        built, _ = build_scene("home-status")
        configure_render(False)
        fit_scene_camera(built)
        bpy.ops.file.pack_all()
        path = OUT / "agent-phone-concept.blend"
        bpy.ops.wm.save_as_mainfile(filepath=str(path), compress=True)
        print(f"SAVED {path}")


if __name__ == "__main__":
    main()
