# Camera strategy

Updated: 2026-09-23

## Problem

A wrist is a poor primary camera position. Framing requires an unnatural arm pose, the angle is wrong for many subjects, and a wide wrist computer already has enough thickness pressure.

Glasses are better for point-of-view capture and spatial understanding, but they do not always produce the composition, lens choices or image quality people expect from a phone camera.

AGENT therefore should not pretend that one fixed wrist camera solves photography.

## Proposed camera system

### 1. Glasses camera = context camera

The glasses camera is always the best place for:
- spatial mapping;
- identifying what the user points at;
- reading QR codes / labels;
- low-friction first-person memories;
- video calls from the user's perspective;
- hand tracking for ring gestures.

It is *not* the only camera.

### 2. Detachable camera tile = deliberate photography

A small magnetic camera tile is the preferred phone-camera replacement.

The tile can:
- dock to the wrist base or battery wing for charging;
- clip to clothing / a pendant / bag strap;
- be held between two fingers for conventional framing;
- stick magnetically to metal surfaces;
- use the wrist display or glasses as a live viewfinder;
- use the ring as shutter / zoom / exposure control.

This is much more natural than rotating the entire wrist computer toward the subject.

A useful existing reference is the detachable/wearable direction of Hohem Eyepic:
https://www.hohem.com/product/eyepic

And the scale benchmark is Insta360 GO 3S: about 25.6 × 54.4 × 24.8 mm and 39.1 g. AGENT's camera tile should be materially thinner and lighter than that because it can borrow compute/storage/viewfinder from the wrist computer.

https://onlinemanual.insta360.com/go3s/en-us/faq/specs/hardware

### 3. Wrist camera = optional utility sensor

If a wrist camera exists, keep it small and use it for:
- document/QR scan while holding an object;
- environment context;
- emergency capture;
- device tracking for spatial gestures.

Do not optimize the industrial design around it.

## Prototype camera modules

### Raspberry Pi Camera Module 3

A practical first prototype camera:
- Sony IMX708;
- 12 MP;
- autofocus;
- HDR mode;
- 25 × 24 × 11.5 mm;
- standard or 120° wide lens;
- about $25–$38.50 depending version.

Official:
https://www.raspberrypi.com/products/camera-module-3/

This is too thick for a polished final tile but excellent for proving the camera workflow.

### Waveshare OV5647 OIS module

For stabilization experiments:
- 5 MP;
- dual-axis optical stabilization;
- ±5° compensation;
- 6 g;
- about $52.

https://www.waveshare.com/OV5647-70-5MP-OIS-Camera.htm

The resolution is modest, but it proves that the tile can have real optical stabilization independent of the wrist.

### Arducam IMX219 autofocus USB

Useful when the main prototype exposes USB rather than CSI:
- 8 MP;
- autofocus;
- UVC;
- about $34.99.

https://www.arducam.com/8mp-hdr-autofocus-usb-camera-module-with-metal-housing-1080p-mini-uvc-usb2-0-webcam-a219.html

## Final-product direction

For a custom board, target:
- 1/1.3"–1/1.7" main sensor if thickness permits;
- OIS or sensor-shift if the module can stay under roughly 8–10 mm;
- autofocus;
- one good wide/normal lens rather than multiple mediocre cameras;
- computational multi-frame HDR;
- burst buffer in the camera tile;
- UWB/BLE for discovery and low-rate control;
- high-rate transfer over Wi-Fi Direct or a dock connector.

A second telephoto camera belongs in an optional photography accessory rather than making the base wrist computer thicker.

## Viewfinder model

The user should be able to choose any display:
- wrist panel for ordinary framing;
- glasses HUD for eye-level framing;
- TV/monitor for tripod-style shots;
- another AGENT device as a remote monitor.

The camera tile is a sensor/lens/buffer device, not a miniature phone.

## Ring controls for photography

Suggested vocabulary:
- point camera + ring tap: focus;
- ring squeeze: shutter;
- thumb slide on ring: exposure compensation;
- double tap: switch photo/video;
- pinch + wrist roll: zoom;
- long squeeze: lock AE/AF;
- two-ring chord: manual parameter mode.

## Privacy

Glasses and tile cameras need unmistakable capture indication. Spatial mapping can be processed locally without retaining raw video. Recording a photo/video and background scene understanding are separate permissions and separate visible states.
