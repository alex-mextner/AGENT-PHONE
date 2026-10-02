"""Evaluated intersections in the full on-hand scenes: laptop, desk and ring."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bpy
from blender.collision import min_gap, overlap_count
from blender.scene_builder import reset_scene
from blender.screen_concept import build_scene

MODULE = ('display_frame', 'glass', 'ui', 'carrier', 'base', 'cuff_left', 'cuff_right')


def built_scene(name):
    reset_scene()
    built, _ = build_scene(name)
    bpy.context.view_layer.update()
    named = {o.name: o for o in built['context_objects']}
    return built, named


def check_laptop():
    built, named = built_scene('desk-clearance')
    laptop = [named['Laptop Base']]
    hand = [built['human']['object']]
    device = [built['objects'][k] for k in MODULE]
    for label, group in (('hand', hand), ('device', device)):
        hits = overlap_count(group, laptop)
        gap = 1000 * min_gap(group, laptop)
        print(f'  laptop vs {label}: hits={hits} gap={gap:.2f} mm')
        assert hits == 0, ('laptop intersects', label, hits)
        assert gap > 0.5, ('laptop touches', label, gap)


def check_ring():
    built, named = built_scene('ring-spatial')
    ring = [named['Agent Ring']]
    hand = [built['human']['object']]
    hits = overlap_count(ring, hand)
    gap = 1000 * min_gap(ring, hand)
    print(f'  ring vs finger: hits={hits} gap={gap:.2f} mm')
    assert hits == 0, ('ring cuts through the finger', hits)
    assert gap < 3.0, ('ring floats off the finger', gap)


check_laptop()
check_ring()
print('scene-collision-runtime: PASS')
