## Increment W.3b — Encode and publish: the three loops on media.uzume.io

**Type:** infrastructure (**site repo**).

**Objective.** After this session, the three W.3a masters exist as web loops on
`https://media.uzume.io` — an AV1/WebM and an H.264/MP4 rendition of each, with AVIF and
JPEG posters — produced reproducibly by `Scripts/encode_captures.py`, checked for quality,
colour, frame timing and steady luminance at the loop seam, reviewed by Matt, served with
correct headers, verified playing under the production CSP, and described by an asset
manifest at `src/data/media.json`. No page or component changes: W.4 puts the footage on
the site.

**What exists now.** Three accepted ProRes 422 masters (1920×1080, 60 fps) under
`~/Movies/Uzume masters/W3a/`, each with a proven-clean loop window, recorded in
`docs/captures/W3a-capture-log.json`. As of 2026-09-16 there is **no R2 bucket and no
`media.uzume.io`** — the hostname has no DNS record — and Wrangler on this Mac is not
logged in. Setting those up is part of this session.

**One fact that shapes the whole encode.** Safari decodes AV1 only on Macs with an AV1
hardware decoder (M3 and later). On M1 and M2 Macs — Matt's M2 Pro included — Safari plays
the **H.264** file. For a site selling a Mac app, the "fallback" is what a large share of
visitors will actually see. Hold it to the same quality bar as the AV1 file.

## Skill invocations

None. This repo carries none of the app repo's skills. Closeout is inline, below.

## Read first, in order

1. `docs/captures/W3a-capture-log.json` — masters, sha256s, in-points, loop windows,
   provenance and rights. The encode's single source of input.
2. `docs/planning/WEBSITE_PLAN.md` §5 — encode ladder, budget, R2, manifest.
3. `docs/planning/WEBSITE_ROADMAP.md` §3 W.3 and W.4 — what this delivers and what W.4
   consumes.
4. `src/components/VideoTile.astro` and `src/components/PresetCard.astro` — the eventual
   consumers of the manifest.
5. `public/_headers` — the CSP already allows `media-src` and `img-src` from
   `https://media.uzume.io`, and its comment explains why this must be tested in a real
   browser.
6. `Scripts/check_capture.py` — reuse its timing logic; its docstring records three
   ffmpeg measurement traps (dropped frames without `-fps_mode passthrough`, rounded
   `framemd5` timestamps, file-wide versus in-window judgement).
7. `BRAND.md` §Image and footage direction and §Motion behavior; `CLAUDE.md`.

## Pre-flight invariants — stop if any fails

1. Site repo: clean working tree, branched from an up-to-date `main` that contains W.3a
   (merge `d95c63b6`).
2. All three masters are present and match the log:
   `shasum -a 256 ~/Movies/"Uzume masters"/W3a/*/video.mov` against each entry's `sha256`.
3. `ffmpeg` has `libsvtav1`, `libx264`, `mjpeg`, the `avif` muxer, and the `ssim`,
   `xpsnr` and `signalstats` filters (`ffmpeg -hide_banner -encoders` / `-muxers` /
   `-filters`). `python3 Scripts/check_capture.py --self-test` passes.
4. **Matt runs `npx wrangler login` himself**, in a browser. The session never asks for,
   receives or creates an API token. Confirm with `npx wrangler whoami`.
5. **R2 is enabled on the Cloudflare account.** Enabling it requires billing details in the
   dashboard, which only Matt can do. `npx wrangler r2 bucket list` succeeding is the
   check; if it errors that R2 is not enabled, stop and ask Matt to enable it.

## Tasks

**1. Branch.** `git checkout -b w3b-encode`.

**2. Confirm the decisions.** Read the DECISION-NEEDED section to Matt and record his
answers. If he does not answer, proceed on the stated defaults.

*Done-when:* both decisions recorded.

**3. The encoder.** Write `Scripts/encode_captures.py` (Python, beside
`check_capture.py`; the roadmap's `.sh` name predates it). It reads the capture log and,
for each master, writes to a directory **outside the repo** (default
`~/Movies/Uzume masters/W3b/`):

- The loop: cut from inside the master's `loop_window_s` only, at the decided length, with
  the decided seam treatment.
- `AV1/WebM` via `libsvtav1` and `H.264/MP4` via `libx264` (High profile, `yuv420p`,
  `+faststart`). 1920×1080, constant 60 fps, **no audio stream**. Colour tagged BT.709
  (`-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`) so
  browsers do not guess. No sharpening, grading, denoising or upscaling — this is real
  footage, published as captured.
- Posters: one `AVIF` and one `JPEG` of the same frame, chosen from inside the loop with
  mean luma near the loop's median. The poster is what reduced-motion visitors see
  instead of the loop, so it must not be an outlier frame.
- Content-hashed filenames: `loops/<preset-slug>.<sha256[:8]>.webm|mp4`,
  `posters/<preset-slug>.<sha256[:8]>.avif|jpg`.
- Rate control is the session's call. Target the budget per rendition (see Task 4) and
  prefer a quality-based mode with a cap over a fixed bitrate: particle and fine-line
  content (Cymatic Resonance, Murmuration) and Ferrofluid Ocean — 2.26 GB/min as ProRes,
  the least compressible — need different rates for the same quality.

Deterministic: running it twice produces byte-identical outputs, or the closeout says why
not.

*Done-when:* four files per preset exist outside the repo; the script re-runs cleanly.

**4. Measure every rendition.** For each preset × {AV1, H.264}, report:

| Measure | Bar |
|---|---|
| Stream | codec as intended; 1920×1080; exactly 60 fps constant; no audio; BT.709 tags present |
| Frames | frame count = duration × 60, and no timing gap (reuse `check_capture.py`'s logic on packet timestamps) |
| Size | gallery loops within **8–12 MB per rendition**; the hero "somewhat larger" (WEBSITE_PLAN §5) — report the number, and **report an overrun rather than silently degrading quality to hide it** |
| Fidelity | `ssim` and `xpsnr` against the same span of the master; report both, no fixed pass bar — Matt judges by eye in Task 5 |
| Seam luminance | the mean-luma change across the loop seam (last frame → first) must not exceed the loop's own largest frame-to-frame change (`signalstats` YAVG). A seam that jumps brighter than anything in the performance introduces a flash the engine never made — D-157 steady luminance applies to what we publish, not only to what the app renders |
| Colour | a four-frame contact sheet per preset — master, AV1, H.264 at the same timestamp — checked for shifts in brightness, saturation or black level. Washed-out blacks are the usual sign of a range or matrix mismatch |

*Done-when:* the table exists for all six renditions, and the contact sheets are saved for
Matt.

**5. STOP — Matt reviews the encodes.** Before anything leaves the Mac. Matt watches each
loop **looping** — the seam is the thing to watch — in **Chrome** (plays AV1) and in
**Safari** (on his M2 Pro, plays H.264), opening the local files directly. QuickTime cannot
play AV1 WebM, so it is not a substitute. He reviews the contact sheets, and gives a
verdict per preset on quality and on steady luminance at the seam. Record it verbatim.

*Done-when:* verbatim verdicts for all three; any rejection sends that preset back to
Task 3.

**6. STOP — set up R2, with Matt's explicit yes.** Creating a bucket and attaching a domain
changes the Cloudflare account; ask first and wait for a yes.

- Bucket: `npx wrangler r2 bucket create uzume-media`.
- Custom domain: `npx wrangler r2 bucket domain add uzume-media --domain media.uzume.io
  --zone-id <uzume.io zone id> --min-tls 1.2`. The zone id comes from Matt or the
  dashboard. `--min-tls` defaults to **1.0** if omitted — set it.
- Wait for `dig +short media.uzume.io` to resolve and `curl -sI https://media.uzume.io/`
  to answer before continuing.

*Done-when:* `media.uzume.io` resolves and answers over HTTPS.

**7. Upload.** Every object with `--remote`. **Wrangler 4's `r2 object` commands default to
local storage** — without `--remote` the upload goes to a local simulation, reports
success, and nothing reaches Cloudflare. Verified 2026-09-16 on Wrangler 4.131.2, which
printed `Resource location: local` and then `Upload complete.` Per object:

```
npx wrangler r2 object put uzume-media/<key> --file <path> --remote \
  --content-type <video/webm | video/mp4 | image/avif | image/jpeg> \
  --cache-control "public, max-age=31536000, immutable"
```

`immutable` is safe only because every filename carries its content hash. Masters are never
uploaded.

*Done-when:* twelve objects uploaded.

**8. Verify delivery.**

- Headers, per object: `curl -sI https://media.uzume.io/<key>` → `200`, the right
  `content-type`, the immutable `cache-control`, `accept-ranges: bytes`.
- Range requests, which seeking and Safari's playback depend on:
  `curl -s -o /dev/null -w "%{http_code}" -H "Range: bytes=0-1023" <url>` → `206`.
- **Playback under the production CSP.** On `https://uzume.io` itself (not a local
  preview, which has no `_headers` CSP), use the browser to add a muted, looping
  `<video>` with the AV1 source, then again with the H.264 source. Confirm each reaches
  `readyState >= 3` with `currentTime` advancing, and that the console shows no CSP
  violation. Repeat with an `<img>` for each poster format. This is the test the
  `_headers` comment demands; curl cannot see CSP.
- **Safari, by Matt:** open each `.mp4` URL in Safari and confirm it plays and loops.

*Done-when:* every check reported, with the browser console output.

**9. Manifest.** Write `src/data/media.json` — an array, one entry per preset:

- **Identity:** `preset`, `slug`, `role` (`hero` | `gallery`), `roster_quote`.
- **Renditions:** each with `url`, `bytes`, `sha256`, `width`, `height`, `fps`,
  `duration_s`, and a full `type` **including the codecs parameter**, derived from
  `ffprobe` of the actual file — for example `video/webm; codecs="av01.0.09M.08"` and
  `video/mp4; codecs="avc1.64002A"`. Do not hard-code these strings.
- **Posters:** `avif` and `jpeg`, each with `url` and `bytes`.
- **Provenance** (copied from the capture log, never retyped): `source_master_sha256`,
  `loop_window_s`, the loop's span within the master, `captured_at`, `app_commit`,
  `track`, `rights`, `d157_verdict`, and Task 5's `encode_verdict`.

*Done-when:* the file parses; every URL in it returns `200`; `npm run build` and
`npx astro check` pass.

**10. Record the decisions.** Per `CLAUDE.md`, decisions land in
`docs/planning/WEBSITE_ROADMAP.md`: this session's two decisions, the bucket name, and
W.3's status. Its "Not started … no R2 bucket" line is now stale — correct it.

*Done-when:* the roadmap reflects what exists.

## Do NOT

- **Do not change pages or components.** W.4 wires the footage in. The one thing W.4 must
  know is under Closeout.
- **Do not commit media.** Encodes live outside the repo; `.gitignore` blocks `.mov`,
  `.mp4` and `.m4v` as a backstop, and does not block `.webm`, `.avif` or `.jpg` — so the
  output directory must be outside the tree.
- **Do not upload the masters**, or anything not listed in the manifest.
- **Do not cut outside a loop window**, and do not re-capture. A loop window that can't
  make a good loop is a finding to report.
- **Do not add renditions beyond AV1 and H.264.** HEVC would suit Safari but is not in the
  plan; raise it as a finding if H.264 cannot meet the bar.
- **Do not sharpen, grade, denoise or upscale.**
- **Do not handle credentials.** Matt logs in; no tokens in commands, files or chat.
- **Do not create the bucket or attach the domain without Matt's explicit yes** (Task 6).
- **Do not push.** Commits stay local until Matt says "yes, push."

## Verification commands — all must pass before closeout

```
python3 Scripts/check_capture.py --self-test
python3 Scripts/encode_captures.py            # re-run: reproduces, or the closeout says why not
python3 -c "import json;d=json.load(open('src/data/media.json'));assert len(d)==3;print('3 entries')"
python3 -c "import json,subprocess;[print(r['url'],subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}',r['url']],capture_output=True,text=True).stdout) for e in json.load(open('src/data/media.json')) for r in e['renditions']+list(e['posters'].values())]"
git status --short --ignored | grep -iE '\.(mov|mp4|m4v|webm|avif|jpe?g)$' || echo "no media in tree"
npx astro check
npm run build
npx prettier --check .
python3 Scripts/check_contrast.py tokens.css
```

## Commits

`[W.3b] media: <description>` — the encoder, the manifest, the roadmap update. Never media.

## Closeout (inline — this repo has no closeout skill)

1. Files changed.
2. Verification output, verbatim.
3. The Task 4 table and Matt's Task 5 verdicts.
4. Every public URL, with its size.
5. Anything over budget, and what was traded.
6. The two decisions, as answered.
7. **Handoff to W.4:**
   - The manifest path and its shape.
   - **`VideoTile` must emit the manifest's full `type`, codecs included.** It currently
     builds `type` from the file extension alone (`video/webm`), and to that Safari on
     M1/M2 answers "maybe", tries the AV1 file, and fails, rather than skipping to the
     H.264 source. With the codecs parameter, Safari declines the AV1 source outright and
     plays the MP4.
   - Cymatic Resonance is the hero.

## DECISION-NEEDED (answer at Task 2)

**1. How long should each loop be?**

- **A — 15 s everywhere.** The loop repeats sooner and a watchful visitor may notice, but
  every file has the most bitrate per second, so the H.264 file most Mac visitors see
  looks its best within budget.
- **B — 30 s everywhere.** Repetition is much harder to spot, but the budget spreads over
  twice the time, so the H.264 file looks visibly softer on fine particles — or runs over
  budget.
- **C — hero 30 s, gallery 15 s.** Visitors linger on the hero, where the plan already
  allows a larger file; gallery tiles are glanced at.

**Recommendation: C.** **Default if no answer: C.**

**2. How should each loop's end meet its start?**

- **A — A half-second crossfade.** The loop reads as continuous. It is a transition between
  two real stretches of the same performance, not invented motion.
- **B — A hard cut at the best-matching frame pair inside the window.** Pure footage, but a
  visible jump every cycle, and a cut can change overall brightness at once — the very
  thing steady luminance exists to prevent.

**Recommendation: A**, with Task 4's seam-luminance check applied either way. **Default if
no answer: A.**
