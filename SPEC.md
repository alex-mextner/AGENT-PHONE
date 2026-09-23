# AGENT — Product Specification

Status: concept / feasibility prototype
Working product name: **AGENT**
Working identity-layer name: **Passport**
Working input-system name: **Telekinesis**

## 1. Problem

A phone occupies a hand, pocket or bag, is easy to misplace, pulls on one side of clothing, and defaults most software to a narrow portrait viewport. AGENT is intended to make common communication, AI, navigation, purchasing and control tasks available without carrying a phone-shaped object.

It is deliberately not a replacement for every screen. Video and long-form visual work are better on a TV, monitor, tablet or glasses. Games are intentionally excluded from the core device.

## 2. Industrial design

### 2.1 Display module

Prototype envelope:
- active display target: about 96–102 mm × 40–44 mm — approximately two Watch Ultra-sized faces side by side;
- landscape aspect ratio roughly 2.2–2.5:1, with UI designed as a wide workspace;
- left/right visual border target below 1 mm where manufacturable;
- module thickness target: 5.5–6.5 mm before protective glass curvature;
- rounded corners and no visual split between "two watches."

The display module contains the primary SoC, RAM/storage, eSIM radio path, antennas that cannot live in the base, microphones, wireless radios, haptics/audio interfaces, and a small reserve cell.

### 2.2 Base and battery wings

The base remains on the wrist. It holds the main battery, power management, wrist sensors, the haptic actuator, and the mechanical carrier for the detachable module.

Two battery wings extend **along the wrist/cuff direction** from the top and bottom edges of the base. They curve around the wrist and become the transition into the body of the cuff. They must not protrude from the left and right sides of the screen.

The base model is a wraparound bracelet/cuff rather than a conventional watch strap with a buckle. A Dive variant may use a secure buckle/ratchet for wetsuit use.

There is no rigid battery pack or clasp at the underside of the wrist, because that surface contacts a desk, keyboard and laptop.

### 2.3 Hidden tilt mechanism

The hinge must visually disappear when closed. The first prototype uses a thin carrier plate that stays with the base:
- two short friction barrels, approximately 2.2–3.0 mm diameter, recessed below the far long edge;
- hinge axis parallel to the long edge of the screen;
- closed, ~30° and ~60° positions;
- a hard mechanical stop before ~70°;
- no large central barrel or exposed camera-style hinge.

The detachable screen docks to the tilting carrier with magnets plus a positive latch. Spring contacts provide power/data. A short slide-and-lift motion prevents accidental vertical release.

Separating "tilt" from "detach" keeps the screen module thin and lets the carrier take mechanical loads.

### 2.4 Battery allocation

Prototype target, assuming ~3.85 V nominal Li-ion chemistry:
- detachable module: ~100–180 mAh (~0.4–0.7 Wh), sized for at least a short 10-minute standalone interaction;
- base + curved wings: ~2,100–3,000 mAh (~8–12 Wh) depending wrist size and thickness;
- stretch target around 3,200 mAh only if comfort tests permit.

Capacity is a packaging target, not a promise. Wh, discharge curve, radio duty cycle and display behavior matter more than mAh alone.

For the first physical prototype, use conventional high-energy-density Li-ion/Li-poly pouch cells in segmented curved compartments. Treat solid-state and exotic structural batteries as research tracks until suppliers offer validated cycle life, safety and form factors.

## 3. Screen behavior

The display is normally dark. Always-on information uses only a few emissive pixels where useful.

Home / lock state should show:
- current time, compactly;
- next calendar event and whether it is confirmed;
- food-delivery ETA/status;
- status of long-running AI work such as deep research;
- only urgent notifications, not a feed.

Primary visual tasks:
- marketplace browse and purchase;
- Telegram-like messaging;
- split view: chat + photos;
- TV / air-conditioner / lighting control;
- maps and short navigation;
- AI assistant status and results;
- quick document/credential views.

Video should offer "play here" only as an exception and otherwise suggest the nearest trusted TV/display. Games are intentionally absent.

## 4. Screen-off composition

Telekinesis composition is designed to work with the display off:
1. User arms input with a deliberate gesture.
2. A tiny pixel indicator and one haptic pulse confirm capture.
3. Silent articulation, finger gestures or dictation enter text.
4. Word/phrase boundaries receive subtle haptic confirmation.
5. Low-confidence segments produce a distinct haptic pattern.
6. TTS or bone-conduction readback can speak the draft privately.
7. The user corrects with gesture, silent speech or voice.
8. Send is a separate deliberate action.

The system must never infer that ordinary private thoughts are input.

## 5. Multimodal controls

Required gesture vocabulary:
- thumb–index tap and double tap;
- pinch / squeeze;
- thumb rubbing or sliding against index finger;
- wrist flick away-and-back;
- wrist roll / pronation and return;
- wrist flex inward and return;
- finger chords recognized by sEMG;
- ring tap / double tap / squeeze / capacitive slide;
- ring "virtual rotation" by pinching and moving around its touch arc;
- gaze target + pinch when compatible glasses are present;
- point + confirm for room/device control;
- deliberate grab/move/release for cross-device object transfer.

Sensor fusion should combine sEMG, IMU, PPG, ring motion, optional UWB and glasses vision/contextual confidence rather than assigning every gesture to a single sensor. Spatial gestures are mode-gated so ordinary hand motion cannot trigger effects.

## 6. Companion devices

Optional companion nodes:
- **Agent Ring** with IMU, tactile/capacitive input, squeeze sensing and optional UWB/health sensing;
- glasses with a low-duty-cycle display, gaze sensing and camera-based spatial context;
- earbuds/headphones for private TTS, bone/air audio and acoustic silent-speech experiments;
- necklace/choker for optical PPG, strain or throat sensing;
- pendant as a microphone/compute/radio accessory;
- detachable camera tile for deliberate photography;
- optional external battery pack for exceptional endurance.

AGENT remains independently usable without these accessories.

## 7. Camera model

The wrist is not the primary photography position.

- Glasses camera: spatial context, hand tracking, QR/label scan and first-person capture.
- Detachable camera tile: deliberate photography, autofocus/HDR, clothing clip or handheld framing.
- Wrist camera: optional utility/context sensor only.
- Ring can act as focus/shutter/zoom/exposure control.
- Wrist display, glasses or another trusted screen can become the viewfinder.

See [Camera strategy](docs/camera-strategy.md).

## 8. Connectivity

- eSIM only.
- 5G RedCap-class cellular preferred for lower complexity/power than full smartphone 5G.
- Wi-Fi, Bluetooth and UWB for display handoff, accessories and proximity.
- GNSS may be integrated or delegated opportunistically.
- NFC should be considered for access/payment, subject to certification and secure-element architecture.
- A tiny always-on domain handles low-rate connectivity/notification triage while the application SoC sleeps.

## 9. Agent OS

AGENT is a hardware endpoint for [Agent OS](https://agentos-bible.vercel.app/). The UI should be entity/task-first rather than a grid of miniature phone apps. Ring, gaze and Telekinesis inputs publish typed intents/events into the capability system rather than injecting unrestricted key events.

See [AGENT hardware × Agent OS](docs/agent-os.md).

## 10. Privacy and safety

- Silent-speech capture is opt-in and visibly/haptically armed.
- Prefer local feature extraction and local inference for raw biosignals.
- Raw EMG/PPG/audio retention defaults to off.
- Personalized adaptation must be inspectable and resettable.
- Glasses cameras and microphones are not prerequisites for core operation.
- Authentication-sensitive actions require a second confirmation channel or explicit gesture.

## 11. Prototype acceptance tests

A prototype is useful only if it proves ergonomics:
- wrist can rest on a laptop palm rest and desk with no rigid underside obstruction;
- tilted screen is readable while forearm rests naturally;
- one-handed tilt/close/detach works without looking at the mechanism;
- closed hinge does not visually dominate the product;
- screen module cannot release from a knock;
- battery wings do not collide with wrist bones across a test set of wrist sizes;
- all UI demo states are shown on an actual wrist render.
