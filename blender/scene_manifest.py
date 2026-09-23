"""Declarative render-scene manifest.

This module intentionally has no Blender dependency so unit tests can validate
the gallery contract with ordinary Python.
"""

BASE = {
    "screen_long_axis": "forearm",
    "cuff": "open",
    "watch_reference": False,
    "render_kind": "lifestyle",
    "tilt_deg": 18,
    "texture": "home",
}

SCENES = {
    "scale-comparison": {**BASE, "render_kind": "technical", "tilt_deg": 0, "watch_reference": True, "texture": None},
    "closed-side": {**BASE, "render_kind": "technical", "tilt_deg": 0, "texture": None},
    "tilt-30": {**BASE, "render_kind": "technical", "tilt_deg": 30, "texture": None},
    "tilt-55": {**BASE, "render_kind": "technical", "tilt_deg": 55, "texture": None},
    "open-cuff-underside": {**BASE, "render_kind": "technical", "tilt_deg": 0, "texture": None},
    "mechanism-exploded": {**BASE, "render_kind": "technical", "tilt_deg": 20, "texture": "home"},
    "detached-module": {**BASE, "render_kind": "technical", "tilt_deg": 0, "texture": "home"},
    "home-status": {**BASE, "texture": "home", "tilt_deg": 18},
    "chat-list-thread": {**BASE, "texture": "chat", "tilt_deg": 28},
    "marketplace": {**BASE, "texture": "marketplace", "tilt_deg": 22},
    "split-chat-photos": {**BASE, "texture": "split", "tilt_deg": 20},
    "smart-home": {**BASE, "texture": "remote", "tilt_deg": 20},
    "blind-input": {**BASE, "texture": "blind-input", "tilt_deg": 10},
    "media-handoff": {**BASE, "texture": "handoff", "tilt_deg": 20},
    "ring-spatial": {**BASE, "texture": "remote", "tilt_deg": 18},
    "glasses-companion": {**BASE, "texture": "research", "tilt_deg": 18},
    "camera-companion": {**BASE, "texture": "camera", "tilt_deg": 24},
    "desk-clearance": {**BASE, "texture": "chat", "tilt_deg": 24},
    "outdoor-navigation": {**BASE, "texture": "navigation", "tilt_deg": 18},
    "dive-concept": {**BASE, "texture": "home", "tilt_deg": 10},
}

def scene_names():
    return tuple(SCENES)
