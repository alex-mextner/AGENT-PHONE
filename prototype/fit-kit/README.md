# AGENT-PHONE inert fit kit (GH-4)

Inert, non-powered size/weight mockups for testing the 92 × 44 mm along-arm
concept before committing to electronics. Nothing in this kit is a
functional device, and no wear trial has been run or claimed.

## Contents

| File | Purpose |
| --- | --- |
| `dummy-92x44x6.6mm.stl` | 1:1 rigid dummy of the 92 × 44 × 6.6 mm module envelope |
| `dummy-92x44x10mm.stl` | 10 mm-thick size comparator |
| `dummy-92x44x14mm.stl` | 14 mm-thick size comparator |
| `calibration-10mm.stl` | 10 mm calibration cube for checking print scale |
| `template-1to1.svg` | 1:1 paper template of the module footprint |
| `wear-diary.csv` | Blank wear-diary form (headers only, no results) |

Mesh-size, non-degenerate-triangle, and closed-edge tests cover these files
(`tests/test_fit_kit.py`). Print scale must be verified before any fitting: paper template at 100 %
(scale check: printed 10 mm square measures 10 mm), 3D prints checked
against the 10 mm calibration cube. This kit contains module-envelope
dummies only (92 × 44 mm slabs); it is not a tested cuff and proves no
fit, comfort, or wearability. No wear trial has been run or claimed;
no actual trial has been conducted under this protocol.

## Seven-day INERT trial protocol (proposed, not executed)

Hypotheses to test, not findings. Compare the existing watch/phone baseline
against the non-powered dummy.

1. **Baseline (days 1–2).** Record the participant's current watch/phone
   routine: task time and errors for messaging, navigation checks, and
   media handoff, plus measured wrist width/thickness (calipers/ruler; no
   custom/perfect fit claimed).
2. **Short removable trials (days 3–4).** Wear the 6.6 mm dummy on a
   skin cuff for short sessions. Record inert dummy assembly mass only
   (dummy mass ≠ device mass), module thickness, total height above skin,
   clothing snags, movement restraint, and removal reason after each
   session. Stop immediately on discomfort, pressure marks, numbness,
   tingling, or skin color/temperature change; do not push through.
3. **Thickness comparison (day 5).** Repeat key tasks with the 10 mm and
   14 mm comparators. Record task time, errors, and comfort/movement
   scores in `wear-diary.csv`. No live cells or loose ballast in any trial.
4. **Mount comparison (day 6).** Compare skin cuff, winter sleeve cuff,
   and quick-detach jacket mount for retention, release, and snagging.
   All mounts must be easily removable without tools or force.
5. **Touch-free flow dry run (day 7, simulated).** Simulated
   Wizard-of-Oz workflow-comprehension walkthrough only (activate,
   select, enter, review, correct, confirm, cancel, private feedback)
   with the inert dummy. Tests workflow comprehension, NOT recognition
   accuracy or task speed; no recognition/task-speed data is collected.
   A ring gesture is not assumed usable while gripping or carrying.

Rules:

- Begin with short, easily removable trials. No live cells or loose
  ballast in any wear trial.
- Optional added-load study conditions are 60/80/100 g total only;
  150–200 g is not an assumed acceptable wrist target.
- Cold operation, charging limits, condensation, retention, and release
  need separate engineering validation.
- Distinguish genuinely lost phones, temporarily misplaced phones,
  known-location but out-of-reach phones, and inconvenient retrieval
  with occupied hands. Do not infer population frequency from anecdotes.
- Keep deliberate silent articulation a personalized research track; it
  is not passive thought reading.
- Start mobility tests stationary or in a controlled traffic-free
  setting. No messaging while moving.
- Recruit by tasks, preferences, and measured fit, not by demographic
  or diagnostic assumptions.
- Preserve negative results and cases where a normal watch plus phone
  is already sufficient.

## Research grounding (optional, portable)

The following are laboratory results, not AGENT-PHONE capabilities. Do not
generalize their accuracy figures to this device, and do not claim
demographic, ADHD, mass tolerance, reading-speed, or battery-safety
findings from them:

- Kapur et al., AlterEgo (IUI 2018), MIT publication record:
  https://www.media.mit.edu/publications/alterego-IUI/ — wearable records
  neuromuscular signals of voluntary internal articulation with
  bone-conduction feedback; abstract reports 92% median word accuracy in
  their study. Not unrestricted text, every user, or our sensor placement.
- Zhang et al., EchoSpeech (CHI 2023), coauthor publication page:
  https://keli97.github.io/publication/2023-03-01-EchoSpeech-Continuous-Silent-Speech-Recognition-on-Minimally-obtrusive-Eyewear-Powered-by-Acoustic-Sensing
  — active acoustic sensing on glasses; 12 participants, 31 isolated
  commands and connected digits; 4.5%/6.1% mean WER. Not passive thought
  reading or a validated free-form keyboard. DOI 10.1145/3544548.3580801.
- Tang et al., Nature Neuroscience (2023):
  https://www.nature.com/articles/s41593-023-01304-9 — semantic language
  reconstruction from fMRI with subject cooperation in training and use;
  scanner brain signals differ from peripheral articulation sensors.

Design inference (proposed tests, not results): explicit enable/disable
state, short command vocabulary first, personalized calibration,
correction/confirmation/cancel, false-activation tests during
chewing/reading/walking. No verified population rate for
losing/misplacing phones; keep lost / temporarily misplaced /
known-location-but-out-of-reach / inconvenient-with-occupied-hands
separate. No 10x reading-speed, universal tongue-movement, 100–200 g
acceptance, gender-preference, or cold-battery safety claims.
