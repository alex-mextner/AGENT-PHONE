# Hardware architecture

Updated: 2026-09-23

## Principle: never cold-boot for an interaction

AGENT should feel instantly awake because the application processor normally **suspends**, rather than shutting down. A tiny always-on domain remains active for radios, gestures, sensors, haptics and wake decisions.

The architecture is intentionally asymmetric:

- **Always-on controller**: notifications, gesture classifier, ring/glasses links, low-rate sensor fusion, haptics, wake policy.
- **Application SoC**: UI composition, browser/media codecs, larger local models, camera processing and rich apps/micro-apps; normally asleep.
- **Cellular**: low-power signaling must not require waking the application SoC.
- **Display**: stays black unless the interaction actually benefits from pixels.

This is more realistic than rebooting a RAM-only OS for every interaction. Suspend-to-RAM plus persistent local state gives the instant-on behavior the product needs.

## Final-product compute target

Qualcomm Snapdragon Wear Elite is the closest currently announced reference architecture:
- 3 nm process;
- dedicated NPU up to 12 TOPS;
- support for up to 2B-parameter on-device models;
- 5G RedCap, Micro-Power Wi-Fi, Bluetooth 6, UWB, GNSS and NB-NTN;
- "Intelligent Low-Power Islands";
- eMMC support up to 64 GB.

Official:
https://www.qualcomm.com/wearables/products/snapdragon-wear-elite-platform

This does not mean the product is locked to Qualcomm. The important properties are the heterogeneous low-power islands, wearable thermal envelope, integrated connectivity and hardware video/AI blocks.

## Always-on companion

### Product architecture

Use a tiny MCU / low-power island for:
- packet and notification triage;
- ring and accessory BLE;
- wrist/ring IMU fusion;
- simple sEMG/gesture classifier;
- haptic feedback;
- sparse display status;
- wake-word / event detection where appropriate;
- secure wake of the application SoC.

A notification classifier does not need an LLM. Start with rules plus a tiny quantized classifier. It should decide things such as:
- ignore until later;
- haptic only;
- show one-line status;
- wake application SoC;
- urgent call/alarm.

### Cellular research option: nRF9161

Nordic nRF9161 combines an Arm Cortex-M33 application core with LTE-M/NB-IoT and GNSS, 1 MB flash and 256 KB RAM.

https://www.nordicsemi.com/Products/nRF9161
https://www.digikey.com/en/products/detail/nordic-semiconductor-asa/NRF9161-LACA-R/22107874

It is a good prototype for **low-power notification/data connectivity**, not a substitute for smartphone-class broadband. LTE-M/NB-IoT is intentionally constrained.

For early AGENT prototypes, the cleanest sequence is:
1. Wi-Fi/BLE tether for rich data;
2. nRF91-class cellular for always-on messaging experiments;
3. 5G RedCap wearable platform for the integrated product.

## Two compute rails

### Rail A — always on

Typical state:
- MCU active intermittently;
- BLE connected;
- cellular paging / low-rate data;
- IMU interrupt mode;
- sEMG only while armed or sampled at a low duty cycle;
- OLED entirely off or only a few pixels active.

### Rail B — application

Wake on:
- display raise/tilt;
- explicit ring/sEMG command;
- call;
- camera capture;
- AI request requiring local compute;
- rich UI handoff.

The app processor should return to suspend immediately after the interaction rather than waiting for a phone-style screen timeout.

## Prototype compute choices

### P0: laptop/phone off-body

For validating industrial design and input, the first wrist prototype should not carry a Linux SBC at all. A small BLE MCU in the cuff streams input to a nearby computer. This keeps the prototype thin enough to test the actual ergonomics.

### P1: Milk-V Duo S-class board

An inexpensive embedded Linux/RTOS board can validate local services, UI protocol and wake domains, but its square development-board shape does not represent final packaging.

Official:
https://milkv.io/duo-s

### P1 alternative: Raspberry Pi Zero 2 W

Useful for camera/UI integration and cheap enough to treat as disposable prototype hardware. It is 65 × 30 mm and should live in an oversized engineering cuff, not be mistaken for final packaging.

https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/

### Bench prototype: Compute Module 5

CM5 gives a powerful Linux environment, camera/display I/O and up to 64 GB eMMC, but at 55 × 40 × 4.7 mm it is too large and power-hungry for the final wrist computer.

https://www.raspberrypi.com/products/compute-module-5/

Use it only for bench integration and software development.

## Storage

The user's desired split — small fast system storage plus a much larger "heavy file" store — is sensible, but an M.2 NVMe SSD is the wrong final form factor.

### Product target

- **64 GB** soldered system storage for OS, local entities, models and rollback slots.
- **512 GB** optional high-density UFS / managed NAND package for media, cached datasets and local AI assets.
- Encryption keys held by the secure element / hardware-backed keystore.
- All storage treated as a local cache of user-owned objects, not an app silo.

A soldered UFS/NAND package avoids the connector, controller idle power and physical envelope of an M.2 SSD.

### Prototype

Use microSD or a tiny USB/NVMe adapter off-body during software work. Do not distort wrist industrial design to accommodate it.

## Display interface

The prototype display is likely MIPI-DSI. The application board can initially sit off-wrist if necessary, with a flexible cable into the display.

The final display controller should support:
- per-pixel emissive black;
- very low static refresh;
- self-refresh / panel RAM if supplier offers it;
- partial updates;
- display wake controlled from the always-on domain.

## Battery / power domains

Use at least three independently switchable rails:
1. always-on MCU/radios;
2. display/touch/haptics;
3. application SoC/storage/camera.

The detachable screen reserve cell only bridges:
- detachment;
- a short handheld interaction;
- graceful sleep/shutdown if it is not returned to the base.

Most energy belongs in the curved cuff/battery wings.

## Cuff construction

The base version uses a wraparound cuff rather than a conventional watch strap:
- two curved PETG shells for the first prototype;
- flexible inner liner against skin;
- split battery compartments above and below the screen;
- no rigid closure under the wrist;
- enough spring/compliance to slip over the hand or open laterally.

The **Dive** variant may use a real buckle/ratchet because security over a wetsuit matters more than desk comfort.

## No physical buttons

The prototype deliberately omits buttons.

Hard recovery should still exist through:
- hidden magnetic/reed service trigger;
- charger/dock sequence;
- capacitive service pad;
- debug pads inside the shell.

Normal interaction uses touch, ring, gestures, haptics and voice.

## Security boundary

The always-on controller must not become an ambient master key. It receives narrow capabilities:
- wake display;
- vibrate;
- read specific sensor streams;
- accept authenticated accessory packets;
- request a higher-trust agent action.

Sensitive effects remain capability-gated in Agent OS.
