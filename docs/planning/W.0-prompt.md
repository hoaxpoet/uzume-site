## Increment W.0 — Foundation: scaffold, CI, and uzume.io live

**Type:** infrastructure (site repo).

**Objective.** After this session, a hello-world Astro + Starlight site is live at
https://uzume.io, built by Cloudflare's git-connected pipeline with a preview URL per
PR, gated by CI, styled from `tokens.css`, and with security headers and cookieless
analytics in place. No real pages exist yet — the pipeline exists before any page
does. Governed by `docs/planning/WEBSITE_ROADMAP.md` §3 (W.0).

## Skill invocations

This repo carries none of the app repo's skills (`closeout`, `preset-session`,
`shader-authoring` do not apply here — do not invoke them). Closeout is inline, §9.

## Read first, in order

1. `docs/planning/WEBSITE_ROADMAP.md` — §1 (resolved decisions), §3 W.0
2. `docs/planning/WEBSITE_PLAN.md` — §6 (repo/pipeline), §7 (hosting checklist)
3. `CLAUDE.md` — non-negotiables and conventions
4. `README.md` — source-of-truth boundary
5. `.github/workflows/fast-gate.yml` — the CI that must keep passing
6. `tokens.css` — skim the token names; do not modify

## Pre-flight invariants — stop if any fails

1. On `main`, clean working tree, up to date with `origin/main`.
2. `CLAUDE.md`, `docs/planning/WEBSITE_ROADMAP.md`, and this prompt are **committed**
   (not untracked). If untracked → stop and ask Matt to commit them first.
3. `python3 Scripts/check_contrast.py tokens.css` passes.
4. No `package.json`, `src/`, or `astro.config.*` exists at the repo root (nothing
   half-scaffolded).
5. `node --version` is an active even-major LTS. Record the major — it becomes `.nvmrc`.
6. Ask Matt to confirm: the **uzume.io zone is active in his Cloudflare account**
   (domain registered, DNS on Cloudflare). If he can't confirm → stop; Task 5 is
   impossible without it.

## Tasks

**1. Branch.**
`git checkout -b claude/w0-foundation`.
**Done when:** on the branch with a clean tree.

**2. Scaffold Astro + Starlight into the repo root.**
Scaffold with `npm create astro@latest` in a temporary directory (minimal template,
TypeScript strict), then graft into the repo root file-by-file: `src/`, `public/`,
`astro.config.mjs`, `tsconfig.json`, `package.json`, `package-lock.json`. Never
overwrite an existing path; existing directories (`brand/`, `design/`,
`DesignSystem/`, `docs/`, `Scripts/`) are untouched. Extend `.gitignore`
(`node_modules/`, `dist/`, `.astro/`). Add Starlight (`npx astro add starlight`),
docs mounted at `/docs` with exactly one stub page. Pin **exact** versions in
`package.json` — no `^` or `~` ranges. Write `.nvmrc` with the pre-flight Node major.
Add a `prettier` config consistent with the scaffold defaults.
**Done when:** `npm run dev` serves locally; `npx astro check` passes; `npm run
build` emits `dist/`; `git status` shows no unintended changes to pre-existing paths.

**3. Wire tokens and the stub index.**
Import root `tokens.css` from a single base layout so every page inherits it — the
file stays at the root, unmodified (the fast-gate contrast check path must not
change). Build the index stub: midnight canvas, ivory text, the outlined wordmark
from `brand/wordmark/Uzume.svg`, favicon links using copies of `brand/favicon/`
files placed in `public/` (copying is permitted; editing is not). Stub copy per the
DECISION-NEEDED default in §10 unless Matt has answered. Honor
`prefers-reduced-motion` trivially (no motion exists yet — keep it that way).
**Done when:** the built index renders tokens correctly (midnight/ivory verified in
the browser); favicon appears; `grep -rn '#[0-9a-fA-F]\{3,8\}' src/` returns no
hardcoded colors outside token references.

**4. Site CI workflow.**
New `.github/workflows/site.yml` on `ubuntu-latest`, triggered on `pull_request` and
`workflow_dispatch`: `npm ci` (Node from `.nvmrc`), `npx astro check`, `npm run
build`, then a `lychee` link check over the built `dist/`. Do not modify
`fast-gate.yml`.
**Done when:** both workflows pass on the PR opened in Task 5.

**5. Open the PR, then STOP — Cloudflare is Matt's dashboard work.**
Get Matt's explicit "yes, push," push the branch, open the PR titled
`[W.0] Foundation: scaffold, CI, uzume.io`. Then **stop and report**, handing Matt
this checklist:
   - Cloudflare dashboard → Workers & Pages → Create → import `hoaxpoet/uzume-site`
     (Workers Builds; Worker with static assets). Build command `npm run build`,
     assets directory `dist/`.
   - Confirm the PR gets a preview URL; send it back into the session.
   - Attach custom domain `uzume.io`; add the `www` → apex redirect.
   - Enable Cloudflare Web Analytics for the site; send the beacon token back.
The session resumes only when Matt reports done and provides the preview URL and
beacon token.
**Done when:** Matt has confirmed; preview URL renders the stub.

**6. Headers, redirect, analytics.**
`public/_headers`: CSP (self, plus what the analytics beacon requires — verify the
current Cloudflare Web Analytics host from its own docs at run time, do not guess),
`X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`,
a minimal `Permissions-Policy`. Verify at run time whether the Workers static-assets
path honors `_headers`/`_redirects` files or needs the redirect at the Cloudflare
zone level — implement whichever the current docs prescribe. Add the analytics
beacon to the base layout with the token from Task 5.
**Done when:** `curl -sI https://<preview-url>` shows the headers;
`http://www.uzume.io` 301s to the apex (after merge, verified in Task 7); the beacon
appears once in built page source.

**7. Exit verification.**
After Matt merges: production serves the stub at https://uzume.io over HTTPS; a
trivial follow-up test PR receives its own preview URL; note the rollback path
(dashboard redeploy of a previous build). Then closeout (§9).
**Done when:** all three observed and recorded with URLs.

## Do NOT

- No landing-page design or copy — the index is deliberately a stub (W.2 owns the
  landing; W.1 owns components). Do not port anything from `DesignSystem/Web/`.
- Do not modify `tokens.css`, `fast-gate.yml`, or anything under `brand/`,
  `design/`, `DesignSystem/`, `docs/` (beyond this increment's closeout notes).
- No R2, no media files in git — ever (W.3 owns media).
- No dependencies beyond Astro, Starlight, and Prettier. No UI frameworks, no
  Tailwind, no client-side JS.
- No app-repo (`hoaxpoet/uzume`) changes.
- No product claims beyond the approved stub line — `PRODUCT.md` tense rules apply
  even to a stub. Never imply anything is downloadable.

## Verification commands — all must pass before closeout

```bash
npx astro check
npm run build
python3 Scripts/check_contrast.py tokens.css
node --check DesignSystem/Web/catalogue.js
node --check DesignSystem/Web/uzume-components.js
python3 Scripts/check_web_catalogue.py
```

## Commits

`[W.0] site: <description>` — separate commits for scaffold, tokens/stub, CI,
headers/analytics. First push requires Matt's explicit "yes, push"; after that,
pushes to `claude/w0-foundation` are pre-authorized for the rest of the increment.
Merging the PR is Matt's action.

## Closeout (inline — this repo has no closeout skill)

Report five parts: **(1)** what shipped — files, commits, PR link; **(2)**
verification evidence — the §7 command outputs verbatim, live production and preview
URLs, CI run links; **(3)** deviations from this prompt and why; **(4)** state handed
to W.1 — branch/PR status, anything W.1's pre-flight should check; **(5)** proposed
roadmap edit — the one-line "done <date>" mark for W.0 in `WEBSITE_ROADMAP.md` §3,
plus any learned fact that changes W.1+ (proposed, not applied — Matt approves).

## DECISION-NEEDED (answer before or during Task 3)

**What does the stub page at uzume.io say while the real landing page is being
built?**

- **(a) Wordmark only.** The Uzume wordmark centered on the midnight canvas. Nothing
  else — quiet, zero claims.
- **(b) Wordmark + one plain line + the repo.** The wordmark, one sentence — "A
  macOS music visualizer that performs light to the music you're already playing.
  Public beta coming." — and a single link to the GitHub repository.

**Recommendation: (b).** The site will be indexed and shared from day one; one
verified present-tense sentence and the repo link make every early visit worth
something, and the copy is already within PRODUCT.md's rules ("performs" is true of
the buildable app today; the beta stays future-tense).

**Default if no reply: (b).**
