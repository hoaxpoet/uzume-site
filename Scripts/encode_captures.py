#!/usr/bin/env python3
"""Encode the W.3a capture masters into the website's loops, measure them, and write the
asset manifest (W.3b).

For each master in docs/captures/W3a-capture-log.json:

  - cut a loop from the middle of its clean loop window — hero (Murmuration)
    30 s, gallery 15 s — and
    join its end to its start with a half-second crossfade (W.3b decisions 1C and 2A).
    The crossfade blends the loop's last half second into the half second of real
    footage just before its first frame, so the last frame leads straight into the first;
  - encode AV1/WebM and H.264/MP4, 1920x1080 at a constant 60 fps, no audio, tagged
    BT.709, with no filtering beyond the 10-bit 4:2:2 -> 8-bit 4:2:0 conversion;
  - write an AVIF and a JPEG poster of the loop frame whose mean luma is closest to the
    loop's median;
  - measure each rendition (stream, frame timing, size, SSIM/XPSNR against the same
    loop built from the master, luminance at the seam) and save a contact sheet;
  - write src/data/media.json, keeping any `encode_verdict` already recorded in it.

Outputs go outside the repo, named by content hash. The posters and the manifest
reproduce byte for byte, and so does x264 wherever its rate cap does not bind hard;
Ferrofluid Ocean's H.264 loop, capped throughout, does not, and SVT-AV1 v4.1 does not
in any thread or rate configuration tried (W.3b). So a plain run keeps the loops the manifest already
publishes and only re-measures them — the published, reviewed bytes stay the source of
truth — and `--reencode` encodes every loop afresh.

    python3 Scripts/encode_captures.py [--reencode] [--only=<slug>] [out_dir]
                                                     default ~/Movies/Uzume masters/W3b

`--only=<slug>` re-encodes just that preset and keeps the rest, which is what you want
when a setting changes for one role: SVT-AV1 does not reproduce, so a blanket
`--reencode` rewrites every loop's bytes for no reason. An `encode_verdict` is carried
forward only onto the exact bytes it was recorded against — re-encode a clip and it
returns to unjudged, whatever the manifest said before.

Exit 0 when every rendition meets its bars, 1 when any does not, 2 on a tool error.
"""

import hashlib
import json
import pathlib
import re
import statistics
import subprocess
import sys

from check_capture import gaps, run

REPO = pathlib.Path(__file__).resolve().parent.parent
LOG = REPO / "docs/captures/W3a-capture-log.json"
MANIFEST = REPO / "src/data/media.json"
BASE_URL = "https://media.uzume.io"

FPS = 60
# W.3b: Matt moved the hero from Cymatic Resonance (the W.3a log's `role`) to
# Murmuration, the more atmospheric of the three. The log keeps its W.3a record.
HERO = "Murmuration"
SECONDS = {"hero": 30, "gallery": 15}  # decision 1C
FADE = FPS // 2  # decision 2A, frames
BUDGET_MB = {"hero": 24, "gallery": 12}  # WEBSITE_PLAN §5: 8-12 MB, hero "somewhat larger"

# Quality-targeted, with a peak-rate cap so a hard stretch cannot blow the budget.
# Measured on the 15 s loops (W.3b): SVT-AV1's mbr lets the average run ~10 % over the
# cap, hence 5000 against x264's 6M. Ferrofluid Ocean is near-incompressible — uncapped
# AV1 at CRF 30 is 48 MB for SSIM 0.949, against 0.937 in budget — so its cap binds.
# The hero is capped lower (Matt, W.3b): at the gallery cap Murmuration's 30 s loop was
# 22.5 MB, about 6 Mbit/s, which stalls on a weak connection. Lowered again at W.5l, the
# same decision continued: 4 Mbit/s still bought 15.4 MB for SSIM 0.9892, far above the
# 0.937 accepted for Ferrofluid Ocean, and the hero is the one file every landing-page
# visitor downloads. Both codecs sat pinned to their caps at 4 Mbit/s — AV1 and x264
# within 1 % of each other on a clip AV1 should win easily — so the cap, not CRF, is what
# sets this clip's size, and moving the cap moves the bytes almost linearly.
# ponytail: one setting per role; per-preset rates if one misses its bar.
CAPS = {"hero": ("2500", "3M"), "gallery": ("5000", "6M")}  # (SVT-AV1 kbps, x264)

CRF = {"webm": "34", "mp4": "20"}
# Per-preset CRF, where a role's default puts a rendition outside a bar. Skein's canvas
# is so luminance-stable that AV1's quantization noise at CRF 34 is larger than the
# motion the loop itself makes: the source loop seams at 0.004 YAVG against a 0.137
# in-loop maximum, but the AV1 encode of it seams at 0.08 against 0.07 and fails the
# seam bar — on noise, not on the cut. CRF 26 puts the noise back under the signal, and
# Skein's WebM is 2.8 MB against a 12 MB budget, so the bits are free.
# ponytail: one override, not a per-preset table; widen it only if another preset needs one.
CRF_OVERRIDE = {("skein", "webm"): "26"}

# Posters are placeholders, not prints. Six of the eight loops land at 13-52 kB of AVIF
# at CRF 20; Skein and Ferrofluid Ocean land at 439 and 382, because the dense
# high-frequency fields that make their video the heaviest on the site make their stills
# heavy too. Measured at W.5m before choosing this: the frame is not the cause — the 24
# frames closest to Skein's median luma, every one as representative as the one picked,
# span 427-441 kB — and the quality curve is shallow, so a ladder that stops at the first
# step inside budget beats a blanket quality cut. The first rung is the setting the light
# posters already use, so they encode once and reproduce byte for byte; only a poster
# over budget walks further down.
# ponytail: a flat ceiling, not a per-preset table; the ladder is the escape hatch.
POSTER_LADDER = {"avif": ("20", "26", "30", "34", "38", "42"),
                 "jpg": ("2", "4", "6", "8", "10")}

# Two sizes of still. The full one is what `<video poster>` shows, which is sized for a
# gallery frame. The narrow one is for the landing page's cards, which were drawing a few
# hundred pixels wide out of a 1920x1080 file. Measured at W.5n: the widest a card ever
# draws is 438 CSS px (at a 1100 px viewport, where the column is capped but the gutter
# has not yet grown), and the one-column phone layout at 375 px asks 303 CSS px, which a
# DPR 3 screen turns into 909 device px. 960 clears both with headroom and carries a
# quarter of the pixels, so one narrow rendition covers every case and the cards need no
# srcset. Budgets scale with the area.
# The thumb budget is not the poster's scaled by area. A quarter of it put Skein — the
# densest frame on the site — off the bottom of the ladder at CRF 42, which is a budget
# no encode of that frame can meet rather than an alarm worth hearing. These let it land
# mid-ladder and still cut the heaviest card by more than half.
POSTER_SIZES = (("posters", 1920, {"avif": 220_000, "jpg": 250_000}),
                ("thumbs", 960, {"avif": 80_000, "jpg": 100_000}))


def video_codec(ext, role, name):
    av1, x264 = CAPS[role]
    crf = CRF_OVERRIDE.get((name, ext), CRF[ext])
    return {
        "webm": ["-c:v", "libsvtav1", "-preset", "4", "-crf", crf,
                 "-svtav1-params", f"mbr={av1}:lp=4"],
        "mp4": ["-c:v", "libx264", "-preset", "veryslow", "-profile:v", "high", "-level:v", "4.2",
                "-crf", crf, "-maxrate", x264, "-bufsize", f"{int(x264[:-1]) * 2}M",
                "-movflags", "+faststart",
                # Frame threads under a VBV cap vary run to run; sliced threads fix that
                # unless the cap binds throughout (Ferrofluid). ponytail: -threads 1 fixes
                # it too, at ~5x the time; add it if a re-encode must be reproducible.
                "-x264-params", "sliced-threads=1"],
    }[ext]


MIME = {"webm": "video/webm", "mp4": "video/mp4", "avif": "image/avif", "jpg": "image/jpeg"}


def slug(preset):
    return preset.lower().replace(" ", "-")


def loop_input(entry, frames):
    """ffmpeg input args and filter chain for the loop of `frames` frames, built from the
    middle of the master's loop window; also returns its span within the master."""
    master = pathlib.Path(entry["file"]).expanduser()
    pts = sorted(float(t) for t in run(
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(master)).split())
    lo, hi = entry["loop_window_s"]
    need = frames + FADE
    window = [t - pts[0] for t in pts if lo - 1e-3 <= t - pts[0] <= hi + 1e-3]
    if len(window) < need:
        sys.exit(f"encode_captures: {entry['preset']}: loop window has {len(window)} frames, "
                 f"needs {need}")
    first = (len(window) - need) // 2
    span = window[first:first + need]
    if gaps(span) != [1] * (need - 1):
        sys.exit(f"encode_captures: {entry['preset']}: timing gap inside the loop window")
    # The loop is span[FADE:]; its last FADE frames fade into span[:FADE], the footage
    # immediately before its first frame.
    graph = (
        f"trim=end_frame={need},setpts=N/{FPS}/TB,split[a][b];"
        f"[a]trim=start_frame={FADE},setpts=N/{FPS}/TB,split[c][d];"
        f"[c]trim=end_frame={frames - FADE}[head];"
        f"[d]trim=start_frame={frames - FADE},setpts=N/{FPS}/TB[tail];"
        f"[b]trim=end_frame={FADE}[intro];"
        f"[tail][intro]blend=all_expr='A*(1-(N+1)/{FADE + 1})+B*(N+1)/{FADE + 1}'[seam];"
        f"[head][seam]concat=n=2:v=1:a=0,setpts=N/{FPS}/TB,"
        f"scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv,"
        f"format=yuv420p,"
        # Tag the frames: ffmpeg 8 encoders take colour from the frames, and the
        # -colorspace/-color_* output options alone left every stream untagged.
        f"setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv"
    )
    # Seek to half a frame before the first frame, so float rounding cannot skip it.
    args = ["-ss", f"{pts[0] + span[0] - 0.5 / FPS:.6f}", "-i", str(master)]
    return args, graph, (round(span[FADE], 3), round(span[-1] + 1 / FPS, 3))


def ffmpeg(*args):
    return subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", *args],
                          check=True, capture_output=True, text=True).stderr


def publish(tmp, out, stem, ext):
    """Rename to the content-hashed name; True if that exact file already existed."""
    digest = hashlib.sha256(tmp.read_bytes()).hexdigest()
    final = out / f"{stem}.{digest[:8]}.{ext}"
    existed = final.exists()
    tmp.replace(final)
    return final, digest, existed


def signal(inputs, graph):
    """Per-frame mean Y, U and V (signalstats) of the first output of `graph`."""
    out = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", *inputs, "-filter_complex",
                          f"{graph},signalstats,metadata=print:file=-", "-f", "null", "-"],
                         check=True, capture_output=True, text=True).stdout
    return tuple([float(v) for v in re.findall(rf"{c}AVG=([\d.]+)", out)] for c in "YUV")


def luma(inputs, graph):
    """Per-frame mean luma (signalstats YAVG) of the first output of `graph`."""
    return signal(inputs, graph)[0]


def seam_ok(yavg):
    """(seam change, largest in-loop change, ok): the jump from the last frame back to the
    first must be no larger than any change the performance itself makes."""
    seam = abs(yavg[0] - yavg[-1])
    inner = max(abs(b - a) for a, b in zip(yavg, yavg[1:]))
    return seam, inner, seam <= inner


def chroma_seam_ok(uavg, vavg):
    """(seam change, largest in-loop change, ok), the same bar as seam_ok but on colour:
    the hue jump from the last frame back to the first must be no larger than any colour
    change the performance itself makes. Distance is Euclidean in the U/V plane.

    Luma alone cannot see this. Nacre (W.3c) is a full-frame iridescent sheet whose hue
    drifts continuously, and its best-scoring span by luma held YAVG to within 3.6 while
    running teal to green — a chroma distance of 98, which would have snapped at the loop
    point with every luma bar passing.
    """
    def dist(i, j):
        return ((uavg[i] - uavg[j]) ** 2 + (vavg[i] - vavg[j]) ** 2) ** 0.5

    seam = dist(0, -1)
    inner = max(dist(i, i + 1) for i in range(len(uavg) - 1))
    return seam, inner, seam <= inner


def codecs_param(path):
    """RFC 6381 codecs string from the file's own decoder configuration record."""
    stream = json.loads(run("ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_streams", "-show_data", "-of", "json", str(path)))["streams"][0]
    data = bytes.fromhex("".join(re.findall(r"^[0-9a-f]+: ((?:[0-9a-f]{2,4} )+)",
                                            stream["extradata"], re.M)).replace(" ", ""))
    if stream["codec_name"] == "h264":  # avcC: version, profile, constraints, level
        return f"avc1.{data[1]:02X}{data[2]:02X}{data[3]:02X}"
    if stream["codec_name"] == "av1":  # av1C: marker|version, profile|level, tier|depth...
        depth = 12 if data[2] & 0x20 else 10 if data[2] & 0x40 else 8
        return f"av01.{data[1] >> 5}.{data[1] & 0x1F:02d}{'H' if data[2] & 0x80 else 'M'}.{depth:02d}"
    sys.exit(f"encode_captures: no codecs rule for {stream['codec_name']}")


def measure(path, ext, entry, inputs, graph, frames):
    probe = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", str(path)))
    video = [s for s in probe["streams"] if s["codec_type"] == "video"]
    v = video[0]
    times = sorted(float(t) for t in run(
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(path)).split())
    size = path.stat().st_size
    stats = ffmpeg("-i", str(path), *inputs, "-filter_complex",
                   f"[1:v]{graph}[ref];[0:v]split[e1][e2];[ref]split[r1][r2];"
                   f"[e1][r1]ssim;[e2][r2]xpsnr", "-v", "info", "-f", "null", "-")
    ssim = float(re.findall(r"SSIM Y:([\d.]+)", stats)[-1])
    ssim_all = float(re.findall(r"All:([\d.]+)", stats)[-1])
    xpsnr = float(re.findall(r"XPSNR +y: *([\d.]+)", stats)[-1])
    yavg, uavg, vavg = signal(["-i", str(path)], "null")
    seam, inner, seam_pass = seam_ok(yavg)
    cseam, cinner, cseam_pass = chroma_seam_ok(uavg, vavg)
    budget = BUDGET_MB[entry["role"]] * 1e6
    checks = {
        "stream": (v["codec_name"] == {"webm": "av1", "mp4": "h264"}[ext]
                   and (v["width"], v["height"]) == (1920, 1080)
                   and v["avg_frame_rate"] == v["r_frame_rate"] == f"{FPS}/1"
                   and len(probe["streams"]) == 1
                   and (v.get("color_space"), v.get("color_primaries"), v.get("color_transfer"),
                        v.get("color_range")) == ("bt709", "bt709", "bt709", "tv")
                   and (ext != "mp4" or v["profile"] == "High" and v["pix_fmt"] == "yuv420p")),
        "frames": len(times) == len(yavg) == frames and set(gaps(times)) == {1},
        "size": size <= budget,
        "seam": seam_pass,
        "chroma": cseam_pass,
    }
    return {
        "ext": ext, "path": path, "bytes": size, "type": f'{MIME[ext]}; codecs="{codecs_param(path)}"',
        "width": v["width"], "height": v["height"], "frames": len(times),
        "duration_s": round(len(times) / FPS, 3), "ssim_y": ssim, "ssim_all": ssim_all,
        "xpsnr_y": xpsnr, "seam": seam, "inner": inner,
        "chroma_seam": cseam, "chroma_inner": cinner, "checks": checks,
    }


def contact_sheet(out, stem, inputs, graph, renditions, frames):
    """Rows: four moments in the loop. Columns: master, AV1, H.264."""
    pick = "+".join(f"eq(n\\,{frames * k // 5})" for k in range(1, 5))
    column = f"select='{pick}',scale=960:540,format=rgb24,tile=1x4"
    ffmpeg(*inputs, "-i", str(renditions[0]), "-i", str(renditions[1]), "-filter_complex",
           f"[0:v]{graph},{column}[m];[1:v]{column}[a];[2:v]{column}[h];[m][a][h]hstack=3",
           "-frames:v", "1", str(out / f"{stem}.contact.png"))


def main():
    args = sys.argv[1:]
    reencode = "--reencode" in args
    only = {a.split("=", 1)[1] for a in args if a.startswith("--only=")}
    args = [a for a in args if a != "--reencode" and not a.startswith("--only=")]
    out = pathlib.Path(args[0] if args else "~/Movies/Uzume masters/W3b").expanduser()
    if REPO in out.resolve().parents or out.resolve() == REPO:
        sys.exit("encode_captures: the output directory must be outside the repo")
    for sub in ("loops", "posters", "thumbs", "contact"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    published = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
    verdicts = {e["slug"]: e["provenance"].get("encode_verdict") for e in published}
    # sha256 per slug as published, so a verdict can be carried forward only onto the
    # exact bytes it was given for.
    shas = {e["slug"]: {r["sha256"] for r in e["renditions"]} for e in published}
    kept = {r["url"].rsplit("/", 1)[1] for e in published for r in e["renditions"]}
    if only - {slug(e["preset"]) for e in json.loads(LOG.read_text())}:
        sys.exit(f"encode_captures: --only names no such preset: {sorted(only)}")

    manifest, all_ok = [], True
    for entry in json.loads(LOG.read_text()):
        # A captured master that cannot ship yet stays in the log as a capture record but
        # out of the manifest; `hold` says why.
        if entry.get("hold"):
            print(f"{entry['preset']} — held, not published: {entry['hold']}")
            continue
        entry = {**entry, "role": "hero" if entry["preset"] == HERO else "gallery"}
        name, frames = slug(entry["preset"]), SECONDS[entry["role"]] * FPS
        inputs, graph, span = loop_input(entry, frames)
        print(f"{entry['preset']} ({entry['role']}, {frames // FPS} s, master {span[0]}-{span[1]} s)")

        renditions = []
        fresh = reencode or name in only
        for ext in ("webm", "mp4"):
            keep = [p for p in (out / "loops").glob(f"{name}.*.{ext}") if p.name in kept]
            if keep and not fresh:
                path, existed = keep[0], True
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            else:
                tmp = out / "loops" / f".{name}.tmp.{ext}"
                ffmpeg(*inputs, "-filter_complex", graph, "-frames:v", str(frames), "-an",
                       "-map_metadata", "-1", "-fps_mode", "cfr", "-r", str(FPS),
                       *video_codec(ext, entry["role"], name), str(tmp))
                path, digest, existed = publish(tmp, out / "loops", name, ext)
            r = measure(path, ext, entry, inputs, graph, frames)
            r.update(sha256=digest, reproduced=existed)
            renditions.append(r)
            all_ok &= all(r["checks"].values())
            failed = [k for k, ok in r["checks"].items() if not ok]
            print(f"  {ext:4} {r['type']:38} {r['bytes'] / 1e6:5.2f} MB  {r['frames']} frames  "
                  f"SSIM Y {r['ssim_y']:.4f} (all {r['ssim_all']:.4f})  XPSNR Y {r['xpsnr_y']:.2f} dB  "
                  f"seam dY {r['seam']:.2f} <= {r['inner']:.2f}  "
                  f"dUV {r['chroma_seam']:.2f} <= {r['chroma_inner']:.2f}  "
                  f"{'PASS' if not failed else 'FAIL ' + ','.join(failed)}"
                  f"{'  (kept)' if keep and not fresh else '  (reproduced)' if existed else ''}")

        # Poster: the frame nearest the loop's median luma, from the same 8-bit loop.
        yavg = luma(inputs, graph)
        median = statistics.median(yavg)
        frame = min(range(len(yavg)), key=lambda i: (abs(yavg[i] - median), i))
        stills = {}
        for kind, width, budget in POSTER_SIZES:
            stills[kind] = {}
            # Lanczos rather than the default bilinear: this is a one-off downscale of a
            # still, so the sharper filter costs nothing and keeps the fine detail that
            # makes these frames worth showing.
            resize = "" if width == 1920 else f",scale={width}:-2:flags=lanczos"
            for ext, finish, codec in (
                    ("avif", "",
                     lambda q: ["-c:v", "libsvtav1", "-crf", q, "-svtav1-params", "lp=4"]),
                    ("jpg", ",scale=out_range=pc,format=yuvj420p",
                     lambda q: ["-c:v", "mjpeg", "-q:v", q])):
                tmp = out / kind / f".{name}.tmp.{ext}"
                for q in POSTER_LADDER[ext]:
                    ffmpeg(*inputs, "-filter_complex",
                           f"{graph},select=eq(n\\,{frame}){resize}{finish}",
                           "-frames:v", "1", "-map_metadata", "-1", *codec(q),
                           "-f", "avif" if ext == "avif" else "image2", str(tmp))
                    if tmp.stat().st_size <= budget[ext]:
                        break
                else:
                    print(f"  {ext:4} {kind[:-1]}: {tmp.stat().st_size / 1e3:.0f} kB at the "
                          f"bottom of the ladder, over the {budget[ext] / 1e3:.0f} kB budget")
                path, digest, existed = publish(tmp, out / kind, name, ext)
                stills[kind]["jpeg" if ext == "jpg" else ext] = {
                    "url": f"{BASE_URL}/{kind}/{path.name}", "bytes": path.stat().st_size,
                    "width": width}
                print(f"  {ext:4} {kind[:-1]:6} frame {frame} (Y {yavg[frame]:.1f}, "
                      f"median {median:.1f}) {width}w q {q:>2}  "
                      f"{path.stat().st_size / 1e3:.0f} kB"
                      f"{'  (reproduced)' if existed else ''}")
        posters = stills["posters"]

        contact_sheet(out / "contact", name, inputs, graph, [r["path"] for r in renditions], frames)

        manifest.append({
            "preset": entry["preset"], "slug": name, "role": entry["role"],
            "roster_quote": entry["roster_quote"],
            "renditions": [{
                "url": f"{BASE_URL}/loops/{r['path'].name}", "type": r["type"], "bytes": r["bytes"],
                "sha256": r["sha256"], "width": r["width"], "height": r["height"], "fps": FPS,
                "duration_s": r["duration_s"]} for r in renditions],
            "posters": posters,
            "thumbs": stills["thumbs"],
            "provenance": {
                "source_master_sha256": entry["sha256"],
                "loop_window_s": entry["loop_window_s"],
                "master_span_s": list(span),
                "crossfade_s": FADE / FPS,
                **{k: entry[k] for k in ("captured_at", "app_commit", "track", "rights",
                                         "d157_verdict")},
                "encode_verdict": (verdicts.get(name)
                                   if {r["sha256"] for r in renditions} == shas.get(name)
                                   else None),
            },
        })

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    subprocess.run(["npx", "prettier", "--write", "--log-level", "warn", str(MANIFEST)],
                   cwd=REPO, check=True)  # src/ is Prettier's; match it, or CI fails
    print(f"wrote {MANIFEST.relative_to(REPO)}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as error:
        print(error.stderr.strip()[-2000:], file=sys.stderr)
        sys.exit(2)
