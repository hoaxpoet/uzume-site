# Uzume — brand & website

Brand foundations and public website workspace for **Uzume**, a native macOS
music visualizer (the application was called *Phosphene* until the 2026-08-31
rename; see `docs/planning/NAMING_REPORT.md`).

## Source-of-truth boundary

This repository and the application repository each own different things, and
neither should re-derive the other's content.

| Owned here (`hoaxpoet/uzume-site`) | Owned in the app (`hoaxpoet/uzume`) |
|---|---|
| Brand story, voice, palette, typography — `BRAND.md` | Product behaviour and UX contract — `docs/PRODUCT_SPEC.md`, `docs/UX_SPEC.md` |
| Design system and component contracts — `DESIGN.md`, `DesignSystem/` | Engineering decisions — `docs/DECISIONS.md` |
| Production identity assets — `brand/` (icon, favicon, wordmark, fonts) | Build, test and contributor commands — `README.md`, `CONTRIBUTING.md`, `docs/RUNBOOK.md` |
| Naming research and website planning — `docs/planning/` | Preset authoring and certification — `docs/SHADER_CRAFT.md` |
| Public marketing copy and claims — `PRODUCT.md` | Whether a claim is *true of the shipped build* |

The app repository holds a **frozen RN.0 snapshot** of `docs/planning/` as
rename evidence. This repository's copies are the live ones; the snapshots are
not maintained.

Claims about what the application does, requires, or ships must be verified
against the app repository before they appear in public copy — this repository
does not get to assert product facts on its own.

## Start here

- `PRODUCT.md` — durable product and audience brief
- `BRAND.md` — story, voice, palette, usage rules
- `DESIGN.md` — the First Opening design system
- `ARTIFACTS.md` — what exists, where, and under which licence
- `docs/planning/BRAND.1-prompt.md` — the increment that produced the identity
- `docs/planning/` — naming, myth, and website-plan background

## Checks

```bash
node --check DesignSystem/Web/catalogue.js
node --check DesignSystem/Web/uzume-components.js
python3 Scripts/check_web_catalogue.py
python3 Scripts/check_contrast.py tokens.css
swift test --package-path DesignSystem/SwiftUI
```
