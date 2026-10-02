"""Blender-runtime contract for physical scenario props."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bpy
from mathutils import Vector

from blender.context_props import add_context
from blender.scene_builder import reset_scene

EXPECTED = {
    "tv": {"Context TV", "Context Wall", "Media Console"},
    "ring-room": {"Agent Ring", "Context TV", "Context Wall", "Media Console", "Context Light"},
    "glasses": {"Agent Glasses Left Lens", "Agent Glasses Right Lens"},
    "camera-tile": {"Agent Camera Tile", "Agent Camera Lens"},
    "desk-laptop": {"Desk", "Laptop Base"},
    "dive-clasp": {"Dive Clasp", "Dive Clasp Left Latch", "Dive Clasp Right Latch"},
    "external-battery": {"External Battery Pack", "Flat Power Ribbon"},
    "car-hud": {"Car Windshield", "Car HUD Route", "Car HUD Speed"},
}

ring_anchors = {
    "ring_proximal": Vector((0.015, 0.105, -0.020)),
    "ring_middle": Vector((0.020, 0.132, -0.027)),
}

for kind, expected_names in EXPECTED.items():
    reset_scene()
    objects = add_context(kind, anchors=ring_anchors if kind == "ring-room" else None)
    names = {obj.name for obj in objects}
    assert expected_names.issubset(names), (kind, expected_names, names)
    if kind in {"tv", "ring-room"}:
        tv = next(obj for obj in objects if obj.name == "Context TV")
        assert tv.location.y > 0.12, tuple(tv.location)
    if kind == "ring-room":
        ring = next(obj for obj in objects if obj.name == "Agent Ring")
        segment_mid = (ring_anchors["ring_proximal"] + ring_anchors["ring_middle"]) / 2
        assert (ring.location - segment_mid).length < 0.012, (tuple(ring.location), tuple(segment_mid))
        assert ring.dimensions.x < 0.024 and ring.dimensions.y < 0.024 and ring.dimensions.z < 0.024
    if kind == "glasses":
        assert {"Bone Conduction Left", "Bone Conduction Right"}.issubset(names)
        lenses = [obj for obj in objects if obj.name.endswith("Lens")]
        assert lenses and all(obj.location.z < 0.0 for obj in lenses), [tuple(obj.location) for obj in lenses]
        assert all(obj.location.x > 0.03 for obj in lenses), [tuple(obj.location) for obj in lenses]
    if kind == "camera-tile":
        tile = next(obj for obj in objects if obj.name == "Agent Camera Tile")
        assert tile.location.z < 0.0, tuple(tile.location)
    if kind == "external-battery":
        pack = next(obj for obj in objects if obj.name == "External Battery Pack")
        ribbon = next(obj for obj in objects if obj.name == "Flat Power Ribbon")
        assert pack.location.y < -0.06, tuple(pack.location)
        assert ribbon.dimensions.y > ribbon.dimensions.x * 5, tuple(ribbon.dimensions)
    print(kind, sorted(names))

print("context-runtime: PASS")
