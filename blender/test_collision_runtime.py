"""Evaluated tilt collision: module vs carrier, base, cuffs and wrist proxy."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from blender.collision import min_gap, overlap_count
from blender.scene_builder import build_product_scene, reset_scene

MODULE = ('display_frame', 'glass', 'ui')
STATIC = ('carrier', 'base', 'cuff_left', 'cuff_right', 'wrist')
MIN_GAP_MM = 0.05


def build(tilt):
    reset_scene()
    return build_product_scene(tilt_deg=tilt, texture='home', include_wrist_proxy=True)['objects']


def check_tilt(tilt):
    objs = build(tilt)
    module = [objs[k] for k in MODULE]
    for key in STATIC:
        other = [objs[key]]
        hits = overlap_count(module, other)
        gap = 1000 * min_gap(module, other)
        print(f'  {tilt} deg {key}: hits={hits} gap={gap:.3f} mm')
        assert hits == 0, (tilt, key, 'intersecting triangles', hits)
        assert gap >= MIN_GAP_MM, (tilt, key, 'gap mm', gap)
    print(f'tilt {tilt}: clear of {STATIC}')


def check_detects_real_collision():
    """Negative control: a pushed-down module must be reported as colliding."""
    objs = build(30)
    objs['display_frame'].parent.location.z -= 0.004
    hits = overlap_count([objs[k] for k in MODULE], [objs['carrier']])
    assert hits > 0, 'collision query cannot see a 4 mm interpenetration'


for angle in (0, 30, 55):
    check_tilt(angle)
check_detects_real_collision()
print('tilt-collision: PASS')
