"""Minimal physical props that make lifestyle renders read as real scenarios."""

import math

import bpy
from mathutils import Vector

from blender.scene_builder import material, rounded_box, cylinder


def _emissive(name, color, strength=1.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = strength
    return mat


def _tv():
    shell = material("Context TV shell", (0.015, 0.018, 0.023), metallic=0.35, roughness=0.28)
    screen = _emissive("Context TV screen", (0.025, 0.10, 0.16), 1.2)
    wall_mat = material("Context wall plaster", (0.16, 0.17, 0.18), roughness=0.82)
    console_mat = material("Media console wood", (0.11, 0.065, 0.035), roughness=0.48)
    wall = rounded_box(
        "Context Wall", (0.0, 0.265, 0.115), (0.52, 0.012, 0.34), wall_mat, bevel=0.004
    )
    console = rounded_box(
        "Media Console", (0.0, 0.225, 0.010), (0.31, 0.070, 0.060), console_mat, bevel=0.008
    )
    body = rounded_box(
        "Context TV", (0.0, 0.240, 0.155), (0.185, 0.009, 0.104), shell, bevel=0.006
    )
    panel = rounded_box(
        "Context TV Screen", (0.0, 0.2345, 0.155), (0.175, 0.0012, 0.094), screen, bevel=0.004
    )
    return [wall, console, body, panel]


def _light():
    metal = material("Context light shell", (0.13, 0.14, 0.16), metallic=0.65, roughness=0.28)
    glow = _emissive("Context light glow", (1.0, 0.62, 0.22), 2.0)
    stem = cylinder("Context Light", (-0.115, 0.105, 0.032), 0.008, 0.090, metal, axis="Z")
    bulb = cylinder("Context Light Glow", (-0.115, 0.105, 0.079), 0.018, 0.022, glow, axis="Z")
    return [stem, bulb]


RING_MINOR_RADIUS = 0.00125
RING_SKIN_CLEARANCE = 0.0004
RING_SEGMENT_FRACTION = 0.6
_SECTION_SLAB = 0.0015
_SECTION_RADII = (0.016, 0.014, 0.013, 0.012, 0.012, 0.012)


def _finger_section(skin, center, direction):
    """Fit centre and max radius of the finger cross-section at `center`.

    Uses the evaluated skin vertices in a thin slab normal to the finger axis,
    iteratively re-centred so neighbouring fingers drop out of the sample.
    """
    evaluated = skin.evaluated_get(bpy.context.evaluated_depsgraph_get())
    world = [evaluated.matrix_world @ v.co for v in evaluated.data.vertices]
    section = [v - direction * (v - center).dot(direction)
               for v in world if abs((v - center).dot(direction)) < _SECTION_SLAB]
    middle = center.copy()
    near = section
    for radius in _SECTION_RADII:
        near = [s for s in section if (s - middle).length < radius]
        if not near:
            raise ValueError("no skin found where the ring should sit")
        middle = sum(near, Vector()) / len(near)
    return middle, max((s - middle).length for s in near)


def _ring(anchors, skin=None):
    if not anchors or "ring_proximal" not in anchors or "ring_middle" not in anchors:
        raise ValueError("ring-room context requires MakeHuman ring-finger anchors")

    metal = material("Agent Ring metal", (0.045, 0.055, 0.068), metallic=0.85, roughness=0.22)
    proximal = Vector(anchors["ring_proximal"])
    middle = Vector(anchors["ring_middle"])
    direction = (middle - proximal).normalized()
    center = proximal.lerp(middle, RING_SEGMENT_FRACTION)
    major = 0.0084
    if skin is not None:
        center, skin_radius = _finger_section(skin, center, direction)
        major = skin_radius + RING_SKIN_CLEARANCE + RING_MINOR_RADIUS

    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=RING_MINOR_RADIUS,
        major_segments=72,
        minor_segments=20,
        location=center,
    )
    ring = bpy.context.object
    ring.name = "Agent Ring"
    ring.rotation_euler = Vector((0, 0, 1)).rotation_difference(direction).to_euler()
    ring.data.materials.append(metal)
    for polygon in ring.data.polygons:
        polygon.use_smooth = True
    return [ring]


def _glasses():
    """Lay the companion glasses on the desk instead of floating in mid-air."""

    frame = material("Agent Glasses frame", (0.018, 0.022, 0.028), metallic=0.55, roughness=0.24)
    lens = material("Agent Glasses lens", (0.035, 0.065, 0.075), metallic=0.05, roughness=0.10)
    objects = []
    for name, x in (("Agent Glasses Left Lens", 0.064), ("Agent Glasses Right Lens", 0.128)):
        outer = rounded_box(name, (x, 0.112, -0.0315), (0.059, 0.040, 0.0035), frame, bevel=0.010)
        inner = rounded_box(name + " Glass", (x, 0.112, -0.0298), (0.052, 0.033, 0.0010), lens, bevel=0.009)
        objects.extend((outer, inner))
    bridge = rounded_box(
        "Agent Glasses Bridge", (0.096, 0.112, -0.0310), (0.020, 0.006, 0.0035), frame, bevel=0.002
    )
    objects.append(bridge)
    audio = material("Bone conduction audio", (0.03, 0.04, 0.05), metallic=0.45, roughness=0.28)
    left_audio = rounded_box(
        "Bone Conduction Left", (0.026, 0.133, -0.029), (0.018, 0.012, 0.006), audio, bevel=0.004
    )
    right_audio = rounded_box(
        "Bone Conduction Right", (0.166, 0.133, -0.029), (0.018, 0.012, 0.006), audio, bevel=0.004
    )
    objects.extend((left_audio, right_audio))
    return objects


def _camera_tile():
    """A detachable camera tile resting next to the user's hand."""

    shell = material("Agent Camera shell", (0.055, 0.061, 0.072), metallic=0.72, roughness=0.25)
    glass = material("Agent Camera lens glass", (0.004, 0.010, 0.018), metallic=0.08, roughness=0.08)
    tile = rounded_box(
        "Agent Camera Tile", (0.112, 0.085, -0.0305), (0.038, 0.028, 0.008), shell, bevel=0.006
    )
    lens = cylinder("Agent Camera Lens", (0.112, 0.085, -0.025), 0.008, 0.004, glass, axis="Z")
    return [tile, lens]


def _desk_laptop():
    deskmat = material("Desk material", (0.12, 0.085, 0.055), roughness=0.62)
    laptop = material("Laptop aluminum", (0.16, 0.17, 0.18), metallic=0.78, roughness=0.25)
    desk = rounded_box("Desk", (0, 0, -0.050), (0.42, 0.42, 0.018), deskmat, bevel=0.004)
    base = rounded_box("Laptop Base", (-0.215, 0.080, -0.032), (0.245, 0.170, 0.010), laptop, bevel=0.006)
    return [desk, base]


def _dive_clasp():
    metal = material("Dive clasp metal", (0.07, 0.08, 0.09), metallic=0.82, roughness=0.24)
    accent = material("Dive latch accent", (0.08, 0.22, 0.34), metallic=0.65, roughness=0.24)
    clasp = rounded_box("Dive Clasp", (0, 0, -0.027), (0.040, 0.032, 0.0045), metal, bevel=0.003)
    left = rounded_box("Dive Clasp Left Latch", (-0.036, 0, -0.005), (0.009, 0.030, 0.022), accent, bevel=0.003)
    right = rounded_box("Dive Clasp Right Latch", (0.036, 0, -0.005), (0.009, 0.030, 0.022), accent, bevel=0.003)
    return [clasp, left, right]


def _external_battery():
    """Optional endurance pack resting on the dorsal forearm with a flat lead."""

    shell = material("External battery shell", (0.045, 0.050, 0.060), metallic=0.52, roughness=0.30)
    accent = material("External battery accent", (0.12, 0.28, 0.40), metallic=0.25, roughness=0.30)
    pack = rounded_box(
        "External Battery Pack", (0.0, -0.108, 0.031), (0.045, 0.070, 0.012), shell, bevel=0.008
    )
    ribbon = rounded_box(
        "Flat Power Ribbon", (0.0, -0.045, 0.026), (0.007, 0.078, 0.0018), accent, bevel=0.001
    )
    return [pack, ribbon]


def _car_hud():
    glass = material("Car windshield glass", (0.025, 0.050, 0.070), metallic=0.02, roughness=0.10)
    hud = _emissive("Car HUD cyan", (0.05, 0.80, 1.0), 2.2)
    windshield = rounded_box("Car Windshield", (0.0, 0.165, 0.130), (0.235, 0.005, 0.110), glass, bevel=0.010)
    route = rounded_box("Car HUD Route", (0.008, 0.1615, 0.135), (0.105, 0.0012, 0.006), hud, bevel=0.003)
    speed = rounded_box("Car HUD Speed", (-0.070, 0.1613, 0.165), (0.030, 0.0012, 0.018), hud, bevel=0.004)
    arrow = rounded_box("Car HUD Arrow", (0.064, 0.1611, 0.150), (0.022, 0.0012, 0.022), hud, bevel=0.004)
    return [windshield, route, speed, arrow]


def add_context(kind, anchors=None, skin=None):
    if kind is None:
        return []
    if kind == "tv":
        return _tv()
    if kind == "ring-room":
        return _ring(anchors, skin) + _tv() + _light()
    if kind == "glasses":
        return _glasses()
    if kind == "camera-tile":
        return _camera_tile()
    if kind == "desk-laptop":
        return _desk_laptop()
    if kind == "dive-clasp":
        return _dive_clasp()
    if kind == "external-battery":
        return _external_battery()
    if kind == "car-hud":
        return _car_hud()
    raise ValueError(f"Unknown render context: {kind}")
