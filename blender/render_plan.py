"""Camera/render configuration separated from Blender for testability."""

COMMON = {
    "preview_resolution": (1000, 760),
    "final_resolution": (1800, 1368),
    "orthographic": False,
    "watch_reference": False,
    "texture": "home",
    "ground": True,
    "wrist_proxy": True,
    "human_profile": None,
    "human_offset_y_mm": 55.0,
    "context": None,
}

LIFESTYLE = {
    **COMMON,
    "wrist_proxy": False,
    "human_profile": "average",
}

RENDER_PLAN = {
    "scale-comparison": {
        **COMMON, "camera": "top-ortho", "orthographic": True,
        "watch_reference": True, "texture": None, "wrist_proxy": False,
    },
    "closed-side": {
        **COMMON, "camera": "tilt-tech", "texture": None,
        "ground": False, "wrist_proxy": False,
    },
    "tilt-30": {
        **COMMON, "camera": "tilt-tech", "texture": None,
        "ground": False, "wrist_proxy": False,
    },
    "tilt-55": {
        **COMMON, "camera": "tilt-tech", "texture": None,
        "ground": False, "wrist_proxy": False,
    },
    "open-cuff-underside": {
        **COMMON, "camera": "underside-wide", "texture": None,
        "ground": False, "wrist_proxy": False,
    },
    "mechanism-exploded": {
        **COMMON, "camera": "exploded", "texture": "home",
        "ground": False, "wrist_proxy": False,
    },
    "detached-module": {
        **COMMON, "camera": "exploded", "texture": "home",
        "ground": False, "wrist_proxy": False,
    },

    "home-status": {**LIFESTYLE, "camera": "hero", "texture": "home"},
    "chat-list-thread": {**LIFESTYLE, "camera": "hero", "texture": "chat"},
    "marketplace": {**LIFESTYLE, "camera": "hero", "texture": "marketplace"},
    "split-chat-photos": {
        **LIFESTYLE, "camera": "hero", "texture": "split", "human_profile": "slim",
    },
    "smart-home": {**LIFESTYLE, "camera": "hero", "texture": "remote"},
    "blind-input": {
        **LIFESTYLE, "camera": "hero", "texture": "blind-input", "human_profile": "slim",
    },
    "media-handoff": {
        **LIFESTYLE, "camera": "context", "texture": "handoff", "context": "tv",
    },
    "ring-spatial": {
        **LIFESTYLE, "camera": "context", "texture": "remote", "context": "ring-room",
    },
    "glasses-companion": {
        **LIFESTYLE, "camera": "context", "texture": "research",
        "context": "glasses", "human_profile": "slim",
    },
    "camera-companion": {
        **LIFESTYLE, "camera": "context", "texture": "camera", "context": "camera-tile",
    },
    "desk-clearance": {
        **LIFESTYLE, "camera": "desk", "texture": "chat", "context": "desk-laptop", "ground": False,
    },
    "outdoor-navigation": {
        **LIFESTYLE, "camera": "hero", "texture": "navigation", "human_profile": "slim",
    },
    "dive-concept": {
        **LIFESTYLE, "camera": "hero", "texture": "home", "context": "dive-clasp",
    },
    "external-battery": {
        **LIFESTYLE, "camera": "context", "texture": "home", "context": "external-battery",
    },
    "car-hud": {
        **LIFESTYLE, "camera": "context", "texture": "navigation", "context": "car-hud",
        "human_profile": "slim",
    },
}
