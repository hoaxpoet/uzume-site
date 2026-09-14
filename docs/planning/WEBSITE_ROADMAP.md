# Website Execution Roadmap — uzume.io

*2026-09-14 · Supersedes §8 (Phases) and resolves §10 (Open questions) of `WEBSITE_PLAN.md`. Everything else in that plan — stack, hosting, IA, media pipeline, repo structure — stands as written.*

## 1. Decisions resolved 2026-09-14

- **Domain.** uzume.io is registered. DNS/custom-domain wiring is W.0 work, not a purchase decision.
- **Launch posture: ship early.** The site launches before a notarized build exists. `/download` (working label: "Get Uzume") states the honest current shape — open source, clone-and-build today, notarized beta coming — and offers a notify path (GitHub repo watch / release notifications). Beta copy stays in the future tense per `PRODUCT.md` until a Releases artifact exists. The download CTA flip is its own later session (W.7), not a launch gate.
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

### W.0 — Foundation *(one session; unblocked now)*

Scaffold Astro + Starlight at the repo root (`src/` layout per plan §6; `brand/`, `design/`, `DesignSystem/`, and the planning docs stay where they are). `.nvmrc` pinned. CI on PR: install, `astro check`, build, `lychee` link check. Cloudflare Worker with static assets, git-connected build, preview URL per PR. Custom domain uzume.io, `www` → apex, security headers in `public/_headers`. Web Analytics on. Wire the existing root `tokens.css` into the build as the single token source (move or import — don't fork it).

**Exit:** hello-world live at uzume.io; a test PR shows its own preview URL; CI green.

### W.1 — Tokens and components *(one session)*

Port the `DesignSystem/Web` catalogue into `.astro` components: `Nav`, `Footer`, `Button`, `VideoTile` (poster + lazy loop + reduced-motion fallback), `Callout`, `RequirementsList`, `PresetCard`. Zero client JS except where `VideoTile` needs it. Build `/design` from the live components.

**Exit:** `/design` renders every component; `Scripts/check_contrast.py` passes against the served tokens; reduced-motion verified by hand.

### W.2 — Landing *(one to two sessions → public launch)*

The landing page per plan §3, built with **placeholder footage** (a rough capture of any certified preset) so layout never waits on the capture pipeline. Copy constraints from `PRODUCT.md` are hard: beta in future tense, no AI claims, steady-luminance phrasing (never a flashes-per-second figure), primary CTA "On GitHub today — build from source" plus the notify path.

**Exit: the site is public.** A good landing page alone is a legitimate site; this is launch #1.

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
