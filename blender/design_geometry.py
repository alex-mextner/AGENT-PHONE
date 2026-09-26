"""Measured industrial-design constants shared by tests and Blender scenes.

All dimensions are millimetres. Blender scene helpers convert to metres at
object creation time so the source-of-truth numbers stay human-readable.
"""

DISPLAY_OUTER_MM = (94.0, 45.0, 6.2)  # long, short, total module thickness
DISPLAY_ACTIVE_MM = (91.0, 42.0)
WATCH_ULTRA_MM = (49.0, 44.0, 14.4)

SCREEN_LONG_AXIS = "across_wrist"
TILT_ANGLES_DEG = (0, 30, 55)

WRIST_MODEL_MM = {
    "width": 58.0,
    "thickness": 42.0,
    "circumference": 168.0,
    "slim_width": 52.0,
    "slim_thickness": 36.0,
}

# Open zone centred on the underside of the wrist; rigid cuff never crosses it.
CUFF_GAP_MM = 32.0
CUFF_PLATE_THICKNESS_MM = 5.2
CUFF_PLATE_WIDTH_MM = 34.0
BASE_THICKNESS_MM = 4.0
BASE_FOOTPRINT_MM = (60.0, 30.0)
CARRIER_FOOTPRINT_MM = (66.0, 22.0)
GLASS_THICKNESS_MM = 0.9
CARRIER_THICKNESS_MM = 1.2
HINGE_PIN_DIAMETER_MM = 2.2

# Visible structural border beneath edge-to-edge glass.
BEZEL_LONG_EDGE_MM = (DISPLAY_OUTER_MM[1] - DISPLAY_ACTIVE_MM[1]) / 2
BEZEL_SHORT_END_MM = (DISPLAY_OUTER_MM[0] - DISPLAY_ACTIVE_MM[0]) / 2

REQUIRED_MECHANICAL_SCENES = (
    "scale-comparison",
    "closed-side",
    "tilt-30",
    "tilt-55",
    "open-cuff-underside",
    "mechanism-exploded",
    "detached-module",
)

REQUIRED_LIFESTYLE_SCENES = (
    "home-status",
    "chat-list-thread",
    "marketplace",
    "split-chat-photos",
    "smart-home",
    "blind-input",
    "media-handoff",
    "ring-spatial",
    "glasses-companion",
    "camera-companion",
    "desk-clearance",
    "outdoor-navigation",
    "dive-concept",
    "external-battery",
    "car-hud",
)


def visible_bezel_mm():
    """Return (long-edge bezel, short-end bezel) in mm."""

    return BEZEL_LONG_EDGE_MM, BEZEL_SHORT_END_MM


def validate_geometry():
    """Return a list of human-readable violations of the baseline."""

    errors = []
    if SCREEN_LONG_AXIS != "across_wrist":
        errors.append("display long axis must run across the wrist")
    if DISPLAY_OUTER_MM[0] > WATCH_ULTRA_MM[0] * 2:
        errors.append("display is longer than two Watch Ultra cases")
    if DISPLAY_OUTER_MM[1] > WATCH_ULTRA_MM[1] + 1.0:
        errors.append("display is wider than the Watch Ultra scale target")
    if max(visible_bezel_mm()) > 1.5:
        errors.append("visible structural bezel exceeds 1.5 mm")
    if CUFF_GAP_MM < 28.0:
        errors.append("open cuff leaves too little underside clearance")
    if any(angle not in TILT_ANGLES_DEG for angle in (0, 30, 55)):
        errors.append("required tilt states are missing")
    if CUFF_PLATE_THICKNESS_MM >= 7.0:
        errors.append("battery plate thickness exceeds concept target")
    return errors
