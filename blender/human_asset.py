"""Licensed MakeHuman wrist/hand asset support.

The module is importable in ordinary Python for metadata tests. Blender-only
helpers import bpy lazily.
"""

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "assets" / "human" / "cache"

HUMAN_ASSET_METADATA = {
    "source_url": "https://github.com/makehumancommunity/makehuman",
    "base_obj_url": "https://raw.githubusercontent.com/makehumancommunity/makehuman/master/makehuman/data/3dobjs/base.obj",
    "skin_pack_url": "https://files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip",
    "license": "CC0-1.0",
    "license_url": "https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.md",
    "redistribution": "download-on-demand",
    "base_obj": str(CACHE_DIR / "base.obj"),
    "body_obj": str(CACHE_DIR / "base_body.obj"),
    "skin_zip": str(CACHE_DIR / "makehuman_system_assets_cc0.zip"),
    "male_skin": str(CACHE_DIR / "system-assets" / "male" / "young_lightskinned_male_diffuse.png"),
    "female_skin": str(CACHE_DIR / "system-assets" / "female" / "young_lightskinned_female_diffuse.png"),
}

WRIST_PROFILES = {
    "average": {
        "wrist_width_mm": 58.0,
        "wrist_thickness_mm": 42.0,
        "gender_skin": "male",
        "scale": 1.0,
    },
    "slim": {
        "wrist_width_mm": 52.0,
        "wrist_thickness_mm": 36.0,
        "gender_skin": "female",
        "scale": 0.93,
    },
}

# MakeHuman base-object joint centroids are read from the helper groups rather
# than treated as visual geometry. One MakeHuman unit is ~0.1 m.
MH_UNIT_METRES = 0.1


def require_asset(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Human asset missing: {path}. Run blender/fetch_human_asset.py first."
        )
    return path


def _parse_obj_vertices_and_groups(path):
    vertices = []
    group_indices = {}
    current = None
    for line in Path(path).read_text().splitlines():
        if line.startswith("v "):
            vertices.append(tuple(map(float, line.split()[1:4])))
        elif line.startswith("g "):
            current = line[2:].strip()
            group_indices.setdefault(current, set())
        elif current and line.startswith("f "):
            for token in line.split()[1:]:
                index = int(token.split("/")[0])
                group_indices[current].add(index)
    return vertices, group_indices


def _group_centroid(vertices, indices):
    pts = [vertices[index - 1] for index in sorted(indices)]
    if not pts:
        raise RuntimeError("empty MakeHuman helper group")
    return tuple(sum(p[i] for p in pts) / len(pts) for i in range(3))


def joint_centers(side="right"):
    """Return hand/wrist and elbow helper centres in MakeHuman coordinates."""

    base = require_asset(HUMAN_ASSET_METADATA["base_obj"])
    vertices, groups = _parse_obj_vertices_and_groups(base)
    prefix = "r" if side == "right" else "l"
    hand_name = f"joint-{prefix}-hand"
    elbow_name = f"joint-{prefix}-elbow"
    if hand_name not in groups or elbow_name not in groups:
        raise RuntimeError(f"MakeHuman joint groups missing: {hand_name}, {elbow_name}")
    return {
        "wrist": _group_centroid(vertices, groups[hand_name]),
        "elbow": _group_centroid(vertices, groups[elbow_name]),
    }


def hand_anchor_centers(side="right"):
    """Return semantic hand/finger anchors in MakeHuman source coordinates."""

    base = require_asset(HUMAN_ASSET_METADATA["base_obj"])
    vertices, groups = _parse_obj_vertices_and_groups(base)
    prefix = "r" if side == "right" else "l"
    names = {
        "hand_center": f"joint-{prefix}-hand-3",
        "ring_proximal": f"joint-{prefix}-finger-4-1",
        "ring_middle": f"joint-{prefix}-finger-4-2",
        "index_tip": f"joint-{prefix}-finger-2-4",
        "index_knuckle": f"joint-{prefix}-finger-2-1",
        "pinky_knuckle": f"joint-{prefix}-finger-5-1",
    }
    missing = [name for name in names.values() if name not in groups]
    if missing:
        raise RuntimeError(f"MakeHuman hand joint groups missing: {missing}")
    return {
        key: _group_centroid(vertices, groups[group_name])
        for key, group_name in names.items()
    }


def _skin_path(profile):
    profile_data = WRIST_PROFILES[profile]
    key = "male_skin" if profile_data["gender_skin"] == "male" else "female_skin"
    return require_asset(HUMAN_ASSET_METADATA[key])


def _skin_material(profile):
    import bpy

    texture_path = _skin_path(profile)
    mat = bpy.data.materials.new(f"MakeHuman skin {profile}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    image = nodes.new("ShaderNodeTexImage")
    image.image = bpy.data.images.load(str(texture_path), check_existing=True)
    image.image.colorspace_settings.name = "sRGB"
    tone = nodes.new("ShaderNodeHueSaturation")
    tone.inputs["Saturation"].default_value = 0.90
    tone.inputs["Value"].default_value = 0.82
    links.new(image.outputs["Color"], tone.inputs["Color"])
    links.new(tone.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.58
    if "Subsurface Weight" in bsdf.inputs:
        bsdf.inputs["Subsurface Weight"].default_value = 0.035

    # Fine pore-scale relief. The diffuse map remains the source of actual
    # skin colour; procedural noise only breaks the perfectly smooth CG sheen.
    texcoord = nodes.new("ShaderNodeTexCoord")
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 185.0
    noise.inputs["Detail"].default_value = 3.0
    noise.inputs["Roughness"].default_value = 0.72
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.14
    bump.inputs["Distance"].default_value = 0.00018
    links.new(texcoord.outputs["Generated"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def _pose_hand(point):
    """Gently extend the existing hand mesh; preserve forearm and UV topology."""
    from mathutils import Vector
    x, y, z = point
    if y <= 0 or y >= 0.30 or abs(x) > 0.10 or abs(z) > 0.16:
        return point.copy()
    t = min(1.0, y / 0.035)
    angle = math.radians(24) * t*t*(3-2*t)  # lift the thumb clear of the tabletop
    c, s = math.cos(angle), math.sin(angle)
    return Vector((x, c*y-s*z, s*y+c*z))


def load_makehuman_wrist(profile="average", side="right"):
    """Import, align and skin a real MakeHuman hand/forearm.

    The full body mesh remains available outside the camera crop, avoiding a
    destructive arm cut while preserving natural wrist and hand topology.
    The selected wrist helper is transformed to world origin and the forearm
    points along +Y, as does the long display axis. The hand is posed dorsal-up.
    """

    import bpy
    from mathutils import Matrix, Vector

    if profile not in WRIST_PROFILES:
        raise ValueError(f"Unknown wrist profile: {profile}")
    if side not in {"right", "left"}:
        raise ValueError(f"Unknown side: {side}")

    body_obj = require_asset(HUMAN_ASSET_METADATA["body_obj"])
    centres = joint_centers(side)
    anchors = hand_anchor_centers(side)
    wrist = Vector(centres["wrist"])
    elbow = Vector(centres["elbow"])
    forearm = wrist - elbow
    target = Vector((0.0, 1.0, 0.0))
    rotation = forearm.normalized().rotation_difference(target)

    before = set(bpy.context.scene.objects)
    bpy.ops.wm.obj_import(filepath=str(body_obj), forward_axis="NEGATIVE_Z", up_axis="Y")
    imported = [obj for obj in bpy.context.scene.objects if obj not in before and obj.type == "MESH"]
    if not imported:
        raise RuntimeError("MakeHuman OBJ import produced no mesh")
    obj = max(imported, key=lambda candidate: len(candidate.data.vertices))
    obj.name = f"MakeHuman {profile} {side} wrist"

    scale = MH_UNIT_METRES * WRIST_PROFILES[profile]["scale"]
    aligned = rotation.to_matrix().to_4x4() @ Matrix.Scale(scale, 4)
    # The raw base arrives palm-up after forearm alignment. A 180° roll around
    # the forearm keeps +Y direction but puts the back of the hand at +Z.
    transform = Matrix.Rotation(math.pi, 4, "Y") @ aligned
    wrist_world_before_translation = transform @ wrist
    transform.translation = -wrist_world_before_translation
    obj.matrix_world = transform
    inverse = transform.inverted()
    for vertex in obj.data.vertices:
        vertex.co = inverse @ _pose_hand(transform @ vertex.co)
    obj.data.update()

    obj.data.materials.clear()
    obj.data.materials.append(_skin_material(profile))
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    subdivision = obj.modifiers.new("Skin subdivision", "SUBSURF")
    subdivision.levels = 1
    subdivision.render_levels = 1

    wrist_world = obj.matrix_world @ wrist
    elbow_world = obj.matrix_world @ elbow
    anchors_world = {
        key: _pose_hand(obj.matrix_world @ Vector(source))
        for key, source in anchors.items()
    }
    return {
        "object": obj,
        "wrist_origin_world": wrist_world,
        "elbow_world": elbow_world,
        "anchors_world": anchors_world,
        "profile": profile,
        "side": side,
    }
