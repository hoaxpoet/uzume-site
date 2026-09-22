#!/usr/bin/env python3
"""Fail when prose loses the space beside an inline element.

Astro trims leading and trailing whitespace on each line of JSX-like markup, so
prose that ends a line and an inline element that starts the next are joined
with no space between them:

    The Goddamn Shame,
    <em>Dispatches from the Grey City</em>

renders as "The Goddamn Shame,Dispatches from the Grey City". It is invisible in
the source, it survives review, and this repository shipped three of them — one
live on /gallery for weeks. The guard is an explicit `{" "}` at the end of the
text line.

Source, not built output: a branch the build never renders cannot be checked in
the HTML, and gallery.astro's Milkdrop lineage line is exactly that — correct,
but only by luck until a preset with `inspired_by` is published.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "src"

# Elements that sit inside a sentence. A block element on the next line is a
# new paragraph and wants no space.
INLINE = r"a|em|strong|span|code|b|i|abbr|cite|small|sub|sup|time|mark|q"

# Prose ending a line: a word character or the punctuation that can close a
# clause. A line ending in `>` is markup and never matches.
TEXT_END = re.compile(r"[A-Za-z0-9,;:.)!?”’]$")
INLINE_OPEN = re.compile(rf"<(?:{INLINE})\b", re.IGNORECASE)
INLINE_CLOSE = re.compile(rf"</(?:{INLINE})>$", re.IGNORECASE)
TEXT_START = re.compile(r"^[A-Za-z0-9(“‘]")
GUARD = ('{" "}', "{' '}", "{&nbsp;}")


def strip_non_markup(text: str) -> list[str]:
    """Blank out frontmatter, <style> and <script> so only markup is scanned.

    Lines are blanked rather than removed so reported numbers match the file.
    """
    lines = text.split("\n")
    out = list(lines)
    inside = None
    fence = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "---":
            fence += 1
            out[i] = ""
            inside = "frontmatter" if fence == 1 else None
            continue
        if inside == "frontmatter":
            out[i] = ""
            continue
        if re.match(r"<(style|script)\b", stripped, re.IGNORECASE):
            inside = "block"
        if inside == "block":
            out[i] = ""
            if re.search(r"</(style|script)>", stripped, re.IGNORECASE):
                inside = None
    return out


def findings(path: Path) -> list[tuple[int, str, str]]:
    lines = strip_non_markup(path.read_text(encoding="utf-8"))
    hits: list[tuple[int, str, str]] = []
    for i in range(len(lines) - 1):
        current, following = lines[i].rstrip(), lines[i + 1].lstrip()
        if not current or not following or current.lstrip().startswith(("//", "*")):
            continue
        if current.endswith(GUARD):
            continue
        if TEXT_END.search(current) and INLINE_OPEN.match(following):
            hits.append((i + 1, current.strip(), following))
        elif INLINE_CLOSE.search(current) and TEXT_START.match(following):
            hits.append((i + 1, current.strip(), following))
    return hits


def main() -> int:
    files = sorted(SOURCES.rglob("*.astro"))
    if not files:
        print("No .astro sources found — nothing to check.", file=sys.stderr)
        return 1

    total = 0
    for path in files:
        for line, current, following in findings(path):
            total += 1
            rel = path.relative_to(ROOT)
            print(f"{rel}:{line}: prose meets an inline element with no space")
            print(f"    {current[-72:]}")
            print(f"    {following[:72]}")
            print('    fix: end the first line with {" "}')

    if total:
        print(f"\nCopy spacing gate failed: {total} joined pair(s).")
        return 1

    print(f"Copy spacing gate passed: {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
