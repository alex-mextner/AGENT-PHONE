# Deep research: keyboardless input

Updated: 2026-09-23

## Executive conclusion

A keyboard-free Screen is plausible, but no single sensor is ready to replace a keyboard for arbitrary text in every setting. The strongest architecture is **multimodal and personal**:

1. wrist sEMG + IMU for mode control, selection, punctuation and corrections;
2. deliberate silent articulation for primary private text entry;
3. gaze for target selection when glasses are worn;
4. private TTS / bone-conduction readback instead of keeping the screen lit;
5. ordinary voice dictation when privacy allows.

The system should learn a user's articulation and gesture signatures over time. It should fuse confidence across sensors rather than pretend that one experimental modality is universally reliable.

## Important distinction: silent speech is not thought reading

MIT AlterEgo demonstrates that deliberate internal/silent articulation can create measurable neuromuscular signals at the face and neck. MIT explicitly describes it as conscious silent voicing and says the device does not read arbitrary thoughts.

- MIT FAQ: https://www.media.mit.edu/projects/alterego/frequently-asked-questions/
- 2018 paper: https://www.media.mit.edu/publications/alterego-IUI/

That is the product model for Telekinesis: the user deliberately enters an input state and silently articulates. We should not depend on involuntary tongue motion during ordinary thought, even if future research discovers useful correlates.

## Technology landscape

| Modality | Wear location | What it can sense | Evidence / current result | Product view |
|---|---|---|---|---|
| Surface EMG | wrist | finger intent, pinch, wrist motion, chords | Meta ships Neural Band with Ray-Ban Display; subtle muscle signals | **V1 control layer** |
| Surface EMG | face/neck | deliberate silent articulation | AlterEgo reported 92% median word accuracy in its 2018 task | **High-value R&D** |
| Acoustic sonar | glasses | lip/jaw/mouth motion | EchoSpeech: up to 31 commands; low-power wearable | **V1/V2 research** |
| Acoustic sonar | glasses | open-vocabulary silent speech | SoniSpeech 2026 baseline: 26.3% WER, 5,356 unique words | **Promising, not solved** |
| Acoustic sonar | headphones | TMJ motion | HPSpeech: 8 commands, >90% across 18 participants | **Very practical accessory** |
| Acoustic sonar | nose | tongue/mouth/breath gestures | EchoNose: 16 gestures, 93.7% average in 10 participants | **Great lab signal, poor daily form factor** |
| Optical PPG | neck | under-skin blood/neck modulation from articulation | PPGSpeech: 81.41% ±9.74 on 15 commands | **Direct match to necklace idea** |
| Textile strain | neck | throat micromovements | Cambridge graphene choker: 95.25% in reported decoding task | **Strong necklace/choker path** |
| Ultrasound imaging | under chin | direct tongue shape/motion | SottoVoce demonstrates silent speech from ultrasound images | **Too bulky/coupled for V1** |
| Acoustic eye tracking | glasses | gaze direction | GazeTrak: 3.6° same-session; embedded 30 Hz path ~95 mW | **Good for coarse targeting** |
| Acoustic wrist sonar | wrist | 3D hand pose / object interactions | EchoWrist reports smartwatch-scale all-day sensing | **Optional secondary channel** |
| Camera/IR | glasses/neck | mouth/chin/eyes | technically strong but high privacy/power burden | **Avoid as required input** |

## Evidence notes

### Wrist sEMG

Meta's Neural Band is the clearest evidence that subtle wrist muscle activity has crossed from research into a consumer product. Meta describes EMG control for scrolling/clicking and a path toward writing messages using subtle finger movements.

Source: https://about.fb.com/news/2025/09/meta-ray-ban-display-ai-glasses-emg-wristband/

For Screen, place dry sEMG electrodes in the strap/base where skin contact is already expected. Target gestures:
- thumb–index tap and double tap;
- pinch and squeeze;
- thumb swipe/rub against the index finger;
- finger chords;
- very small attempted motions that do not need to become visually obvious.

### IMU + PPG wrist gestures

Apple Watch already supports tap-style and wrist-flick interactions using its sensor stack. Telekinesis should add:
- rapid flick away-and-back;
- roll/pronation and return;
- inward wrist flex and return;
- hold/squeeze as a mode modifier.

These gestures are best used as editing/navigation primitives, not as an alphabet.

### Acoustic glasses

Cornell EchoSpeech uses inaudible acoustic sensing on ordinary-looking glasses to infer unvoiced mouth movements:
https://news.cornell.edu/stories/2023/04/ai-equipped-eyeglasses-can-read-silent-speech

The important 2026 reality check is SoniSpeech. It scales acoustic eyewear to open vocabulary, but its published baseline is still 26.3% WER. That is exciting research, not yet invisible-keyboard quality:
https://arxiv.org/abs/2608.00803

This suggests a practical hybrid: acoustic glasses provide phonetic evidence; a personalized language model, wrist gestures and explicit confirmations reduce errors.

### Headphones / earbuds

HPSpeech reuses headphone speakers to emit inaudible signals and senses temporomandibular-joint movement with an inward microphone. In an 18-participant study it recognized eight commands at >90% accuracy. The authors note that ANC headphones already contain much of the required hardware.

Paper: https://czhang.org/assets/pdf/HPSpeech.pdf

For Screen this is attractive because earbuds/headphones already solve private TTS output. Future earbuds could be both input sensor and output channel without a visible extra device.

### Tongue sensing

The user's tongue idea is technically credible, but the best evidence is for **deliberate tongue gesture**, not passive thought decoding.

EchoNose sends inaudible acoustic signals through the nostril/oral cavity and distinguished 16 speech/tongue/breath gestures at 93.7% average accuracy. Its study includes tongue tap, double-tap and directional swipes along the palate.

ACM program summary: https://ubicomp.hosting.acm.org/ubicompiswc2023_wp/program/iswc-toc/

This is excellent evidence that tongue gestures can be a high-bandwidth private command channel. A nose interface is not the desired consumer form factor, so the research task is to move comparable sensing to glasses, earbuds, a necklace or a comfortable collar.

### Light "under the skin": PPG

PPGSpeech is particularly relevant to the proposed neck wearable. It uses multi-wavelength photoplethysmography in a necklace-style device and finds that subtle neck muscle movement during silent articulation modulates the optical signal.

In a 16-participant, 15-command study the user-dependent model reported 81.41% ± 9.74 accuracy, plus experimental speech reconstruction.

IEEE: https://ieeexplore.ieee.org/document/11271667/

This is the closest existing research to "scan with light under the skin" in a compact neck form factor. It should be a first-class Telekinesis experiment.

### Textile choker / vibration and strain

A graphene-coated textile strain sensor around the throat captures micromovements from silent articulation. The 2024 Cambridge work reports 95.25% decoding accuracy in its evaluated task:
https://www.nature.com/articles/s41528-024-00315-1

A 2026 Nature Communications system extends throat sensing to continuous communication in a small stroke-patient study:
https://www.nature.com/articles/s41467-025-68228-9

This is more mechanically simple than ultrasound imaging and may pair naturally with PPG in the same soft collar.

### Ultrasound tongue imaging

SottoVoce places an ultrasound imaging sensor under the jaw and uses tongue/internal articulation images for silent speech:
https://lab.rekimoto.org/projects/sottovoce/

It directly observes the articulator we care about, but conventional ultrasound needs good mechanical coupling and a transducer under the chin. Keep this as an R&D benchmark, not a V1 industrial-design assumption.

### Gaze without a camera

GazeTrak mounts one speaker and four microphones on each side of glasses and uses inaudible acoustic reflections around the eye. The published system reports 3.6° accuracy in the same remounting session and an embedded implementation around 95.4 mW at 30 Hz.

https://www.scifilab.org/copy-of-posesonic-1

That is sufficient to explore coarse UI target selection. For tiny text insertion points, camera/IR eye tracking remains more mature. Screen should therefore use gaze to select regions/cards and pinch to confirm, not rely on gaze-only text editing.

### Acoustic wrist hand tracking

EchoWrist uses miniature speakers and microphones on a wristband to reconstruct hand pose and recognize interactions. Cornell reports it fits smartwatch-scale hardware and can run all day on a standard smartwatch battery.

https://bowers.cornell.edu/news-stories/echowrist-uses-sonar-ai-track-hand-movements

Because Screen already needs microphones/speakers for calls and interaction, a low-duty-cycle acoustic hand-pose mode is worth prototyping after sEMG.

## Proposed Telekinesis sensor stack

### On Screen itself
- 6–8 dry sEMG electrodes distributed through the base/strap contact area;
- 6-axis IMU with high-rate burst mode;
- optical PPG sensor;
- 1–2 tiny acoustic emitters + microphones for hand-pose experiments;
- haptic actuator;
- touch screen as fallback;
- microphones for ordinary dictation.

### Optional glasses
- low-duty-cycle emissive display;
- gaze tracking, with acoustic sensing as a low-power research track;
- microphones/speakers for silent-speech acoustics and TTS;
- camera optional, not required for base interaction.

### Optional earbuds/headphones
- inward ANC microphone + speaker-based acoustic sensing for TMJ motion;
- private TTS;
- voice dictation;
- potentially bone-conduction output.

### Optional neck band / necklace
- multi-wavelength PPG;
- textile strain sensor around throat contact points;
- contact microphone / vibroacoustic pickup;
- optional electrodes for neck sEMG.

The neck accessory should look like jewelry or a soft collar, not medical equipment.

## Interaction vocabulary

Telekinesis should separate **continuous language** from **editing commands**.

Silent articulation:
- free-form message text;
- search queries;
- AI instructions;
- short command phrases.

Wrist/finger gestures:
- arm/disarm input;
- confirm/send;
- undo last word;
- choose between 2–4 candidates;
- punctuation;
- cursor/selection movement;
- cancel.

Gaze:
- pick app/card/object;
- point to a photo, message, light or TV;
- establish context before a gesture.

TTS/haptics:
- word/phrase confirmation;
- confidence warnings;
- private readback;
- no need to illuminate the full display.

## Personalization strategy

The model should have a shared encoder plus a tiny per-user adaptation layer. Enrollment starts with short prompted phrases, then improves from accepted/rejected corrections.

Important principles:
- never silently train on unarmed private behavior;
- keep raw biosignals local by default;
- expose "forget my calibration";
- maintain per-context profiles because walking, eating and resting change signals;
- fuse language-model priors only after preserving a way to recover literal input.

## What to prototype first

**P0 — software simulation**
- gesture grammar and confidence model;
- screen-off composition state machine;
- TTS correction loop.

**P1 — wrist**
- commodity multichannel sEMG development board + IMU;
- implement tap, double tap, pinch, squeeze, wrist flick, roll and flex;
- compare against optical/IMU-only recognition.

**P2 — neck**
- multi-wavelength reflective PPG around the neck;
- soft strain sensor;
- 20–50 phrase personal vocabulary;
- test whether PPG + strain outperforms either alone.

**P3 — glasses/headphones**
- reproduce EchoSpeech/HPSpeech-style inaudible acoustic features;
- gaze target + pinch confirmation;
- fuse with language model and wrist editing gestures.

**P4 — open vocabulary**
- train personalized silent-speech model;
- measure WER, correction rate, time-to-compose and social comfort;
- do not ship until correction overhead is lower than simply pulling out a keyboard.

## Success metrics

- words per minute after 1 hour / 1 week / 1 month of adaptation;
- word error rate before and after user correction;
- gestures per corrected word;
- false activation per hour;
- input energy per hour;
- percentage of messages composed with the main display fully off;
- time looking at a display per composed message;
- confidence calibration: when the system says 90%, is it actually right about 90% of the time?
