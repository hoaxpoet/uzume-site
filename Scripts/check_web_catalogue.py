#!/usr/bin/env python3
"""Fail when the static design-system catalogue contains broken local references."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "DesignSystem" / "Web"


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.urls: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if identifier := values.get("id"):
            self.ids.add(identifier)
        for attribute in ("href", "src"):
            if url := values.get(attribute):
                self.urls.append((attribute, url))


def parse(path: Path) -> References:
    parser = References()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> int:
    pages = sorted(CATALOGUE.rglob("*.html"))
    parsed = {page: parse(page) for page in pages}
    failures: list[str] = []

    for page, references in parsed.items():
        for attribute, raw_url in references.urls:
            url = urlsplit(raw_url)
            if url.scheme in {"http", "https", "mailto", "tel", "data"} or raw_url.startswith("//"):
                continue
            if url.scheme:
                failures.append(f"{page.relative_to(ROOT)}: unsupported {attribute} scheme in {raw_url!r}")
                continue
            if raw_url == "#":
                failures.append(f"{page.relative_to(ROOT)}: placeholder {attribute}={raw_url!r}")
                continue

            target = page if not url.path else (page.parent / unquote(url.path)).resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                failures.append(f"{page.relative_to(ROOT)}: missing {attribute} target {raw_url!r}")
                continue
            if url.fragment and target.suffix == ".html":
                target_references = parsed.get(target) or parse(target)
                if unquote(url.fragment) not in target_references.ids:
                    failures.append(f"{page.relative_to(ROOT)}: missing fragment target {raw_url!r}")

    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures))
        return 1

    print(f"Catalogue gate passed: {len(pages)} pages and all local references resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
