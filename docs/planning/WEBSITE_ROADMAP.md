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

**Scoped as W.3c** (2026-09-18): `docs/planning/W.3c-prompt.md`. Four presets — Fractal
Tree, Aurora Veil, Nimbus, Dragon Bloom — taking the gallery to seven. The selection is
driven by one fact from `docs/PRESET_ROSTER_REVIEW_2026-09-04.md`: **Matt criticises music
sync on 13 of the 25 certified presets**, and sync is the claim the whole site rests on,
so the filter is to capture what the review praises and skip what it faults. Those four
also add the `fractal`, `hypnotic` and `volumetric` families to a gallery that is
currently `particles`, `geometric`, `geometric`, and Dragon Bloom is the only candidate
carrying an `inspired_by` block — publishing it would be the first real exercise of the
gallery's Milkdrop-attribution path.

Only the recording step needs a human at a Mac; everything after it is scripted. The
prompt's second decision asks whether to capture one preset against a *second*
rights-clear track, which is the only route anyone has found to demonstrating sync in a
still image — the thing reduced-motion visitors, phone visitors and OG cards all currently
lack.

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

**Found, then solved by the W.2 pass: a centred hero cannot show the footage.**
Murmuration's flock drifts between 0.38 and 0.70 of the frame's height over the
30 s loop (measured frame by frame), and a full-width copy block — tagline,
lede, note, notify form, CTA, requirements — needs the bottom half of the
section, which put the flock under the copy's scrim and hid the one thing it is
there to show. W.4 shipped a cropped top band as the workaround. The W.2 hero
pass below removed the cause: a copy *column* on one side leaves the other side
clear, so the loop now runs the full height of the section at its own scale.

**Found: the scrim can be sized from the footage rather than by eye.** Alpha
compositing is linear in relative luminance, so a scrim of `--color-canvas` at
alpha *a* over footage of luminance *L* lands the background at
`a·0.0037 + (1−a)·L`. The loop's brightest local patch reaches 0.4476. That
turns "is this legible?" into arithmetic against a measured map of the footage
rather than a judgement call, and it is how both the W.4 scrim and the W.2
pass's veil below were sized. It is worth reusing on any future hero.

**Found: none of the three published presets has an `inspired_by`.** Murmuration,
Cymatic Resonance and Ferrofluid Ocean are all Matt's originals. The generator
and the gallery both handle the field, and it will render on the first ported
preset that gets footage. `docs/CREDITS.md` in the app repo was not cited: it
covers bundled ML weights and reference code and says nothing about presets, so
the roadmap's earlier line naming it as an attribution source was wrong.

**Found and then fixed: W.2's header handoff had never run, and the CSS
minifier was why.**
`Nav.astro` sets `animation: header-settle linear both` followed by
`animation-timeline: --uz-hero-lockup`. The build's minifier folds the longhand
back into the shorthand as `animation: linear both header-settle --uz-hero-lockup`
— and `animation-timeline` is not a component of the `animation` shorthand, so
the whole declaration is invalid and dropped. `animation-name` computes to `none`
and `animation-timeline` to `auto` in the built site. The result is the fallback
the component's own comment describes as safe: an opaque header with a visible
wordmark, from the first pixel. It was pre-existing — the same source is on
`main` — and W.4 left it alone. **The W.2 hero pass below rebuilt it and it now
runs.** The fix is to write longhands only and never the `animation` shorthand;
the check is to grep `dist` for `animation-timeline`, `view-timeline` and
`timeline-scope` after any build that touches these rules, because the failure
is completely silent in the source and completely invisible until you look at
the built CSS.

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

### W.2 hero pass *(done 2026-09-18, on top of W.4)*

Matt: "hand it to W.4. w.4 should complete and then update hero with the desired
changes." The unmerged branch `claude/w2-hero-impeccable` (`5562117`, `9b6ec38`)
was never merged — it forks 54 commits back and carries copy that `main` has
since corrected. Its hero ideas were applied to the finished W.4 hero instead.

**Applied.**

- **The wordmark is live text**, in the header and in the hero. BRAND.md's
  "never set the wordmark in live type" was written before the site served
  Alumni Sans; the wordmark file is itself outlined Alumni Sans SemiBold, so the
  real face at 600 is the same drawing — selectable, scaled by the reader's text
  settings, one asset lighter. It is also what lets the hero's h1 and the
  header's wordmark be the same word in the same face, which is what makes the
  handoff read as one lockup moving rather than two swapping.
- **A spec list inside the first viewport**, and the GitHub CTA demoted to the
  sentence after the form. The notify path is the primary action now.
- **The Coleridge tagline moved to the footer**, as the atmospheric close
  BRAND.md describes rather than the second thing a visitor reads.
- **`NotifyForm` leaves alignment to its container.**
- **No `vw` in the page frame.** `50vw` counts the scrollbar and `50%` does not,
  so W.4's `margin-inline: calc(50% - 50vw)` bleed produced real horizontal
  scroll on classic-scrollbar machines. `main` runs full width and each section
  centres its own column in percentages, which also makes the hero full-bleed by
  default rather than by escaping a constraint. Verified after: `scrollWidth`
  1425 against `innerWidth` 1440, no overflow.
- **The authored opening moved to the field.** A full-bleed field paints over
  the violet glow W.2 spent it on, so the reveal is the footage arriving.
  Opacity only — a scale at the width of the window is a zoom.

**Decision: the footage keeps the field; `FirstOpening.astro` is not merged**
(Matt, 2026-09-18). The branch's hero art and W.4's footage are the same slot.
BRAND.md makes engine output the principal image language and W.3 existed to
produce it, so the SVG stays on the branch.

**Decision: "Uzume" is the hero headline and the page h1, and it animates into
the header** (Matt, 2026-09-18), with the header fixed to the top, transparent
on load so the footage's clouds run behind it, and filled with a brand colour
once the name has gone. An intermediate draft made the *claim* the h1 and put
the copy in a column beside the footage; Matt: "two column layout should be dead
too". The hero is centred again — footage as the upper band, the name over it,
the copy on its own field below.

**The handoff runs this time**, and the reason it never did is worth keeping:
the minifier finding above. `Nav.astro` now writes six `animation-*` longhands
and no shorthand, `Base.astro` carries `timeline-scope`, and the hero's h1
carries `view-timeline`. All three survive minification — verified in `dist`,
which is the only place the failure was ever visible. The whole handoff sits
inside `prefers-reduced-motion: no-preference`, so the reduced-motion state is
simply the base rule: an opaque header with a visible wordmark from the first
pixel. On the homepage the header's links take `--color-text-primary`, because
secondary ink reads at 2.5:1 against the brightest the sky gets under a
transparent header and primary reads at 5.1:1.

**The band's veil is flat at 0.46 rather than lighter at the top.** The crop
that puts the flock under the name also puts the sky's brighter middle under the
header — 0.256 at most over the loop, against the 0.090 the frame's own top
would have given — so the header's strip cannot be lighter than the rest without
failing. 54% of the cloud's light still reaches the reader through it.

**Found: a percentage inside a padded box cannot escape that box.** The copy
field's veil was meant to bleed to the window's edges via a negative margin, but
`50%` in a child of `main > section`'s inline padding resolves against the padded
box, not the window, so the veil rendered as a rectangle with visible sides. The
hero is excluded from the frame's padding and centres its own parts instead.

**Every veil on this page was solved numerically**, against a per-cell map of
the loop's maximum luminance — every frame, every part of the frame — rather
than chosen by eye. Worst case over the whole 30 s loop: header links 5.08:1,
the name 4.17:1 (large text, 3:1 is the bar), claim 16.12:1, spec list 11.65:1,
notify label 17.96:1, notify terms 8.10:1, alt 8.10:1, alt link 11.65:1.

One technique worth keeping from the discarded two-column draft: where a veil
has to fall away across footage, sample a smoothstep into stops rather than
using a two-stop linear ramp. The linear ramp kinks at both ends and the kink
reads as the edge of a panel rather than as haze.

**Not carried, all four older than `main`:** the deletion of
`public/uzume-icon.png` (`404.astro` and `confirmed.astro` still reference it),
`oo-ZOO-may` for the pronunciation, the present-tense contributor line, and the
retired Kit form id `9918547`. A branch that far behind `main` is a source of
ideas, not a merge.

**Left on the branch, not applied:** its closing `Uzume will be free when it
lands.` section, which repeats the notify form at the foot of the page. That is
a page addition rather than a hero change; it is a small, easy win whenever
someone wants it.

### W.4b — The impeccable critique, and what it changed *(2026-09-18)*

A `/impeccable critique` run over the finished landing page and `/gallery`, two
isolated assessments — a design review and a deterministic scan plus browser
evidence. **24/40.** Snapshot at
`.impeccable/critique/2026-09-18T17-54-11Z__src-pages-index-astro.md`.

**What the scan could not fault.** Detector clean across 16 files (and verified
genuine — a synthetic control fired correctly). Zero CSP violations. Zero
horizontal overflow at 1440, 768 and 375. The header handoff live on a real
`ViewTimeline`. Mobile fetching no video at all; desktop selecting the AV1 WebM.
Every control named, tab order clean, reduced motion correct.

**What it caught that no scan could.** The page never said what it was anywhere
a machine or a screen reader could find it: the heading outline held the word
"Uzume" twice and the words macOS, music and visualizer zero times, and `<title>`
was "Uzume — a light in sound". Fixed in both places.

**Fixed in this pass.**

- **`/gallery` had no headings and no exit.** Its three performances were
  `<strong>` inside a figcaption — the page whose entire content is those three
  had two headings. `VideoTile` now takes `titleAs`; the catalogue gets
  `.uz-media-frame__title` so `strong` and `h2` render identically. And its last
  focusable element was the footer's GitHub link, so both audiences now get a
  door: "Write a preset" and the notify form.
- **A publishable sentence per preset.** `Scripts/preset_captions.json`, merged
  by the generator. The sidecars already name the drivers; they just carry
  "CR.2" and "FA #73" and cannot ship. `roster_quote` retired — required,
  generated, rendered nowhere since the pull quote was cut.
- **The signup's outcome.** One 16px line in the hole the fields vacated became
  a panel at display scale with a way back, because Kit's double opt-in made a
  typo unrecoverable. The error is finally wired to the field with
  `aria-invalid`/`aria-describedby`; it had lived in a sibling `<p>` nothing
  pointed at.
- **The invitation card was padded twice** — 248.5px each side of a 928px card,
  its body at 33 characters. **A percentage padding resolves against the
  parent's width, not the element's own**, so the frame rule's centring padding
  was computed as if the card were still full-bleed. This is the second time
  that trap has bitten this file; the first was `.hero__copy`.
- **Two hit targets under the 44x44 floor**: the header brand at 53x28 (it lost
  the catalogue's `min-height` when it became live text) and the skip link at 43.

**Found, not fixed — open.**

- **The hero image reads as a nature photograph, not software.** Murmuration
  cropped to a letterbox of dusk sky says nothing about rendered, Metal, Mac or
  music; swap the h1 and it sells a birdwatching app. The two presets that would
  read unmistakably as engine output are 2,300px down as inert posters. Options
  on the table: let the band grow with the viewport, or open on Cymatic
  Resonance's cyan rings and cut to Murmuration.
- **The name is the h1 for a product with no recognition.** Matt's explicit
  decision, and the title and heading fixes close most of the cost. The
  structural alternative — claim as `h1`, "Uzume" as a `<span>` lockup keeping
  its 112px and its timeline — remains available and costs the handoff nothing.
- **The two teaser posters look clickable and are not.** Inert `<figure>`s with
  `cursor: auto`.
- **The trust band uses status colour for non-status content** — a warning
  callout for a permission explanation, a success callout for a luminance
  policy. Nothing failed and nothing succeeded.
- **Reduced-motion and phone visitors see no evidence of what Uzume does.** The
  guards are right; the consequence is that a large share of visitors are asked
  for an email having seen a static frame. There is no still-image answer to
  "performs light to music" yet, and OG cards will have the same problem at W.6.

### W.4c — Second critique: the two P0s and the media spend *(2026-09-22)*

A second `/impeccable critique` over the live `uzume.io` and `/gallery`, same
dual-assessment shape. **23/40**, down from W.4b's 24 — not a regression in the
pages, but a harder look at three things the first pass did not reach.

**Decision — engine footage is exempt from the looping-chrome ban.** Matt's
call, recorded in `BRAND.md` and `DESIGN.md`. The ban exists so that chrome does
not compete with the output it frames; a loop of real engine output *is* the
output, and stays exempt even though the page crops, positions and veils it to
seat type. Two conditions hold the exemption: the footage is real capture,
published unedited and labelled; and any self-starting loop carries a visible,
labelled stop control. Fail either and it is chrome again.

**Fixed in this pass.**

- **The hero loop could not be stopped.** WCAG 2.2.2 wants a mechanism for
  self-starting motion past five seconds and is *not* conditioned on
  `prefers-reduced-motion` — the reduced-motion work, which is good, never
  covered it. `VideoTile`'s bare mode now carries a labelled toggle in the
  band's corner, revealed only when there is motion to stop, with the choice
  kept in `sessionStorage` so it survives a trip to `/gallery` and back.
- **The steady-luminance commitment was on the wrong page.** `/gallery` plays
  eight bright loops and never said the word; "certified" appeared on every tile
  there and was defined only on the landing page, which a visitor arriving on a
  shared gallery link has never seen. Now stated in the intro, worded as the app
  gates it (D-157), never as a flashes-per-second figure.
- **Scrolling `/gallery` spent every byte it had.** Every tile carried
  `data-uz-loop`, so the observer played each one it touched; `preload="none"`
  means `play()` is also the download. Measured on the live site: passing two
  tiles fetched 15.8 MB, and a full scroll was ~40 MB with two or three 1080p
  streams decoding at once. The bug in both was the same — intersection is not
  attention. A tile must now hold 60% of the frame and still be there 400 ms
  later, and only one plays at a time. Verified: a fast scroll to the bottom
  fetches nothing; a dwell fetches exactly one clip. Tiles the visitor starts
  through the native controls are left alone.

**Left for later, deliberately.**

- **AVIF posters are encoded, published and unreferenced.** `media.json` carries
  an AVIF for all eight (979 kB against 1,554 kB of JPEG); both templates
  hardcode `posters.jpeg.url`. It is a landing-page saving, not a gallery one —
  `<video poster>` takes a single URL and cannot fall back — and wiring
  `<picture>` means changing `.uz-preset-card__media > img` to a descendant
  selector in the catalogue. Its own increment, and the landing page is about to
  be rethought anyway.
- **`murmuration` is 14.55 MB**, over this repo's own ≈8–12 MB per-loop budget.
  Needs the encoder and an R2 upload, not a template change.
- **`skein.jpg` (585 kB) and `ferrofluid-ocean.jpg` (551 kB)** are 12× their
  siblings. Same re-encode job.
- **The homepage copy, and the homepage itself.** Matt's direction: the hero
  credit line goes, the copy is revisited completely, and the landing page is
  rethought rather than replaced by `/gallery`. Its own session.

**Still open from the report** (unchanged here): `/docs` is a nav promise
resolving to "it arrives in a later increment"; the eight preset `h2`s render at
16px, smaller than the lede above them, which is what the detector's eight
`heading-rhythm` hits are measuring; the seven teaser figures are still inert;
`--text-3xl` is still unclamped; `"The Goddamn Shame,"` and `<em>` render with no
space between them on the live gallery.

**Tooling finding.** `impeccable detect` silently skips `.astro` — a byte-
identical broken control file returns exit 2 as `.html` and exit 0 as `.astro`.
Every prior detector run over this repo's source was a false all-clear. The
live-URL target works and is what W.4c used.

### W.5a — The homepage rewritten *(2026-09-22)*

Built as `/mock` so it could be judged rendered rather than in diff form, then
promoted over `index.astro`. `/mock` is gone; there is one landing page.

**Decisions, all Matt's.**

- **The claim is musicality, not the mechanism.** "A music visualizer for macOS
  that listens, analyzes, and accompanies." The draft before it led on
  stem-separated reactivity, which is expensive and largely unavailable on the
  streaming path — where most visitors will be — so it was false for the
  majority case. *Still to verify against the app repo: whether stem-separated
  features reach scene parameters at render time at all. The old beat copy
  asserted it flatly.*
- **Presets are scenes, for everyone.** No split vocabulary between listeners
  and contributors. "Visual" was tested first and failed: it is a mass noun, so
  it dies in the singular, and "write a visual" — the contributor's whole
  invitation — is unusable. **The app repo still says "preset"**, so the CTA and
  its destination disagree until that follows.
- **No certification language, no jargon, no counts.** "Certified", "Metal
  shader and a JSON file", "the gates", "the engine", "repertoire" all out. No
  preset count anywhere: eight was the number of recorded clips, not of scenes
  that exist, and any real figure is wrong within the month.
- **Architecture:** the hero is the name and its sentence over the footage; the
  ask is its own section beneath it, carrying the specs a visitor needs to
  self-qualify before handing over an address. Then what it does, featured
  scenes, the name.
- **The name carries narrative.** It opens the section explaining the app —
  "what the app does is less mythic" — and the Kojiki telling closes the page.
- **GitHub is not for everyone.** Out of the nav, kept where scene-writers are.
- **American spelling throughout.** The site was writing in two dialects, and
  the British half was live in six gallery captions.

**Cut, with reasons.** The three trust callouts — only the Screen Recording one
is a real objection-handler and it belongs at install, which is W.7; local
processing is table stakes for a native Mac app; steady luminance belongs on
/gallery, where the loops play, and is already there. The requirements band,
folded into the signup specs. The hero credit line.

**Still open.** Two application captures render as labelled gaps — real captures
of the Preflight and the Preparation Stage, which PRODUCT.md forbids inventing.
The claim sits at 18px over live footage on phones; the glyph halo carries it on
Murmuration's poster but contrast over moving video cannot be measured, and
unlike the wordmark the claim has no WCAG exemption. W.3c's skyless scenes are
the real fix.

### W.5l — The hero's encode weight *(2026-09-23)*

Murmuration re-encoded at a lower rate cap: **15.26 → 11.45 MB** (AV1/WebM) and
**15.42 → 11.57 MB** (H.264/MP4), 4.07 → 3.05 Mbit/s, still 30 s at 1080p60.
Every other loop is byte-identical; only the hero moved.

**First, a correction.** The critique that raised this called the hero "over the
repo's 8–12 MB ceiling". It was not. That is the *gallery* budget;
`encode_captures.py` records `BUDGET_MB = {"hero": 24, "gallery": 12}` and
WEBSITE_PLAN §5 says "hero somewhat larger". At 15.26 MB the hero was inside its
budget, and the finding compared it against the wrong number.

**Why it moved anyway.** Not the budget — the fact that both codecs sat pinned
to their caps. AV1 landed within 1 % of x264 on a clip AV1 should win easily,
which only happens when the cap and not CRF is setting the size. So the bits
were bounded by a number we chose, the quality was bounded with them, and the
number was chosen once before for exactly this reason: W.3b already lowered the
hero from the gallery cap because 22.5 MB "stalls on a weak connection". This is
that decision continued, not reversed.

**What it cost.** SSIM Y 0.9892 → 0.9840, XPSNR 37.29 dB. For scale, the lowest
quality the site has ever published is Ferrofluid Ocean at 0.9337, accepted as
shippable; the hero after this change sits far above it. Both renditions pass
every bar — stream, frames, size, luminance seam, chroma seam — and the posters
reproduce byte-identically, so the loop's framing and its still are unchanged.

**Rejected: a shorter loop.** 30 → 20 s would have saved the same bytes at
identical per-frame quality, and was the first instinct. It loses to the rate
cut because W.3b chose 30 s on the reasoning that "visitors linger on the hero",
and trading a third of the footage before repetition is a visible change to the
page, where a 0.005 SSIM step is not.

**Two encoder fixes this surfaced.**

- `--only=<slug>` re-encodes one preset and keeps the rest. SVT-AV1 does not
  reproduce, so the existing `--reencode` rewrites all eight loops' bytes to
  change one — churning R2 objects and invalidating verdicts for nothing.
- **An `encode_verdict` is now carried forward only onto the bytes it was
  recorded against.** It was carried by slug, so any re-encode silently kept
  Matt's "quality appears strong" against footage he had never seen. Murmuration's
  verdict is now `null`, which is the honest state: **this encode is unjudged.**

**Needs Matt.** The new hero is on the preview URL. The quality call is his, and
until he makes it `encode_verdict` stays null.

### W.5m — The two heavy posters *(2026-09-23)*

Skein and Ferrofluid Ocean's stills roughly halved. AVIF **439 → 213 kB** and
**382 → 199 kB**; JPEG **585 → 240 kB** and **551 → 250 kB**. The other six
posters and all eight loops are byte-identical.

**The cause is the content, not the settings.** These two carry the densest
fields on the site — which is also why their video is the heaviest — so their
stills were 8-30x their siblings' 13-52 kB at the same CRF 20.

**Two cheaper explanations were measured and ruled out first.**

- *The frame.* The poster is whichever frame sits closest to the loop's median
  luma, so a dense frame could have been bad luck. It was not: the 24 frames
  nearest Skein's median — every one as representative as the one picked — span
  427-441 kB. Frame choice is worth 1-3 %, so selecting for compressibility
  would have bought nothing and cost the selection rule its meaning.
- *A blanket quality cut.* The curve is shallow. Even CRF 42, visibly degraded,
  leaves Skein at 171 kB — still 3x Murmuration at CRF 20. There is no setting
  that makes these frames cheap, only one that makes every other poster worse.

**So: a budget with a ladder.** 220 kB AVIF, 250 kB JPEG; the first rung is the
CRF 20 / q2 the light posters already use, so six of eight encode once and
reproduce byte for byte, and only a poster over budget walks further down.
Ferrofluid lands at CRF 34, Skein at CRF 38.

**Checked by eye, not by SSIM.** Both were compared against their CRF 20
originals at 1:1 on a 700x560 crop. Skein's flat poster-paint shapes and
Ferrofluid's violet gradients both hold; no banding in Ferrofluid's dark field,
which was the risk worth looking for.

**Not addressed: the same posters are the homepage's card images.** Six
`PresetCard` stills render a few hundred pixels wide and load the full 1920x1080
poster, because `<video poster>` takes one URL and the cards reuse it. A second
narrow rendition would help every card, not just these two, and would also serve
phones — where reduced motion, a metered connection or a narrow screen means the
poster is the only image a visitor ever sees. That is a manifest-shape change
and its own increment.

### W.5n — The landing page's cards stop borrowing the gallery's stills *(2026-09-23)*

Six `PresetCard` images were loading full 1920x1080 posters to draw a few
hundred pixels wide, because `<video poster>` takes one URL and the cards reused
the manifest key that served it. They now load a 960-wide rendition: the six
featured cards go **306 → 123 kB** of AVIF.

**Why 960, and why only one size.** Measured rather than assumed: the widest a
card ever draws is **438 CSS px**, at a 1100 px viewport — where the column is
already capped at `--content-reading` but the gutter has not yet grown to its
`clamp` ceiling, so it is wider there than at 1920. The one-column layout at
375 px draws 303 CSS px, which a DPR 3 phone turns into 909 device px. 960
clears both with headroom, so one rendition covers every case and the cards need
no `srcset` or `sizes` at all.

**Manifest shape.** A `thumbs` key beside `posters`, same shape, plus a `width`
on both. Additive on purpose: `posters` is now read by the W.6 JSON-LD as well
as by the tiles, and changing its shape would have changed what search engines
are told as a side effect of a layout fix.

**The thumb budget is not the poster's divided by four.** That is what it was at
first, and it put Skein — the densest frame on the site — off the bottom of the
ladder at CRF 42, which is not an alarm worth hearing but a budget no encode of
that frame can meet. At 80 kB AVIF / 100 kB JPEG the two heavy frames land
mid-ladder (Ferrofluid CRF 26, Skein CRF 38) and still more than halve.

**Still full-size: the `<video poster>` on phones.** Where reduced motion, a
metered connection or a narrow screen stops the loop from ever playing, the
poster is the only image a visitor sees — and it is still the 1920 one, because
`VideoTile` assigns it in JS and would have to choose by width as well as by
format. The rendition it would need now exists; wiring it is a separate change.

### W.5o — The poster a phone actually gets *(2026-09-23)*

`VideoTile` now chooses between the full still and W.5n's 960-wide one by the
width the element is actually drawn at. A phone loading `/gallery` fetches
**571 → 213 kB** of AVIF, 63 % less, and the hero's still goes 52 → 15 kB.

**This is the half of W.5n that mattered more.** The cards were a waste; this is
not. A narrow screen never plays a loop — `VideoTile` gates playback on reduced
motion, `saveData` and a 48rem breakpoint — so on a phone the poster is not a
placeholder waiting for video, it is the entire image. It was being served at
1920 to a screen that cannot resolve it, over the connection most likely to be
metered.

**Chosen at assignment time, not by a media query.** `<video poster>` cannot
negotiate, which is why the format is already picked in script; the size joins
it there, from `clientWidth × devicePixelRatio` once the element is laid out.
Both cases verified rendered: at 375 px / DPR 2 the need is 686 and the thumbs
are assigned, at 1440 px / DPR 2 it is 2112 and the full posters are.

**The 1.25 factor is a judgement with a stated cost.** The narrow rendition is
taken when the need is within 1.25 × 960. A DPR 3 phone at 393 CSS px needs
about 1180 and gets 960 — roughly 82 % — so the densest frames soften slightly
on exactly the screens where the poster is final. That is the trade: those
screens are also the metered ones, and the alternative is 199 kB rather than 78
for Ferrofluid Ocean. A 1280-wide rendition would remove the compromise, and the
comment in `VideoTile` says to add one if it ever reads as soft on a real phone.

**Testing note.** The Browser pane reports `visibilityState: "hidden"` when it
is not fronted, and `IntersectionObserver` does not fire in a hidden document —
so posters stay unassigned and the lazy path looks broken when it is not. This
cost a wrong conclusion once already (W.5i). Front the tab before believing a
poster measurement.

### W.5 — Docs *(about two sessions)*

Starlight curation, outsider-first, per plan §3: Getting Started (requirements, build-from-source today, the Screen Recording permission explainer, local files vs. streaming), Using Uzume, Contributing Presets (two-file drop-in, hot reload, gates and certification lifecycle). Each page's frontmatter names its upstream app-repo doc; `lychee` checks those references in CI.

**Getting Started is also the site's FAQ — write it question-shaped.** Nothing
on the site is currently phrased as a question, which is the form answer engines
extract; the answers all exist, as prose, spread across the landing page. Rather
than a second copy of them on a `/faq` page — which would duplicate this page's
content within weeks and split the source of truth on exactly the facts the
`README.md` boundary protects — the headings here carry the questions and this
page carries the markup. The seven worth answering, from what the landing page
already argues: does it work with Apple Music and Spotify; does it need the
Screen Recording permission; is it free; does it run on Intel Macs; which macOS
version; is it safe to watch if light-sensitive (steady luminance, per the
D-157 wording on /gallery — never a flashes-per-second figure); how do I write
a scene.

`FAQPage` JSON-LD on the same page, one `mainEntity` per heading. **Not** via
`Base.astro`'s `schema` prop — /docs renders through Starlight's own layout,
which that prop never reaches. Starlight's frontmatter `head` is the route:

```yaml
head:
  - tag: script
    attrs: { type: application/ld+json }
    content: '{"@context":"https://schema.org","@type":"FAQPage",...}'
```

`content` is emitted raw, so escape `<` as `\u003c` in it by hand — the same
hazard `Base.astro` handles for the pages it does own.

### W.5 — Docs, first session *(2026-09-23)*

`/docs` is a section rather than a placeholder: **Getting started** and **Using
Uzume**, plus an overview that routes between them. Contributing is the second
session's (decision 3). The commit prefix is `[W.5]`, which the homepage rewrite
also holds — `git log --grep '\[W\.5'` now returns two unrelated bodies of work
(decision 1, and this is the flag it asked for).

**The four decisions, all Matt's, all on their defaults (2026-09-23).**

- **1 → A.** Keep **W.5** for docs, as the roadmap has it; the homepage keeps
  `W.5a`–`W.5m`. Collision noted above rather than relabelled.
- **2 → A.** **"Scene" throughout**, naming the repo's term once, early. It is
  said twice, deliberately: on the overview, and inside the answer to "how do I
  write a scene?" — the two places a reader is one click from app-repo filenames.
- **3 → A.** **Getting Started + Using Uzume now, Contributing next.** The
  listener path ships whole.
- **4 → A.** **Upstream references render visibly**, as a "Drawn from" line of
  links to the files on GitHub. `lychee` checks them with no CI change. Proven:
  renaming one reference to `docs/RUNBOOK_RENAMED.md` turned the link check red
  with a 404 on `dist/docs/using-uzume/index.html`; reverted. The frontmatter
  field the plan describes is deliberately **not** also carried — it would be a
  second copy of the same fact, checked by nothing, free to drift.

**Getting Started is the site's FAQ.** Seven question-shaped headings, one
`FAQPage` `mainEntity` each, emitted through Starlight's frontmatter `head`
because `Base.astro`'s `schema` prop never reaches a Starlight layout. All seven
`acceptedAnswer` texts were checked to appear verbatim in the rendered prose.
Answer six is `/gallery`'s steady-luminance sentence with exactly one word
changed — "here" → "in the gallery" — because the sentence moved off the page
its deixis pointed at; the D-157 clause is untouched, and no flashes-per-second
figure appears anywhere.

**The claims table.** Every product fact these pages assert, and where it comes
from in `hoaxpoet/uzume`:

| Claim | Source |
|---|---|
| Apple silicon only, M1 or newer; a few features reserved for M3+ | `README.md` §Requirements; `docs/PRODUCT_SPEC.md` §Target Platform (Tier 1 / Tier 2) |
| macOS 14 Sonoma or later | `README.md` §Requirements; `docs/RUNBOOK.md` §Preconditions |
| Xcode 26.5, pinned | `README.md` §Requirements; `.xcode-version` |
| Clone, `Scripts/fetch_weights.sh` (~167 MB, a release asset), `xcodebuild -scheme UzumeApp` | `README.md` §Getting started |
| Source public, MIT-licensed | `README.md` §License; `LICENSE` |
| Uzume does not control your player; it listens to system audio | `README.md` §Running it; `docs/PRODUCT_SPEC.md` §What Uzume Is |
| System-audio capture needs Screen Recording; audio only is captured | `README.md` §Running it; `docs/GLOSSARY.md` "Tap"; `docs/UX_SPEC.md` §3.2 |
| macOS bundles system-audio capture with screen recording | `docs/UX_SPEC.md` §3.2 (the app's own explainer) |
| Nothing leaves the Mac | `docs/PRODUCT_SPEC.md` §Non-Goals (no cloud processing, no telemetry) |
| Local files need no permission and no account | `README.md` §Running it; `CONTRIBUTING.md` §The development loop |
| File → Open Local File (⌘O) | `README.md` §Running it; `UzumeApp/UzumeApp.swift:184` |
| `.m4a` / `.mp3` / `.flac`, folders, M3U | `docs/UX_SPEC.md` §2 (file association, unsupported-format alerts) |
| Apple Music playlists read from the running app, with a permission prompt | `docs/UX_SPEC.md` §4.3 (`.permissionDenied` → Automation) |
| A Spotify session needs your own client ID against the copy you built | `docs/RUNBOOK.md` §Spotify connector setup (`Uzume.local.xcconfig`) |
| Preparation shows either the widening opening or the track list; "Show track info" toggles | `docs/UX_SPEC.md` §5.2 |
| Start before preparation finishes; it continues behind the session | `docs/UX_SPEC.md` §5.4 |
| Nothing upcoming is ever shown | `docs/UX_SPEC.md` §5.2, §7.3 (D-238) |
| Local files: a 3–2–1 count, then it begins | `docs/UX_SPEC.md` §6.2 |
| Streaming: ready screen, "Begin now", auto-start on first audio, 90 s prompt | `docs/UX_SPEC.md` §6.1, §6.3, §6.4 |
| Chrome shows ~3 s then hides; returns on mouse, click, any key | `docs/UX_SPEC.md` §7.2 (D-241) |
| Top-left track card with the current scene's name; top-right dots, toggle, settings, end | `docs/UX_SPEC.md` §7.3 |
| Transport bar for local files only | `docs/UX_SPEC.md` §7.3 (LF.5.fix carve-out) |
| The keystroke table as published | `UzumeApp/Services/PlaybackShortcutRegistry.swift` (verified against source, not only the spec) |
| Reduced motion: feedback blur off, slower palette shifts, beat pulse at half | `docs/UX_SPEC.md` §7.10 |
| Scenes stay alive at silence; "Listening…" badge after ~3 s | `docs/UX_SPEC.md` §7.5 |
| A card after ~10 s of no audio, with fixes | `docs/UX_SPEC.md` §7.5 (D-165) |
| Output-device change or rebuild silently invalidates the grant | `docs/RUNBOOK.md` §Audio levels too low; §Signal health monitor (`deadTap`); `README.md` §Running it |
| Scrubbing kills the tap; it reinstalls automatically | `docs/RUNBOOK.md` §App captures silence |
| Protected tracks deliver silence; expected, degrades and recovers | `docs/RUNBOOK.md` §App captures silence |
| Normalize volume / Sound Check off; 48 kHz output | `docs/RUNBOOK.md` §Audio levels too low |
| A scene is a Metal shader plus a JSON file beside it, picked up automatically | `CONTRIBUTING.md` §What a preset is |
| Photosensitivity: steady luminance; the app's first-run notice and Reduce motion | `CONTRIBUTING.md` §Gates; `docs/UX_SPEC.md` §3.3; D-157 wording already live on `/gallery` |

**Gaps — what a page wanted to say and the app repo could not support.**

1. **What a shipped build does about Spotify.** The only documented setup is a
   developer one (bring your own client ID in a gitignored xcconfig). No upstream
   doc says what a released build will do, so the page states the requirement as
   it stands today and promises nothing.
2. **The two Spotify accounts of the truth disagree.** `docs/UX_SPEC.md` §4.4
   says v1 is URL-paste only, public playlists, "No OAuth"; `docs/RUNBOOK.md`
   §U.11 documents a full OAuth PKCE login with Keychain storage. The docs
   therefore describe *that* you hand Uzume a playlist, never *how* the connect
   flow looks. Worth resolving upstream before the Contributing session.
3. **How long preparation takes.** No upstream figure exists — only the 90 s and
   2 min fallback thresholds. These pages state no timing. (The landing page's
   "ten or fifteen seconds" for the streaming path predates this session and is
   still unsourced.)
4. **Which features are the M3 tier.** `PRODUCT_SPEC.md` names an enhanced tier
   and never enumerates it, so the page can only say "a few features".
5. **The stall card's words.** `UX_SPEC.md` §7.5 says its copy is
   developer-facing and must be softened before a public build, so the page
   describes that a card appears, not what it says.
6. **Certification without the word.** The Contributing session inherits a real
   problem: the lifecycle a submitted scene goes through is called certification
   upstream, and W.5a removed that word from the site. The mechanism is sourced
   (`CONTRIBUTING.md` §Gates, §Certification lifecycle); the vocabulary is not.
7. **Install.** Unchanged and app-side: no signed, notarized artifact exists, so
   every page stays in the future tense about the beta (W.7).

**A gate that is red for an unrelated reason.** `Scripts/generate_presets.py
--check` reports four sidecars as drifted. The drift is W.5a's American-spelling
pass: regenerating would re-import "colour" from the app repo's sidecars. The
script runs nowhere in CI (it reads a local app checkout), so nothing is failing
on the PR, but it is red on a clean tree and will stay red until either the app
repo follows the spelling decision or the generator Americanizes on import.

**Indexing.** `/docs` should **stay indexed**, and now earns it: W.6 left the tag
off on the assumption this session would land, and it has. All three docs pages
join the sitemap automatically; none needs `noindex`.

**Handed to the second docs session.** Contributing: what a scene is as two
files, the hot-reload loop (`~/Library/Application Support/Uzume/Presets/`,
documented upstream and unverified here), a first walkthrough, what the gates
check, and what happens after a merge — with the gallery as the payoff, and with
gap 6 above to decide first. GitHub belongs in that page's body, not the nav.

### W.6 — Launch polish *(one session)*

OG/social images from hero frames, favicons from `brand/favicon/`, 404 page, sitemap and basic SEO, `prefers-reduced-motion` audit across all pages, Lighthouse pass on throttled mobile.

**Discovery and structured data, done.** `@astrojs/sitemap` emits the three
indexable pages; the three `noindex` ones are filtered out, because a sitemap
entry asks for indexing and contradicts the tag on the page. `robots.txt` exists
for its `Sitemap:` line only — it keeps the allow-all that having no file already
meant, and names no AI crawler in either direction, since blocking them is Matt's
call and would forfeit being cited when someone asks an assistant for a Mac music
visualizer. JSON-LD renders through one optional `schema` prop on `Base.astro`:
`SoftwareApplication` on the landing page, and a `VideoObject` per clip on
/gallery, built from the manifest fields the encoder already writes. The eight
clips were otherwise invisible — cross-origin `<video>` behind lazy posters
indexes as nothing.

**Phrasing, done.** "Spotify" and "Apple Music" existed on the site only inside
an image `alt`; they are in the landing page's prose now, and /gallery and /docs
say in their titles what they are about. "MilkDrop" is still absent, but
`inspired_by` is schema'd and renders the moment a preset carries one, so that
one costs nothing and waits on the roster rather than on this repo.

**Handed to W.5.** The question-shaped content and its `FAQPage` markup — see
W.5 above. /docs is indexed today saying only that the docs are not written; it
is deliberately not `noindex`-ed, because W.5 lands shortly and the tag would be
added and removed to accomplish nothing in between.

**Still open.** Per-preset pages (`/gallery/<slug>/`) are the largest available
increase in indexable surface — eight pages, each with a video, a description
and a named author — and the largest cost. They cut against the one-page
gallery, so they are a W.7 question, not a W.6 one. With them: per-page OG
images, `max-image-preview:large`, and Search Console verification.

### W.7 — Download flip *(blocked on app-side work; no site work wasted meanwhile)*

When a signed, notarized artifact is on GitHub Releases: `/download` gains the real CTA, the landing CTA flips, beta copy moves to present tense. The landing page's `SoftwareApplication` schema gains `offers`, `downloadUrl` and `softwareVersion` at the same moment — all three assert an installable artifact, so they are omitted until one exists. Prerequisite track (app repo, parallel, start whenever): ADP membership → Developer ID signing → `notarytool` in the release pipeline → tagged Release.

## 4. Order

W.0 → W.1 → W.2 is the critical path to a public site. W.3 → W.4 follows independently; W.5 can start any time after W.1; W.6 precedes whatever moment gets called "launch"; W.7 trails on its own dependency. The placeholder-footage decision in W.2 is what decouples shipping from capturing.

## 5. Costs

Domain ~$50/yr (spent). Hosting, R2 (≤10 GB, zero egress), analytics, CI: $0 at this site's volumes on current free tiers. ADP $99/yr when the W.7 track starts — app-side, already flagged there. Steady-state ceiling including a possible uzume.app backorder landing: ~$150/yr. No API or token costs; the site is static.

## 6. Risks

- **Footage is the argument, and W.3 is the schedule risk.** Mitigated by placeholder-first W.2 — the site ships without it.
- **Clip staleness.** The roster is mid-uplift (Phase PR observations); captured clips can lag improved presets. The manifest's capture-date + app-commit fields make staleness visible, and re-capture is cheap once `encode_captures.sh` exists.
- **Docs drift.** Manual curation + frontmatter upstream refs + CI link-checking, per plan; revisit scripted sync only if drift becomes a real cost.
- **Claim discipline.** Every product claim on the site traces to the app repo (`README.md` source-of-truth rule). The certified count above is a build fact for planning, not marketing copy — the site shows certified presets; it doesn't promise a number.
