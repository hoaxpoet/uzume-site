---
title: Contributing a scene
description: What a scene is on disk, how to get one rendering on your own Mac, what the project's gates check, and what happens between opening a pull request and seeing your name in the gallery.
---

Uzume takes contributions with a specific focus: the scenes themselves — the
visuals that play against the music. Changes to the engine or the app are
welcome too, as an issue first, because the core is maintained by a small team
and moves through its own decision process.

This page is the outside view of the contributor path. The long version lives in
the app repository and stays canonical; everything here was drawn from it.

## What a scene is

Two files, sharing a name:

```
Halo.metal
Halo.json
```

The first is a Metal shader, and it is the whole of the visual — what gets
drawn, every frame. The second is its sidecar, plain JSON: the display name, which family the scene belongs to, how long it
likes to run, how busy and how kinetic it is — and the part the project's gates
care about most, an `audio_routes` list declaring every piece of the music the
shader actually reads.

Nothing registers a scene anywhere. Drop the pair into a directory Uzume watches
and it is found. The directory is called `Presets` — the code's word for a
scene, which you will keep meeting in paths and JSON keys from here on.

## Getting one rendering

While the app is running, put the two files in:

```
~/Library/Application Support/Uzume/Presets/
```

That folder is created the first time Uzume launches. Every save recompiles the
shader and swaps the scene in live, so the loop is: edit, save, look.

A save that does not compile costs you nothing. A toast appears, the previous
version keeps running, and the compiler's actual complaint goes to the log:

```bash
log stream --predicate 'subsystem == "io.uzume.presets"'
```

To watch it, open a music file with **File → Open Local File** (⌘O) and arrow
across to it. None of this needs an account, a streaming service, or the Screen
Recording permission — a file on your disk is enough to develop against.

When the scene is ready to live in the repository, the same pair goes into
`UzumeEngine/Sources/Presets/Shaders/` and is picked up at build time. A shader
that fails to compile there is logged and skipped rather than taken personally:
a broken scene never brings the app down with it.

## The one rule to know before you write anything

Drive the visuals from the music's continuous energy — how much is there, and
how that is changing — rather than from individual beats as they are detected.
Motion locked to the beat is still worth having, but it belongs on the beat grid
the analysis has already worked out, not on live detections.

The app repository calls this the single most important design rule, learned
empirically and more than once. A scene that ignores it is the mistake the rule
exists to prevent, so it is the one piece of the authoring discipline worth
carrying here rather than linking. The rest — musical role before pixels, the
temporal contract, the quality bar — is upstream in the scene session checklist
and in the shader craft guide, and both are worth the read before you start.

## What the gates check

All of them run locally with `swift test --package-path UzumeEngine`, and again
in CI on your pull request.

- **Every route you declared is exercised by real music.** The coverage gate
  replays committed recordings against your scene and asserts that each route in
  your `audio_routes` list actually fires. A route that stays silent fails the
  gate, and the fix is the route or the declaration — never the threshold.
- **The scene clears the project's visual floor.** An automated rubric scores it
  against a documented bar.
- **Steady luminance.** The photosensitivity gate measures the scene's
  brightness from frame to frame under a harness; a scene that flashes does not
  get through it. This is the same floor every scene in the gallery has already
  cleared.
- **Lint, and the suite stays green.** `swiftlint lint --strict` plus the engine
  tests. Length is not held against a `.metal` file — a good ray-march shader
  legitimately runs well past a thousand lines, and the rule is relaxed for
  exactly that reason.

## What a submission carries

- The two files, with `"certified": false` in the sidecar. It is how you ship;
  that flag is not yours to set.
- Your `audio_routes` — every route the shader reads, and no route it does not.
- A reference folder under `docs/VISUAL_REFERENCES/<name>/`, copied from the
  template that sits beside it, stating what the scene is aiming at and where
  its reference imagery came from, licensing included.

## What happens after you open the pull request

The gates run. Then a maintainer sits down and plays the scene against real
music, which is the review that actually decides — the automated gates are the
floor beneath it rather than the bar itself. If it holds up there, the scene
joins the rotation every listener sees, and it is planned into sessions
alongside everything else.

Nobody is promising you a date for that. It happens when someone watches it.

## Where it ends up

In the [gallery](/gallery/), under your name. A merged scene stops being your
side project and becomes part of what the app does for everyone who runs it —
and the author field in your own sidecar is what the gallery reads, so the
attribution travels with the work rather than being granted to it.

## Porting a Milkdrop idea

Welcome, and with an established posture: the *idea* ports, the code does not.
Author the scene from scratch on Uzume's own primitives, put an `inspired_by`
block in the sidecar naming the original visualizer, its artist and the pack it
came from, and add the matching row to the repository's credits file. **Never
commit a `.milk` file** — no original source is redistributed here.

Milkdrop calls its visualizers presets, and that is what they stay called when
you are naming one. The thing you are writing is a scene.

## Where to ask

Open an issue on the [app repository](https://github.com/hoaxpoet/uzume). The
documentation there is extensive and was written for the maintainers first, so
if something on the contributor path is confusing, that is a bug in the docs —
reporting it as one is a real contribution.

---

**Drawn from** the app repository:
[CONTRIBUTING.md](https://github.com/hoaxpoet/uzume/blob/main/CONTRIBUTING.md),
[docs/presets/YOUR_FIRST_PRESET.md](https://github.com/hoaxpoet/uzume/blob/main/docs/presets/YOUR_FIRST_PRESET.md),
[docs/presets/NEW_PRESET_CHECKLIST.md](https://github.com/hoaxpoet/uzume/blob/main/docs/presets/NEW_PRESET_CHECKLIST.md),
[docs/PRESET_SESSION_CHECKLIST.md](https://github.com/hoaxpoet/uzume/blob/main/docs/PRESET_SESSION_CHECKLIST.md),
[docs/SHADER_CRAFT.md](https://github.com/hoaxpoet/uzume/blob/main/docs/SHADER_CRAFT.md)
and [docs/CREDITS.md](https://github.com/hoaxpoet/uzume/blob/main/docs/CREDITS.md).
Those are written maintainers-first and stay canonical; this page is a rewrite
of the parts that face outward.
