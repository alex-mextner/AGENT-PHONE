"""Runtime integration test: lifestyle scenes must contain real human/context geometry."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bpy

from blender.scene_builder import reset_scene
from blender.screen_concept import build_scene


def names():
    return {obj.name for obj in bpy.context.scene.objects}


reset_scene()
build_scene("home-status")
home_names = names()
assert any(name.startswith("MakeHuman average") for name in home_names), sorted(home_names)
assert "Wrist proxy" not in home_names

reset_scene()
build_scene("ring-spatial")
ring_names = names()
assert any(name.startswith("MakeHuman average") for name in ring_names)
assert "Agent Ring" in ring_names
assert "Context TV" in ring_names
assert "Context Light" in ring_names

reset_scene()
build_scene("glasses-companion")
glasses_names = names()
assert any(name.startswith("MakeHuman slim") for name in glasses_names)
assert "Agent Glasses Left Lens" in glasses_names
assert "Agent Glasses Right Lens" in glasses_names

print("lifestyle-runtime: PASS")
