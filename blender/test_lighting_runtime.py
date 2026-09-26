"""Regression check: studio lights must not blow out dark wrist materials."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bpy
from blender.scene_builder import reset_scene
from blender.screen_concept import setup_lighting

reset_scene()
setup_lighting()
energies = {
    obj.name: obj.data.energy
    for obj in bpy.context.scene.objects
    if obj.type == "LIGHT"
}
print("studio-light-energies", energies)
assert energies, "expected studio lights"
assert max(energies.values()) <= 10.0, energies
print("lighting-runtime: PASS")
