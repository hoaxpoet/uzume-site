#!/usr/bin/env python3
"""Verify the semantic text/background pairs used by Uzume brand pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


COMMON_PAIRINGS = (
    ("--color-text-primary", "--color-canvas", 4.5),
    ("--color-text-secondary", "--color-canvas", 4.5),
    ("--color-text-tertiary", "--color-canvas", 4.5),
    ("--color-text-primary", "--color-surface", 4.5),
    ("--color-text-secondary", "--color-surface", 4.5),
    ("--color-text-tertiary", "--color-surface", 4.5),
    ("--color-text-primary", "--color-surface-raised", 4.5),
    ("--color-text-secondary", "--color-surface-raised", 4.5),
    ("--color-text-tertiary", "--color-surface-raised", 4.5),
    ("--color-on-accent", "--color-accent", 4.5),
    ("--color-on-accent", "--color-accent-hover", 4.5),
    ("--color-focus", "--color-canvas", 3.0),
    ("--color-focus", "--color-surface", 3.0),
    ("--color-text-disabled", "--color-control-disabled-background", 4.5),
)

STATUS_PAIRINGS = tuple(
    pairing
    for tone in ("warning", "danger", "success", "info")
    for pairing in (
        (f"--color-status-{tone}-foreground", f"--color-status-{tone}-background", 4.5),
        (f"--color-status-{tone}-border", f"--color-status-{tone}-background", 3.0),
        ("--color-text-primary", f"--color-status-{tone}-background", 4.5),
        ("--color-text-secondary", f"--color-status-{tone}-background", 4.5),
    )
)

PAIRINGS = COMMON_PAIRINGS + STATUS_PAIRINGS


def channel(value: int) -> float:
    value /= 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    color = hex_color.lstrip("#")
    if len(color) == 3:
        color = "".join(character * 2 for character in color)
    red, green, blue = (int(color[index : index + 2], 16) for index in (0, 2, 4))
    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def contrast(first: str, second: str) -> float:
    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_contrast.py tokens.css", file=sys.stderr)
        return 2

    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    def declarations(block: str) -> dict[str, str]:
        return dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8}|var\(--[\w-]+\))\s*;", block))

    root_match = re.search(r":root\s*\{(.*?)\n\}", source, re.DOTALL)
    light_match = re.search(
        r':root\[data-theme="light"\],\s*\[data-theme="light"\]\s*\{(.*?)\n\}',
        source,
        re.DOTALL,
    )
    if not root_match or not light_match:
        print("FAIL expected root and explicit light-theme token blocks", file=sys.stderr)
        return 1

    theme_declarations = {
        "dark": declarations(root_match.group(1)),
        "light": {**declarations(root_match.group(1)), **declarations(light_match.group(1))},
    }

    def resolve(mapping: dict[str, str], name: str, seen: set[str] | None = None) -> str | None:
        seen = set() if seen is None else seen
        if name in seen:
            return None
        seen.add(name)
        value = mapping.get(name)
        if value is None:
            return None
        if value.startswith("#"):
            return value
        reference = re.fullmatch(r"var\((--[\w-]+)\)", value)
        return resolve(mapping, reference.group(1), seen) if reference else None

    failures = 0

    for theme, mapping in theme_declarations.items():
        values = {name: value for name in mapping if (value := resolve(mapping, name))}
        print(f"\n{theme.upper()} THEME")
        for foreground, background, minimum in PAIRINGS:
            missing = [name for name in (foreground, background) if name not in values]
            if missing:
                print(f"FAIL missing token(s): {', '.join(missing)}")
                failures += 1
                continue
            ratio = contrast(values[foreground], values[background])
            status = "PASS" if ratio >= minimum else "FAIL"
            print(f"{status} {foreground} on {background}: {ratio:.2f}:1 (minimum {minimum:.1f}:1)")
            failures += ratio < minimum

    if failures:
        print(f"Contrast gate failed: {failures} pairing(s).", file=sys.stderr)
        return 1

    print(f"\nContrast gate passed: {len(PAIRINGS) * len(theme_declarations)} pairing(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
