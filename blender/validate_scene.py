import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from blender.design_geometry import (
    CUFF_GAP_MM,
    DISPLAY_OUTER_MM,
    TILT_ANGLES_DEG,
    validate_geometry,
)
from blender.scene_builder import build_product_scene, reset_scene


def metres_to_mm(value):
    return value * 1000.0


def approx(actual, expected, tolerance=0.35):
    return abs(actual - expected) <= tolerance


def validate_flat_dimensions():
    reset_scene()
    built = build_product_scene(tilt_deg=0, texture=None, include_wrist_proxy=True)
    import bpy
    bpy.context.view_layer.update()
    graph = bpy.context.evaluated_depsgraph_get()
    vertices = []
    for key in ("display_frame", "glass", "ui"):
        obj = built["objects"][key].evaluated_get(graph)
        vertices.extend(obj.matrix_world @ v.co for v in obj.data.vertices)
    dims = tuple(round(1000*(max(v[i] for v in vertices)-min(v[i] for v in vertices)), 3) for i in range(3))
    # X is across the wrist; Y is the long along-arm axis.
    expected = (DISPLAY_OUTER_MM[1], DISPLAY_OUTER_MM[0], DISPLAY_OUTER_MM[2])
    errors = []
    for axis, actual, exp in zip("XYZ", dims, expected):
        if not approx(actual, exp):
            errors.append(f"display {axis} dimension {actual} mm != {exp} mm")
    gap = built["metadata"]["underside_gap_mm"]
    if gap < CUFF_GAP_MM:
        errors.append(f"underside gap {gap} mm < {CUFF_GAP_MM} mm")
    if built["metadata"]["screen_long_axis"] != "along_arm":
        errors.append("screen long axis is not along_arm")
    return errors, {"display_dimensions_mm": dims, "underside_gap_mm": gap}


def validate_tilt_clearance():
    from blender.collision import min_gap, overlap_count

    errors = []
    samples = {}
    for angle in TILT_ANGLES_DEG:
        reset_scene()
        built = build_product_scene(tilt_deg=angle, texture=None, include_wrist_proxy=True)
        objects = built["objects"]
        module = [objects[k] for k in ("display_frame", "glass", "ui")]
        static = [objects[k] for k in ("carrier", "base", "cuff_left", "cuff_right", "wrist")]
        hits = overlap_count(module, static)
        gap_mm = round(1000 * min_gap(module, static), 3)
        samples[str(angle)] = {
            "intersecting_triangle_pairs": hits,
            "sampled_min_gap_mm": gap_mm,
            "method": "evaluated-mesh triangle intersection + bidirectional vertex-to-surface sampling, not exact edge-edge minimum",
        }
        if hits > 0:
            errors.append(f"tilt {angle}° has {hits} intersecting triangle pairs")
        if gap_mm < 0.05:
            errors.append(f"tilt {angle}° sampled gap {gap_mm} mm below 0.05 mm")
    return errors, samples


def validate_closed_stack():
    """Evaluated complete closed-stack height above nominal proxy skin.

    Measured (not assumed): evaluated max-Z of all product objects vs
    evaluated proxy-skin top at tilt 0, average profile. Distinct from the
    6.6 mm module envelope. Real skin/hardware unvalidated.
    """
    reset_scene()
    built = build_product_scene(tilt_deg=0, texture=None, include_wrist_proxy=True,
                                wrist_profile="average")
    import bpy
    bpy.context.view_layer.update()
    graph = bpy.context.evaluated_depsgraph_get()
    prod_z, skin_z = [], []
    for key, obj in built["objects"].items():
        ev = obj.evaluated_get(graph)
        zs = [(ev.matrix_world @ v.co).z for v in ev.data.vertices]
        if not zs:
            continue
        if key == "wrist":
            skin_z.extend(zs)
        else:
            prod_z.extend(zs)
    product_top_mm = round(1000 * max(prod_z), 3)
    skin_top_mm = round(1000 * max(skin_z), 3)
    above_mm = round(product_top_mm - skin_top_mm, 3)
    errors = []
    # Regression band around the independently probed 14.8 mm (35.8 vs 21.0).
    if not 13.0 <= above_mm <= 17.0:
        errors.append(f"closed stack {above_mm} mm outside 13-17 mm regression band")
    return errors, {"product_top_mm": product_top_mm, "skin_top_mm": skin_top_mm,
                    "closed_stack_mm": above_mm,
                    "method": "evaluated depsgraph max-Z at tilt 0, average proxy; static fit only"}


def main():
    errors = list(validate_geometry())
    dim_errors, dimensions = validate_flat_dimensions()
    clearance_errors, clearances = validate_tilt_clearance()
    stack_errors, closed_stack = validate_closed_stack()
    errors.extend(dim_errors)
    errors.extend(clearance_errors)
    errors.extend(stack_errors)
    report = {
        "ok": not errors,
        "errors": errors,
        "dimensions": dimensions,
        "tilt_clearance_mm": clearances,
        "closed_stack_mm": closed_stack,
    }
    out = ROOT / "renders" / "validation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
