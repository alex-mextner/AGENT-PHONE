"""Blender-runtime test for the MakeHuman wrist loader."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bpy

from blender.human_asset import load_makehuman_wrist
from blender.scene_builder import reset_scene

reset_scene()
result = load_makehuman_wrist(profile="average", side="right")
obj = result["object"]
assert obj.type == "MESH"
assert obj.name.startswith("MakeHuman")
assert obj.dimensions.x > 0.5, obj.dimensions[:]
assert len(obj.data.uv_layers) >= 1
assert obj.data.materials, "skin material not assigned"
mat = obj.data.materials[0]
assert mat.use_nodes
image_nodes = [n for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"]
assert image_nodes and image_nodes[0].image is not None
assert any(n.type == "TEX_NOISE" for n in mat.node_tree.nodes), "skin micro-noise missing"
assert any(n.type == "BUMP" for n in mat.node_tree.nodes), "skin bump node missing"
assert result["wrist_origin_world"].length < 0.003, result["wrist_origin_world"]
print("human-runtime: PASS", tuple(round(v, 4) for v in obj.dimensions))
