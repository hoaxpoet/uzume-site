## Increment W.3c — More footage before launch

**Type:** capture and encode (**site repo**, with the app repo running on Matt's Mac).

**Objective.** The gallery shows three performances. After this session it shows seven,
chosen so that every one of them demonstrates the claim the site is built on — that the
visuals answer the music. No site code changes: W.4 already renders whatever the manifest
and the generator produce.

**Why now.** Matt, 2026-09-18: "we should capture more preset videos before launch." The
roadmap has carried this as W.3 **Open** since W.3b. It is the last content gap before
W.6 launch polish, and it is also the only route to closing the critique's biggest finding
— that the landing hero reads as a nature photograph rather than as software.

## What exists now

Three loops, all captured 2026-09-16 against the same track: Murmuration (hero, 30 s),
Cymatic Resonance and Ferrofluid Ocean (gallery, 15 s). The pipeline they came through is
unchanged and needs no work:

1. The **app records itself** — `UZUME_RECORD_VIDEO=capture` (app repo REC.1) writes
   ProRes 422 1920×1080, one frame per rendered frame, no audio.
2. `python3 Scripts/check_capture.py <session_dir>` accepts or rejects the master. It
   wants a clean run of **≥ 30 s** — every frame exactly 1/60 s after the last, no frame
   identical to the one before it.
3. A JSON entry per capture in `docs/captures/W3a-capture-log.json`.
4. `python3 Scripts/encode_captures.py` cuts the loops, encodes AV1/WebM + H.264/MP4 +
   AVIF/JPEG posters, uploads to R2, and rewrites `src/data/media.json`.
5. `python3 Scripts/generate_presets.py` writes the content entries. The site renders.

**Only step 1 needs a human at a Mac.** Everything after it is scripted.

## The selection, and the evidence behind it

`docs/PRESET_ROSTER_REVIEW_2026-09-04.md` in the app repo is the source of truth, and it
is blunt: **Matt criticises music sync on 13 of the 25 certified presets.** The site's
central claim is that the performance answers the music. Publishing a preset its own
author says does not sync would undermine the thing the gallery exists to prove, so the
filter is: capture what the review praises, skip what it faults on sync.

That leaves four strong candidates, in priority order.

| # | Preset | Family | Why | Watch for |
|---|---|---|---|---|
| 1 | **Fractal Tree** | `fractal` | "Fun, it just dances along with the music pretty convincingly" — the strongest un-captured sync endorsement in the review. A fractal tree also reads unmistakably as *generated*, which is the direct answer to the critique's finding that the hero looks photographic. | "Might consider adding additional trees so dancing is synchronized" — one tree may read thin at 1080p. |
| 2 | **Aurora Veil** | `hypnotic` | "Looks great. Stars blink well with the beat." Praise aimed exactly at beat sync. `fatigue_risk: low`. | "Wish there was more color variation, purple is fleeting." Pick a window with colour movement in it. It is also a *sky*, like Murmuration — do not let it become a second atmospheric piece in the hero position. |
| 3 | **Nimbus** | `volumetric` | "Doesn't do much and yet people seem to really like it and think the ball has a personality." The only audience-tested preset in the roster. | `motion_intensity: 0.3` — the lowest of the four. It will not carry the sync argument on its own; it is there for character. |
| 4 | **Dragon Bloom** | `hypnotic` | "Reds look gorgeous." It is also a **port** — the only candidate with an `inspired_by` block, so publishing it would exercise the gallery's Milkdrop-attribution path, which has never rendered in production because none of the three published presets has lineage. | "Washed out, extreme brightness." Check the D-157 steady-luminance read carefully; this is the one candidate whose review note is a brightness warning. |

**Families.** The three published are `particles`, `geometric`, `geometric`. These four add
`fractal`, `hypnotic`, `volumetric` — the gallery stops looking like three versions of one
idea.

**Deliberately not captured**, and why, so nobody re-litigates it from the preset list
alone: Witchlight, Fata Morgana, Filigree, Floret, Glaze, Gossamer, Lumen Mosaic,
Membrane, Meniscus, Mitosis, Nacre, Nebula, Ricercar and Volumetric Lithograph are all
certified and all carry a sync criticism in the review. Cytokinesis "hangs for seconds
before restart". Staged Sandbox: "Get rid of it." Plasma, Waveform, Spectral Cartograph
and the two sandboxes are **not certified**. Alfvén is certified but postdates the review
and carries `fatigue_risk: high` — unreviewed footage should not launch a site.

Seven strong performances beat twelve uneven ones. `WEBSITE_PLAN.md` §5 says the same
thing: "a gallery of strong clips beats a complete one."

## Pre-flight invariants — stop if any fails

1. Site repo clean, branched from an up-to-date `main`.
2. The app repo builds and runs, and its commit is recorded — the log stores `app_commit`
   per capture and W.3a's three all read `682175ad`. A different commit is fine and
   expected; it just has to be written down.
3. **A rights-clear track.** W.3a used "Delinquent Frequencies" — The Goddamn Shame, used
   with the songwriters' and band's permission, audio not published. The roster review
   itself was watched against Bowie's *Low*, which is **not** publishable. Any new capture
   uses a track Matt has the rights to, and the `rights` string is copied into every log
   entry.
4. Disk: masters run 1.2–2.3 GB/min and the check wants ≥ 30 s clean inside a longer take.
   W.3a's takes were 110–158 s. Budget ~5 GB for four.

## Tasks

**1. Branch.** `git checkout -b w3c-capture`.

**2. Confirm the selection.** Read DECISION-NEEDED to Matt. He may cut or add; the table
above is a recommendation from the review, not a decision.

**3. Capture, one preset at a time** (Matt, at the Mac). For each: run the app with
`UZUME_RECORD_VIDEO=capture` against the rights-clear track, let the cycle reach the
preset, and record well past it — W.3a's shortest useful take was 110 s for a 54 s clean
run. Note the in-point where the preset actually appears; the cycle is often showing
something else at 0 s.

*Done-when:* four `video.mov` masters exist under `~/Movies/Uzume masters/W3c/<slug>/`.

**4. Check each master.** `python3 Scripts/check_capture.py <session_dir>`. A master that
cannot show a ≥ 30 s clean run is re-recorded, not argued with. Paste the check output
verbatim into the log entry, as W.3a did.

**5. Log each capture** into `docs/captures/W3a-capture-log.json` — sha256, duration,
codec line, `app_commit`, track, rights, `in_point_s`, `loop_window_s`, the check output,
and the D-157 verdict in Matt's own words. Keep the existing entries untouched.

**6. Judge steady luminance** (Matt). D-157 is the gate and the site states it as "a
bounded change in brightness from frame to frame" — never a flashes-per-second figure
(`PRODUCT.md`). Dragon Bloom is the one to look hardest at.

**7. Encode and publish.** `python3 Scripts/encode_captures.py`. It reads the log, cuts,
encodes, uploads to R2 and rewrites `src/data/media.json`. New presets take `role:
"gallery"` and the 15 s length; the hero stays Murmuration unless Matt moves it.

**8. Regenerate the content entries.** `python3 Scripts/generate_presets.py`, then write a
caption for each new preset in `Scripts/preset_captions.json` — one sentence: what the
visitor is looking at, then what in the music drives it. Draw it from the sidecar's own
`description` and assert nothing the sidecar does not. The raw descriptions carry
increment ids and cannot ship.

**9. Verify.** The gallery renders seven performances; Dragon Bloom shows its `inspired_by`
line, which no published preset has exercised before. Safari plays the MP4, Chrome the
WebM, phones fetch neither.

## Do NOT

- **Do not publish a preset the roster review faults on sync** without saying so out loud
  and getting Matt's agreement. That is the whole basis of this selection.
- **Do not capture against a track without publication rights.** Not Bowie.
- **Do not re-encode or delete the three existing loops.** They are published under
  immutable cache headers and reviewed.
- **Do not commit media.** `.gitignore` blocks `.mov`/`.mp4`/`.m4v`; it does not block
  `.webm`, `.avif` or `.jpg`.
- **Do not edit `src/data/media.json` by hand.** It is the encoder's output.
- **Do not hand-write preset entries.** `generate_presets.py` produces them.
- **Do not edit the app repo.** Captures read it; this repo never writes to it.

## Verification commands

```
python3 Scripts/check_capture.py <each session dir>
python3 Scripts/encode_captures.py
python3 Scripts/generate_presets.py && python3 Scripts/generate_presets.py --check
python3 -c "import json;d=json.load(open('src/data/media.json'));print(len(d),'entries')"
git status --short --ignored | grep -iE '\.(mov|mp4|m4v|webm|avif|jpe?g)$' || echo "no media in tree"
npx astro check && npm run build && npx prettier --check .
python3 Scripts/check_contrast.py tokens.css
```

## DECISION-NEEDED

**1. Is the four-preset selection right?**

- **A — Fractal Tree, Aurora Veil, Nimbus, Dragon Bloom**, as argued above. Seven
  performances, four families added, every one of them praised in the review.
- **B — The same four minus Dragon Bloom.** Its review note is a brightness warning and
  D-157 is the site's loudest safety claim; dropping it avoids the only candidate that
  could fail the gate after the work is done. Costs the `inspired_by` path its first real
  test.
- **C — More than four**, accepting presets the review faults on sync to reach
  `WEBSITE_PLAN` §5's "best 8–12".

**Recommendation: A.** Capture Dragon Bloom last, so if its luminance read fails, the
other three are already published and nothing is blocked. **Default if no answer: A.**

**2. One track, or two?**

- **A — The same rights-clear track as W.3a.** Simplest, and the loops stay comparable.
- **B — A second rights-clear track as well.** Capturing one preset against two different
  tracks is the only way the site could ever show *sync* in a still image — the critique's
  open question, and the one that reduced-motion visitors, phone visitors and every OG
  card currently have no answer to. It costs one extra take of one preset.

**Recommendation: B**, with the second track used for Fractal Tree only, since it is the
preset the review credits with visibly dancing to the music. **Default if no answer: A**,
because rights come first and a second cleared track may not exist.
