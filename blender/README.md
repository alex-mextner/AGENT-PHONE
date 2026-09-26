# Render pipeline

Requires Blender 5.x and Python 3 with Pillow for UI texture generation.

## Generate UI textures

```bash
python3 blender/generate_ui.py
```

## Fetch the licensed human asset

```bash
python3 blender/fetch_human_asset.py
```

MakeHuman graphical assets are cached under `assets/human/cache/` and are not committed. Source/license details live in `assets/human/README.md`.

## Render concept views

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python blender/screen_concept.py
```

Use `-- --scene car-hud`, `-- --scene ring-spatial`, or another scene name for one render. Add `-- --preview` for the lower-resolution preview path.

The current source checkpoint is `renders/agent-phone-concept.blend`.

## Design intent encoded by the model

- 94 × 45 mm module: approximately two Watch Ultra-sized faces side by side;
- long display axis **across the wrist**;
- edge-to-edge glass with a subordinate structural rim;
- two curved battery plates integrated into the open cuff;
- rigid cuff stops before the underside desk-contact zone;
- recessed tilt mechanism with 0° / 30° / 55° validation states;
- detachable display/compute module with a small reserve cell;
- licensed MakeHuman wrist/hand asset for lifestyle scenes;
- companion contexts for TV handoff, ring, glasses/private audio, camera tile, external battery, Dive clasp, desk/laptop and car HUD;
- every public UI state is rendered on the worn device.

This remains an industrial-design massing model, not production CAD.
