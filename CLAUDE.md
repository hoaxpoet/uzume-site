# CLAUDE.md — uzume-site

Public website and brand workspace for **Uzume** (oo-ZOO-meh), a native macOS music
visualizer. The application lives in `hoaxpoet/uzume`; this repo builds uzume.io.
Governing docs: `docs/planning/WEBSITE_ROADMAP.md` (sessions W.0–W.7) and
`docs/planning/WEBSITE_PLAN.md` (durable decisions: stack, hosting, IA, media pipeline).

## Non-negotiables

- **Source-of-truth boundary** (`README.md` table): this repo never asserts product
  facts on its own. Any claim about what the app does, requires, or ships is verified
  against the app repo before it appears in copy.
- **Copy law** (`PRODUCT.md`): the beta is written in the **future tense** until a
  signed, notarized artifact exists on GitHub Releases. No AI or AI-orchestration
  claims. Flash safety is stated as **"steady luminance"** (the D-157 gate), never as
  a flashes-per-second figure. "Open source and buildable" and "available to install"
  are different claims — only the first is true today.
- **Tokens first**: all styling flows from the custom properties in `tokens.css`
  (repo root — the single source; import it, never fork it). No hardcoded colors or
  type in pages or components. Gate: `python3 Scripts/check_contrast.py tokens.css`.
- **Media lives in R2, never in git.** Video and large assets are served from
  `media.uzume.io`; the repo carries only an asset manifest. Encode budget ≈8–12 MB
  per gallery loop.
- **`prefers-reduced-motion` is honored absolutely** on every page. Motion is an
  enhancement, never a requirement.
- **`brand/` contains production identity artifacts.** Reference or copy them into
  `public/`; never regenerate, recolor, or edit them (usage rules in `BRAND.md`).

## Stack

Astro + Starlight (exact versions pinned in `package.json`, no ranges), static
output, deployed as a Cloudflare Worker with static assets via git-connected builds —
`main` → production at uzume.io, every PR → its own preview URL. Node pinned in
`.nvmrc`. Zero client-side JS by default; components earn their JavaScript.

## Working conventions

- One session = one PR, judged rendered on its Cloudflare preview URL — not in diff
  form. Lighter ceremony than the app repo: no DECISIONS.md; decisions land in
  `WEBSITE_ROADMAP.md`.
- Session prompts live at `docs/planning/<ID>-prompt.md` (precedent: `BRAND.1-prompt.md`).
- Commits: `[W.x] site: <description>`, small and per logical step. **Push only on
  Matt's explicit "yes, push."**
- CI must stay green: `.github/workflows/fast-gate.yml` (brand/design-system gates)
  plus the site workflow once W.0 lands.

## Checks

```bash
node --check DesignSystem/Web/catalogue.js
node --check DesignSystem/Web/uzume-components.js
python3 Scripts/check_web_catalogue.py
python3 Scripts/check_contrast.py tokens.css
swift test --package-path DesignSystem/SwiftUI
# once scaffolded (W.0+):
npx astro check
npm run build
```
