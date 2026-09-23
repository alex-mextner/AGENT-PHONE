# Blender render pipeline

Requires Blender 5.x and Python 3 with Pillow for UI texture generation.

## Generate UI textures

```bash
python3 blender/generate_ui.py
```

## Render all concept views

On macOS with Blender installed in Applications:

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python blender/screen_concept.py
```

The script writes PNG files to `renders/` and saves `renders/screen-concept.blend`.

## Design intent encoded by the model

- wide ~100 × 34 mm landscape screen;
- sub-millimeter-looking left/right glass borders;
- battery wings above and below the screen, following the strap direction;
- no rigid battery block under the wrist;
- two small recessed hinge barrels instead of a giant central hinge;
- detachable screen/carrier architecture;
- UI states are rendered on the worn device;
- one exploded view is included to explain the mechanism.

This is an industrial-design massing model, not a production CAD model.
