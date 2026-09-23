# Display, silicon, battery and connectivity

## Display recommendation

### V1: LTPO OLED

The first prototype should target a custom **LTPO3-class OLED** or equivalent low-refresh emissive OLED:
- true per-pixel emission and deep black;
- ~1 Hz or lower low-power idle modes;
- wide viewing angle because the device is often tilted;
- excellent contrast for sparse screen-off indicators;
- thin flexible substrate options.

A polarizer-free stack is especially attractive. Samsung Display's Eco²OLED architecture reports 33% higher light transmission and up to 25% lower panel power versus a conventional polarizer-based OLED stack:
https://global.samsungdisplay.com/31141?type=main

Treat those numbers as vendor-specific, not a guaranteed Screen saving.

### Tandem OLED

Tandem OLED stacks can trade extra emissive layers for brightness, lifetime and/or lower operating current. If a supplier can deliver a thin custom wearable panel, it is worth evaluating together with polarizer-free optics.

### MicroLED

MicroLED is now a real smartwatch technology, not science fiction. Garmin's 2025 fēnix 8 Pro MicroLED uses more than 400,000 individual LEDs and advertises up to 4,500 nits:
https://www.garmin.com/en-US/newsroom/press-release/wearables-health/introducing-fenix-8-pro-the-first-ever-smartwatches-from-garmin-with-inreach-technology-for-satellite-and-cellular-connectivity/

However, the MicroLED model is significantly more expensive and has lower quoted smartwatch battery life than Garmin's AMOLED sibling. For Screen, MicroLED is a future premium option; OLED is the lower-risk V1.

## Screen power strategy

Hardware only helps if the UI cooperates:
- black is the default canvas;
- screen stays fully off during blind composition;
- a few status pixels may show listening / confidence / sent;
- refresh drops aggressively for static cards;
- animations are short and local;
- video defaults to handoff;
- optional glasses may show transient text while the wrist screen stays dark.

## Compute platform

Qualcomm's Snapdragon Wear Elite, announced in March 2026, is unusually close to Screen's requirements:
- 3 nm wearable architecture;
- dedicated NPU;
- 5G RedCap;
- Micro-Power Wi-Fi;
- Bluetooth 6;
- UWB;
- GNSS and NB-NTN;
- Linux / Android / Wear OS support.

Official overview:
https://www.qualcomm.com/wearables/products/snapdragon-wear-elite-platform

This is a reference target rather than a locked supplier decision. The architecture should allow an equivalent low-power Linux/Android wearable SoC.

## Cellular

**eSIM only.** There is no physical SIM tray.

5G RedCap is preferred because it is designed for reduced-capability devices that do not need flagship-phone throughput. Screen should prioritize standby efficiency, messaging, calls, navigation and AI coordination over sustained video bandwidth.

Large model inference should normally be hybrid:
- local intent / input decoding / privacy-sensitive features on-device;
- nearby trusted devices when present;
- cloud for large AI workloads;
- progressive results so the user can leave the main display off.

## Battery architecture

Use energy in Wh for engineering decisions even though mAh is convenient for product discussion.

At ~3.85 V nominal:
- 150 mAh ≈ 0.58 Wh;
- 2,500 mAh ≈ 9.6 Wh;
- 3,000 mAh ≈ 11.6 Wh.

The detachable module should not carry phone-scale energy. Its reserve cell exists to survive detachment and short hand-held use. The base and two curved wings carry most energy.

### Cell technology for prototypes

Use proven Li-ion/Li-poly pouch chemistry with high-silicon-anode variants where a reputable supplier can certify cycle life and swelling. Split cells into mechanically isolated curved/segmented cavities instead of forcing one large pouch around a tight bend.

Research tracks:
- semi-solid / solid-state cells for higher packaging freedom;
- structural battery strap segments;
- curved custom pouch cells;
- wireless/galvanic power bridge across the hinge carrier.

Do not base the first ergonomic prototype on lab-only chemistry.

## External endurance pack

An optional external battery can attach by a flat, clothing-integrated cable or decorative illuminated cable and live under clothing at the torso. It is an accessory, never required for normal operation.

The core industrial design must remain useful with no cable attached.
