# AGENT-PHONE Visual Rebuild Implementation Plan

> SUPERSEDED by GH-4 (27 Sept 2026): 92 × 44 × 6.6 mm along-arm module,
> single Watch Ultra reference, central tapered cuff supports, open underside.
> The 94 × 45 mm across-wrist targets below are historical. See SPEC.md.

> For agentic workers: use superpowers:executing-plans task-by-task.

**Goal:** Replace the misleading concept renders with a measured, mechanically coherent, visually credible wrist-computer gallery and a real visual moodboard.

**Architecture:** Keep industrial-design dimensions and scenario requirements in a plain-Python geometry module used by both tests and Blender. Generate UI textures separately, then build/render scenes from parameterized Blender helpers. Document human/photo asset licensing beside the render pipeline.

**Tech Stack:** Python 3, unittest, Pillow, Blender 5.1 Python (bpy), Markdown, Git/GitHub.

**Spec:** docs/superpowers/specs/2026-09-23-agent-phone-visual-rebuild-design.md

## Global Constraints
- Display outer target: 94 × 45 mm; active area about 91 × 42 mm.
- Long display axis runs across the wrist; short axis follows the forearm/strap direction.
- Main device uses an open cuff; no rigid underside battery/clasp.
- Edge-to-edge glass with approximately 0.7–1.5 mm visible structural border.
- Hinge/carrier is visually recessed; no large central exposed barrel.
- All product UI examples appear on the worn device.
- Existing incorrect public renders are replaced only after full-resolution manual inspection.

## Review Focus
1. Thin wrist must not intersect cuff plates or lose the underside gap.
2. At 55° tilt the display must clear the cuff/base and remain connected.
3. Watch Ultra reference remains 49 × 44 mm and is not independently scaled.
4. Chat retains a real left chat list and right conversation after texture mapping.
5. Missing human asset must fail clearly rather than silently restoring the rejected cylinder arm.

---

### Task 1: Canonical naming, links, and gallery copy
Files: README.md, renders/README.md, docs/references.md, tests/test_repo_copy.py
Produces: repository-copy invariants used by later documentation.
- [ ] Write failing tests requiring AGENT-PHONE, Concept renders, Agent OS/Sapio State URLs, ring/camera links, and forbidding the public heading Blender renders.
- [ ] Run: python3 -m unittest tests.test_repo_copy -v. Expected: FAIL.
- [ ] Update copy and first-mention cross-links.
- [ ] Re-run. Expected: PASS.
- [ ] Commit: docs: align AGENT-PHONE naming and cross-links

### Task 2: Measured geometry contract
Files: blender/design_geometry.py, tests/test_design_geometry.py, SPEC.md
Produces: DISPLAY_OUTER_MM, DISPLAY_ACTIVE_MM, WATCH_ULTRA_MM, WRIST_MODEL_MM, CUFF_GAP_MM, TILT_ANGLES_DEG, validate_geometry().
- [ ] Write failing tests: outer=(94,45,6.2), active=(91,42), watch=(49,44,14.4), long axis=across_wrist, cuff gap>=28, bezel<=1.5, tilt includes 0/30/55.
- [ ] Run: python3 -m unittest tests.test_design_geometry -v. Expected: FAIL because module is absent.
- [ ] Implement constants and validator; update SPEC orientation/dimensions.
- [ ] Re-run. Expected: PASS.
- [ ] Commit: design: lock measured AGENT-PHONE geometry

### Task 3: Wide-display UI system
Files: blender/generate_ui.py, tests/test_ui_generator.py, blender/ui/*.png
Produces textures: home, chat, marketplace, split, remote, blind-input, research, handoff, navigation, camera.
- [ ] Write failing tests for required texture set, 1400×660 size, chat left/right pane marker pixels, and >92% near-black blind-input texture.
- [ ] Run tests. Expected: FAIL.
- [ ] Redesign UI generator for realistic density and required states.
- [ ] Generate textures and re-run. Expected: PASS.
- [ ] Commit: ui: redesign wrist interfaces for wide display

### Task 4: Rebuild Blender product geometry
Files: blender/screen_concept.py, blender/scene_builder.py, blender/validate_scene.py, tests/test_scene_manifest.py
Consumes geometry constants and UI texture names; produces mechanical/lifestyle scene manifest and renders.
- [ ] Write failing manifest tests requiring comparison, closed, 30°, 55°, underside, exploded, detached, and lifestyle scene names; require screen_long_axis=across_wrist, cuff=open, watch_reference=true on comparison.
- [ ] Run tests. Expected: FAIL.
- [ ] Implement elliptical wrist coordinate system, continuous curved cuff battery plates with open underside, thin base, across-wrist display, edge-to-edge glass, recessed pivots/carrier, detachable module, and two 49×44 mm Watch Ultra references.
- [ ] Add Blender-side validation of object dimensions, cuff gap, and display/base clearance at 0/30/55°; emit JSON report and nonzero exit on violation.
- [ ] Run headless validation with Blender. Expected: PASS.
- [ ] Commit: render: rebuild measured open-cuff product geometry

### Task 5: Photorealistic hand/wrist asset path
Files: assets/human/README.md, blender/human_asset.py, tests/test_human_asset.py
Produces load_human_wrist(scene, profile) for average and slim profiles.
- [ ] Write failing metadata/loader tests: source URL, license, redistribution decision, expected local asset; missing asset raises clear exception.
- [ ] Source MakeHuman CC0 output/core asset, a licensed BlenderKit asset, or a licensed real-photo plate.
- [ ] Implement loader/profile transforms and re-run tests.
- [ ] Render one human-scale proof image and inspect it manually.
- [ ] Commit: render: add licensed realistic wrist asset pipeline

### Task 6: Visual moodboard
Files: docs/moodboard.md, docs/references.md, tests/test_moodboard.py
- [ ] Write failing test requiring film/game, wearables, cuffs/tilts, flexible displays, rings/spatial, glasses, camera; Novate URL; KEEP/AVOID/WHY; >=12 cards and >=8 visual preview URLs.
- [ ] Run. Expected: FAIL.
- [ ] Research and author board. Include Novate, Fallout, Star Citizen, Mass Effect, Nubia Alpha, Meta Neural Band/Ray-Ban Display, Apple Vision Pro, Behance/Pinterest tilting/flexible concepts, ring/spatial and detachable-camera references.
- [ ] Do not redistribute copyrighted images; use externally hosted previews/links with attribution.
- [ ] Re-run. Expected: PASS.
- [ ] Commit: docs: add visual reference moodboard

### Task 7: Scenario render set, manual QA, gallery
Files: blender/screen_concept.py, renders/README.md, renders/*.png, renders/agent-phone-concept.blend, renders/QA.md
- [ ] Render low-sample previews for required mechanical/lifestyle scenes.
- [ ] Inspect every preview manually and record pass/fail/defects in renders/QA.md.
- [ ] Fix failed scenes, re-render, re-inspect.
- [ ] Render final set and inspect full resolution for anatomy/perspective, clipping, floating plates, orientation, scale, materials, UI readability, hinge and bezel.
- [ ] Update public Concept renders gallery.
- [ ] Run full verification: unittest discover; py_compile blender/*.py; Blender validation; git diff --check.
- [ ] Commit: render: publish corrected AGENT-PHONE concept gallery

### Task 8: Review and PR
- [ ] Run final full-branch review against plan/spec.
- [ ] Fix Important/Critical findings with tests/verification.
- [ ] Push branch and open PR referencing issue #1.
- [ ] Merge only after gates pass; mark ticket shipped and complete acceptance flow.