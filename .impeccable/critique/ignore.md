# Accepted findings

Findings recorded as accepted rather than fixed. `/impeccable critique` drops
matching findings silently, so anything here must carry its reason — an entry
without one is a finding that got tired, not one that was decided.

## low-contrast — the hero claim over the footage

**Finding:** pixel contrast 2.9:1 on desktop against a 3:1 bar, 3.0:1 at 375px
against 4.5:1, on "A music visualizer for macOS that listens, analyzes, and
accompanies." Text shadow over video underlay. Raised 2026-09-23.

**Accepted by Matt, 2026-09-23.** Near-white text over a bright dusk sky: every
fix changes what is behind the text, the text itself, or where it sits, and all
three are visible. Three were built and measured before accepting:

- A denser glyph halo moved the number not at all — a blur-only shadow spreads
  its darkness too thinly over a bright sky.
- An opaque stroke painted behind the fill reached 3.0:1 / 3.1:1. Still short,
  and it thickens the letterforms.
- Bold weight, to claim WCAG's 18.66px large-text bar, made it worse: the
  detector then applied 4.5:1 at both widths rather than 3:1 at either.
- A radial scrim behind the line passed at every viewport and was rejected on
  sight — it reads as a box on the picture, and the hero is the page.

**The real fix is the footage, not the type.** Murmuration's sky brightens
toward the bottom — measured 0.080 at the top to 0.448 at the foot — which is
why the line fails where it sits. W.3c's skyless scenes (Cymatic Resonance,
Dragon Bloom) have no sky at all, and `index.astro`'s own stage comment named
this before the critique did: "The real fix is footage whose sky does not
brighten toward the bottom, which is what W.3c is for."

**Revisit when** the hero clip changes, or when a scene with no sky is ready to
lead the page. Until then this is a known, recorded exception — not an oversight.

## heading-rhythm — the scene name on /gallery

**Finding:** the scene title sits 20px below the block above it and 44px above
the block below, against a rule that a heading should be closer to what it
introduces than to what precedes it. Eight instances, one per scene. Raised
2026-09-23.

**Declined, 2026-09-23.** The rule reads the title as an introduction to the
prose under it. It is not: `.uz-media-frame__title` is the caption of the frame
it sits inside, and the 20px is that frame's own padding. Measured at 1280px,
the name's immediate sibling below is the `author · family` line, which shares
its box — the 44px the detector saw is the distance to the *next* element, the
scene description, which is a separate block by design.

Widening the gap above would push the scene's name away from the scene's own
footage to satisfy a rule about prose headings. The grouping is already the one
the content has: footage, its name and author, then a paragraph about it.

**Revisit if** the title ever stops being a caption — if the name moves out of
the frame and becomes a section heading with the video beneath it.

## line-height — display headings at 0.92

**Finding:** `h1`/`h2` compute a 0.92 line-height, below the 1.08 floor.

**Declined, 2026-09-23.** `--leading-tight: 0.92` is the display set, applied
only where `--font-display` (Alumni Sans SemiBold) and `--tracking-display` are
applied with it — BRAND.md: "Keep display lines short, sentence case, and
tightly composed." The floor is a body-copy rule; body copy on this site runs
`--leading-body`. Tight-setting a display face is the typographic choice, not
an oversight, and loosening it would unpick the type system rather than fix a
heading.

**Revisit if** a display line ever wraps to three or more lines, where 0.92
stops being tight and starts being cramped.

## 404 — /favicon.ico

**Finding:** `/favicon.ico` returns 404.

**Declined, 2026-09-23.** Every page declares `rel="icon"` at 16, 32 and 64 and
`apple-touch-icon` at 180, so a browser that reads the document never asks for
`/favicon.ico` — only clients that skip the markup and guess the legacy path
do, and they get a 404 instead of an icon. Shipping one means a fifth copy of
the mark, in a container BRAND.md does not supply, to serve clients that did
not read the four it does.

**Revisit if** a real client is observed requesting it — a feed reader or link
unfurler whose card comes back blank.
