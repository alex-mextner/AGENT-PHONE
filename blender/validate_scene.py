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
    module = built["objects"]["display_frame"]
    dims = tuple(round(metres_to_mm(v), 3) for v in module.dimensions)
    # X is the long across-wrist axis; Y is the short forearm axis.
    expected = (DISPLAY_OUTER_MM[0], DISPLAY_OUTER_MM[1], DISPLAY_OUTER_MM[2])
    errors = []
    for axis, actual, exp in zip("XYZ", dims, expected):
        if not approx(actual, exp):
            errors.append(f"display {axis} dimension {actual} mm != {exp} mm")
    gap = built["metadata"]["underside_gap_mm"]
    if gap < CUFF_GAP_MM:
        errors.append(f"underside gap {gap} mm < {CUFF_GAP_MM} mm")
    if built["metadata"]["screen_long_axis"] != "across_wrist":
        errors.append("screen long axis is not across_wrist")
    return errors, {"display_dimensions_mm": dims, "underside_gap_mm": gap}


def validate_tilt_clearance():
    errors = []
    samples = {}
    for angle in TILT_ANGLES_DEG:
        reset_scene()
        built = build_product_scene(tilt_deg=angle, texture=None, include_wrist_proxy=True)
        clearance = built["metadata"]["minimum_screen_clearance_mm"]
        samples[str(angle)] = clearance
        # Hinge edge intentionally sits almost flush. Negative means penetration.
        if clearance < -0.15:
            errors.append(f"tilt {angle}° penetrates base by {-clearance:.2f} mm")
    return errors, samples


def main():
    errors = list(validate_geometry())
    dim_errors, dimensions = validate_flat_dimensions()
    clearance_errors, clearances = validate_tilt_clearance()
    errors.extend(dim_errors)
    errors.extend(clearance_errors)
    report = {
        "ok": not errors,
        "errors": errors,
        "dimensions": dimensions,
        "tilt_clearance_mm": clearances,
    }
    out = ROOT / "renders" / "validation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
