"""Fetch the CC0 MakeHuman base mesh and natural skin textures.

Assets are cached locally and intentionally ignored by git.
"""

import sys
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from blender.human_asset import CACHE_DIR, HUMAN_ASSET_METADATA

BODY_OBJ = CACHE_DIR / "base_body.obj"
MALE_SKIN = CACHE_DIR / "system-assets" / "male" / "young_lightskinned_male_diffuse.png"
FEMALE_SKIN = CACHE_DIR / "system-assets" / "female" / "young_lightskinned_female_diffuse.png"


def extract_body_only(source, destination):
    lines = Path(source).read_text().splitlines()
    prefix = []
    body_faces = []
    in_body = False
    for line in lines:
        if line.startswith(("v ", "vt ", "vn ")):
            prefix.append(line)
        elif line.startswith("g "):
            group = line[2:].strip()
            if group == "body":
                in_body = True
            elif in_body:
                break
        elif in_body and line.startswith("f "):
            body_faces.append(line)
    if not body_faces:
        raise RuntimeError("MakeHuman body face group not found")
    destination.write_text("\n".join(prefix + ["g body"] + body_faces) + "\n")


def main():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    base = Path(HUMAN_ASSET_METADATA["base_obj"])
    archive = Path(HUMAN_ASSET_METADATA["skin_zip"])
    if not base.exists():
        print("Downloading MakeHuman base mesh…")
        urlretrieve(HUMAN_ASSET_METADATA["base_obj_url"], base)
    if not archive.exists():
        print("Downloading MakeHuman CC0 system assets…")
        urlretrieve(HUMAN_ASSET_METADATA["skin_pack_url"], archive)

    extract_body_only(base, BODY_OBJ)

    members = {
        "skins/young_caucasian_male/young_lightskinned_male_diffuse.png": MALE_SKIN,
        "skins/young_caucasian_female/young_lightskinned_female_diffuse.png": FEMALE_SKIN,
    }
    with ZipFile(archive) as zf:
        for member, target in members.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                with zf.open(member) as src, target.open("wb") as dst:
                    dst.write(src.read())

    print("Human assets ready:")
    for path in (BODY_OBJ, MALE_SKIN, FEMALE_SKIN):
        print(" ", path)


if __name__ == "__main__":
    main()
