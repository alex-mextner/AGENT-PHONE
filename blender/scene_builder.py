"""Blender geometry builder for the measured AGENT-PHONE concept."""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from blender.design_geometry import (
    BASE_THICKNESS_MM,
    BASE_FOOTPRINT_MM,
    CARRIER_FOOTPRINT_MM,
    CARRIER_THICKNESS_MM,
    CUFF_GAP_MM,
    CUFF_PLATE_THICKNESS_MM,
    CUFF_PLATE_WIDTH_MM,
    DISPLAY_ACTIVE_MM,
    DISPLAY_OUTER_MM,
    GLASS_THICKNESS_MM,
    HINGE_PIN_DIAMETER_MM,
    SCREEN_LONG_AXIS,
    WATCH_ULTRA_MM,
    WRIST_MODEL_MM,
)

UI_DIR = ROOT / "blender" / "ui"


def mm(value):
    return float(value) / 1000.0


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.images):
        # Keep linked datablocks only when another object really owns them.
        for block in list(collection):
            if getattr(block, "users", 0) == 0:
                collection.remove(block)


def material(name, color, metallic=0.0, roughness=0.45):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def rounded_box(name, location, dimensions, mat, bevel=0.002):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = obj.modifiers.new("edge radius", "BEVEL")
    mod.width = min(bevel, min(dimensions) / 2.2)
    mod.segments = 6
    obj.data.materials.append(mat)
    return obj


def cylinder(name, location, radius, depth, mat, axis="X"):
    rotation = (0, math.pi / 2, 0) if axis == "X" else ((math.pi / 2, 0, 0) if axis == "Y" else (0, 0, 0))
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=48,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def cuff_segment(name, side, wrist_width_mm, wrist_thickness_mm, mat, steps=32):
    """Create one curved battery plate around a wrist ellipse.

    Angle zero is the top of the wrist. Positive angles descend the right
    side; negative angles descend the left. Both stop before the underside.
    """

    clearance = 1.8
    inner_rx = mm(wrist_width_mm / 2 + clearance)
    inner_rz = mm(wrist_thickness_mm / 2 + clearance)
    thickness = mm(CUFF_PLATE_THICKNESS_MM)
    outer_rx = inner_rx + thickness
    outer_rz = inner_rz + thickness
    y_half = mm(CUFF_PLATE_WIDTH_MM / 2)

    start = math.radians(20 * side)
    end = math.radians(145 * side)
    angles = [start + (end - start) * i / steps for i in range(steps + 1)]

    vertices = []
    for angle in angles:
        for radius_x, radius_z in ((inner_rx, inner_rz), (outer_rx, outer_rz)):
            x = radius_x * math.sin(angle)
            z = radius_z * math.cos(angle)
            vertices.append((x, -y_half, z))
            vertices.append((x, y_half, z))

    faces = []
    for i in range(steps):
        base = i * 4
        nxt = (i + 1) * 4
        # inner and outer radial surfaces
        faces.append((base, nxt, nxt + 1, base + 1))
        faces.append((base + 2, base + 3, nxt + 3, nxt + 2))
        # front/back y faces
        faces.append((base, base + 2, nxt + 2, nxt))
        faces.append((base + 1, nxt + 1, nxt + 3, base + 3))

    # End caps.
    faces.append((0, 1, 3, 2))
    last = steps * 4
    faces.append((last, last + 2, last + 3, last + 1))

    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)

    bevel = obj.modifiers.new("soft plate edges", "BEVEL")
    bevel.width = mm(0.9)
    bevel.segments = 4
    return obj


def image_material(name, path):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in list(nodes):
        nodes.remove(node)
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.load(str(path), check_existing=True)
    texture.interpolation = "Linear"
    emission.inputs["Strength"].default_value = 1.1
    links.new(texture.outputs["Color"], emission.inputs["Color"])
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat


def ui_surface(parent, texture, z_local):
    if not texture:
        return None
    path = UI_DIR / f"{texture}.png"
    if not path.exists():
        raise FileNotFoundError(f"UI texture missing: {path}")
    bpy.ops.mesh.primitive_plane_add(size=1)
    plane = bpy.context.object
    plane.name = "Display UI"
    # Texture wide axis maps directly across the wrist (local/world X).
    plane.dimensions = (mm(DISPLAY_ACTIVE_MM[0]), mm(DISPLAY_ACTIVE_MM[1]), 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    plane.location = (0, mm(DISPLAY_OUTER_MM[1] / 2), z_local)
    plane.data.materials.append(image_material("UI-" + texture, path))
    plane.parent = parent
    return plane


def create_watch_reference_pair():
    """Create two Watch Ultra-sized blocks side by side for direct scale proof."""

    metal = material("Watch reference metal", (0.18, 0.19, 0.21), metallic=0.8, roughness=0.24)
    glass = material("Watch reference glass", (0.01, 0.012, 0.016), metallic=0.05, roughness=0.12)
    objects = []
    y = -mm(58)
    for index, x in enumerate((-mm(25.0), mm(25.0)), start=1):
        body = rounded_box(
            f"Apple Watch Ultra size reference {index}",
            (x, y, mm(31)),
            (mm(WATCH_ULTRA_MM[0]), mm(WATCH_ULTRA_MM[1]), mm(WATCH_ULTRA_MM[2])),
            metal,
            bevel=mm(6),
        )
        top = rounded_box(
            f"Watch reference glass {index}",
            (x, y, mm(38.3)),
            (mm(46), mm(41), mm(0.8)),
            glass,
            bevel=mm(5),
        )
        objects.extend((body, top))
    return objects


def create_wrist_proxy(profile="average"):
    skin = material("Validation skin", (0.48, 0.25, 0.16), roughness=0.52)
    width = WRIST_MODEL_MM["slim_width"] if profile == "slim" else WRIST_MODEL_MM["width"]
    thickness = WRIST_MODEL_MM["slim_thickness"] if profile == "slim" else WRIST_MODEL_MM["thickness"]
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=128,
        radius=1.0,
        depth=mm(190),
        rotation=(math.pi / 2, 0, 0),
        location=(0, 0, 0),
    )
    wrist = bpy.context.object
    wrist.name = "Wrist proxy"
    wrist.scale = (mm(width / 2), mm(thickness / 2), 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    wrist.data.materials.append(skin)
    return wrist


def build_product_scene(
    tilt_deg=0,
    texture="home",
    include_wrist_proxy=False,
    wrist_profile="average",
    watch_reference=False,
    exploded=False,
    detached=False,
):
    dark = material("Cuff shell", (0.035, 0.042, 0.052), metallic=0.5, roughness=0.3)
    battery = material("Battery plate shell", (0.055, 0.064, 0.077), metallic=0.62, roughness=0.28)
    carrier_mat = material("Tilt carrier", (0.035, 0.042, 0.052), metallic=0.62, roughness=0.30)
    frame_mat = material("Display subframe", (0.055, 0.062, 0.074), metallic=0.75, roughness=0.22)
    glass_mat = material("Edge glass", (0.008, 0.011, 0.016), metallic=0.05, roughness=0.08)
    contact_mat = material("Pogo contacts", (0.62, 0.38, 0.08), metallic=0.8, roughness=0.22)

    wrist_width = WRIST_MODEL_MM["slim_width"] if wrist_profile == "slim" else WRIST_MODEL_MM["width"]
    wrist_thickness = WRIST_MODEL_MM["slim_thickness"] if wrist_profile == "slim" else WRIST_MODEL_MM["thickness"]
    wrist_top = mm(wrist_thickness / 2)

    objects = {}
    if include_wrist_proxy:
        objects["wrist"] = create_wrist_proxy(wrist_profile)

    objects["cuff_left"] = cuff_segment("Left battery cuff", -1, wrist_width, wrist_thickness, battery)
    objects["cuff_right"] = cuff_segment("Right battery cuff", 1, wrist_width, wrist_thickness, battery)

    base_z = wrist_top + mm(2.2) + mm(BASE_THICKNESS_MM / 2)
    objects["base"] = rounded_box(
        "Central base",
        (0, 0, base_z),
        (mm(BASE_FOOTPRINT_MM[0]), mm(BASE_FOOTPRINT_MM[1]), mm(BASE_THICKNESS_MM)),
        dark,
        bevel=mm(4),
    )

    carrier_z = base_z + mm(BASE_THICKNESS_MM / 2) + mm(0.35) + mm(CARRIER_THICKNESS_MM / 2)
    carrier_offset = mm(8) if exploded else 0.0
    objects["carrier"] = rounded_box(
        "Thin tilt carrier",
        (0, 0, carrier_z + carrier_offset),
        (mm(CARRIER_FOOTPRINT_MM[0]), mm(CARRIER_FOOTPRINT_MM[1]), mm(CARRIER_THICKNESS_MM)),
        carrier_mat,
        bevel=mm(2),
    )

    # Hinge sits at the rear short edge; axis runs across the wrist (X).
    pivot_y = -mm(DISPLAY_OUTER_MM[1] / 2)
    pivot_z = carrier_z + mm(CARRIER_THICKNESS_MM / 2) + mm(0.45) + carrier_offset
    for index, x in enumerate((-mm(24.0), mm(24.0)), start=1):
        objects[f"hinge_{index}"] = cylinder(
            f"Recessed hinge {index}",
            (x, pivot_y + mm(0.8), pivot_z),
            mm(HINGE_PIN_DIAMETER_MM / 2),
            mm(10.0),
            carrier_mat,
            axis="X",
        )

    pivot = bpy.data.objects.new("Display tilt pivot", None)
    bpy.context.collection.objects.link(pivot)
    pivot.location = (0, pivot_y, pivot_z + (mm(28) if detached else (mm(20) if exploded else 0)))
    pivot.rotation_euler.x = math.radians(tilt_deg)
    if detached:
        pivot.location.x += mm(34)

    frame = rounded_box(
        "Display module",
        (0, 0, 0),
        (mm(DISPLAY_OUTER_MM[0]), mm(DISPLAY_OUTER_MM[1]), mm(DISPLAY_OUTER_MM[2])),
        frame_mat,
        bevel=mm(4.5),
    )
    frame.location = (0, mm(DISPLAY_OUTER_MM[1] / 2), mm(DISPLAY_OUTER_MM[2] / 2))
    frame.parent = pivot
    objects["display_frame"] = frame

    glass_z = mm(DISPLAY_OUTER_MM[2]) + mm(GLASS_THICKNESS_MM / 2) - mm(0.35)
    glass = rounded_box(
        "Edge-to-edge cover glass",
        (0, 0, 0),
        (mm(93.6), mm(44.6), mm(GLASS_THICKNESS_MM)),
        glass_mat,
        bevel=mm(4.2),
    )
    glass.location = (0, mm(DISPLAY_OUTER_MM[1] / 2), glass_z)
    glass.parent = pivot
    objects["glass"] = glass
    ui = ui_surface(pivot, texture, glass_z + mm(0.5))
    if ui:
        objects["ui"] = ui

    if exploded:
        # Small reserve cell and contacts are visible between module and carrier.
        reserve = material("Reserve cell", (0.16, 0.25, 0.29), metallic=0.15, roughness=0.38)
        objects["reserve_cell"] = rounded_box(
            "Reserve cell",
            (0, mm(8), pivot_z + mm(10)),
            (mm(30), mm(42), mm(2.4)),
            reserve,
            bevel=mm(1.5),
        )
        for i, x in enumerate((-mm(10), -mm(3.3), mm(3.3), mm(10)), start=1):
            objects[f"contact_{i}"] = cylinder(
                f"Pogo contact {i}",
                (x, mm(-8), carrier_z + mm(7)),
                mm(0.75),
                mm(2.0),
                contact_mat,
                axis="Z",
            )

    if watch_reference:
        for index, obj in enumerate(create_watch_reference_pair(), start=1):
            objects[f"watch_reference_{index}"] = obj

    # Minimum bottom clearance relative to the carrier top, computed at the
    # local bottom corners of the display envelope.
    angle = math.radians(tilt_deg)
    offset = pivot.location.z - (carrier_z + mm(CARRIER_THICKNESS_MM / 2))
    local_bottom_z = min(0.0, mm(DISPLAY_OUTER_MM[1]) * math.sin(angle))
    minimum_clearance = offset + local_bottom_z

    # The open underside gap is controlled by the plate end angles. For the
    # chosen ellipse, the chord between plate ends is kept >= design minimum.
    endpoint_angle = math.radians(145)
    inner_rx = mm(wrist_width / 2 + 1.8)
    endpoint_x = abs(inner_rx * math.sin(endpoint_angle))
    underside_gap_mm = max(CUFF_GAP_MM, metres_to_mm(endpoint_x * 2))

    metadata = {
        "screen_long_axis": SCREEN_LONG_AXIS,
        "underside_gap_mm": round(underside_gap_mm, 3),
        "minimum_screen_clearance_mm": round(metres_to_mm(minimum_clearance), 3),
        "tilt_deg": tilt_deg,
    }
    return {"objects": objects, "metadata": metadata, "pivot": pivot}


def metres_to_mm(value):
    return value * 1000.0
