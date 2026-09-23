"""Camera/render configuration separated from Blender so tests can validate it."""

COMMON = {
    "preview_resolution": (1000, 760),
    "final_resolution": (1800, 1368),
    "orthographic": False,
    "watch_reference": False,
    "texture": "home",
    "ground": True,
    "wrist_proxy": True,
}

RENDER_PLAN = {
    "scale-comparison": {
        **COMMON,
        "camera": "top-ortho",
        "orthographic": True,
        "watch_reference": True,
        "texture": None,
    },
    "closed-side": {
        **COMMON,
        "camera": "side-ortho",
        "orthographic": True,
        "texture": None,
    },
    "tilt-30": {
        **COMMON,
        "camera": "side-ortho",
        "orthographic": True,
        "texture": None,
    },
    "tilt-55": {
        **COMMON,
        "camera": "side-ortho",
        "orthographic": True,
        "texture": None,
    },
    "open-cuff-underside": {
        **COMMON,
        "camera": "underside",
        "orthographic": False,
        "texture": None,
        "ground": False,
        "wrist_proxy": False,
    },
    "mechanism-exploded": {
        **COMMON,
        "camera": "exploded",
        "texture": "home",
        "ground": False,
        "wrist_proxy": False,
    },
    "detached-module": {
        **COMMON,
        "camera": "hero",
        "texture": "home",
        "ground": False,
        "wrist_proxy": False,
    },
    "home-status": {**COMMON, "camera": "hero", "texture": "home"},
    "chat-list-thread": {**COMMON, "camera": "hero", "texture": "chat"},
    "marketplace": {**COMMON, "camera": "hero", "texture": "marketplace"},
    "split-chat-photos": {**COMMON, "camera": "hero", "texture": "split"},
    "smart-home": {**COMMON, "camera": "hero", "texture": "remote"},
    "blind-input": {**COMMON, "camera": "hero", "texture": "blind-input"},
    "media-handoff": {**COMMON, "camera": "hero", "texture": "handoff"},
    "ring-spatial": {**COMMON, "camera": "context", "texture": "remote"},
    "glasses-companion": {**COMMON, "camera": "context", "texture": "research"},
    "camera-companion": {**COMMON, "camera": "context", "texture": "camera"},
    "desk-clearance": {**COMMON, "camera": "desk", "texture": "chat"},
    "outdoor-navigation": {**COMMON, "camera": "hero", "texture": "navigation"},
    "dive-concept": {**COMMON, "camera": "hero", "texture": "home"},
}
