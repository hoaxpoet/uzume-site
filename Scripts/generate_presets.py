#!/usr/bin/env python3
"""Generate the `presets` content collection from the app repo's preset sidecars.

The site never reads the app repo at build time — CI, Cloudflare and a
contributor's laptop have no checkout of it. This script is how the generated
entries are refreshed; the entries themselves are committed.

One entry per preset that has footage in `src/data/media.json`. Authorship comes
from the sidecar's own `author` / `inspired_by`; the app repo's `docs/CREDITS.md`
is about bundled ML weights and reference code and says nothing about presets.

    python3 Scripts/generate_presets.py [--app-repo PATH] [--check]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
MANIFEST = SITE / "src" / "data" / "media.json"
OUT_DIR = SITE / "src" / "content" / "presets"
SIDECARS = "UzumeEngine/Sources/Presets/Shaders/*.json"

# The site publishes these and nothing else: engine-internal sidecar fields
# (audio routes, pass lists, complexity costs) are not product facts the site
# asserts. `inspired_by` rides along only when the sidecar carries one.
FIELDS = ("name", "author", "description", "family", "certified")


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--app-repo",
        type=Path,
        default=Path("~/Documents/Projects/uzume").expanduser(),
        help="path to the app repo checkout (default: ~/Documents/Projects/uzume)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail instead of writing if any entry would change",
    )
    args = parser.parse_args()

    app_repo = args.app_repo.expanduser()
    sidecars = sorted(app_repo.glob(SIDECARS))
    if not sidecars:
        print(f"no sidecars under {app_repo / SIDECARS}", file=sys.stderr)
        return 1

    # Sidecar filenames are PascalCase and the slugs are not derived from them,
    # so match on the sidecar's own `name` — the same string the manifest holds.
    by_slug = {}
    for path in sidecars:
        sidecar = json.loads(path.read_text())
        by_slug[slugify(sidecar["name"])] = sidecar

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stale = set(OUT_DIR.glob("*.json"))
    changed = []

    for media in json.loads(MANIFEST.read_text()):
        slug = media["slug"]
        sidecar = by_slug.get(slug)
        if sidecar is None:
            print(f"{slug}: no sidecar in {app_repo}", file=sys.stderr)
            return 1

        entry = {"slug": slug}
        entry.update({key: sidecar[key] for key in FIELDS})
        if "inspired_by" in sidecar:
            entry["inspired_by"] = sidecar["inspired_by"]
        entry["roster_quote"] = media["roster_quote"]

        out = OUT_DIR / f"{slug}.json"
        stale.discard(out)
        text = json.dumps(entry, indent=2, ensure_ascii=False) + "\n"
        if not out.exists() or out.read_text() != text:
            changed.append(out)
            if not args.check:
                out.write_text(text)

    for orphan in sorted(stale):
        changed.append(orphan)
        if not args.check:
            orphan.unlink()

    for path in changed:
        print(f"{'would change' if args.check else 'wrote'} {path.relative_to(SITE)}")
    if args.check and changed:
        return 1
    print(f"{len(json.loads(MANIFEST.read_text()))} entries in {OUT_DIR.relative_to(SITE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
