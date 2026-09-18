---
target: the Uzume landing page and gallery
total_score: 24
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 1
timestamp: 2026-09-18T17-54-11Z
slug: src-pages-index-astro
---
Method: dual-agent (A: design review · B: detector + browser evidence)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Busy label, `role="status"`, focus move and the scroll handoff are right; nothing signals a 15.4 MB loop loading, and the teaser cards have no state at all. |
| 2 | Match System / Real World | 3 | Plain and human except `Matt · geometric` and "the roster's certified presets" — internal vocabulary shipped raw. |
| 3 | User Control and Freedom | 2 | A mistyped address is unrecoverable: on success the fields are `hidden` permanently, with no "wrong address?" path. |
| 4 | Consistency and Standards | 2 | Default Chrome video chrome sits on the footage on /gallery while every other control is designed; the same three presets appear in two grammars across the two pages. |
| 5 | Error Prevention | 3 | `type=email` + `required` + `reportValidity()` before any network, `preload="none"`, save-data and narrow guards. No confirmation on the one irreversible input. |
| 6 | Recognition Rather Than Recall | 2 | /gallery shows name + author + family and nothing else; "geometric"/"particles" is a taxonomy introduced nowhere. |
| 7 | Flexibility and Efficiency | 2 | Scored, not n/a: PRODUCT.md names two audiences and the contributor path sits 2,967px down the listener's page, absent from /gallery entirely. |
| 8 | Aesthetic and Minimalist Design | 3 | Genuinely restrained and token-clean; minimalism tips into emptiness in three measurable places. |
| 9 | Error Recovery | 2 | The error message is never associated with the input (`aria-invalid`/`aria-describedby` absent), so it does not exist for a screen reader returning to the field. |
| 10 | Help and Documentation | 2 | Scored, not n/a: "build from source" is the only thing anyone can do today, and the link points at the repo root, not a build guide. |
| **Total** | | **24/40** | **Needs work** |

## Design Specificity Verdict

**LLM assessment:** Partially authored — and the unauthored part is the hero. The three beats, the trust band's naming of Screen Recording and steady luminance, and the header handoff are things no other product could ship unchanged. But the hero image reads as a nature photograph, not software: Murmuration cropped to a 400px letterbox of dusk sky says nothing about "rendered," "Metal," "Mac" or "music." Swap the h1 and the same hero sells a birdwatching app. The page then has to *tell* you what it is in a `<p>` because the image cannot. The two presets that would read unmistakably as rendered light — Cymatic Resonance's cyan nodal rings, Ferrofluid Ocean's violet spike lattice — are 2,300px down as inert posters.

**Deterministic scan:** `detect.mjs --json src/pages src/components src/layouts` → `[]`, exit 0, 16 files, zero findings. Verified genuine, not a silent no-op: a synthetic control file fired `gradient-text` at the correct line with exit 2. Caveat worth recording — the static pass does not run the browser-engine rules (`skipped-heading`, `tiny-text`, `low-contrast`, `text-overflow`), so exit 0 means "no static findings," not "no findings."

**Browser evidence:** Zero CSP violations on either page. Zero horizontal overflow at 1440, 768 and 375. The scroll-driven handoff is confirmed live on a real `ViewTimeline` — `rgba(0,0,0,0)` / brand opacity `0` at scrollY 0, `rgb(11,12,16)` / opacity `1` at 400. Mobile confirmed fetching **no** `.webm`/`.mp4` at 375px, posters only; desktop selects the AV1 `.webm`. Tab order is clean and every control is named.

## Overall Impression

The engineering is in better shape than the design. Everything measurable passes — contrast, CSP, overflow, reduced motion, tab order, format negotiation, the codecs trap — and the detector is clean. What is weak is what no scan can catch: **the page never says what it is anywhere a machine or a screen reader can find it.** The document's complete heading outline contains the word "Uzume" twice and the words macOS, music and visualizer zero times; `<title>` is "Uzume — a light in sound." A Google result, a Slack unfurl, a heading rotor and a bookmark all render a name and an 18th-century poem. That is the hierarchy of a brand everyone already knows, used by a product with no recognition at all.

The single biggest opportunity: /gallery is the most persuasive thing the project owns and it is both unnavigable by heading and impossible to leave.

## What's Working

1. **The three beats are the product's argument, compressed.** "It listens to the whole playlist first / Then it plans the session / And it keeps listening while you play" turns a prepared-performance architecture into three sentences a listener can hold, and the third pre-empts the "so it's a waveform?" objection without naming it. It works because it is stated as a sequence *in time*, which is what the product actually is.

2. **The trust band is placed before it is needed, not after.** Explaining Screen Recording before anyone has been asked for it — and that local playback needs no permission at all — converts the scariest sentence in the product into a reason to trust it. The order *is* the reassurance: nobody is defending anything yet.

3. **The header handoff is a real state change, not decoration.** Both halves ride one `view-timeline` anchored to the hero's h1, so the name is never legible in two places at once. It reports something true — you have left the top of the page — rather than running on a timer, which is DESIGN.md's own test for welcome motion. `visibility` in the keyframes, keeping an invisible link out of the tab order, is the detail that proves it was thought through.

## Priority Issues

**[P1] Nothing in the document structure says what Uzume is.**
Verified: headings are `h1 Uzume` + 8 `h2`, two of which are the word "Uzume"; `<title>` is "Uzume — a light in sound." The only sentence identifying the product is a non-heading `<p class="hero__claim">`. The hero image does not carry it either.
*Why it matters:* SERP, social unfurls, heading rotor and bookmarks all render the same uninformative pair. A visitor who has never heard of Uzume gets a name over starlings.
*Fix (cheap):* `<title>` → "Uzume — a native macOS music visualizer"; rename the myth `h2` from "Uzume" to "The name". Two one-line changes that fix the rotor and the SERP without touching composition.
*Fix (structural):* make `.hero__claim` the `h1` at display scale and keep "Uzume" as a `<span>` lockup at 112px — it stays the largest *object* without being the largest *statement*, and the `view-timeline` lives on it just as happily.
*Suggested command:* `/impeccable clarify`

**[P2] /gallery is the argument, and it has neither headings nor an exit.**
Verified: the whole page is 2 headings — the three preset names are `<strong>` inside a figcaption, so heading navigation surfaces none of the work. And the last anchor in the document is the footer GitHub link: no CONTRIBUTING link under "Your preset could be the next one here," no email form, no route back.
*Why it matters:* this is the page where a visitor becomes convinced, and the only completable action on the site is not on it. A screen-reader user cannot navigate to any performance.
*Fix:* give `VideoTile` an optional heading level for its caption title so the gallery renders `h2` per performance (keeps the design-system contract); add the `Write a preset` button the landing page already has, plus `NotifyForm`, to `.outro`.
*Suggested command:* `/impeccable harden`

**[P2] The success state is the smallest moment on the page.**
On submit, `[data-fields]` is hidden and one 16px green sentence is left stranded in the ~300px the form vacated.
*Why it matters:* peak-end. The one outcome the surface exists to produce currently looks like an error recovered from, and it is rendered smaller than the fine print above it.
*Fix:* hold the `.notify` box height, set the confirmation at `--text-3xl` in `--font-display` with a success mark, add a line naming what arrives, and a quiet "Used the wrong address?" link that un-hides the fields — which also closes heuristic 3.
*Suggested command:* `/impeccable polish`

**[P2] The contributor invitation is padded twice: 33 characters per line in a 928px card.**
Verified: card 928px, `padding-inline` **248.5px each side**, content box 431px, paragraph 266px. Cause is mine — `main > section:not(.hero)` applies `padding-inline: max(gutter, calc(50% - var(--page-column)/2))`, and **a percentage padding resolves against the parent's width (1425px), not the element's own 928px**, so the centring padding is computed as if the card were still full-bleed after `max-width` already narrowed it. It is the same percentage-resolution trap I hit on `.hero__copy` and then reintroduced here.
*Why it matters:* one of PRODUCT.md's two audiences gets the worst-set text on the site, with 500px of dead width beside it.
*Suggested command:* `/impeccable layout`

**[P2] DESIGN.md now contradicts the shipped page in two places.**
§Shapes: "The outlined wordmark is never recreated with live text and is at least 96 px wide" — both the header and the hero h1 now do exactly that. §Layout: the first viewport is specified as footage + a product sentence + Apple Silicon/macOS 14+ requirements + "Download the beta" — the requirements were just removed and there is no download.
*Why it matters:* a design system that documents a rule its flagship page visibly violates is one nobody trusts the next time.
*Independent read:* keep the live text — the rule existed to stop the wordmark being approximated in a fallback face, and that risk is gone now the site serves Alumni Sans (the artefact *is* outlined Alumni Sans SemiBold); decisively, the handoff is only possible because both marks are the same live glyphs on one timeline. Amend the rule instead, and add a `font-display`/fallback-metrics check, because if Alumni Sans fails to load the h1 becomes Arial Narrow at 112px. On §Layout: removing the requirements line was right — it answered a question nobody had asked — so update the doc rather than restoring the line.
*Suggested command:* `/impeccable document`

## Persona Red Flags

**A Mac-owning listener who has never heard of Uzume (primary audience).**
- Nothing in the first 400px is a Mac, an app, or music. The identifying word is below the band.
- Clicks the Cymatic Resonance poster in "See it perform." Nothing happens — verified `<figure>`, no anchor, `cursor: auto`. Clicks Ferrofluid Ocean. Nothing happens.
- On /gallery, watches three silent loops in default Chrome video chrome sitting on the footage, told each is by "Matt · geometric." Cannot tell the visuals react to music at all, because the clips are silent and nothing says so until the last paragraph.
- Finishes /gallery convinced, finds no form, no button and no link but the nav, and leaves.
- On a phone: a static 211px JPEG strip where the demonstration should be. The narrow guard correctly blocks the 15.4 MB fetch, but nothing replaces the demonstration — so the mobile visitor is asked for an email having seen no evidence.

**A shader-writing contributor (second audience in PRODUCT.md).**
- The only thing they can do today — clone and build — is styled as a disclaimer: `--color-text-tertiary`, link demoted to `--color-text-secondary`. Every other link on the site is violet; this one is grey.
- `Write a preset` is at y ≈ 2,967 on the landing page and absent from /gallery.
- The invitation they finally reach sets its body at 33 characters in a card with 500px of unused width.
- `build it from source` points at the repo root, not a build guide.

**A reduced-motion / screen-reader visitor.**
- Reduced motion is handled properly — handoff inside `no-preference`, base rules are the finished state, the observer never runs. Genuinely good. The consequence: this visitor sees **zero evidence of what Uzume does on any page**. There is no still-image or textual substitute that demonstrates a performance.
- Navigating by heading: "Uzume", four sections, "Uzume" again. None of the nine says macOS, music or visualizer.
- On a failed submit, the message lands in a `<p role="status">` never referenced from the input. Returning to the field they hear the label and no error.
- On /gallery, three videos named only by preset — no duration, no indication they are silent.

## Minor Observations

- **Hit targets under 44px** (DESIGN.md: "Web interactive targets are at least 44×44 px"): skip link 122×**43** (1px under); header brand "Uzume" 53×**28** — the catalogue gives `.uz-site-navigation__link` a `min-height` of `--target-min-web`, and converting the brand to live text dropped it. The other two flagged links ("build it from source" 134×18, "Source on GitHub" 105×17) are inline in sentences and exempt under WCAG 2.5.8.
- **Stale public copy:** `gallery.astro`'s meta description still promises "the roster review's own words." The quotes were dropped in W.4. The page advertises content that no longer exists.
- `roster_quote` is still required by the content schema and generated into all three entries while rendering nowhere. Either drop it or use it.
- The trust band uses **status colour for non-status content** — a yellow `warning` callout for a permission explanation, a green `success` callout for a luminance policy. Nothing failed and nothing succeeded; it reads as three alert banners where the section is three reassurances.
- At 768px the `.beats` grid breaks a three-step argument into 2 + 1, leaving beat three alone beside an empty half-row.
- `<html data-theme="dark">` is hard-coded, so tokens.css's entire light appearance is dead on the site. Defensible for a dark theater — worth recording as a decision rather than leaving as an accident.
- `.myth__pronunciation` ("oo-ZOO-meh") sits 3,400px below the h1 that needed it.
- The `--focus-ring` inner stop is `--color-canvas`, which punches a 3px black halo into the footage when a header link is focused on the homepage.
- The landing page and /gallery use two different width systems (`--page-column` vs `--content-default`), so their text columns don't align across a navigation.
- `.beat p` has no `max-width` — safe at today's three-column grid, not after the first change to it.

## Questions to Consider

1. **If you deleted `.hero__claim`, could anyone tell what Uzume is from the first screen?** Today, no. If the image cannot carry any of the explaining, is the image wrong or is the crop wrong?
2. **The name is the biggest thing on the page for a product nobody has heard of. What is that scale buying?** A 112px "Uzume" earns its size the day the name means something.
3. **The gallery is the argument and it has no door out. What if it were the landing page?** Three full-width performances, the beats as captions underneath, the form at the foot.
4. **What is the still-image version of "performs light to music"?** Every reduced-motion visitor, every phone on cellular and every OG card is a static frame, and the site has no answer — which puts its argument out of reach of a large share of the people who see it.
