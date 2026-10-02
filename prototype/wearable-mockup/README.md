# Wearable inert mass-and-size mockup

This is a printable **fixed-closed assembly**, not a working computer or hinge.
The module is **92 mm along the forearm × 44 mm across × 6.6 mm**.
The complete closed top is **14.8 mm above nominal dorsal skin**, not 6.6 mm.
The two thin open cuff blades attach centrally. Their visible width grows from
12 mm to 28 mm, then narrows to a blunt tip. No hooks at the module ends and
no rigid hardware across the underside of the wrist are part of this design.

## Print the fit gauges first

No actual wrist measurements have been supplied. These are **nominal** profiles:

| Profile | Nominal wrist width × depth | Rigid-free underside opening | Total opening displacement to admit wrist + 1 mm |
|---|---:|---:|---:|
| slim | 52 × 36 mm | 46.56 mm | 6.44 mm |
| average | 58 × 42 mm | 51.49 mm | 7.51 mm |
| large | 64 × 46 mm | 56.40 mm | 8.60 mm |

The nominal radial clearance is 2.5 mm. The full C-shaped gauges represent
width, depth and the opening; they do **not** reproduce full-blade stiffness.
Use `plates/fit-gauges-TPU-first.3mf`, in TPU. Try them unloaded, briefly,
with an easy removal route. Stop for pressure, pain, tingling, numbness or
skin changes. Do not force a rigid PLA/PETG cuff onto a wrist.
These profiles do not promise that any particular person's wrist fits.
A thin removable soft liner may reduce play; repeat the unloaded fit check
with the liner. Never tighten a cuff merely to prevent all movement.

## Printable parts and material

| Part | Material | Print pose already saved in STL |
|---|---|---|
| tray, lid | PETG, or PLA for a brief indoor inert study | flat bottom down; open cavity/countersinks up |
| base | PETG or PLA | flipped: open hex-nut pockets up |
| left + right cuff of one profile | TPU, nominal 95A trial material | the common flat side down |
| dorsal protective pad | TPU | skin face down, shallow adhesive recess up |
| complete fit gauges | TPU | flat side down |

Use **one** rigid plate and **one** matching cuff plate (left blade, right blade and dorsal pad), not all profiles.
All plates fit inside a 220 mm square bed with margins and retain the chosen
orientation. Start with a calibrated 0.4 mm nozzle and 0.2 mm layers; these
are proposed settings, not a validated recipe for a particular printer.
Use at least four walls for rigid parts and a near-solid cuff for the first
unloaded fit test. TPU settings and material hardness change flexibility.
Keep temperature/speed/drying settings specific to the filament manufacturer.

The cuff has one flat axial face: its asymmetric hidden-to-visible taper
allows side printing without narrow ends starting in mid-air. The two bolt
holes have a teardrop roof in this print pose. The model needs no large
support bridges in these orientations. Inspect the actual slicer preview.
`3d printability` counts bed-contact bottom faces as overhangs; those advisory
warnings are not support-free certification. See the separate slicer results.
Never print `reference/` as one fused assembly. It includes metal reference
pieces, overlapping intended mating contacts, and assembly coordinates.

## Hardware (not printed)

- Four **M3 × 12 mm, DIN 965 H / ISO 7046-2, 90° Phillips countersunk** screws.
- Four **M3 DIN 934** hex nuts, nominal 5.5 mm across flats and 2.4 mm thick.
- Optional deburred steel insert, plus a thin adhesive/foam liner to immobilize it.

Do not substitute larger-head socket countersunk screws without modifying
and verifying the seats. The modeled screw envelopes have 5.6 mm heads,
0.2 mm nominal head recess, 2.3 mm axial nut/thread overlap and 1.2 mm tip
recess. Threads and head fillets are simplified, not manufacturing drawings.
Check the actual hardware and printed tolerances before wearing.

## Assembly, off the wrist

1. Clean the prints, remove strings and gently smooth all skin-contact edges.
   Check that screw holes and nut pockets are open; do not hammer nuts in.
2. Seat the four nuts in the base's underside hex pockets. Hold them in place
   while assembling, for example with removable tape. They are retained
   axially by the screws after assembly, not while the parts are separated.
3. Place the left and right cuff flanges on top of the base, then place the
   tray over them. Each flange has two aligned bolts to prevent free rotation.
4. For the first fit trial, leave the ballast out. Place the lid in its recess
   and tighten the four countersunk screws gently in a cross pattern.
   The nut pockets have a solid upper reaction roof; do not crush the TPU.
5. Check the lid is closed, both cuffs are secure, screw tips and nuts remain
   recessed, and no metal or sharp print edges can press on skin. Stop if the
   joint loosens, cracks or the opening cannot be used comfortably.
6. Cover the underside of the dorsal base with the printed TPU pad. Its
   shallow upper recess accepts approximately 0.2 mm adhesive tape; the rim
   should sit against the base, without an additional full-thickness tape
   layer. This pad protects the nut pockets and brings the nominal skin
   contact to Z=0 while the closed top remains at 14.8 mm. Recheck that no
   hardware can contact skin. Replace loose adhesive; do not rely on it
   for structural retention of the cuff.
7. Remove the whole mockup before opening the lid or changing ballast. Repeat
   the off-wrist retention check and weigh the entire assembly after changes.

## Real ballast capacity, not a fabricated final mass

The included steel-cutting outline is **37 × 83 mm**, with rounded corners
and four clearance holes. A 2.5 mm-thick version fits inside the actual bay
around the four bosses. It needs deburred edges and a thin bottom adhesive
layer plus compressed soft packing under the lid so it cannot rattle.

Its modeled steel capacity is **55.9 g** at an assumed density of 7.85 g/cm³.
The actual finished insert must be weighed. No loose washers, pellets or
live batteries belong in the mockup. `reference/steel-insert-cut-outline-1to1.svg`
is a metal-cutting template, not a printable part that magically weighs 55.9 g.

Weigh the printed assembly **including screws, nuts and packing** first.
Then calculate a requested study load, for example:

```sh
python generate.py --mass 48 80
```

This asks for 32 g above a measured 48 g empty assembly. It is not a claim
that every print weighs 48 g or that 80 g is comfortable. The calculator
rejects targets below the measured empty mass or beyond the available
insert capacity. Infill and TPU settings alter printed mass. 100–200 g is
not presumed acceptable or achievable; no final electronics mass is known.
The current ballast location tests a dorsal load, not production battery
mass distribution. Record location as well as total mass in the wear diary.

## Rebuild and verify

Install `requirements.txt` in a Python environment, then run `python generate.py`.
The existing `~/xp/3d-cli/.venv/bin/python` is the tested local environment.
`qa/assembly.json` records actual volumes, transforms, export hashes and
Boolean checks. `parts/` is print-oriented, `reference/` is assembly-oriented.
Run repository `scripts/check-wearable.sh` for actual mesh, printability,
3MF packing and slicer checks; `render.py` runs in Blender on exported STLs.
No command sends a job to a printer. Do not use another printer's G-code.

## What verification does and does not mean

The exported parts are closed connected positive-volume meshes. The code
checks unintended volumetric intersections, nominal wrist intrusion, nut
reaction roofs, remaining head-bearing material, screw end recess and the
actual inserted ballast, not only nominal bounding boxes. The full opening
is measured from lower cuff geometry. Exact thread engagement is represented
by axial envelopes, not modeled helical threads.

`3d-cli` topology checks explicitly leave general geometric self-intersection
unverified where its optional triangle-intersection backend is unavailable.
Boolean checks and a successful slicer run are useful but do not certify
strength, layer adhesion, comfortable pressure, fatigue, grip or retention.
No physical print, assembly, wear, winter-clothing or movement trial has run.
Do the first fitting unloaded; add measured ballast gradually only after the
joint and removal path have been checked. Do not trial experimental gear in
traffic, while carrying a child, asleep, or where a snag could trap the arm.

## Sources for purchased-material assumptions

The dimensions above are design choices except the nominal purchased
fastener envelope. Manufacturer/supplier references do not validate this CAD:
- [M3 × 12 Phillips DIN 965 H specification](https://www.accu.co.uk/phillips-countersunk-screws/66064-SIK-M3-12-A4).
- [M3 DIN 934 nut specification](https://www.accu.co.uk/hexagon-nuts/766460-NUT203M3-B).
- [Prusa flexible-material printing guide](https://help.prusa3d.com/article/flexible-materials_2057).

## Printer-neutral and configured projects

`plates/*.3mf` contains the original 220 mm layouts without a machine
profile. The generic files open correctly, but Orca's empty default profile
cannot slice them until a real printer/process/filament profile is selected.
That exact failure is retained in `qa/bare-project-profile-limitation.txt`.

`plates/snapmaker-u1/*.3mf` contains separate **unsliced** copies configured
from OrcaSlicer's bundled **Snapmaker U1, 0.4 mm nozzle, 0.20 Standard**
profiles, with **four walls, 95% infill and supports off**. The rigid plate
uses the bundled PETG preset; cuffs, pad and gauges use the TPU 95A preset.
These are proposed first-test settings, not a physical print qualification.
Confirm your nozzle and actual filament before printing. Geometry, part
count, orientation and bed fit are checked again after profile export.

The configured projects are checked by `3d slice-check`, including real
headless slicing. Temporary G-code is not included in the delivered files
and no printer job is sent. The receipt is per project in `qa/U1-*-slice.txt`.
Profile versions and file hashes are recorded in `qa/configured-projects.json`.

For the first print and assembly, see [the Russian quickstart](QUICKSTART-RU.md).
