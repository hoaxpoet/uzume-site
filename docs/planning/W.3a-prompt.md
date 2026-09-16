## Increment W.3a — Capture: real engine footage for uzume.io

**Type:** infrastructure (**app repo — `hoaxpoet/uzume`**, not this one).

**Objective.** After this session, three rights-clear master recordings of real Uzume
performances exist on disk — Cymatic Resonance (the website hero loop), Ferrofluid
Ocean, and Murmuration — each with a provenance entry (preset, app commit, track, rights
statement, capture date) and an acceptance judgement against steady luminance. Nothing is
encoded, uploaded, or published here; W.3b (site repo) turns the masters into
`media.uzume.io` assets.

This is the increment that unblocks every visual claim on the website. uzume.io today
argues for a *visualizer* entirely in prose.

> **Blocked on REC.1 (`docs/planning/REC.1-prompt.md`) — do not run as written.**
> Measured 2026-09-16: Uzume renders a steady 60 fps, but ⌘⇧5 records only 55–58 fps
> and burns in the pointer and the macOS recording indicator, while the built-in recorder
> is capped at 30 fps and delivers 24. Once REC.1 lands, capture uses
> `UZUME_RECORD_VIDEO=capture` instead of ⌘⇧5, and this prompt needs revising before it
> runs: Tasks 2–3 and pre-flights 6–7 change (no pointer, fades or recording indicator to
> manage), and ProRes 422 at 1080p60 is ≈ 9 GB per 4-minute master, so the disk
> pre-flight rises. The decisions below stand.

**Who does what.** **Matt records**, with the macOS screen recorder, and watches every
clip. The session prepares, verifies each file, judges nothing on Matt's behalf, and
writes the log. That split is deliberate: Matt has to watch each clip anyway to accept it,
and no agent is given standing Screen Recording permission.

**Cross-repo note.** Authored in the site repo (`docs/planning/` is where session prompts
live) because the site owns the website roadmap. The work runs in the app repo. Copy it
into the app repo's `prompts/` if you want it tracked there; the site repo must not modify
the application.

## Skill invocations

- `closeout` at the end.
- **Do not** invoke `preset-session` or `shader-authoring`. No `.metal`, sidecar, or GPU
  code is edited. A preset defect seen during capture is recorded and reported, not fixed.

## Read first, in order

1. `docs/PRESET_ROSTER_REVIEW_2026-09-04.md` — §Cymatic Resonance, §Ferrofluid Ocean,
   §Murmuration only. Quote, never paraphrase.
2. `docs/UX_SPEC.md` §7.2 (chrome fades after inactivity), §7.4 and §7.7 (live-adaptation
   keys, including the preset nudge).
3. `UzumeApp/VisualizerEngine+Presets.swift` — `nextPreset()` / `previousPreset()`: a
   manual cycle sets `manualPresetOverrideThisTrack` and **holds until the next track**
   (LFPLAN.3). That hold is what makes one track yield three single-preset clips.
4. `CLAUDE.md` — commit format, push rule, closeout.
5. Site repo `docs/planning/WEBSITE_ROADMAP.md` §3 W.3 — encode budget and manifest
   fields the log must satisfy.
6. Site repo `BRAND.md` §Image and footage direction — published footage must be real.

## Pre-flight invariants — stop if any fails

1. Clean working tree, up to date with `origin/main`.
2. `xcodebuild -scheme UzumeApp -destination 'platform=macOS' build` succeeds. **Record the
   commit SHA** — it goes in every log entry.
3. `swift test --package-path UzumeEngine` green, or failures limited to flakes already
   documented in `CLAUDE.md`.
4. The track is present and decodes:
   `/Volumes/Extreme SSD/G/The Goddamn Shame/[2006] - Dispatches from the Grey City (EP)/01 Delinquent Frequencies.m4a`
   (ALAC, 44.1 kHz stereo, 4:05). Confirm with `ffprobe`.
5. **Hudac's permission is on file.** The composer tag reads Deming/Hudac. Ask Matt to
   confirm his co-writer has agreed to the song's name appearing publicly beside the
   clips. **If he has not confirmed, stop.** The clips carry no audio, but the log is
   published as a manifest and names the track.
6. Matt confirms Screen Recording is enabled for the recorder (⌘⇧5 → Options:
   Microphone **None**, Show Mouse Pointer **off**; Do Not Disturb on).
7. ≥ 20 GB free. Native-resolution recordings of a 4-minute track are large.

## Tasks

**1. Branch.** `git checkout -b w3a-capture`.

**2. Test clip — then stop and report.** Matt adds the **single file** to Uzume, not its
folder: the drive holds macOS `._` AppleDouble files beside every track, which a folder
source could list as tracks that fail to analyse. He starts playback, cycles to any preset,
and records **10 seconds**. Probe it:

```
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,avg_frame_rate,r_frame_rate -of default=noprint_wrappers=1 <test-clip>
```

Report resolution and frame rate. **If the frame rate is below 59.9 fps, stop** — do not
record the three masters; a 30 fps capture cannot become a 60 fps loop. Resolution below or
above 1920×1080 is fine; W.3b scales it.

Also confirm, on the same clip: the preset stayed put for the whole 10 s after the manual
cycle, and how long the preset-name indication and the chrome take to disappear.

*Done-when:* frame rate ≥ 59.9 reported, the hold confirmed, fade timing noted.

**3. Record the three masters.** For each of Cymatic Resonance, Ferrofluid Ocean,
Murmuration, in that order:

1. Start the track from the beginning.
2. Cycle presets with the nudge until the target's name shows. It now holds to the end of
   the track.
3. Keep hands off mouse and keyboard until the preset name **and** the chrome have faded —
   any input brings the chrome back (D-241).
4. Matt records the **whole track**. The published loop is 15–30 s, but a full-length
   master lets W.3b choose the section with the most movement rather than whatever
   happened to be on screen when recording started.

Viewer output only: no settings, debug overlay (`D`), toasts, cursor, or notifications in
frame. A clip with any of them is re-recorded, not cropped.

*Done-when:* three master files exist, each ≈ 4:05, at the frame rate confirmed in Task 2.

**4. Acceptance — Matt's judgement.** Matt watches each master end to end and gives a
verdict against **D-157 steady luminance**: no global flashes, beat-locked motion confined
to regions. Record his verdict verbatim. A failed clip is rejected and its preset marked
defective — never "fixed in post."

*Done-when:* each master has Matt's verbatim verdict recorded.

**5. Provenance log.** Write `docs/captures/W3a-capture-log.json`, one entry per master:
`preset`, `role` (`hero` for Cymatic Resonance, else `gallery`), `file`, `sha256`,
`duration_s`, `width`, `height`, `fps`, `captured_at` (ISO 8601), `app_commit` (pre-flight
2), `track`, `rights` (the statement under Decisions), `roster_quote` (verbatim),
`d157_verdict` (verbatim, Task 4), `notes`.

*Done-when:* parses as JSON; three entries; every `app_commit` matches pre-flight 2.

**6. Defect report.** Any preset defect seen during capture that is **not** already in the
roster review goes into `KNOWN_ISSUES.md` as a new BUG-\* entry. Observation only.

*Done-when:* a BUG-\* entry per new defect, or an explicit "none observed."

## Do NOT

- **Do not fix presets.** Capture is observation. Bundling fixes is how a capture session
  becomes a tuning spiral.
- **Do not record the multi-preset hero reel.** Deferred. The only catalog-narrowing
  control the app ships is the family blocklist (`UX_SPEC.md` §Settings), so a
  planner-driven reel on one track would draw from the whole roster, including presets
  with recorded defects; and a reel steered by manual nudges would show curator steering,
  not the planner — the one claim the reel exists to prove. It needs a multi-track
  playlist and its own decision.
- **Do not use `RENDER_VISUAL=1` output as footage.** That harness renders discrete stills
  from synthetic `FeatureVector` fixtures at fixed `time` values — not motion, and not the
  engine responding to music.
- **Do not build an offline frame-sequence renderer this session.** Right durable answer,
  wrong increment. Note it in closeout as the W.3 follow-on.
- **Do not use `docs/VISUAL_REFERENCES/` images.** Third-party fidelity targets, not
  Uzume output.
- **Do not encode, upload, or touch R2.** W.3b, site repo.
- **Do not commit the masters.** LFS was retired repo-wide (CLEAN.5.8); `.gitignore` them
  and record their `sha256`.
- **Do not push.** Local commits until Matt says "yes, push," then a branch and a PR —
  never directly to `main`.

## Verification commands — all must pass before closeout

```
swiftlint lint --strict --config .swiftlint.yml
xcodebuild -scheme UzumeApp -destination 'platform=macOS' build 2>&1
swift test --package-path UzumeEngine 2>&1
python3 -c "import json;d=json.load(open('docs/captures/W3a-capture-log.json'));assert len(d)==3;print('3 entries')"
```

Per master (expect frame rate ≥ 59.9, no audio stream):

```
ffprobe -v error -show_entries stream=codec_type,width,height,avg_frame_rate -of csv <master>
```

## Commits

`[W.3a] capture: <description>` — small commits per logical step. Log and any BUG-\*
entries are committed; masters are not.

## Closeout

Invoke the `closeout` skill; produce the 8-part report with the verbatim
`Scripts/closeout_evidence.sh` block as §2. Increment-specific additions:

- Task 2's measured resolution and frame rate.
- Per master: accepted or rejected, with Matt's verbatim D-157 verdict.
- Master file paths and `sha256`, for W.3b.
- The two deferrals — the hero reel and the offline sequence renderer — and why.

## Decisions — resolved by Matt, 2026-09-16

No DECISION-NEEDED remains; do not stop to re-ask these.

**Presets.**

| Preset | Role | Roster note (verbatim) |
|---|---|---|
| Cymatic Resonance | **Hero loop** | "One of the best to watch. Wish there were more presets like this one. I want to see more variation of the patterns it creates." |
| Ferrofluid Ocean | Gallery | "Brilliant sync with the music, but everything seems like 4/4 time." |
| Murmuration | Gallery | "Beautiful. Cloud could be bigger, take up more of the screen" |

Nacre was considered and dropped: its note records a visible defect ("Too fast overall"),
and a clip would freeze it on the site.

**Timing.** Capture these now, and **re-capture after the preset uplift**. The log's
`app_commit` and `captured_at` fields exist to make staleness visible.

**Track.** "Delinquent Frequencies" — The Goddamn Shame, *Dispatches from the Grey City*
(EP, 2006). Matt's own band. One track drives all three clips, which also keeps the
footage comparable.

**Rights statement** (for the log's `rights` field, verbatim):

> "Delinquent Frequencies" — The Goddamn Shame, *Dispatches from the Grey City* (EP, 2006,
> self-released). Written by Deming/Hudac. Used with the permission of the songwriters and
> the band. Audio not published.

That statement is accurate only once pre-flight 5 holds.
