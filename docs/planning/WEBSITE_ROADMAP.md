# Website Execution Roadmap — uzume.io

*2026-09-14 · Supersedes §8 (Phases) and resolves §10 (Open questions) of `WEBSITE_PLAN.md`. Everything else in that plan — stack, hosting, IA, media pipeline, repo structure — stands as written.*

## 1. Decisions resolved 2026-09-14

- **Domain.** uzume.io is registered. DNS/custom-domain wiring is W.0 work, not a purchase decision.
- **Launch posture: ship early.** The site launches before a notarized build exists. `/download` (working label: "Get Uzume") states the honest current shape — open source, clone-and-build today, notarized beta coming — and offers a notify path. **Revised 2026-09-14:** that path is an email capture, not GitHub watch — a plain form posting to **Kit (ConvertKit)**, so there is a list to mail when the beta lands. No embed script, no cookies on this origin, so the no-consent-banner position holds. Beta copy stays in the future tense per `PRODUCT.md` until a Releases artifact exists. The download CTA flip is its own later session (W.7), not a launch gate.
- **Capture licensing.** All published footage is captured against self-produced or openly-licensed tracks only, muted or not. The asset manifest records track and license per clip. No exceptions.
- **Analytics.** Cloudflare Web Analytics (cookieless, free, no consent banner), enabled at W.0 setup.

## 2. Verified current state (checked 2026-09-14)

**Done since the Aug 9 plan:**

- Rename complete through RN.5; both repos are Uzume; the GitHub social-preview card exists.
- BRAND.1 shipped the entire identity layer the plan's Phase 1 assumed would need creating: icon set, wordmark, favicons, fonts (OFL), `tokens.css`, the web component catalogue (`DesignSystem/Web/`), component contracts (`DesignSystem/COMPONENTS.md`), a rendered design reference (`design/index.html`), and contrast/catalogue check scripts. Phase 1 is now a *porting* job, not a design job.
- **24 of 31 preset sidecars carry `"certified": true`** (grep of `UzumeEngine/Sources/Presets/Shaders/*.json`, app repo, 2026-09-14). The plan's ≥6–8 gallery gate is met several times over; the gallery question is now curation, not supply.

**Not started:** the site itself — no Astro scaffold, no Cloudflare project, no R2 bucket, no pages, no capture footage.

**Deferred by decision:** the notarized build (Apple Developer Program, Developer ID signing, `notarytool`). App-repo work; gates only W.7.

**Stack check (2026-09-14):** Astro 7.x is current (7.2 latest minor); Starlight is at 0.42. The plan's choices hold; pin exact versions at scaffold time, not here.

## 3. Sessions

Each session is one PR, judged on its Cloudflare preview URL, with the exit criteria below. Lighter ceremony than app increments, per `WEBSITE_PLAN.md` §6.

### W.0 — Foundation *(done 2026-09-14)*

Scaffold Astro + Starlight at the repo root (`src/` layout per plan §6; `brand/`, `design/`, `DesignSystem/`, and the planning docs stay where they are). `.nvmrc` pinned. CI on PR: install, `astro check`, build, `lychee` link check. Cloudflare Worker with static assets, git-connected build, preview URL per PR. Custom domain uzume.io, `www` → apex, security headers in `public/_headers`. Web Analytics on. Wire the existing root `tokens.css` into the build as the single token source (move or import — don't fork it).

**Exit:** hello-world live at uzume.io; a test PR shows its own preview URL; CI green.

**Learned:** Starlight renders its own layout — anything global (tokens, analytics,
future nav/footer) must be wired in both `Base.astro` and the Starlight config, not
one. W.1's component port should assume two integration points, not one.

### W.1 — Tokens and components *(done 2026-09-14)*

Port the `DesignSystem/Web` catalogue into `.astro` components: `Nav`, `Footer`, `Button`, `VideoTile` (poster + lazy loop + reduced-motion fallback), `Callout`, `RequirementsList`, `PresetCard`. Zero client JS except where `VideoTile` needs it. Build `/design` from the live components.

**Exit:** `/design` renders every component; `Scripts/check_contrast.py` passes against the served tokens; reduced-motion verified by hand.

**Learned:**

- The two-integration-points problem from W.0 dissolves if each component imports
  `uzume-components.css` itself. Astro dedupes the import and ships it only to
  pages that use a component, so the components work under `Base.astro` and under
  Starlight's layout without either being configured for them.
- `VideoTile` needs no play/pause cluster: native `controls` on a muted, looping,
  `preload="none"` video covers the reduced-motion case, and the only client JS on
  the site is one IntersectionObserver that plays in-viewport loops when motion is
  welcome. If `play()` is refused for any reason the poster and controls remain.
- **The brand fonts are not served.** `tokens.css` names "Alumni Sans" and
  "PT Sans"; nothing declares `@font-face`, so every page renders in the fallback
  stack. `brand/fonts/PTSans.ttc` is 2.7 MB and `.ttc` is poorly supported in
  browsers — wiring this properly means subsetting to woff2. It belongs to W.2,
  where display type first carries weight.

### W.2 — Landing *(page built 2026-09-14; launch pending the hero decision)*

The landing page per plan §3, built with **placeholder footage** (a rough capture of any certified preset) so layout never waits on the capture pipeline. Copy constraints from `PRODUCT.md` are hard: beta in future tense, no AI claims, steady-luminance phrasing (never a flashes-per-second figure), primary CTA "On GitHub today — build from source" plus the notify path.

**Exit: the site is public.** A good landing page alone is a legitimate site; this is launch #1.

**Built:** hero, three beats, requirements, the three trust callouts, contributor
invitation, and the myth note. Every product claim is checked against the app
repo's `README.md` and preset sidecars — which caught `macOS 15 Sequoia` in the
W.1 `/design` sample data; the app requires **macOS 14 Sonoma**. Alumni Sans is
now served (`src/styles/fonts.css`, wired into both layouts), so display type
finally renders as designed.

**Open — the hero has no footage.** The plan asks for a full-bleed reel; the
session shipped a typographic hero instead, which is defensible on its own terms
(`PRODUCT.md`: "brand chrome is a restrained, dark, typographic frame") but is
not what the plan describes. No capture exists and none can be produced from this
repo: the app's `RENDER_VISUAL=1` harness emits **single frames**, not motion,
and its own notes say single-frame renders do not exercise frame-to-frame
accumulation. So a rough loop needs someone running the app on a Mac. Until then
the landing page is footage-ready but footage-free, and whether that is enough to
call the site public is Matt's call.

**Deferred to W.4 by the roadmap's own sequencing:** the gallery teaser. A teaser
built now is three "preview unavailable" boxes, which teases nothing; W.4 already
owns "add the gallery teaser" alongside the real clips.

**Added after review:**

- **Email capture.** `NotifyForm.astro` posts to Kit, form `9918547`. The id is
  public — it ships in the HTML either way — so it is a constant, not an
  environment variable, and needs no Cloudflare configuration.

  **The form answers in place and never leaves uzume.io** (Matt, 2026-09-14): a
  submit handler posts JSON and swaps the fields for a confirmation. Kit's
  endpoint permits cross-origin requests — verified against the live form — and
  returns `{"status": "success" | "failed", "errors": {...}}`, so a bad address
  is reported using Kit's own wording. The native `action`/`method` are real, so
  without JavaScript the form still posts and Kit shows its own page. The submit
  button reuses `setUzumeBusy` from the catalogue rather than a second spinner.

  **What the list is for (Matt, 2026-09-14):** the beta announcement first, then
  occasional release and feature news. An earlier draft promised "one message,
  nothing else" — that was not a decision anyone made, it was invented in the
  writing, and it would have locked every subscriber out of anything but the
  launch mail. Consent is scoped to what the form says at the moment of
  collection, so the promise has to cover the widest thing that will ever be
  sent. It now does. The list was empty when this landed, so no one needed
  re-permissioning.

  True onboarding mail — triggered when someone installs — is not possible from
  this list: nothing tells Kit an install happened. What it supports is the
  launch announcement, a getting-started follow-up after it, and release news.

  The **incentive email** (double opt-in) is Matt's to author in Kit. Its copy
  must keep the same scope as the form, or the two promises drift apart:

  > **Subject:** Confirm your email for the Uzume beta
  >
  > Click below and we'll email you when Uzume is ready to download.
  >
  > **[ Confirm my email ]**
  >
  > Uzume is a Mac app that listens to whatever music you're already playing and
  > performs light to it. It reads your playlist first, plans what to show, then
  > adjusts as the music goes.
  >
  > You can't download it yet. The first email you get will be the one that says
  > you can. After that, occasional notes when there's a new release.
  > Unsubscribe any time.
  >
  > Didn't sign up? Ignore this and you'll hear nothing.

  Written for the **listener** persona, not the contributor: an earlier draft led
  with GitHub Releases and building from source, which is message 4 of
  `BRAND.md`'s hierarchy aimed at someone who only wants their music made
  visible. Pythagoras does not sign it — `BRAND.md` scopes him to future in-app
  onboarding, explicitly not routine messaging.

  `consent.enabled` is still `false` on the form. Turning the incentive email on
  makes the inline success copy wrong — "You're on the list" stops being true
  until they click — so the two must ship together.

  `COMPONENTS.md` had removed `Input` as speculative "until a named consumer";
  this is that consumer and the only one, so the field stays local until a
  second earns it a place in the catalogue.
- **The authored opening.** The first W.2 draft shipped no motion, on a reading
  of "the engine's output is the brand" that the brand docs do not support.
  `BRAND.md` §Motion behavior defines the movement — *"content begins legible,
  darkness yields, and light becomes visible"* — and forbids only decorative
  motion (looping chrome, parallax, pulsing, synchronized section entrances).
  The hero now opens once at `--duration-deliberate` on `--ease-out`: light
  rises behind the wordmark, text legible from the first frame. Reduced motion
  needs no special case — `tokens.css` already collapses the duration to 1 ms.
  Contrast over the glow was checked by hand (weakest pairing ≈ 6.5:1); the
  gate script only covers flat token pairings.

**The pronunciation is live text, not a lockup.** It reads **oo-ZOO-may** (Matt,
2026-09-14): English speakers' untutored rendering of a Japanese final /e/ is
already "-ay", so the respelling agrees with what a reader will do rather than
fighting it, and it keeps the word "meh" out of the product's own pronunciation.
Three open syllables still holds, so nothing in `NAMING_REPORT.md`'s rationale
breaks.

`brand/wordmark/Uzume-pronunciation.svg` is **not used, and should not be**: it
bakes the respelling into vector letterforms, so it cannot be selected, scaled
with the reader's text settings, read as text, or corrected without regenerating
the artwork — which is exactly what stalled this. The myth section renders the
name as a heading in Alumni Sans (the wordmark's own face, so the look survives)
with the pronunciation as a plain paragraph beneath. It is deliberately **not**
uppercased like the lockup: "oo-ZOO-may" carries the stress in its capitals and
OO-ZOO-MAY throws that away.

Left alone: "oo-ZOO-meh" still stands in `PRODUCT.md`, `BRAND.md`, `CLAUDE.md`,
`NAMING_REPORT.md`, `WEBSITE_PLAN.md`, the three direction lockups, both BRAND.1
review pages, and eight files in the app repo. That is internal history, not
public copy, and this is a style call rather than a defect — sweep it when
something else touches those files.

**Found:** `[hidden]` was inert site-wide. A class rule carrying its own
`display` outranks the UA style for the attribute, so `el.hidden = true` set the
attribute and changed nothing — caught only because a screenshot disagreed with
a DOM assertion that had passed. `Base.astro` now carries
`[hidden] { display: none !important; }`.

**Found:** `brand/fonts/licenses/AlumniSans-OFL.txt` is a byte-for-byte copy of
`Geologica-OFL.txt` and names the wrong copyright holder, so the font ships
without its licence text until the brand file is corrected. `PTSans.ttc` and
`STIXTwoText.ttf` have no licence file at all.

### W.3 — Capture pipeline *(one to two sessions, plus capture time)*

Source or produce rights-clear tracks. Capture a 15–30 s 1080p60 loop per *selected* preset and one 30–60 s hero reel. `Scripts/encode_captures.sh`: AV1/WebM primary, H.264/MP4 fallback, no audio track, AVIF/JPEG posters, 8–12 MB per loop. R2 bucket served at `media.uzume.io`. Asset manifest (JSON, in-repo) records clip, poster, capture date, app commit, track, and license.

**Curation input:** `docs/PRESET_ROSTER_REVIEW_2026-09-04.md` in the app repo. Capture the roster's best 8–12, not all 24 — a gallery of strong clips beats a complete one.

### W.4 — Gallery *(one session)*

Content collection with a schema congruent with the preset sidecar JSON; a generation script reads the app repo's sidecars and `CREDITS.md` rather than hand-maintaining entries. `/gallery` grid of lazy, in-viewport-only loops with name, author, and `inspired_by` attribution. Re-cut the landing hero with real footage; add the gallery teaser.

### W.5 — Docs *(about two sessions)*

Starlight curation, outsider-first, per plan §3: Getting Started (requirements, build-from-source today, the Screen Recording permission explainer, local files vs. streaming), Using Uzume, Contributing Presets (two-file drop-in, hot reload, gates and certification lifecycle). Each page's frontmatter names its upstream app-repo doc; `lychee` checks those references in CI.

### W.6 — Launch polish *(one session)*

OG/social images from hero frames, favicons from `brand/favicon/`, 404 page, sitemap and basic SEO, `prefers-reduced-motion` audit across all pages, Lighthouse pass on throttled mobile.

### W.7 — Download flip *(blocked on app-side work; no site work wasted meanwhile)*

When a signed, notarized artifact is on GitHub Releases: `/download` gains the real CTA, the landing CTA flips, beta copy moves to present tense. Prerequisite track (app repo, parallel, start whenever): ADP membership → Developer ID signing → `notarytool` in the release pipeline → tagged Release.

## 4. Order

W.0 → W.1 → W.2 is the critical path to a public site. W.3 → W.4 follows independently; W.5 can start any time after W.1; W.6 precedes whatever moment gets called "launch"; W.7 trails on its own dependency. The placeholder-footage decision in W.2 is what decouples shipping from capturing.

## 5. Costs

Domain ~$50/yr (spent). Hosting, R2 (≤10 GB, zero egress), analytics, CI: $0 at this site's volumes on current free tiers. ADP $99/yr when the W.7 track starts — app-side, already flagged there. Steady-state ceiling including a possible uzume.app backorder landing: ~$150/yr. No API or token costs; the site is static.

## 6. Risks

- **Footage is the argument, and W.3 is the schedule risk.** Mitigated by placeholder-first W.2 — the site ships without it.
- **Clip staleness.** The roster is mid-uplift (Phase PR observations); captured clips can lag improved presets. The manifest's capture-date + app-commit fields make staleness visible, and re-capture is cheap once `encode_captures.sh` exists.
- **Docs drift.** Manual curation + frontmatter upstream refs + CI link-checking, per plan; revisit scripted sync only if drift becomes a real cost.
- **Claim discipline.** Every product claim on the site traces to the app repo (`README.md` source-of-truth rule). The certified count above is a build fact for planning, not marketing copy — the site shows certified presets; it doesn't promise a number.
