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

**Not started (as of 2026-09-14):** the site itself — no Astro scaffold, no Cloudflare
project, no R2 bucket, no pages, no capture footage. **Superseded:** W.0–W.2 built the
site, and W.3a/W.3b delivered the footage — the `uzume-media` R2 bucket is live at
`media.uzume.io` and serves three loops (see W.3 below).

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

**Closed at W.4 — the hero has footage.** W.2 shipped a typographic hero because
no capture existed and none could be produced from this repo (the app's
`RENDER_VISUAL=1` harness emits **single frames**, not motion). W.3a/W.3b
captured and published the loops, and W.4 re-cut the hero around Murmuration,
full-bleed behind the lockup with a scrim. The plan's full-bleed reel now exists.

**Deferred to W.4 by the roadmap's own sequencing:** the gallery teaser. A teaser
built now is three "preview unavailable" boxes, which teases nothing; W.4 already
owns "add the gallery teaser" alongside the real clips.

**Added after review:**

- **Email capture.** `NotifyForm.astro` posts to Kit, form `9921149`. The id is
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

  **Critiqued and rebuilt, 2026-09-15.** A dual-agent `/impeccable critique` of
  the shipped fragment scored it 19/40 and found two things a preview could not:
  with images blocked the wordmark's `alt` text inherited the client's default
  ink and rendered at **1.07:1** on the midnight card — the product's name was
  invisible, and the first legible word in the email was "Click" — and Kit's
  button was configured `#FFFFFF` on `#7f6aff`, **3.88:1**, below AA, when the
  file's own comment already specified the passing `#0b0c10` (5.03:1).

  **The email is light (Matt, 2026-09-15).** Kit owns the background and a
  footer carrying the unsubscribe link, the postal address and the "Built with
  Kit" badge; on the free plan none of it can be removed or restyled. Two dark
  designs were tried against that and both failed visibly — a dark card below
  the button left four pale wedges where Kit's light ground showed through the
  button's rounded corners, and the card itself read as a black slab pasted onto
  a white page with a seam everywhere the two met.

  Switching provider does not help. MailerLite, Buttondown and Resend all brand
  their free tiers and charge ~$9–20/month to stop. More to the point, the
  unsubscribe link and the postal address are **required by CAN-SPAM** whatever
  sends the mail, so the footer survives self-hosting too; only the "Built with
  Kit" line is optional. The jank was never the footer — it was the dark card
  above it.

  So the email shares Kit's ground. This is the brand's other half rather than a
  retreat from it: `tokens.css` already ships a complete light theme, and
  `BRAND.md` names "midnight on ivory" an approved inverse of the wordmark. The
  fragments declare **no background colour at all** — Kit's exact ground is not
  ours to know, so the wordmark PNG is transparent, the icon is masked to its
  squircle, and everything declared is ink on whatever Kit supplies. There is no
  edge left for the footer to clash with. Measured on Kit's ground: body 6.80:1,
  small print 4.92:1, lede 16.27:1, button 4.81:1.

  **Kit requires its own confirmation button** and refuses to publish without
  one. An `<a href="{{ confirm_url }}">` in the HTML block does not satisfy it,
  which killed a single-block version that had put the button inside the card.
  The block order is HTML, Kit's confirmation button, HTML. On a light ground
  that is simply a button in a message.

  **New assets.** `public/email/uzume-wordmark-ink.png` is the approved inverse,
  rendered from the unmodified `brand/wordmark/Uzume.svg` with only its fill
  changed, on a transparent ground. `public/email/uzume-icon.png` is downscaled
  straight from `brand/icon/Uzume-1024.png` (lanczos, 192px, no recolouring); an
  earlier derivation had left a #131319 edge lighter than its own card. The
  dark-ground `uzume-wordmark.png` is deleted — nothing referenced it, and it
  bakes #0b0c10 into an email that is no longer dark. The icon's CSS radius is
  the macOS squircle mask, which the PNG never carries; Outlook drops it and
  shows a square, the one place this design visibly degrades.

  **No copy refers to the button's position any more.** "Click
  below" and "the button below" both broke the moment the button moved, in a
  medium where you control neither layout nor client. Changes against the
  approved draft, all deliberate: the lede leads with the action rather than a
  location ("Confirm your email and we'll write the day…"); "Unsubscribe any
  time." is restored, because `NotifyForm.astro` ends its terms on that sentence
  and the two promises must stay identical; `BRAND.md`'s message 3 is added
  verbatim from `index.astro` ("Analysis and rendering run locally…") — for an
  app whose verb is "listens", its absence was the largest unforced omission; and
  the button names the reader's outcome ("Tell me when I can download it") rather
  than ours. `uzume.io` is named in the closing line so a recipient who does not
  remember signing up has somewhere to check that is not the button they distrust.

  **An MSO conditional now holds the card at 520px.** Word's engine does not
  support `max-width`, so the card had nothing constraining it in Outlook and ran
  the measure past 140 characters in a maximised reading pane.

  **The icon was rendering as a square patch.** The artwork is a fully opaque
  square with no alpha — macOS applies the squircle mask at runtime and the PNG
  never carries it — so the 20px CSS radius is the mask, not decoration, and
  dropping it exposed the square. The email asset also carried a #131319 top edge
  from an earlier compositing step, lighter than the #0b0c10 card, so the icon
  read as a rectangle sitting on the card. `public/email/uzume-icon.png` is now
  downscaled straight from `brand/icon/Uzume-1024.png` (lanczos, 192px, no
  recolouring), whose own edges are #09090e and darker and therefore fade into
  the card.

  **Kit's dashboard settings are recorded in `email/KIT_SETUP.md`** — the
  one-block rule, button colour, subject line, sender, and a test-send checklist. They were
  previously carried in an HTML comment that Kit never renders and no gate reads,
  which is how the failing button colour shipped. That file also answers the
  uzume.io address question: Cloudflare Email Routing handles **inbound** mail for
  free and makes `hello@uzume.io` a working reply-to immediately, but it cannot
  send — sending as the domain needs Kit's own domain authentication, with the
  DKIM records hosted in Cloudflare DNS. The From *name* is a free text field on
  any plan and is the highest-leverage part of the fix.

  `consent.enabled` is still `false` on the form. **(Corrected 2026-09-15: that
  field is Kit's GDPR Subscriber Consent Options, not the double opt-in flag —
  it reads `false` regardless of the double opt-in setting, so it was never
  evidence of anything here. Verify double opt-in by subscribing a real address
  and checking Subscribers → Unconfirmed; see `email/KIT_SETUP.md`.)** Turning the incentive email on
  makes the inline success copy wrong — "You're on the list" stops being true
  until they click — so the two must ship together. **The site half has now
  landed:** the form answers "Almost — check your email and confirm. Nothing
  happens until you do." Turning `consent.enabled` on is the remaining step, and
  it is now safe to take.

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

### W.3 — Capture pipeline *(done 2026-09-18: W.3a captured, W.3b encoded and published)*

Source or produce rights-clear tracks. Capture a 15–30 s 1080p60 loop per *selected* preset and one 30–60 s hero reel. `Scripts/encode_captures.sh`: AV1/WebM primary, H.264/MP4 fallback, no audio track, AVIF/JPEG posters, 8–12 MB per loop. R2 bucket served at `media.uzume.io`. Asset manifest (JSON, in-repo) records clip, poster, capture date, app commit, track, and license.

**Curation input:** `docs/PRESET_ROSTER_REVIEW_2026-09-04.md` in the app repo. Capture the roster's best 8–12, not all 24 — a gallery of strong clips beats a complete one.

**Delivered (W.3b, 2026-09-18).** Three loops, each AV1/WebM + H.264/MP4 + AVIF/JPEG
poster, on `https://media.uzume.io` from the `uzume-media` R2 bucket (custom domain,
min TLS 1.2). Built by `Scripts/encode_captures.py` — Python, not the `.sh` this line
first named — from the W.3a masters; manifest at `src/data/media.json`. Matt,
2026-09-18: "Quality appears strong across all three presets. Brightness is steady.
Clear to proceed."

**Decisions (W.3b).**

- **Loop length: hero 30 s, gallery 15 s.** Visitors linger on the hero, where the plan
  already allows a larger file; gallery tiles are glanced at.
- **Seam: a half-second crossfade**, between the loop's last half second and the real
  footage immediately preceding its first frame. Every seam's brightness change is far
  below the largest change the performance itself makes (hero 0.00–0.06 against 0.52).
- **Hero: Murmuration, not Cymatic Resonance** (the role the W.3a log recorded). The
  atmospheric footage suits the position, and its calm sky takes copy without a scrim.
  The capture log keeps its W.3a record; `HERO` in the encoder is the live decision.
- **Hero rate cap lowered to 4 Mbit/s** after review: at the gallery cap the 30 s loop
  was 22.5 MB (~6 Mbit/s), which stalls on a weak connection. 15.4 MB for SSIM 0.9892.

**Found: the budget does not bind Ferrofluid Ocean — its content does.** Uncapped AV1 at
CRF 30 is 48 MB for SSIM 0.949, against 0.937 at 11 MB. Near-incompressible dense
texture; spending four times the bytes buys nothing a viewer would see.

**Open: more footage before launch** (Matt, 2026-09-18). Three performances is what W.3a
captured and what W.4 builds on; the roster's certified 25 deserve a wider selection on
the site before it launches. A second capture-and-encode pass reuses `check_capture.py`
and `encode_captures.py` unchanged — add presets to the capture log and re-run. Not a
W.4 dependency.

**Found: the encodes are not reproducible end to end.** SVT-AV1 v4.1 gives different
bytes every run (tried: single thread, no rate cap), and x264 does too where its cap
binds throughout — Ferrofluid Ocean's H.264 loop. Everything else reproduces: the other
H.264 loops, all six posters, the manifest. So a plain `encode_captures.py` run keeps
the loops the manifest already publishes and only re-measures them; `--reencode` forces
fresh ones. Published, reviewed bytes stay the source of truth.

### W.4 — Gallery *(done 2026-09-18)*

Content collection with a schema congruent with the preset sidecar JSON; a generation script reads the app repo's sidecars and `CREDITS.md` rather than hand-maintaining entries. `/gallery` grid of lazy, in-viewport-only loops with name, author, and `inspired_by` attribution. Re-cut the landing hero with real footage; add the gallery teaser.

**From W.3b.** The footage is at `src/data/media.json` — one entry per preset with
`renditions`, `posters` and `provenance`.

- **`VideoTile` must emit the manifest's full `type`, codecs parameter included.** It
  builds `type` from the file extension today (`video/webm`), and to that Safari on
  M1/M2 answers "maybe", tries the AV1 file and fails, instead of falling through to the
  H.264 source. With `codecs="av01…"` Safari declines the AV1 source outright and plays
  the MP4. Those Macs have no AV1 hardware decoder, so this is most Mac visitors.
- **Murmuration is the hero** (30 s); Cymatic Resonance and Ferrofluid Ocean are gallery
  loops (15 s).
- **Ferrofluid Ocean wants room, not a headline over it.** It is the busiest of the
  three and the strongest demonstration of music sync — give it a wide, uncluttered
  section rather than the hero, where copy would need a scrim over its every pixel.
- **Poster-only on save-data and phone widths** (agreed with Matt, W.3b). The hero is
  15.4 MB; a phone on cellular should get the poster, which is 52–93 kB.

**Delivered (2026-09-18).** `/gallery` presents the three published performances
at full width; the landing hero carries Murmuration full-bleed behind the lockup;
a teaser between the trust band and the contributor invitation points at the
gallery with posters rather than a second loop. Preset entries are generated, not
typed: `Scripts/generate_presets.py` reads the app repo's sidecars and writes one
committed JSON file per preset into the `presets` content collection, whose
schema in `src/content.config.ts` is congruent with the sidecar fields. The build
never reads the app repo — verified by building with the checkout renamed away.

**Decisions (W.4).**

- **1 → A, the three, large.** Matt, 2026-09-18: "we should capture more preset
  videos before launch, but for now i agree with your recommendation." A short
  page of three full-width performances, which reads as curated rather than
  unfinished. The wider selection is W.3's open item, not W.4's job.
- **2 → A, full-bleed behind the lockup with a scrim.** Delivered as a top band
  of the hero rather than the full section — see the finding below.
- **The pull quote is out** (Matt, mid-session): "The pull quote is absolutely
  unnecessary." The roster quote is still generated into each preset entry, and
  is no longer rendered. Each performance carries its loop, poster, name, author
  and family, plus `inspired_by` where a preset has one.

**Found: the footage cannot sit behind the whole hero, only behind the lockup.**
Murmuration's flock drifts between 0.38 and 0.70 of the frame's height over the
30 s loop (measured frame by frame), and the hero's copy — tagline, lede, note,
notify form, CTA, requirements — needs the bottom half of the section. Footage
stretched over the whole hero puts the flock under the copy's scrim, hiding the
one thing it is there to show. The stage is the upper band instead
(`min(52svh, 30rem)`), with `object-position: 40% 58%` centring the crop window
on the flock's travel, and the copy below on its own field. Still full-bleed.

**Found: the scrim can be sized from the footage rather than by eye.** Alpha
compositing is linear in relative luminance, so a scrim of `--color-canvas` at
alpha *a* over footage of luminance *L* lands the background at
`a·0.0037 + (1−a)·L`. The loop's brightest local patch reaches 0.4476. The stage
scrim runs 0.86 across the top 4.5rem (the navigation's height) and 0.50 through
the lockup band; the copy field is 0.92. Measured against the brightest pixel any
row of the footage reaches at any point in the loop: wordmark 4.15:1 (needs 3.0
as a graphic), tagline 9.57:1, citation 7.13:1, lede 16.72:1, note 11.65:1,
notify label 17.96:1, notify terms 8.10:1, requirements 8.10:1. All pass.

**Found: none of the three published presets has an `inspired_by`.** Murmuration,
Cymatic Resonance and Ferrofluid Ocean are all Matt's originals. The generator
and the gallery both handle the field, and it will render on the first ported
preset that gets footage. `docs/CREDITS.md` in the app repo was not cited: it
covers bundled ML weights and reference code and says nothing about presets, so
the roadmap's earlier line naming it as an attribution source was wrong.

**Found: W.2's header handoff has never run, and the CSS minifier is why.**
`Nav.astro` sets `animation: header-settle linear both` followed by
`animation-timeline: --uz-hero-lockup`. The build's minifier folds the longhand
back into the shorthand as `animation: linear both header-settle --uz-hero-lockup`
— and `animation-timeline` is not a component of the `animation` shorthand, so
the whole declaration is invalid and dropped. `animation-name` computes to `none`
and `animation-timeline` to `auto` in the built site. The result is the fallback
the component's own comment describes as safe: an opaque header with a visible
wordmark, from the first pixel. It is pre-existing (the same source is on `main`)
and W.4 left it alone, because turning it on makes the header transparent over
the new footage — a deliberate look Matt should approve rather than inherit. The
fix is to write the four longhands instead of the shorthand. The hero's stage
scrim already carries 0.86 across the navigation's own height for that case.

**Found: Ferrofluid Ocean's poster is the heaviest asset on the site.** 551 kB
JPEG, 382 kB AVIF, against 48/18 kB for Cymatic Resonance and 93/52 kB for
Murmuration — the same near-incompressible dense texture W.3b found in its video.
The teaser's posters are `loading="lazy"`, so it costs nothing until scrolled to,
but the gallery loads it eagerly. The AVIF posters are unused site-wide: the
`<video poster>` attribute takes one URL and cannot negotiate a format. One for
W.6's Lighthouse pass.

**Page weight, measured.** At phone width a first visit is ~336 kB and fetches no
video at all — 243 kB of document, CSS, icon and Alumni Sans, plus the 93 kB
poster. At desktop it is that plus the one loop the browser selects: 15.3 MB
WebM in Chrome, 15.4 MB MP4 in Safari, and not both.

**Safari, verified on this M-series Mac (Safari 26.5, arm64).** With the
manifest's `type` emitted verbatim, `canPlayType('video/webm; codecs="av01…"')`
returns `""` — a definitive no — while the bare `video/webm` returns `"maybe"`,
which is exactly the trap. Safari therefore selects
`murmuration.7d8c7572.mp4` as `currentSrc` and never requests the AV1 file;
source selection happens before any fetch, so the WebM is not merely abandoned,
it is never asked for. Chrome selects the WebM.

**Inherited, not done here: `claude/w2-hero-impeccable`.** Two unmerged W.2
commits (`5562117`, `9b6ec38`) add `src/components/FirstOpening.astro` and
rewrite the hero. Matt: "hand it to W.4. w.4 should complete and then update hero
with the desired changes." So it is a separate pass over the finished W.4 hero,
not part of it. Merging it into `main` conflicts in `src/pages/index.astro` in
five hunks, all in the hero — a design choice, not a mechanical fix — and the
merge deletes `public/uzume-icon.png`, which `index.astro`, `404.astro` and
`confirmed.astro` all reference. Keep `main`'s copy.

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
