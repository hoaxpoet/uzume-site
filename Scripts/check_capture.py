#!/usr/bin/env python3
"""Accept or reject a W.3a capture master.

A master is Uzume's own recording of itself (`UZUME_RECORD_VIDEO=capture`, app repo
REC.1): ProRes 422 in `.mov`, one frame per rendered frame. This checks one recording
against what W.3b needs from it:

  - the stream is ProRes, 1920x1080, video only;
  - no two consecutive frames are identical (a duplicate hides a dropped frame under a
    correct timestamp, which no timing check can see);
  - somewhere in it there is a long enough run of clean 60 fps — every frame exactly
    one sixtieth of a second after the last — to cut a website loop from.

Recording start-up is expected to be irregular for a few seconds (REC.1 measured five
irregular gaps, all in the first 5.7 s). That is why the pass bar is a clean *run*,
not a clean *file*.

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


def run(*args):
    try:
        return subprocess.run(args, check=True, capture_output=True, text=True).stdout
    except FileNotFoundError:
        sys.exit(f"check_capture: {args[0]} not found on PATH (brew install ffmpeg)")
    except subprocess.CalledProcessError as error:
        print(error.stderr.strip(), file=sys.stderr)
        sys.exit(f"check_capture: {args[0]} failed (exit {error.returncode})")


def gaps(times):
    """Interval between consecutive frames, in whole sixtieths of a second."""
    return [int((b - a) * 60 + 0.5) for a, b in zip(times, times[1:])]


def longest_clean_run(times):
    """(seconds, start, end) of the longest stretch where every gap is one frame."""
    best = (0.0, 0.0, 0.0)
    start = 0
    for i, gap in enumerate(gaps(times) + [None]):
        if gap != 1:
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
        sys.exit(f"check_capture: no video at {video}")

    probe = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", str(video)))
    streams = probe["streams"]
    picture = next((s for s in streams if s["codec_type"] == "video"), None)
    audio = [s for s in streams if s["codec_type"] == "audio"]
    if picture is None:
        sys.exit(f"check_capture: {video} has no video stream")

    times = sorted(float(t) for t in run(
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(video)).split())
    # Decodes every frame — the slow step: 81 s for REC.1's 109 s capture, so about
    # three minutes for a full four-minute master.
    hashes = [line.split(",")[-1].strip() for line in run(
        "ffmpeg", "-v", "error", "-i", str(video), "-an", "-f", "framemd5", "-").splitlines()
        if line and not line.startswith("#")]

    size = (picture["width"], picture["height"])
    duration = float(probe["format"]["duration"])
    clean_s, clean_from, clean_to = longest_clean_run(times)
    dupes = duplicate_count(hashes)
    histogram = dict(sorted(collections.Counter(gaps(times)).items()))

    results = [
        (f"codec {picture['codec_name']} {picture.get('profile', '')}".rstrip(),
         picture["codec_name"] == CODEC),
        (f"size {size[0]}x{size[1]}", size == SIZE),
        (f"audio streams {len(audio)}", not audio),
        (f"duplicate consecutive frames {dupes}", dupes == 0),
        (f"longest clean 60 fps run {clean_s:.1f} s ({clean_from:.1f}-{clean_to:.1f} s)",
         clean_s >= MIN_CLEAN_S),
    ]

    print(video)
    print(f"  frames {len(times)}, {duration:.1f} s, "
          f"{int(probe['format']['size']) / 1e9 / (duration / 60):.2f} GB/min")
    print(f"  gaps in 1/60 s: {histogram}")
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
