"""Blender-runtime contract for physical scenario props."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bpy

from blender.context_props import add_context
from blender.scene_builder import reset_scene

EXPECTED = {
    "tv": {"Context TV"},
    "ring-room": {"Agent Ring", "Context TV", "Context Light"},
    "glasses": {"Agent Glasses Left Lens", "Agent Glasses Right Lens"},
    "camera-tile": {"Agent Camera Tile", "Agent Camera Lens"},
    "desk-laptop": {"Desk", "Laptop Base"},
    "dive-clasp": {"Dive Clasp", "Dive Clasp Left Latch", "Dive Clasp Right Latch"},
    "external-battery": {"External Battery Pack", "Flat Power Ribbon"},
    "car-hud": {"Car Windshield", "Car HUD Route", "Car HUD Speed"},
}

for kind, expected_names in EXPECTED.items():
    reset_scene()
    objects = add_context(kind)
    names = {obj.name for obj in objects}
    assert expected_names.issubset(names), (kind, expected_names, names)
    if kind in {"tv", "ring-room"}:
        tv = next(obj for obj in objects if obj.name == "Context TV")
        assert tv.location.y > 0.12, tuple(tv.location)
    if kind == "glasses":
        assert {"Bone Conduction Left", "Bone Conduction Right"}.issubset(names)
    print(kind, sorted(names))

print("context-runtime: PASS")
