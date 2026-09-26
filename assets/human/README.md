# Human wrist asset

Final on-wrist renders use MakeHuman core assets rather than the old cylinder-and-sphere validation arm.

## Source and license

- Project: [MakeHuman](https://github.com/makehumancommunity/makehuman)
- Base mesh: MakeHuman core `base.obj`
- Natural skin assets: MakeHuman system-assets pack
- License: **CC0 1.0 Universal** for the bundled graphical assets, including the base mesh, targets, skins, poses and expressions
- License statement: https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.md
- System-assets pack: https://static.makehumancommunity.org/assets/assetpacks/makehuman_system_assets.html

MakeHuman's application source has a different software license; this project uses only the CC0 graphical assets.

## Cache policy

Large source assets are **download-on-demand** and are not committed to this repository.

Expected local cache:

```
assets/human/cache/base.obj
assets/human/cache/makehuman_system_assets_cc0.zip
assets/human/cache/system-assets/...
```

Run:

```bash
python3 blender/fetch_human_asset.py
```

The final rendered PNGs may be committed. The generated Blender checkpoint may contain a derived CC0 wrist mesh so the scene remains inspectable.

## Why this source

The previous render used primitive cylinders/spheres and looked like a mannequin. The MakeHuman base mesh provides real hand/finger/wrist topology and can use the project's natural-skin textures while remaining legally reproducible.
