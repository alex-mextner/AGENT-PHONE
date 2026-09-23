# AGENT-PHONE Visual Rebuild Design

Status: implementation-ready design derived from the user's reviewed handoff and render critique.

## Outcome

The repository must show a believable wrist computer rather than the current oversized slab. The new visual baseline is an open-cuff device whose display is roughly the footprint of two Apple Watch Ultra faces joined into one uninterrupted landscape screen.

The final imagery has two jobs:
- prove industrial-design proportions and mechanics;
- show believable day-to-day use directly on a human wrist.

The public repository should never require a reader to know or care that Blender produced the images. The gallery heading is **Concept renders**.

## Geometry baseline

The display module is approximately 94 × 45 mm outer size, with an active area around 91 × 42 mm. This is intentionally close to two 49 × 44 mm Apple Watch Ultra cases joined along their 49 mm direction, not a phone-width slab.

The long axis of the module runs **across the wrist**. The short axis follows the forearm/strap direction. A technical comparison render places **two** Apple Watch Ultra-sized reference blocks side by side with the device and labels the dimensions.

The screen is a single continuous surface. There is no visual split into two watch faces.
## Cuff and batteries

The base device is an open bracelet/cuff, not a watch strap with a buckle.

Two curved rigid/semi-rigid battery plates descend around the left and right sides of the wrist and stop before the underside desk-contact zone. They are physically continuous with the central base and visually read as part of one object.

The plates are asymmetrical only where wrist anatomy requires it. They must never appear as floating bars detached from the product.

The underside of the wrist remains free of a rigid battery brick or clasp so the hand can rest on a table, laptop palm rest, or keyboard edge.

A later Dive variant may add a positive clasp; the main render set shows the open cuff.

## Display and bezel

The cover glass is edge-to-edge and visually dominant. Structural metal/polymer sits underneath it rather than forming a thick picture-frame bezel.

Target visible border is approximately 0.7–1.0 mm at the left/right edges and 1.0–1.5 mm at the short ends, subject to the concept model.

The display is emissive OLED/LTPO-like: black UI areas should visually disappear into the glass.
## Tilt and detach mechanism

The screen tilts toward the user's eyes while the forearm rests naturally.

The hinge is not a large exposed barrel. The mechanism uses two short recessed pivots or a thin flexure/carrier hidden below the display edge. Closed, it should read as a thin seam.

Required mechanical states:
- closed;
- about 25–30°;
- about 50–55°;
- detached display/compute module;
- exploded carrier showing magnets/latch, power/data contacts, and the small reserve battery.

The detachable module is the compute/display unit. Its reserve cell is for a short standalone interaction, not primary endurance. The main battery mass remains in the cuff plates.

## Human model and realism

The current cylinder-and-sphere arm is rejected.

Hero and usage images must use either:
- a licensed photorealistic 3D hand/forearm asset; or
- a real licensed photograph used as a Blender compositing/background plate with correctly matched perspective and shadows.

The asset source and license must be documented in the repository. MakeHuman core assets/output are acceptable because the project documents them as CC0; BlenderKit assets are acceptable only if their individual license is recorded.

At least one thin/small wrist and one average wrist should be represented across the gallery so scale is not hidden by one body type.
## UI baseline

All product UI examples appear on the worn device, not as isolated flat mockups.

Home/status view:
- compact time;
- next calendar event;
- delivery ETA/status;
- long-running AI/deep-research progress;
- only a small number of high-value states.

Chat view uses the wide screen properly:
- left column: compact chat list with avatars, names, unread/activity state;
- right pane: current conversation with several short messages;
- bottom/right input-state indicator rather than a giant empty canvas.

Other required UI states:
- marketplace product + buy action;
- split chat + photos;
- TV / AC / lighting controls;
- blind/screen-off composition with only a tiny input indicator;
- media/display handoff;
- AI research result/progress;
- calendar/navigation;
- camera viewfinder/remote shutter context.

Typography must remain readable at realistic wrist size without giant headings.
## Scenario render set

Mechanical / scale:
1. orthographic top comparison with Apple Watch Ultra reference;
2. orthographic side closed;
3. side at 30°;
4. side at 55°;
5. open-cuff underside view;
6. exploded hinge/detach mechanism;
7. detached module in hand.

Lifestyle / product:
8. home/status while seated;
9. chat list + thread;
10. marketplace purchase;
11. split chat + photos;
12. smart-home remote;
13. blind composition with screen almost off;
14. media handoff to TV;
15. ring pointing/selecting a room device;
16. glasses companion / gaze + ring;
17. detachable camera tile used as camera while wrist/glasses act as viewfinder;
18. desk/laptop scenario proving the underside remains unobstructed;
19. outdoors quick navigation;
20. Dive variant concept.

The gallery may contain more renders, but these form the acceptance baseline.

## Moodboard

Create a real visual moodboard, not only a prose reference list.

Each reference entry contains:
- visual thumbnail or externally hosted image preview;
- source link;
- category;
- KEEP;
- AVOID;
- WHY.

Categories include film/game wrist computers, real wearables, open cuffs, tilting displays, flexible OLED concepts, landscape wrist UI, rings/spatial control, glasses, and detachable cameras.

The supplied Novate wrist-computer reference is included specifically for its open-bottom cuff and tilting display. Its keypad-heavy industrial form is not copied.
## Repository presentation

Canonical repository name: **AGENT-PHONE**.

README first mentions should link to:
- Agent OS;
- Telekinesis research;
- Agent Ring/spatial input;
- Agent Glasses concepts where described;
- Agent Camera strategy;
- Passport / Sapio State.

The public gallery uses the heading **Concept renders**. Blender implementation details live only in the render-pipeline documentation.

Existing incorrect images may be replaced in-place only after the new files have been manually inspected.

## Verification

Automated checks cover:
- dimensional constants;
- display/forearm orientation;
- bezel ratio;
- open-cuff clearance;
- required scenario names;
- required UI texture dimensions;
- no object-level bounding-box intersections between display and cuff in closed/tilted states beyond intended hinge/contact regions.

Blender renders are then inspected manually at full resolution for:
- human anatomy/perspective;
- clipping/intersections;
- floating parts;
- orientation;
- scale;
- material/texture breakage;
- UI readability;
- hinge visibility;
- bezel thickness.

A render that fails visual review is not committed merely because the script completed.
