## Increment REC.1 — Capture-grade session video: every frame, ProRes

**Type:** engine (**app repo — `hoaxpoet/uzume`**). The ID is proposed; confirm or
renumber against `docs/ENGINEERING_PLAN.md` before the first commit.

**Objective.** After this session, `UZUME_RECORD_VIDEO=capture` writes **every rendered
frame** — 60 fps whenever the renderer holds 60 — as **ProRes 422 in `.mov`**, and a live
session proves it: at least 99.5 % of rendered frames written, one-frame intervals, no
duplicated content, and no drop in the render frame rate. The existing diagnostic mode
(`UZUME_RECORD_VIDEO=1`) keeps its purpose — about 30 fps, H.264, small files — but
actually delivers 30 instead of the 24 it delivers today.

This is the prerequisite for W.3a, the website's footage capture. Uzume renders a clean 60,
and nothing currently records it at 60.

**Cross-repo note.** Authored in the site repo, which owns the website roadmap that
consumes this. The work runs in the app repo; copy this file into its `prompts/` if you
want it tracked there.

## Evidence (measured 2026-09-16, Matt's M2 Pro, local file, Cymatic Resonance)

| Session | Uzume rendered (`features.csv`) | Recorded |
|---|---|---|
| `2026-09-16T13-37-09Z` — ⌘⇧5 at 4K Retina | **60.00 fps**, 0.07 % late | 54.75 fps (screen recorder) |
| `2026-09-16T13-37-09Z` — ⌘⇧5 at 1080p | **59.90 fps**, 0.44 % late | 57.77 fps (screen recorder) |
| `2026-09-16T14-27-56Z` — `UZUME_RECORD_VIDEO=1` | **59.97 fps**, 3 late frames / 67 s | **23.38 fps** (`video.mp4`, 4 Mbps H.264) |

Screen recording is ruled out: it drops 4–9 % regardless, and burns in the pointer and
the macOS recording indicator. The built-in recorder is the right seam but is capped.

The cap: `SessionRecorder.swift:100`, `minVideoInterval = 1.0 / 30.0`, applied as
`(now - lastVideoFrameTime) < minVideoInterval`. At 60 Hz a two-frame gap is ≈ 33.4 ms,
straddling the 33.3 ms threshold, so render-loop jitter pushes roughly half of them just
under it and the gap becomes three frames. `video.mp4` from `14-27-56Z` shows it
exactly: interval histogram in sixtieths of a second `{1: 1, 2: 684, 3: 892, 4: 1}`.

## Skill invocations

- **`defect-handling`** before changing the throttle. The 24-vs-30 behaviour is a defect
  (Task 2 files it), and the protocol applies.
- `closeout` at the end.
- **Not** `preset-session` or `shader-authoring` — no preset or shader is touched.

## Read first, in order

1. `UzumeEngine/Sources/Shared/SessionRecorder.swift` — video writer state and the BUG-050
   gate (≈ L92–112), `ensureCaptureTexture` (≈ L350–375), `recordFrame` (≈ L381–425).
2. `UzumeEngine/Sources/Shared/SessionRecorder+Video.swift` — `appendVideoFrame`,
   `setupVideoWriter` (codec settings), the dimension relock path.
3. `UzumeApp/VisualizerEngine+InitHelpers.swift` ≈ L40–55 — the call site, from the
   command-buffer completion handler.
4. `docs/QUALITY/KNOWN_ISSUES_HISTORY.md` — **BUG-050** (why video is opt-in; the capture
   costs ≈ 7 ms/frame), **BUG-039** (silent append stalls; its instrumentation must
   survive), **BUG-022** (fragmented output must survive a crash).
5. `UzumeEngine/Tests/UzumeEngineTests/Shared/SessionRecorderTests.swift`.

## Pre-flight invariants — stop if any fails

1. Clean working tree, up to date with `origin/main`.
2. `xcodebuild -scheme UzumeApp -destination 'platform=macOS' build` succeeds and
   `swift test --package-path UzumeEngine` is green (or only documented flakes fail).
3. `ffmpeg` and `ffprobe` on `PATH` — the verification uses both.
4. **Reproduce the 23.38 fps figure** from `~/Documents/uzume_sessions/2026-09-16T14-27-56Z/video.mp4`
   with the Task 6 measurement before changing any code. If the method cannot reproduce
   the baseline, it cannot prove the fix.
5. ≥ 40 GB free on the disk holding `~/Documents/uzume_sessions/`. ProRes 422 at 1080p60
   runs ≈ 294 Mbps — about **37 MB/s**, **≈ 9 GB per 4-minute session**.

## Tasks

**1. Branch.** `git checkout -b rec1-capture-video`.

**2. File the throttle defect.** A new BUG-\* in `docs/QUALITY/KNOWN_ISSUES.md`: the
diagnostic recorder documents ≈ 30 fps and delivers ≈ 24; cause and histogram as under
Evidence.

*Done-when:* the entry exists with the histogram and the `14-27-56Z` session cited.

**3. A pure, tested frame-keep decision.** Extract the throttle into a pure function of
(frame time, last kept time, target fps) that schedules against the *next due time* with
a tolerance of half a render frame, so jitter can no longer turn a two-frame gap into
three. Write the tests first and show them failing against the current comparison.

- 60 Hz frames with ±2 ms jitter, target 30 → keeps exactly every second frame.
- Same input, target 60 → keeps every frame.
- A genuinely late render frame is kept on arrival, not skipped.

*Done-when:* the tests fail on the old logic and pass on the new.

**4. Capture mode.** `UZUME_RECORD_VIDEO=capture`: no throttle beyond Task 3's tolerance,
`AVVideoCodecType.proRes422`, `.mov` container. Preserve the BUG-022 fragment interval and
every BUG-039 log path. `UZUME_RECORD_VIDEO=1` stays H.264 at ≈ 30 fps. The session log's
existing `video recording: ENABLED` line names the mode, codec and target fps.

*Done-when:* both modes selectable; the log states which is running.

**5. Frame integrity at 60 fps.** Every frame is blitted into **one reused shared texture**
(`captureTexture`) and read later with `getBytes`, on the recorder's serial queue. At
30 fps there is slack. At 60, the next frame's blit can overwrite the texture before the
queue reads it, so a buffer can carry the wrong frame's pixels under a correct timestamp:
a duplicate or a skip that no timestamp check would catch. Make each appended buffer hold
exactly the frame its timestamp names.

The implementation is the session's call. One strong option: an IOSurface-backed
`CVPixelBufferPool` shared with Metal through `CVMetalTextureCache`, so the GPU blits
straight into the encoder's buffer. That removes both the race and the `getBytes` copy
BUG-050 measured at ≈ 7 ms/frame.

*Done-when:* Task 6 shows zero duplicate consecutive frames on a moving preset.

**6. Live verification — stop and report.** Two sessions, same setup: the LG at
**1920 × 1080 (low resolution)**, Uzume fullscreen on it, a local file, Cymatic Resonance
held via the preset nudge (feedback plus particles: the hardest case for both copying and
compression), at least 60 s each.

- **Baseline:** recording off.
- **Capture:** `open -n --env UZUME_RECORD_VIDEO=capture <Uzume.app>`.

Report, for the capture session, within the same wall-clock window:

| Measure | Pass |
|---|---|
| Render fps from `features.csv` | ≥ 59.8, and within 0.2 of baseline |
| `frameCPUms` / `frameGPUms` | reported against baseline (no pass bar; BUG-050 context) |
| Frames written ÷ frames rendered | ≥ 99.5 % |
| Interval histogram | one-frame intervals, ≥ 99.5 %; every exception matched to a late render frame |
| Duplicate consecutive frames | 0 |
| Stream | ProRes 422, 1920×1080, no audio |

**Stop here and report the table to Matt** before closeout.

*Done-when:* the table is reported with both session directories named.

**7. Diagnostic mode regression.** A short `UZUME_RECORD_VIDEO=1` session: interval
histogram all two-frame, ≈ 30 fps, H.264.

*Done-when:* histogram reported.

## Do NOT

- **Do not turn video on by default.** BUG-050 stands; capture mode is opt-in.
- **Do not change the diagnostic mode's purpose.** 30 fps H.264 is right for diagnostics;
  its file-size rationale is sound. Fix its accuracy, not its intent.
- **Do not change `features.csv` or `stems.csv` columns.** `SessionRecorderCSVAlignmentTests`,
  the replay harnesses and this very verification read them.
- **Do not remove BUG-039 instrumentation or BUG-022 fragmented writing.**
- **Do not touch presets or shaders.**
- **Do not verify with a screen recorder.** Its drops are the problem being routed around.
- **Do not push directly to `main`.** Local commits until Matt says "yes, push," then a
  branch and a PR.

## Verification commands — all must pass before closeout

```
swiftlint lint --strict --config .swiftlint.yml
xcodebuild -scheme UzumeApp -destination 'platform=macOS' build 2>&1
swift test --package-path UzumeEngine 2>&1
swift test --package-path UzumeEngine --filter SessionRecorder 2>&1
```

Written-frame intervals, in sixtieths of a second:

```
ffprobe -v error -select_streams v:0 -show_entries packet=pts_time -of csv=p=0 <session>/video.mov \
  | sort -g | awk 'NR>1{h[int(($1-p)*60+0.5)]++}{p=$1}END{for(k in h)print k" frames: "h[k]}'
```

Duplicate consecutive frames (expect 0):

```
ffmpeg -v error -i <session>/video.mov -an -f framemd5 - \
  | awk -F', ' '!/^#/{if($6==prev)d++;prev=$6}END{print d+0" duplicate consecutive frames"}'
```

Render fps in a window: count `features.csv` rows by `wallclock_s` (CFAbsoluteTime —
add 978307200 for Unix time) between the same two instants used for the video.

## Commits

`[REC.1] recorder: <description>` — small commits per logical step: the BUG entry, the
failing tests, the throttle fix, capture mode, the integrity fix.

## Closeout

Invoke the `closeout` skill; produce the 8-part report with the verbatim
`Scripts/closeout_evidence.sh` block as §2. Additions:

- The Task 6 table, with both session directories.
- Measured ProRes size per minute, for W.3a's disk pre-flight.
- The Task 7 histogram.
- Which Task 5 approach was taken, and its measured per-frame CPU cost against BUG-050's
  ≈ 7 ms.

## DECISION-NEEDED

None. Two engineering calls are made here, not deferred:

- **ProRes 422, not 422 HQ.** Visually lossless for masters; HQ roughly 1.5× the size.
  Revisit only if W.3a's encodes show banding in fine particle detail.
- **Mode naming** — `UZUME_RECORD_VIDEO=capture` beside the existing `=1`, so no current
  invocation changes meaning.
