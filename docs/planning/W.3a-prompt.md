## Increment W.3a — Capture: real engine footage for uzume.io

**Type:** infrastructure (**app repo — `hoaxpoet/uzume`**, not this one).

**Objective.** After this session, a set of rights-clear, 1080p60 master recordings of
real Uzume performances exists on disk, one per selected preset plus one hero reel,
each with a recorded provenance entry (preset, app commit, track, licence, capture
date). Nothing is encoded, uploaded, or published here — this session produces the
masters and the log that W.3b (site repo) turns into `media.uzume.io` assets.

This is the increment that unblocks every visual claim on the website. uzume.io today
argues for a *visualizer* entirely in prose: no footage, no stills, no gallery. The
chrome was built to recede so the engine could lead, and the engine never arrived.

**Cross-repo note.** This prompt is authored in the site repo (`docs/planning/` is where
session prompts live, per its `CLAUDE.md`) because the site repo owns the website
roadmap. The work runs in the app repo. Copy this file into the app repo's `prompts/`
if you want it tracked there; the site repo must not modify the application.

## Skill invocations

- `closeout` at the end. Mandatory, as for every app-repo increment.
- **Do not** invoke `preset-session` or `shader-authoring`. No `.metal` file, sidecar,
  or GPU code is edited in this increment. If capture reveals a preset defect, record
  it and stop — do not fix it here (see Do NOT).

## Read first, in order

1. `docs/PRESET_ROSTER_REVIEW_2026-09-04.md` — Matt's per-preset observations. **Quote
   these, do not paraphrase.** This is the curation input.
2. `docs/PRODUCT_SPEC.md` §Primary Use Cases — the session shape being recorded.
3. `CLAUDE.md` — commit format, push rule, closeout protocol.
4. Site repo `docs/planning/WEBSITE_ROADMAP.md` §3 W.3 — the encode budget and manifest
   fields this session's log must satisfy.
5. Site repo `BRAND.md` §"Imagery" and §"Motion behavior" — published footage must be
   real or clearly labelled illustrative; no stock imagery, lens flares, or AI shimmer.

## Pre-flight invariants — stop if any fails

1. On a clean working tree, up to date with `origin/main`.
2. `xcodebuild -scheme UzumeApp -destination 'platform=macOS' build` succeeds. Record
   the resulting commit SHA — it goes in every provenance entry.
3. `swift test --package-path UzumeEngine` is green, or its failures are already
   documented as known flakes in `CLAUDE.md`. A red suite means the footage would
   record unverified behaviour — stop.
4. At least one **rights-clear** track is on disk, with its licence recorded. Matt's
   roster review was captured against David Bowie — *Low*, which is **not** usable
   here. If no rights-clear track exists → stop and ask Matt; this is the one
   pre-flight he cannot delegate.
5. Screen Recording permission is granted to the recorder being used. Uzume itself
   needs no permission for local-file playback, but the *recorder* does.
6. Disk headroom: ≥ 20 GB. ProRes masters at 1080p60 are large.

## Tasks

**1. Branch.** `git checkout -b w3a-capture`.

**2. Select the roster.** Read the roster review. Build a table of every preset with
Matt's verbatim observation and a capture verdict: **ready**, **defective**, or
**unseen**. A preset whose observation names an unfixed visual defect (Dragon Bloom
"washed out, extreme brightness"; Fata Morgana "too dark"; Cytokinesis "hangs for
seconds before restart") is **defective** and is not captured this session.

*Done-when:* the table exists in the session notes and every one of the 27 roster
entries has a verdict with its quote attached.

**3. STOP — DECISION-NEEDED.** Present the table and the decision below to Matt. Do not
capture before he answers.

**4. Capture.** For each approved preset: run a real session against the rights-clear
track, local-file path, and record the Viewer output at **1080p60, 1920×1080**, no
audio track in the master. Capture **45–60 s** per preset even though the published
loop is 15–30 s — the surplus is what makes a clean in/out point selectable later.

Requirements per clip:
- Real audio drive. The performance must be the engine responding to the actual track.
  Do **not** substitute synthetic `FeatureVector` fixtures (see Do NOT).
- Viewer output only — no settings, diagnostics, chrome, cursor, or operator controls
  in frame. `docs/UX_SPEC.md`: viewer output never includes those.
- Verify the clip against **D-157 steady luminance** by eye before accepting it: no
  global flashes, beat-locked motion confined to regions. A clip that fails this is
  rejected and the preset is marked defective, not "fixed in post."

*Done-when:* one master file per approved preset exists, each ≥ 45 s, 1920×1080, ≥ 59.9
fps, and each has been watched end-to-end and accepted.

**5. Hero reel.** One 30–60 s continuous capture spanning at least two preset
transitions, so the reel shows the thing prose cannot: that the session is *sequenced*,
not a single looping effect. Same requirements as Task 4.

*Done-when:* the reel exists, contains ≥ 2 visible transitions, and has been watched.

**6. Provenance log.** Write `docs/captures/W3a-capture-log.json`: an array with one
entry per master — `preset`, `file`, `sha256`, `duration_s`, `resolution`, `fps`,
`captured_at` (ISO 8601), `app_commit` (from pre-flight 2), `track`, `track_licence`,
`roster_quote` (Matt's verbatim line), `notes`.

*Done-when:* the file parses as JSON, has one entry per master, and every `app_commit`
matches pre-flight 2.

**7. Defect report.** Any preset defect observed during capture that is not already in
the roster review goes into `KNOWN_ISSUES.md` as a new BUG-* entry. Observation only —
no fixes.

*Done-when:* either a BUG-* entry exists per new defect, or the report states none were
observed.

## Do NOT

- **Do not fix presets.** Capture is observation. A preset that looks wrong is marked
  defective and reported; fixing it is a `preset-session` increment with its own
  reference set and its own prompt. Bundling them is how a capture session becomes a
  three-week tuning spiral.
- **Do not use `RENDER_VISUAL=1` output as footage.** That harness renders discrete
  stills from synthetic `FeatureVector` fixtures at fixed `time` values — it is a
  fidelity-review tool, not a motion capture, and it cannot produce a sequence. Footage
  built from synthetic drive would not be the engine responding to music, which is the
  entire claim the footage exists to support.
- **Do not build the offline frame-sequence renderer this session.** Extending the
  visual-review harness to dump timed sequences fed by *recorded* FeatureVectors is the
  right durable answer — deterministic, re-runnable when presets improve, no screen
  recording — but it is engine work with its own scope. Note it in closeout as the W.3
  follow-on and move on.
- **Do not use `docs/VISUAL_REFERENCES/` images anywhere near this.** Its README says
  "photographic references preferred over renders, sources are Matt's choice" — those
  are third-party fidelity targets, not Uzume output. Publishing them would fabricate
  footage.
- **Do not encode, upload, or touch R2.** W.3b, site repo.
- **Do not capture against copyrighted music**, even though masters carry no audio
  track. Pre-flight 4 is not negotiable at capture time.
- **Do not push.** Local commits only until Matt says "yes, push," then a branch and a
  PR — never directly to `main`.

## Verification commands — all must pass before closeout

```
swiftlint lint --strict --config .swiftlint.yml
xcodebuild -scheme UzumeApp -destination 'platform=macOS' build 2>&1
swift test --package-path UzumeEngine 2>&1
python3 -c "import json;d=json.load(open('docs/captures/W3a-capture-log.json'));print(len(d),'entries')"
```

Per-master probe (expect 1920×1080, ≥ 59.9 fps, no audio stream):

```
for f in docs/captures/masters/*.mov; do ffprobe -v error -show_entries stream=codec_type,width,height,avg_frame_rate -of csv "$f"; done
```

## Commits

`[W.3a] capture: <description>` — small commits per logical step. The masters
themselves are **not committed** (LFS was retired repo-wide at CLEAN.5.8 over billing);
`.gitignore` them and record their `sha256` in the log instead. The log and the defect
entries are committed.

Push only on Matt's explicit "yes, push," then to a branch with a PR.

## Closeout

Invoke the `closeout` skill; produce the 8-part report with the verbatim
`Scripts/closeout_evidence.sh` block as §2. Increment-specific additions:

- The roster table from Task 2, with verdicts and Matt's quotes.
- Per-clip acceptance: which presets were captured, which were rejected and why.
- The D-157 steady-luminance judgement per accepted clip.
- The W.3 follow-on note: the offline sequence renderer, and why it was deferred.

## DECISION-NEEDED (answer before Task 4)

**Which presets should the website show, and should we capture now or after uplift?**

The roster is mid-uplift. Most entries carry a recorded defect in your own words, and a
clip captured today freezes that defect on the website until someone re-captures.

- **A — Capture the few that are already strong, now.** Your notes single out Aurora
  Veil ("Looks great. Stars blink well with the beat"), Cymatic Resonance ("One of the
  best to watch"), and Nacre ("Beautiful"). Three or four clips plus a hero reel. The
  site stops arguing in prose within a week. The gallery is visibly small.
- **B — Wait for the uplift, then capture 8–12.** The gallery launches full and
  consistent. The website keeps making the emotional case for a visualizer in
  paragraphs for as long as that takes.
- **C — Capture the strong ones now, and re-capture after uplift.** Same start as A,
  with a deliberate second pass. Costs one extra capture session; the log's
  `app_commit` and `captured_at` fields already exist to make staleness visible.

**Recommendation: C.** The roadmap's own line is "a gallery of strong clips beats a
complete one," and the cost of re-capture drops to near zero once the encode script
exists. An empty visual argument is a worse problem than a short gallery.

**Default if no reply:** A — capture only the presets your notes praise without
qualification, and stop. Nothing speculative gets published.
