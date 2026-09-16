#!/usr/bin/env python3
"""Accept or reject a W.3a capture master.

A master is Uzume's own recording of itself (`UZUME_RECORD_VIDEO=capture`, app repo
REC.1): ProRes 422 in `.mov`, one frame per rendered frame. This checks one recording
against what W.3b needs from it:

  - the stream is ProRes, 1920x1080, video only;
  - somewhere in it there is a long enough *clean run* to cut a website loop from: every
    frame exactly one sixtieth of a second after the last, and no frame identical to the
    one before it. A duplicate breaks a run just as a timing gap does, because it hides a
    dropped frame under a correct timestamp, which no timing check can see.

The rest of the file is expected to be untidy, and is reported but not judged. Recording
start-up is irregular for a few seconds (REC.1: five gaps, all in the first 5.7 s), and
switching presets can freeze the picture — W.3a's Ferrofluid Ocean take held one image
for half a second while the preset loaded, 29 duplicate frames, all well before the
preset was on screen. A loop is cut from inside the clean run, so that is what passes
or fails.

    python3 Scripts/check_capture.py <session_dir or video.mov>
    python3 Scripts/check_capture.py --self-test

Exit 0 pass, 1 fail, 2 usage or tool error.
"""

import collections
import json
import pathlib
import subprocess
import sys

CODEC = "prores"
SIZE = (1920, 1080)
MIN_CLEAN_S = 30.0  # the longest published loop; W.3b picks its window inside this run

# ponytail: no written-vs-rendered frame count against features.csv. REC.1 proved the
# recorder writes >= 99.97 % of rendered frames, and video timestamps are not on the
# log's clock, so aligning the two needs a heuristic. Add it if a master ever passes
# here and still looks short.


def die(message):
    print(f"check_capture: {message}", file=sys.stderr)
    sys.exit(2)


def run(*args):
    try:
        return subprocess.run(args, check=True, capture_output=True, text=True).stdout
    except FileNotFoundError:
        die(f"{args[0]} not found on PATH (brew install ffmpeg)")
    except subprocess.CalledProcessError as error:
        print(error.stderr.strip(), file=sys.stderr)
        die(f"{args[0]} failed (exit {error.returncode})")


def gaps(times):
    """Interval between consecutive frames, in whole sixtieths of a second."""
    return [int((b - a) * 60 + 0.5) for a, b in zip(times, times[1:])]


def longest_clean_run(times, hashes=None):
    """(seconds, start, end) of the longest stretch where every gap is one frame and, if
    frame hashes are given, no frame repeats the one before it."""
    best = (0.0, 0.0, 0.0)
    start = 0
    for i, gap in enumerate(gaps(times) + [None]):
        repeat = hashes is not None and gap is not None and hashes[i + 1] == hashes[i]
        if gap != 1 or repeat:
            span = times[i] - times[start]
            if span > best[0]:
                best = (span, times[start] - times[0], times[i] - times[0])
            start = i + 1
    return best


def duplicate_count(hashes):
    return sum(1 for a, b in zip(hashes, hashes[1:]) if a == b)


def check(path):
    video = path / "video.mov" if path.is_dir() else path
    if not video.is_file():
        die(f"no video at {video}")

    probe = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", str(video)))
    streams = probe["streams"]
    picture = next((s for s in streams if s["codec_type"] == "video"), None)
    audio = [s for s in streams if s["codec_type"] == "audio"]
    if picture is None:
        die(f"{video} has no video stream")

    # Timing comes from the container's packet timestamps, which are exact. Content comes
    # from decoding every frame. Neither ffmpeg source does both: framemd5's own
    # timestamps are rounded to a coarser time base (a 16.7 ms interval reads as 0 or 2
    # frames), and without `-fps_mode passthrough` ffmpeg re-times its output and silently
    # drops frames — which could hide a duplicate. Both were measured on W.3a's Ferrofluid
    # Ocean take before this was settled.
    if picture["codec_name"] != CODEC:
        print(video)
        print(f"  FAIL  codec {picture['codec_name']} — not a capture master; nothing else checked")
        print("  REJECT")
        return False

    times = sorted(float(t) for t in run(
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(video)).split())
    # The slow step: 81 s for REC.1's 109 s capture, about three minutes for a full track.
    hashes = [line.split(",")[-1].strip() for line in run(
        "ffmpeg", "-v", "error", "-i", str(video), "-an", "-fps_mode", "passthrough",
        "-f", "framemd5", "-").splitlines()
        if line and not line.startswith("#")]
    # ponytail: pairs the nth packet with the nth decoded frame. That holds for ProRes,
    # which is intra-only and never reorders frames. Any mismatch means it does not.
    if len(hashes) != len(times):
        die(f"{len(times)} packets but {len(hashes)} decoded frames")

    size = (picture["width"], picture["height"])
    duration = float(probe["format"]["duration"])
    clean_s, clean_from, clean_to = longest_clean_run(times, hashes)
    dupes = duplicate_count(hashes)
    histogram = dict(sorted(collections.Counter(gaps(times)).items()))

    results = [
        (f"codec {picture['codec_name']} {picture.get('profile', '')}".rstrip(),
         picture["codec_name"] == CODEC),
        (f"size {size[0]}x{size[1]}", size == SIZE),
        (f"audio streams {len(audio)}", not audio),
        (f"longest clean run, no gaps or duplicates: {clean_s:.1f} s "
         f"({clean_from:.1f}-{clean_to:.1f} s)",
         clean_s >= MIN_CLEAN_S),
    ]

    print(video)
    print(f"  frames {len(times)}, {duration:.1f} s, "
          f"{int(probe['format']['size']) / 1e9 / (duration / 60):.2f} GB/min")
    print(f"  gaps in 1/60 s: {histogram}")
    print(f"  duplicate consecutive frames in the whole file: {dupes}")
    for label, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    passed = all(ok for _, ok in results)
    print(f"  {'ACCEPT' if passed else 'REJECT'}")
    return passed


def self_test():
    frame = 1 / 60
    # Irregular start-up (a 3-frame gap, then a 0-frame catch-up), then 40 s clean.
    times = [0, frame, 4 * frame, 4.05 * frame]
    times += [times[-1] + frame * (i + 1) for i in range(40 * 60)]
    assert gaps(times[:4]) == [1, 3, 0], gaps(times[:4])
    seconds, start, end = longest_clean_run(times)
    assert abs(seconds - 40.0) < 1e-6 and abs(start - 4.05 * frame) < 1e-6, (seconds, start, end)
    # A clean file with no irregular gap at all is one run, end to end.
    assert abs(longest_clean_run([i * frame for i in range(61)])[0] - 1.0) < 1e-6
    # A gap at the very end must not extend the run.
    assert abs(longest_clean_run([0, frame, 2 * frame, 5 * frame])[0] - 2 * frame) < 1e-6
    assert duplicate_count(["a", "b", "b", "c", "c", "c"]) == 3
    # Perfect timing, but a frozen picture: a duplicate must split the run in two.
    even = [i * frame for i in range(121)]
    frozen = [str(i) for i in range(121)]
    frozen[50] = frozen[49]
    seconds, start, end = longest_clean_run(even, frozen)
    assert abs(seconds - 70 * frame) < 1e-6 and abs(start - 50 * frame) < 1e-6, (seconds, start)
    # Without hashes, timing alone decides — the same input is one unbroken run.
    assert abs(longest_clean_run(even)[0] - 2.0) < 1e-6
    print("check_capture self-test: ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    elif len(sys.argv) == 2:
        sys.exit(0 if check(pathlib.Path(sys.argv[1]).expanduser()) else 1)
    else:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        print("usage: check_capture.py <session_dir or video.mov> | --self-test", file=sys.stderr)
        sys.exit(2)
