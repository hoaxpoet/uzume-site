## Increment W.3a — Capture: real engine footage for uzume.io

**Type:** infrastructure (**site repo**). Runs from `uzume-site`; builds and launches the
app from a sibling `uzume` checkout but never edits it.

**Objective.** After this session, three accepted master recordings of real Uzume
performances exist outside both repos — Cymatic Resonance (the website hero loop),
Ferrofluid Ocean, and Murmuration — each one ProRes 422 at 1920×1080 and 60 fps,
passed by `Scripts/check_capture.py`, given a steady-luminance verdict by Matt, and
recorded in `docs/captures/W3a-capture-log.json` with its provenance and the window a
loop may be cut from. Nothing is encoded, uploaded, or published here; W.3b turns the
masters into `media.uzume.io` assets.

uzume.io argues for a visualizer entirely in prose today. This is the increment that
gives it something to show.

**How capture works now.** Uzume records itself: `UZUME_RECORD_VIDEO=capture` (app repo
REC.1, merged as `682175ad`) writes every rendered frame straight from the GPU into the
session folder. Nothing on screen is recorded — not the pointer, not the controls, not
the preset name, not the macOS recording indicator — so there is no screen recorder to
set up and nothing to wait out.

**Who does what.** Matt plays the track, cycles to each preset, quits, and gives each
master its verdict. The session builds and launches the app, checks each recording,
moves it somewhere safe, and writes the log.

## Skill invocations

None. This repo carries none of the app repo's skills — do not invoke `closeout`,
`preset-session` or `shader-authoring`. Closeout is inline, below.

## Read first, in order

1. `docs/planning/WEBSITE_ROADMAP.md` §3 W.3 — encode budget and manifest fields W.3b will
   need from this log.
2. `docs/planning/REC.1-prompt.md` §Evidence — why screen recording was ruled out.
3. `Scripts/check_capture.py` — the acceptance gate; read its docstring.
4. `BRAND.md` §Image and footage direction — published footage must be real.
5. App repo `docs/PRESET_ROSTER_REVIEW_2026-09-04.md` — §Cymatic Resonance, §Ferrofluid
   Ocean, §Murmuration only. Quote, never paraphrase.
6. `CLAUDE.md` — commit format and the push rule.

## Pre-flight invariants — stop if any fails

1. Site repo: clean working tree, branched from an up-to-date `main`.
2. App repo at `../uzume` (or wherever Matt's checkout is): tracked tree clean, **at
   `origin/main`, and containing `682175ad`** (`git merge-base --is-ancestor 682175ad HEAD`).
   **Record the SHA** — it goes in every log entry.
3. `xcodebuild -scheme UzumeApp -destination 'platform=macOS' -configuration Debug build`
   succeeds, and `swift test --package-path UzumeEngine --filter SessionRecorder` passes.
   Record the built `Uzume.app` path (`-showBuildSettings` → `BUILT_PRODUCTS_DIR`).
4. The track decodes:
   `/Volumes/Extreme SSD/G/The Goddamn Shame/[2006] - Dispatches from the Grey City (EP)/01 Delinquent Frequencies.m4a`
   (ALAC, 44.1 kHz stereo, 4:05). Confirm with `ffprobe`.
5. `ffmpeg` and `ffprobe` on `PATH`; `python3 Scripts/check_capture.py --self-test` passes.
6. **The LG HDR 4K is set to `1920 × 1080 (low resolution)`** — not "(Default)", which is
   Retina and renders 3840×2160. Uzume records whatever size it renders, and the check
   rejects anything but 1920×1080.
7. ≥ 30 GB free on the volume holding `~/Documents/uzume_sessions/`. REC.1 measured
   1.1 GB/min on Cymatic Resonance; busier presets compress less, so plan ≈ 9 GB per
   full-track master.

## Tasks

**1. Branch.** `git checkout -b w3a-capture` in the site repo.

**2. Record, check and secure each master.** For Cymatic Resonance, then Ferrofluid Ocean,
then Murmuration — one app launch per preset:

1. **Launch** with capture on:
   `open -n --env UZUME_RECORD_VIDEO=capture "<Uzume.app>"`. Confirm the new session's
   `session.log` reads `video recording: ENABLED — mode=capture`. If it doesn't, stop.
2. **Matt** adds the **single file**, not its folder — the drive holds macOS `._` files
   beside every track, which a folder source could list as tracks that fail to analyse.
   He puts Uzume fullscreen on the LG, starts the track **from the beginning**, cycles to
   the target preset (a manual cycle holds until the next track, LFPLAN.3), and lets the
   **whole track** play. The mouse is fine; **no keys** after the cycle — `←`/`→` would
   change the preset. Then **⌘Q**, which finalises the file.
3. **Check it:** `python3 Scripts/check_capture.py <session_dir>`. `REJECT` → record again;
   do not proceed with a rejected master.
4. **Find the in-point.** The recording starts before the target preset is reached, so its
   first seconds show the presets cycled past. One frame every 5 s for the first minute,
   in reading order (0, 5, 10 … 55 s):

   ```
   ffmpeg -v error -t 60 -i <session_dir>/video.mov -vf "fps=1/5,scale=384:-1,tile=4x3" -frames:v 1 -update 1 <scratch>/sheet.png
   ```

   The in-point is the first 5 s mark where the target preset is steadily on screen. The
   **loop window** is from the later of the in-point and the check's clean-run start, to
   the clean-run end.
5. **Move the whole session folder out of `~/Documents/uzume_sessions/` immediately**, to
   `~/Movies/Uzume masters/W3a/<preset-slug>/` (`cymatic-resonance`, `ferrofluid-ocean`,
   `murmuration`). Uzume prunes that folder on every launch — the stored retention policy
   is keep-the-last-10 — and the next launch in this very task could otherwise delete the
   master just accepted. Same volume, so `mv` is instant; confirm `video.mov` is present at
   the new path before the next launch.

*Done-when:* three folders under `~/Movies/Uzume masters/W3a/`, each `video.mov` passing
`check_capture.py`, each with an in-point and loop window.

**3. Matt's verdict.** Matt opens each `video.mov` in QuickTime and watches it from the
in-point to the end against **D-157 steady luminance** — no global flashes, beat-locked
motion confined to regions. Record his words verbatim. A failed master is rejected and its
preset marked defective; it is never "fixed in post."

*Done-when:* three verbatim verdicts.

**4. Provenance log.** Write `docs/captures/W3a-capture-log.json`, one entry per master:

| Field | Value |
|---|---|
| `preset`, `role` | name; `hero` for Cymatic Resonance, else `gallery` |
| `session` | original session folder name, e.g. `2026-09-17T15-02-11Z` |
| `file` | absolute path under `~/Movies/Uzume masters/W3a/` |
| `sha256` | `shasum -a 256` of `video.mov` |
| `duration_s`, `width`, `height`, `codec`, `gb_per_min` | from the check |
| `captured_at` | the session folder's timestamp, ISO 8601 |
| `app_commit` | pre-flight 2 |
| `track`, `rights` | as under Decisions, verbatim |
| `roster_quote` | Matt's note, verbatim |
| `in_point_s`, `loop_window_s` | Task 2; `loop_window_s` is `[start, end]` |
| `check` | the check's `ACCEPT` summary lines |
| `d157_verdict` | Task 3, verbatim |
| `notes` | anything seen during capture, including any preset defect |

*Done-when:* the file parses as JSON with three entries, and every `app_commit` matches
pre-flight 2.

**5. Defects.** A preset defect seen during capture that is not already in the roster
review goes in that master's `notes` and in the closeout, and is reported to Matt. Filing
a BUG-\* entry is an app-repo task; this repo does not write to the app repo.

*Done-when:* each new defect is noted and reported, or the closeout says none were seen.

## Do NOT

- **Do not screen-record.** Measured 2026-09-16: ⌘⇧5 captured 54.75–57.77 fps while Uzume
  rendered 60, and burns in the pointer and the recording indicator (REC.1 §Evidence).
- **Do not fix presets.** Capture is observation; a fix is its own app-repo increment.
- **Do not record the multi-preset hero reel.** The only catalogue-narrowing control the app
  ships is the family blocklist, so a planner-driven reel on one track would draw from the
  whole roster, including presets with recorded defects; manual nudges would show curator
  steering, not the planner the reel exists to prove. It needs a multi-track playlist and
  its own decision.
- **Do not use `RENDER_VISUAL=1` stills or `docs/VISUAL_REFERENCES/` images.** The first are
  synthetic-audio stills, not motion; the second are third-party references, not Uzume.
- **Do not copy a master into either repo.** Masters live under `~/Movies/Uzume masters/`.
  `.gitignore` blocks `.mov`, `.mp4` and `.m4v` as a backstop, not as permission.
- **Do not leave a master in `~/Documents/uzume_sessions/`** past Task 2 step 5.
- **Do not encode, trim, upload or touch R2.** W.3b.
- **Do not edit the app repo.** Build and launch only.
- **Do not push.** Commits stay local until Matt says "yes, push."

## Verification commands — all must pass before closeout

```
python3 Scripts/check_capture.py --self-test
for d in ~/Movies/"Uzume masters"/W3a/*/; do python3 Scripts/check_capture.py "$d"; done
python3 -c "import json;d=json.load(open('docs/captures/W3a-capture-log.json'));assert len(d)==3;print('3 entries')"
git status --short   # no video file anywhere in the tree
npx prettier --check .
python3 Scripts/check_contrast.py tokens.css
```

## Commits

`[W.3a] capture: <description>` — the log and any doc updates. Masters are never committed.

## Closeout (inline — this repo has no closeout skill)

1. Files changed.
2. Verification output, verbatim.
3. Per master: path, `ACCEPT` lines, in-point, loop window, Matt's verdict.
4. App commit captured from.
5. Anything rejected and re-recorded, and why.
6. New preset defects seen, or "none."
7. Handoff to W.3b: the three loop windows and the hero.

## Decisions — resolved by Matt, 2026-09-16

Do not stop to re-ask these.

**Presets.**

| Preset | Role | Roster note (verbatim) |
|---|---|---|
| Cymatic Resonance | **Hero loop** | "One of the best to watch. Wish there were more presets like this one. I want to see more variation of the patterns it creates." |
| Ferrofluid Ocean | Gallery | "Brilliant sync with the music, but everything seems like 4/4 time." |
| Murmuration | Gallery | "Beautiful. Cloud could be bigger, take up more of the screen" |

Nacre was considered and dropped: its note records a visible defect ("Too fast overall"),
and a clip would freeze it on the site.

**Timing.** Capture these now, and **re-capture after the preset uplift**. `app_commit` and
`captured_at` exist to make staleness visible.

**Frame rate.** 60 fps (Matt, 2026-09-16) — the reason REC.1 exists.

**Track.** "Delinquent Frequencies" — The Goddamn Shame, *Dispatches from the Grey City*
(EP, 2006). Matt's own band; one track drives all three masters, which keeps them
comparable.

**Rights.** Hudac, co-writer, confirmed permission (Matt, 2026-09-16). The `rights` field,
verbatim:

> "Delinquent Frequencies" — The Goddamn Shame, *Dispatches from the Grey City* (EP, 2006,
> self-released). Written by Deming/Hudac. Used with the permission of the songwriters and
> the band. Audio not published.
