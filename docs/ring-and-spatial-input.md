# Agent Ring and spatial input

Updated: 2026-09-23

## Purpose

A ring is not a miniature smartwatch. Its job is to give AGENT tactile, eyes-free and spatial controls that remain available when the wrist display is dark or when optional glasses are the active display.

The ring should work alone for simple input and fuse with the wrist device, glasses cameras, UWB anchors and room context for spatial interaction.

## Interaction vocabulary

### Eyes-free tactile controls
- tap / double tap the ring with the thumb;
- press or squeeze two sides of the ring;
- slide or rub the thumb along a capacitive arc;
- short/long stroke for scroll and scrub;
- "virtual rotation": pinch the ring and drag around its outer capacitive arc without physically rotating the ring;
- physical rotation is an optional later experiment, not a V1 requirement;
- tap ring against another finger for discrete commands.

Suggested default mappings:
- vertical thumb slide: volume / brightness / list scroll;
- tap: play/pause, accept, select;
- double tap: next item;
- squeeze: back / cancel or modifier;
- squeeze + slide: coarse/fine adjustment;
- long press: arm Telekinesis / spatial mode.

## Mid-air gestures

The ring IMU provides a stable local motion trace while the wrist IMU provides forearm orientation. Optional glasses cameras provide visual hand pose and scene geometry.

This enables:
- point at a TV, lamp, speaker or air conditioner to select it;
- point + twist wrist to change volume / temperature / dimming;
- point + tap to toggle;
- move a selected object from the wrist display toward another screen;
- "air copy": grab a card/photo/object, point to another device, release;
- switch apps by swiping the hand laterally in front of the wrist device;
- rotate 3D objects by pinching and rotating the hand;
- resize windows on glasses with pinch-spread gestures;
- drag content between wrist, glasses, TV and another person's AGENT.

These must be explicit, mode-gated gestures. Random hand movement must not cause actions.

## Why the idea is technically credible

### RingGesture
RingGesture is a published mid-air typing system that uses an IMU-equipped ring and deep-learning word prediction. It reported 27.3 WPM average and 47.9 WPM peak in its evaluation.

https://pubmed.ncbi.nlm.nih.gov/39250409/

This makes a ring a credible fallback text-entry modality, especially when glasses provide a virtual keyboard or spatial target.

### PointRing
PointRing (IMWUT 2026) studies device selection using a UWB + IMU smart ring without repeated manual calibration.

DOI: https://doi.org/10.1145/3810225

### SeleCon
SeleCon demonstrates the same core interaction pattern at wrist scale: inertial sensing detects pointing and UWB identifies the target device, with UWB activated only when needed to save power.

https://pmc.ncbi.nlm.nih.gov/articles/PMC5909733/

### IRIS
University of Washington's IRIS ring combines a camera, Bluetooth, IMU and battery. It recognizes the pointed-at device from the scene and uses contextual gestures for control.

https://iris.cs.washington.edu/

### PeriSense
PeriSense shows that capacitive proximity around a ring can sense adjacent fingers and multi-finger gestures up to roughly 2.5 cm in its experiments.

https://pmc.ncbi.nlm.nih.gov/articles/PMC7411889/

### picoRing
picoRing is especially interesting for AGENT because it demonstrates fully passive rings read by a wristband over inductive coupling. The paper reports 1.5 g ring prototypes supporting pressing, sliding and scrolling without a battery in the ring.

https://arxiv.org/abs/2411.13065

This suggests a long-term architecture where the wrist computer powers/reads one or more ultra-light rings.

## Prototype architecture

### V0 — fast DIY ring
- Seeed XIAO nRF52840 Sense;
- onboard IMU;
- copper / flex-PCB capacitive arc;
- one thin force or strain element for squeeze;
- tiny LiPo;
- BLE to AGENT;
- PETG shell.

This is larger than a final ring but is fast to build.

### V1 — custom PCB
- nRF54L-class BLE MCU or equivalent;
- BMA400-class low-power accelerometer plus gyro only when spatial mode is armed;
- segmented capacitive electrodes around the outer circumference;
- one or two strain gauges / force sensors;
- haptic click actuator if packaging allows;
- 15–30 mAh curved battery;
- inductive charging.

### V2 — spatial ring
Add UWB only if target selection needs it. Qorvo QM35825 is a compact 4.08 × 3.38 × 0.63 mm UWB SoC and supports ranging plus angle-of-arrival functions.

https://www.qorvo.com/products/p/QM35825

For the first room-control prototype, UWB does not need to be in every appliance. A small UWB/BLE bridge can be attached near a TV or speaker and mapped to the device in Agent OS.

### V3 — battery-free companion rings
Prototype a picoRing-style passive ring whose switches/capacitive elements are inductively read by the wrist base. This is attractive for a second ring on another finger because it avoids charging two rings.

## Glasses fusion

Glasses are the best spatial reference because their camera sees what the user sees.

Fusion pipeline:
1. glasses estimate device positions and hand keypoints;
2. ring IMU supplies high-rate orientation/motion;
3. wrist IMU supplies forearm pose;
4. UWB provides identity/range when ambiguous;
5. Agent OS resolves the selected durable entity (TV, speaker, light, person, file);
6. a deliberate click/squeeze commits the action.

The camera should not be continuously uploaded. Scene semantics and hand/device pose should be reduced locally to compact features when possible.

## Health sensors in the ring

Possible additions:
- PPG for pulse / HRV / SpO2 experiments;
- skin temperature;
- skin-contact / wear detection;
- EDA only if electrode contact is reliable;
- overnight motion / sleep sensing.

Health sensing competes directly with ring thickness, battery and electrode area. For the first control ring, interaction quality takes priority. A dedicated health ring can be a later accessory.

## Multi-ring mode

Two rings can create a richer chord vocabulary:
- thumb-to-index ring: pointer/select/scroll;
- middle-finger ring: modifier / clutch;
- pinch between two instrumented fingers: 3D grab;
- relative orientation between rings: rotate/scale;
- ring-to-ring touch: explicit pairing or transfer gesture.

The system should remain fully useful with one ring. Multiple rings are an optional expert configuration.
