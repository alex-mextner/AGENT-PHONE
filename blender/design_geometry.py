"""Measured industrial-design constants shared by tests and Blender scenes.

All dimensions are millimetres. Blender scene helpers convert to metres at
object creation time so the source-of-truth numbers stay human-readable.
"""

DISPLAY_OUTER_MM = (92.0, 44.0, 6.6)  # long, short, total module thickness
COVER_GLASS_MM = (91.2, 43.2)
DISPLAY_ACTIVE_MM = (89.8, 40.6)
WATCH_ULTRA_MM = (49.0, 44.0, 14.4)

SCREEN_LONG_AXIS = "along_arm"
TILT_ANGLES_DEG = (0, 30, 55)

WRIST_MODEL_MM = {
    "width": 58.0,
    "thickness": 42.0,
    "circumference": 168.0,
    "slim_width": 52.0,
    "slim_thickness": 36.0,
}

# Open zone centred on the underside of the wrist; rigid cuff never crosses it.
# The side supports are broad where the battery mass sits, but taper at both ends.
CUFF_GAP_MM = 48.0
CUFF_PLATE_THICKNESS_MM = 3.2  # polymer support study, not a proven battery envelope
CUFF_END_WIDTH_MM = 12.0
CUFF_MID_WIDTH_MM = 28.0
CUFF_ATTACH_ANGLE_DEG = 20.0
CUFF_END_ANGLE_DEG = 125.0
CUFF_Z_OFFSET_MM = 2.0
BASE_THICKNESS_MM = 4.0
BASE_FOOTPRINT_MM = (40.0, 60.0)  # X across wrist, Y along arm
CARRIER_FOOTPRINT_MM = (22.0, 76.0)
GLASS_THICKNESS_MM = 0.85  # plus 0.05 mm active-surface layer in 6.6 mm envelope
CARRIER_THICKNESS_MM = 1.2
HINGE_PIN_DIAMETER_MM = 2.2
HINGE_INSET_MM = 8.0

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


def cuff_width_at_fraction(fraction):
    """Width of a side support along the arm from one tapered end to the other."""

    if not 0.0 <= fraction <= 1.0:
        raise ValueError("cuff fraction must be between 0 and 1")
    bell = __import__("math").sin(__import__("math").pi * fraction) ** 1.35
    return CUFF_END_WIDTH_MM + (CUFF_MID_WIDTH_MM - CUFF_END_WIDTH_MM) * bell


def estimated_underside_opening_mm(profile="average"):
    """Approximate rigid-free opening between the two cuff tips."""

    width = WRIST_MODEL_MM["slim_width"] if profile == "slim" else WRIST_MODEL_MM["width"]
    inner_rx = width / 2 + 1.8
    endpoint_x = abs(inner_rx * __import__("math").sin(__import__("math").radians(CUFF_END_ANGLE_DEG)))
    return endpoint_x * 2


def validate_geometry():
    """Return a list of human-readable violations of the baseline."""

    errors = []
    if SCREEN_LONG_AXIS != "along_arm":
        errors.append("display long axis must run along the arm")
    if DISPLAY_OUTER_MM[0] > 92.0:
        errors.append("display exceeds the 92 mm along-arm maximum")
    if DISPLAY_OUTER_MM[1] > WATCH_ULTRA_MM[1]:
        errors.append("display is wider than the Watch Ultra scale target")
    if max(visible_bezel_mm()) > 1.7:
        errors.append("visible structural bezel exceeds 1.7 mm")
    if estimated_underside_opening_mm("average") < CUFF_GAP_MM:
        errors.append("open cuff leaves too little hand-entry clearance")
    if CUFF_MID_WIDTH_MM <= CUFF_END_WIDTH_MM:
        errors.append("cuff support must taper from a broad middle to narrow ends")
    if any(angle not in TILT_ANGLES_DEG for angle in (0, 30, 55)):
        errors.append("required tilt states are missing")
    if CUFF_PLATE_THICKNESS_MM >= 7.0:
        errors.append("battery plate thickness exceeds concept target")
    return errors


def rounded_outline(width, length, radius, segments=12):
    """Counter-clockwise XY perimeter; units match the supplied dimensions."""
    import math
    values = (width, length, radius)
    if not all(math.isfinite(v) and v > 0 for v in values):
        raise ValueError('dimensions and radius must be positive and finite')
    if radius >= min(width, length) / 2:
        raise ValueError('radius must be smaller than half the shortest edge')
    if not isinstance(segments, int) or segments < 4:
        raise ValueError('segments must be an integer >= 4')
    centers = ((width/2-radius, length/2-radius),
               (-width/2+radius, length/2-radius),
               (-width/2+radius, -length/2+radius),
               (width/2-radius, -length/2+radius))
    points = []
    for corner, (cx, cy) in enumerate(centers):
        for step in range(segments+1):
            angle = (corner + step/segments) * math.pi/2
            points.append((cx+radius*math.cos(angle), cy+radius*math.sin(angle)))
    return points
