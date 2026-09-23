# Prototype BOM and sourcing plan

Updated: 2026-09-23
Currency: USD unless noted. Prices are single-unit web prices observed on the date above and exclude VAT, shipping and import fees.

The prototype should be split into **ergonomics**, **electronics**, **input**, and **camera** builds. Trying to fit every final subsystem into the first cuff will make the object too thick and teach us the wrong ergonomic lessons.

## 1. Display: the hardest single part

### Best off-the-shelf match found: 4.01" flexible bar AMOLED

Freetech currently lists a 4.01-inch flexible AMOLED for wearable devices:
- 960 × 162;
- MIPI interface;
- capacitive touch option;
- MOQ 1;
- Alibaba price range around **$50–$240** depending configuration.

https://www.alibaba.com/product-detail/Freetech-4-01-Inch-Flexible-AMOLED_1600318913593.html

A related HX401RAN10A panel lists approximately:
- outline 27.39 × 111.74 × 0.81 mm;
- active area 19.99 × 99.94 mm;
- 192 × 960;
- MIPI;
- RM69330 driver.

https://www.ecer.com/corp/details-uuuf92d-p1k3nvk-4-01-inch-flexible-amoled-display-192-960-dots-mipi-interface-driving-ic-rm69330-350c-d.html

**Recommendation:** buy one or two of these first. It is the closest readily sourced single continuous OLED to the desired long landscape shape.

**Limitation:** ~20 mm active height is visibly narrower than the target "two Watch Ultras side by side". It proves the interaction and hinge, not final proportions.

### Fallback display for software work

Waveshare's 1.75" AMOLED modules are small and square-ish, so they are wrong for industrial design but useful for firmware/UI bring-up.

Vendor:
https://www.waveshare.com/

Do not let this fallback redefine the product shape.

### Donor-panel route

A donor flexible phone OLED offers excellent pixels but creates three problems:
1. most are much taller than needed;
2. the panel cannot simply be cut;
3. reverse-engineering the MIPI initialization, touch and power rails may cost more time than the screen.

Use donor phone panels only if a known driver board exists.

### Custom panel later

After wrist geometry is validated, request a custom ~100 × 32–34 mm AMOLED/flexible OLED sample from vendors such as Wisecoco or Freetech.

https://www.wisecocodisplay.com/

Do **not** pay custom-panel NRE before the cardboard/PETG and bar-AMOLED prototypes confirm the dimensions.

## 2. Wrist electronics — P0 ergonomic prototype

Goal: prove comfort, cuff, battery-wing geometry, tilt, detachment and screen readability.

| Part | Qty | Current price / estimate | Notes |
|---|---:|---:|---|
| Freetech 4.01" flexible AMOLED | 1 | **$50–240** | Main long OLED, MOQ 1 listing |
| XIAO nRF52840 Sense | 1 | **$15.99** | BLE + IMU; can run cuff sensors without Linux |
| 1000–1200 mAh flat LiPo | 2 | **~$5–15 each** | One in each cuff wing for the crude prototype |
| 100–200 mAh thin LiPo | 1 | **~$4–10** | Reserve cell in detachable module |
| Charger + protection + regulators | 1 set | **$15–35 est.** | Use reputable protected cells/modules |
| Haptic actuator + driver | 1 | **$8–15 est.** | Tiny input feedback |
| Magnets, pogo pins, latch hardware | 1 set | **$15–30 est.** | Detach mechanism |
| PETG + TPU/liner allocation | — | **$10–20 est.** | Printed cuff and soft contact parts |
| FPC/wire/connectors | — | **$15–30 est.** | Display and service wiring |

**P0 target:** roughly **$150–$400**, dominated by which display/controller configuration the vendor ships.

The application UI may run on a nearby laptop during this stage. That is intentional.

## 3. Functional wrist prototype — P1

### Main compute option A: Raspberry Pi Zero 2 W

Official price: **$15**.
Size: 65 × 30 mm.
512 MB RAM, Wi-Fi/BLE, CSI camera.

https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/

Pros:
- cheap;
- mature Linux;
- camera support;
- enough to validate Agent OS protocols and UI streaming.

Cons:
- too long and power-hungry for the final device;
- no MIPI-DSI output suitable for every raw AMOLED without bridge hardware.

Treat it as a temporary engineering board.

### Main compute option B: Compute Module 5, bench only

Current official entry price: **from $67.50**.
Size: 55 × 40 × 4.7 mm.
eMMC options up to 64 GB.

https://www.raspberrypi.com/products/compute-module-5/

This is useful when the camera/UI stack needs much more CPU, but it should live off-wrist or in an intentionally oversized engineering cuff.

### Final-compute reference: Snapdragon Wear Elite

Not presently a hobbyist single-board purchase, but the architecture matches the product:
- 3 nm;
- NPU up to 12 TOPS;
- 5G RedCap;
- low-power islands;
- eMMC up to 64 GB.

https://www.qualcomm.com/wearables/products/snapdragon-wear-elite-platform

The prototype should therefore keep display, sensors and Agent OS services modular enough to move onto a wearable SoC later.

## 4. Always-on cellular / notification prototype

### Nordic nRF9161

DigiKey observed price: **$32.93** for the SiP; development kit about **$158.86**.

https://www.digikey.com/en/products/detail/nordic-semiconductor-asa/NRF9161-LACA-R/22107874
https://www.digikey.com/en/product-highlight/n/nordic-semi/nrf9161-development-kit

It combines LTE-M/NB-IoT, GNSS, Cortex-M33, 1 MB flash and 256 KB RAM.

**Use it to prototype the always-on plane**, not as the only final modem. LTE-M/NB-IoT is excellent for sparse messaging and notification experiments but not a substitute for the rich-data path expected from 5G RedCap.

Early rich networking can remain Wi-Fi/BLE tethered.

## 5. Battery

### Cheap sanity-check cell

Adafruit 2500 mAh 3.7 V LiPo:
- **$14.95**;
- 50 × 60 × 7.3 mm;
- 50 g.

https://www.adafruit.com/product/328

This cell proves why a single flat 2500 mAh brick is wrong for the final cuff: it is too large and heavy in one place. It is still useful on the bench.

### Final-shape research: Grepow curved cells

Grepow lists off-the-shelf and custom curved pouch cells for wearables. Current catalogue examples extend up to **1660 mAh** in a curved cell; custom dimensions are offered over roughly 0.5–11 mm thickness, 5.6–100 mm width and 11–100 mm length, with inner arc radius ≥8 mm.

https://www.grepow.com/shaped-battery/curved-battery.htm

This strongly supports the two-wing architecture.

**Prototype recommendation:** start with two ordinary flat ~1000–1200 mAh cells in separate printed wing cavities. After geometry is stable, send the CAD envelope to Grepow or another certified custom-cell supplier.

Do not bend a normal flat LiPo to make it fit.

## 6. Ring P0 BOM

| Part | Qty | Current price / estimate | Purpose |
|---|---:|---:|---|
| Seeed XIAO nRF52840 Sense | 1 | **$15.99** | BLE + onboard IMU |
| 15–30 mAh LiPo | 1 | **$4–10 est.** | Ring power |
| Copper tape / flex electrodes | — | **$2–8 est.** | Capacitive slide/rub surface |
| Force/strain element | 1–2 | **$5–15 est.** | Squeeze detection |
| Tiny charger / protection | 1 | **$4–10 est.** | Charging |
| PETG/resin shell allocation | — | **$2–5 est.** | Oversized first ring |
| Optional UWB dev module | 1 | **$59.37** | Spatial ranging experiments |

XIAO source:
https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html

Qorvo DWM3001C UWB module:
https://store.qorvo.com/products/detail/dwm3001c-qorvo/692453/

The DWM3001C is 27 × 19.13 × 3.2 mm, so it belongs on the wrist/bench in P0, **not inside the ring**.

For a custom ring PCB, Qorvo's QM35825 UWB SoC is much smaller:
https://www.qorvo.com/products/p/QM35825

## 7. sEMG / Telekinesis lab BOM

### MyoWare 2.0

Observed price **$43.50**, electrodes sold separately.

https://www.adafruit.com/product/6423

This module is far too large to integrate into the final cuff, but it is ideal for answering the first question: which wrist/forearm placements separate pinch, tap, squeeze, finger chords and attempted micro-movements?

Once the signal set is understood, move to a custom multi-channel analog front end and dry cuff electrodes.

## 8. Optional wrist proximity / hand sensor

Pololu VL53L8CX carrier:
- **$24.95**;
- 8 × 8 zones;
- up to 4 m rated range;
- 65° FoV;
- ~100 mA typical while actively ranging.

https://www.pololu.com/product/3419

This is useful for experiments with a hand moving directly in front of the cuff, but it is too power-hungry for continuous operation. Glasses vision + ring IMU is the stronger spatial solution.

## 9. Camera prototype BOM

### Best first camera: Raspberry Pi Camera Module 3

Official:
- **from $25**;
- Sony IMX708;
- 11.9 MP;
- autofocus;
- HDR;
- 25 × 24 × 11.5 mm.

https://www.raspberrypi.com/products/camera-module-3/

Even better for a custom camera tile, Raspberry Pi now sells the **bare Camera Module 3 sensor assemblies from $15**, specifically for smaller embedded integrations:
https://www.raspberrypi.com/news/available-now-from-15-raspberry-pi-camera-module-3-sensor-assemblies/

Use the full module first; move to the sensor assembly only after the workflow works.

## 10. P1 complete budget

A realistic **functional** prototype, excluding custom PCB fabrication and shipping:

| Group | Low | High |
|---|---:|---:|
| Display + controller uncertainty | $80 | $300 |
| Wrist MCU / Linux compute | $16 | $90 |
| Battery + power | $40 | $100 |
| Mechanical / connectors / haptics | $50 | $120 |
| Camera | $25 | $50 |
| Ring | $35 | $70 |
| One MyoWare lab channel | $49 | $60 |
| Optional UWB | $0 | $60 |
| Misc. debug/FPC/adapters | $40 | $120 |
| **Approx. total** | **$335** | **$970** |

The wide range is deliberate: the display/controller and custom mechanical interconnects are the uncertain parts.

A useful first purchase order should stay near the lower half by keeping the main compute off-wrist until the mechanical concept is comfortable.

## 11. What I would buy first

1. **1–2 × Freetech 4.01" flexible AMOLED samples** with touch and whatever evaluation/bridge board the seller can provide.
2. **2 × XIAO nRF52840 Sense** — one wrist, one ring/spare.
3. **1 × MyoWare 2.0 + electrodes**.
4. **2 × 1000–1200 mAh protected LiPo** + one ~150 mAh thin cell.
5. Charger/protection, haptic, magnets, pogo pins and FPCs.
6. **Raspberry Pi Zero 2 W** and **Camera Module 3** for the functional/camera build.
7. Skip UWB until pointing with glasses/ring IMUs is ambiguous enough to justify it.

## 12. Supplier questions for the OLED vendor

Before ordering, ask for:
- exact active-area dimensions;
- flex-tail drawing;
- panel + touch thickness;
- bending radius and permitted bend region;
- MIPI DSI lane count / voltage;
- initialization command sequence;
- RM69330 or exact driver IC;
- touch-controller part number;
- evaluation board availability;
- Linux/Android reference driver;
- minimum refresh and partial-refresh support;
- idle/self-refresh current;
- maximum brightness;
- whether the flex can exit toward a short edge;
- sample lead time for 1, 2 and 10 pieces.

Without the init sequence and electrical drawing, a cheap raw OLED can become an expensive black rectangle.
