## Increment W.4 — Gallery: the footage on the site

**Type:** feature (**site repo**).

**Objective.** After this session, uzume.io shows its own engine. The landing hero carries
Murmuration's loop, a `/gallery` page presents the three published performances with their
names, authors and `inspired_by` attribution, and a teaser on the landing page points at
it. Every preset entry is generated from the app repo's sidecars rather than hand-typed,
and the site still builds without the app repo present. No new footage: W.3b published
what exists.

**What exists now.** `src/data/media.json` (W.3b, merged as `c456585`) describes three
presets — `murmuration` (`hero`, 30 s), `cymatic-resonance` and `ferrofluid-ocean`
(`gallery`, 15 s each) — with an AV1/WebM and an H.264/MP4 rendition, an AVIF and a JPEG
poster, and provenance. All twelve objects are live on `https://media.uzume.io`, verified
for headers, range requests and playback under the production CSP. `public/_headers`
already allows `media-src` and `img-src` from that host. `VideoTile.astro` and
`PresetCard.astro` exist from W.1 and have never been given real media. The landing hero
is typographic; W.2 left "the hero has no footage" open on purpose.

**One fact that shapes the whole session.** Safari on M1 and M2 Macs has no AV1 hardware
decoder and plays the H.264 file. `VideoTile` currently builds each source's `type` from
the file extension alone (`video/webm`), and to that Safari answers "maybe", commits to
the AV1 file, and fails — rather than skipping to the H.264 source. The manifest's `type`
carries the codecs parameter (`video/webm; codecs="av01.0.09M.08"`) precisely so Safari
declines the first source outright. **Emit the manifest's `type` verbatim; never rebuild
it from the filename.** Test in Safari, not only in Chrome.

## Skill invocations

None. This repo carries none of the app repo's skills. Closeout is inline, below.

## Read first, in order

1. `src/data/media.json` — the manifest. Its shape is the contract for everything here.
2. `docs/planning/WEBSITE_ROADMAP.md` §3 W.3 (**Delivered** and **From W.3b**) and W.4 —
   what W.3b handed over and what this session owes.
3. `docs/planning/WEBSITE_PLAN.md` §3 (information architecture) and §5 (media pipeline).
4. `src/components/VideoTile.astro`, `src/components/PresetCard.astro`,
   `DesignSystem/COMPONENTS.md` — the contracts these components must keep.
5. `src/pages/index.astro` — the hero as W.2 built it, including the one-time opening
   animation and its reduced-motion collapse.
6. `BRAND.md` §Image and footage direction (copy over busy regions needs a scrim or a
   separate field) and §Motion behavior; `CLAUDE.md` (copy law, tokens, source-of-truth
   boundary).
7. App repo, read-only: `UzumeEngine/Sources/Presets/Shaders/*.json` (the sidecars) and
   `docs/PRESET_ROSTER_REVIEW_2026-09-04.md` (quote, never paraphrase).

## Pre-flight invariants — stop if any fails

1. Site repo: clean working tree, branched from an up-to-date `main` containing W.3b
   (merge `c456585`).
2. `python3 -c "import json;d=json.load(open('src/data/media.json'));assert len(d)==3"` and
   every URL in it returns `200` (the W.3b verification one-liner).
3. The app repo is readable at `~/Documents/Projects/uzume` (or wherever this Mac keeps
   it). **Its checkout is a local convenience, not a build dependency** — see Task 3.
4. `npm ci` has been run in this worktree *and* in the main checkout (CLAUDE.md's
   `tsconfig` note), `npx astro check` and `npm run build` pass before any edit.

## Tasks

**1. Branch.** `git checkout -b w4-gallery`.

**2. Confirm the decisions.** Read the DECISION-NEEDED section to Matt and record his
answers. If he does not answer, proceed on the stated defaults.

*Done-when:* both decisions recorded.

**3. Preset data, generated not typed.** Write `Scripts/generate_presets.py` (Python,
beside `check_capture.py` and `encode_captures.py`). It reads the app repo's sidecars —
path from `--app-repo`, defaulting to `~/Documents/Projects/uzume` — and writes a content
collection entry per preset that has footage in `src/data/media.json`, carrying at least:
`name`, `slug`, `author`, `description`, `family`, `certified`, `inspired_by` (when the
sidecar has one) and the roster quote already in the manifest.

- **The generated files are committed.** CI, Cloudflare builds and a contributor's laptop
  have no app repo; the build must never read one. The script is how the data is
  refreshed, not how the site renders.
- **Two attribution sources, and the roadmap names the wrong one.** Preset authorship
  lives in each sidecar's `author` and `inspired_by` (24 of the roster are Matt's, four
  are "Uzume engine", one is a port). The app repo's `docs/CREDITS.md` is about bundled
  third-party ML weights and reference code — nothing about presets. Cite it only if a
  preset's `inspired_by` pack genuinely needs a licence note, and say so in the closeout.
- **Astro content collections need a schema.** Define it in `src/content.config.ts` (or
  the project's existing config) congruent with the sidecar fields — not a loose `any`.
- Re-running the script on unchanged inputs produces no diff.

*Done-when:* the script runs, the collection validates, and `npm run build` passes with
the app repo renamed away.

**4. `VideoTile`: emit the manifest's `type`.** Replace the extension-derived lookup with
the `type` string from the manifest, and give the component a prop shape that takes a
manifest rendition (`{url, type, width, height, ...}`) rather than a bare URL list. Keep
`preload="none"`, `muted`, `loop`, `playsinline`, the poster, and the reduced-motion
behaviour exactly as they are.

*Done-when:* rendered markup shows `type='video/webm; codecs="av01.0.09M.08"'` and
`type='video/mp4; codecs="avc1.64002A"'`, and Safari plays the MP4 (Task 9).

**5. Save-data and small screens get the poster** (Matt, W.3b). The hero loop is 15.4 MB;
a phone on a metered connection should receive the poster, which is 52–93 kB. Prefer the
declarative route (`<video>` without autoplay, poster first, load on interaction) over new
JavaScript. If script is unavoidable, it goes in the existing `VideoTile` block — the
site's only client JS — and must degrade to the poster when it does not run.

*Done-when:* at phone width, the hero costs a poster, not a loop; stated with the measured
number in the closeout.

**6. The hero.** Re-cut the landing hero with Murmuration per decision 2. The lockup,
tagline, lede, CTAs and requirements line stay; the W.2 opening animation and its
reduced-motion collapse survive. Contrast of every text element over whatever now sits
behind it must pass the gate — a bright dusk sky under white type is exactly the case
BRAND.md wants a scrim for.

*Done-when:* the hero shows real footage, reduced motion shows the poster, and contrast
passes with the numbers in the closeout.

**7. `/gallery`.** A page presenting the performances per decision 1: each with its loop,
poster, name, author, `inspired_by` attribution when present, and its roster quote.
Loops are lazy and in-viewport-only (the existing IntersectionObserver). Copy obeys
`PRODUCT.md` — future tense for the beta, no AI claims, "steady luminance" never a
flashes-per-second figure. Add the page to the nav.

*Done-when:* `/gallery` renders three performances on its preview URL.

**8. The landing teaser.** The gallery teaser W.2 deferred, now that there is something to
tease: a short section pointing at `/gallery`. Posters, not more loops — the hero already
spends the page's motion budget.

*Done-when:* the teaser links to `/gallery` and adds no second autoplaying loop.

**9. Verify in a real browser, on the preview URL.**

- **Safari** (Matt's M2 Pro): every loop plays the **MP4**. Confirm in the Network pane
  that the `.webm` was not fetched — that is the test that the codecs parameter worked.
- **Chrome:** every loop plays the **WebM**; console clean of CSP violations.
- **Reduced motion** (System Settings → Accessibility → Display → Reduce motion): no loop
  plays anywhere, posters stand, and the page is still complete.
- **Keyboard and screen reader:** each tile reachable and named; controls operable.
- Report `npx astro check`, `npm run build`, `npx prettier --check .`,
  `python3 Scripts/check_contrast.py tokens.css`, and the CI link check.

*Done-when:* every check reported, with the browser evidence.

**10. Record the decisions.** Per `CLAUDE.md`, decisions land in
`docs/planning/WEBSITE_ROADMAP.md`: this session's two decisions, W.4's status, and
anything found. Correct W.2's "the hero has no footage" open item.

*Done-when:* the roadmap reflects what exists.

## Do NOT

- **Do not re-encode, re-upload or delete media.** W.3b's twelve objects are published
  under immutable cache headers and reviewed by Matt. A rendition the site needs and does
  not have is a **finding**, not a task — say so and stop.
- **Do not commit media.** `.gitignore` blocks `.mov`, `.mp4` and `.m4v` as a backstop and
  does not block `.webm`, `.avif` or `.jpg`.
- **Do not edit `src/data/media.json` by hand.** It is `encode_captures.py`'s output.
- **Do not make the build read the app repo**, and do not add the app repo as a submodule
  or dependency.
- **Do not hand-write preset entries** that the generator should produce.
- **Do not add client JavaScript** beyond the existing `VideoTile` block. Components earn
  their JavaScript; this one already did.
- **Do not fork `tokens.css`** or hardcode a colour, size or type value.
- **Do not weaken `prefers-reduced-motion`.** It is honoured absolutely.
- **Do not assert product facts** the app repo does not support (`CLAUDE.md`, `PRODUCT.md`).
- **Do not push.** Commits stay local until Matt says "yes, push."

## Verification commands — all must pass before closeout

```
python3 Scripts/generate_presets.py            # re-run: no diff
python3 -c "import json;d=json.load(open('src/data/media.json'));assert len(d)==3;print('3 entries')"
git status --short --ignored | grep -iE '\.(mov|mp4|m4v|webm|avif|jpe?g)$' || echo "no media in tree"
npx astro check
npm run build
npx prettier --check .
python3 Scripts/check_contrast.py tokens.css
```

## Commits

`[W.4] site: <description>` — the generator, the component change, the pages, the roadmap.
Small and per logical step. Never media.

## Closeout (inline — this repo has no closeout skill)

1. Files changed.
2. Verification output, verbatim.
3. The preview URL, and what Matt should look at on it.
4. Safari evidence: the MP4 played and the WebM was not fetched.
5. Reduced-motion and contrast results, with numbers.
6. Page weight: what a first visit costs on desktop and at phone width.
7. The two decisions, as answered.
8. **Handoff to W.5:** anything the docs sessions inherit — nav shape, component
   contracts changed, and whether `PresetCard` is still used anywhere.

## DECISION-NEEDED (answered in advance — Matt, 2026-09-18)

**Both are already answered; Task 2 records them rather than asking again.**

- **1 → A**, the three, large. Matt: "we should capture more preset videos before launch,
  but for now i agree with your recommendation." The extra capture is a separate session
  (roadmap W.3, **Open**), not W.4's job.
- **2 → A**, full-bleed behind the lockup with a scrim.


**1. What does `/gallery` show, when only three of 25 certified presets have footage?**

- **A — The three, large.** A short page of three full-width performances. It reads as
  curated rather than unfinished, and matches BRAND.md's "a few large, immersive frames
  over galleries of tiny thumbnails". The page says more are coming, in the future tense.
- **B — The three, plus identity-only cards for the rest.** `PresetCard` already has a
  "preview unavailable" state. Honest about the roster's size, but 22 empty cards is the
  "three preview-unavailable boxes tease nothing" problem W.2 already rejected, at scale.
- **C — The three, plus a plain text list of the other certified presets.** Names without
  empty media frames: the roster's breadth without pretending each entry has a preview.

**Recommendation: A**, with C's list as a later addition once more footage exists.
**Default if no answer: A.**

**2. How does Murmuration's loop meet the hero's copy?**

- **A — Full-bleed behind the lockup, with a scrim.** What WEBSITE_PLAN §5 asks for. The
  loop is the argument the moment the page opens. Needs a scrim tuned so every text
  element still passes contrast over a bright, moving dusk sky, and the W.2 opening
  animation has to be reconciled with footage behind it.
- **B — A framed band directly under the lockup.** The typographic hero W.2 shipped stays
  intact and legible; the footage sits in its own field, which BRAND.md explicitly allows
  as the alternative to a scrim. Less arresting, and much less risky for contrast.

**Recommendation: A**, falling back to B if the scrim needed for contrast dulls the
footage enough that Matt would rather see it clean. **Default if no answer: A.**
