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

- 92 × 44 × 6.6 mm module (6.6 mm is the complete envelope including glass), long axis **along the arm**;
- a single Watch Ultra footprint as the scale reference;
- edge-to-edge glass with a subordinate structural rim (about 0.7–1.7 mm);
- two thin polymer cuff supports attached around the middle of the long module, broad in the middle (about 28 mm) and tapered at both ends (about 12 mm), leaving the underside open with roughly a 48 mm hand-entry gap; not end hooks;
- rigid cuff stops before the underside desk-contact zone;
- recessed tilt mechanism with 0° / 30° / 55° validation states;
- detachable display/compute module with a small reserve cell;
- licensed MakeHuman wrist/hand asset for lifestyle scenes;
- companion contexts for TV handoff, ring, glasses/private audio, camera tile, external battery, Dive clasp, desk/laptop and car HUD;
- every public UI state is rendered on the worn device.

This remains an industrial-design massing model, not production CAD.

Collision-scope limits: `collision.py` reports evaluated-mesh triangle
intersections plus bidirectional vertex-to-surface sampled gaps. Zero
triangle intersections cannot detect one solid fully enclosed in another
(no volumetric containment claim); sampling is not an exact edge-edge
minimum; all checks are static posed fits, not motion, donning, comfort,
or physical validation. Measured whole-stack height (closed, tilt 0°,
average proxy) is about 14.8 mm above proxy skin (`closed_stack_mm` in
`renders/validation.json`), distinct from the 6.6 mm module envelope.
