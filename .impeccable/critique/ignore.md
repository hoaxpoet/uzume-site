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
