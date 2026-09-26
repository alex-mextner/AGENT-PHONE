"""Minimal physical props that make lifestyle renders read as real scenarios."""

import math

import bpy

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
    body = rounded_box(
        "Context TV", (0.0, 0.125, 0.125), (0.16, 0.009, 0.088), shell, bevel=0.006
    )
    panel = rounded_box(
        "Context TV Screen", (0.0, 0.1195, 0.125), (0.150, 0.0012, 0.078), screen, bevel=0.004
    )
    return [body, panel]


def _light():
    metal = material("Context light shell", (0.13, 0.14, 0.16), metallic=0.65, roughness=0.28)
    glow = _emissive("Context light glow", (1.0, 0.62, 0.22), 2.0)
    stem = cylinder("Context Light", (-0.115, 0.105, 0.032), 0.008, 0.090, metal, axis="Z")
    bulb = cylinder("Context Light Glow", (-0.115, 0.105, 0.079), 0.018, 0.022, glow, axis="Z")
    return [stem, bulb]


def _ring():
    metal = material("Agent Ring metal", (0.045, 0.055, 0.068), metallic=0.85, roughness=0.22)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.0135,
        minor_radius=0.0024,
        major_segments=64,
        minor_segments=18,
        location=(0.105, 0.055, 0.082),
        rotation=(math.radians(72), 0, math.radians(18)),
    )
    ring = bpy.context.object
    ring.name = "Agent Ring"
    ring.data.materials.append(metal)
    return [ring]


def _glasses():
    frame = material("Agent Glasses frame", (0.018, 0.022, 0.028), metallic=0.55, roughness=0.24)
    lens = material("Agent Glasses lens", (0.035, 0.065, 0.075), metallic=0.05, roughness=0.10)
    objects = []
    for name, x in (("Agent Glasses Left Lens", -0.121), ("Agent Glasses Right Lens", -0.049)):
        outer = rounded_box(name, (x, 0.110, 0.105), (0.059, 0.0035, 0.040), frame, bevel=0.010)
        inner = rounded_box(name + " Glass", (x, 0.1077, 0.105), (0.052, 0.0010, 0.033), lens, bevel=0.009)
        objects.extend((outer, inner))
    bridge = rounded_box("Agent Glasses Bridge", (-0.085, 0.109, 0.106), (0.020, 0.0035, 0.006), frame, bevel=0.002)
    objects.append(bridge)
    audio = material("Bone conduction audio", (0.03, 0.04, 0.05), metallic=0.45, roughness=0.28)
    left_audio = rounded_box("Bone Conduction Left", (-0.158, 0.102, 0.091), (0.018, 0.008, 0.014), audio, bevel=0.004)
    right_audio = rounded_box("Bone Conduction Right", (-0.012, 0.102, 0.091), (0.018, 0.008, 0.014), audio, bevel=0.004)
    objects.extend((left_audio, right_audio))
    return objects


def _camera_tile():
    shell = material("Agent Camera shell", (0.055, 0.061, 0.072), metallic=0.72, roughness=0.25)
    glass = material("Agent Camera lens glass", (0.004, 0.010, 0.018), metallic=0.08, roughness=0.08)
    tile = rounded_box("Agent Camera Tile", (0.105, 0.070, 0.072), (0.038, 0.028, 0.008), shell, bevel=0.006)
    lens = cylinder("Agent Camera Lens", (0.105, 0.0555, 0.072), 0.008, 0.004, glass, axis="Y")
    return [tile, lens]


def _desk_laptop():
    deskmat = material("Desk material", (0.12, 0.085, 0.055), roughness=0.62)
    laptop = material("Laptop aluminum", (0.16, 0.17, 0.18), metallic=0.78, roughness=0.25)
    desk = rounded_box("Desk", (0, 0, -0.050), (0.42, 0.42, 0.018), deskmat, bevel=0.004)
    base = rounded_box("Laptop Base", (0, 0.080, -0.032), (0.245, 0.170, 0.010), laptop, bevel=0.006)
    return [desk, base]


def _dive_clasp():
    metal = material("Dive clasp metal", (0.07, 0.08, 0.09), metallic=0.82, roughness=0.24)
    accent = material("Dive latch accent", (0.08, 0.22, 0.34), metallic=0.65, roughness=0.24)
    clasp = rounded_box("Dive Clasp", (0, 0, -0.032), (0.040, 0.032, 0.0045), metal, bevel=0.003)
    left = rounded_box("Dive Clasp Left Latch", (-0.036, 0, -0.010), (0.009, 0.030, 0.022), accent, bevel=0.003)
    right = rounded_box("Dive Clasp Right Latch", (0.036, 0, -0.010), (0.009, 0.030, 0.022), accent, bevel=0.003)
    return [clasp, left, right]


def _external_battery():
    shell = material("External battery shell", (0.045, 0.050, 0.060), metallic=0.52, roughness=0.30)
    accent = material("External battery accent", (0.12, 0.28, 0.40), metallic=0.25, roughness=0.30)
    pack = rounded_box("External Battery Pack", (-0.135, 0.095, 0.070), (0.070, 0.045, 0.012), shell, bevel=0.008)
    ribbon = rounded_box("Flat Power Ribbon", (-0.072, 0.038, 0.054), (0.090, 0.006, 0.0018), accent, bevel=0.001)
    return [pack, ribbon]


def _car_hud():
    glass = material("Car windshield glass", (0.025, 0.050, 0.070), metallic=0.02, roughness=0.10)
    hud = _emissive("Car HUD cyan", (0.05, 0.80, 1.0), 2.2)
    windshield = rounded_box("Car Windshield", (0.0, 0.165, 0.130), (0.235, 0.005, 0.110), glass, bevel=0.010)
    route = rounded_box("Car HUD Route", (0.008, 0.1615, 0.135), (0.105, 0.0012, 0.006), hud, bevel=0.003)
    speed = rounded_box("Car HUD Speed", (-0.070, 0.1613, 0.165), (0.030, 0.0012, 0.018), hud, bevel=0.004)
    arrow = rounded_box("Car HUD Arrow", (0.064, 0.1611, 0.150), (0.022, 0.0012, 0.022), hud, bevel=0.004)
    return [windshield, route, speed, arrow]


def add_context(kind):
    if kind is None:
        return []
    if kind == "tv":
        return _tv()
    if kind == "ring-room":
        return _ring() + _tv() + _light()
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
