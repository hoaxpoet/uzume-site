# BRAND.1 Artifact Inventory

## Production identity

| Path | Purpose | Format | License / source |
|---|---|---|---|
| `brand/icon/Uzume-1024.png` | First Opening app-icon master | PNG, 1024×1024 | Generated for Uzume during BRAND.1 |
| `brand/icon/Uzume.iconset/` | Complete macOS size set | 10 PNG files, 16–1024 px | Derived from the selected master |
| `brand/icon/Uzume.icns` | Installable macOS icon container | ICNS | Derived from the selected master |
| `brand/favicon/favicon-16.png` | Browser favicon | PNG, 16×16 | Art-directed crop of First Opening |
| `brand/favicon/favicon-32.png` | Browser favicon | PNG, 32×32 | Art-directed crop of First Opening |
| `brand/favicon/favicon-64.png` | High-density browser favicon | PNG, 64×64 | Art-directed crop of First Opening |
| `brand/favicon/favicon-180.png` | Apple touch icon | PNG, 180×180 | Art-directed crop of First Opening |
| `brand/favicon/favicon-512.png` | Favicon crop master | PNG, 512×512 | Art-directed crop of First Opening |
| `brand/favicon/favicon.svg` | Scalable favicon wrapper | SVG with embedded approved raster crop | Art-directed crop of First Opening |
| `brand/wordmark/Uzume.svg` | Primary outlined wordmark | SVG paths, no live text or raster | Outlined from Alumni Sans SemiBold |
| `brand/wordmark/Uzume-pronunciation.svg` | Introductory pronunciation lockup | SVG paths, no live text or raster | Outlined from Alumni Sans SemiBold |

## System and documentation

| Path | Purpose | Format |
|---|---|---|
| `PRODUCT.md` | Durable product and audience brief | Markdown |
| `DESIGN.md` | First Opening design-system rules | Markdown/YAML |
| `BRAND.md` | Story, voice, palette, and usage rules | Markdown |
| `tokens.css` | Shared website/app-facing design tokens | CSS custom properties |
| `DesignSystem/UzumeTokens.swift` | Semantic native macOS mapping reference | SwiftUI |
| `DesignSystem/COMPONENTS.md` | Website and macOS component contracts | Markdown |
| `DesignSystem/Web/index.html` | Rendered web component catalogue | HTML/CSS/JS |
| `DesignSystem/Web/uzume-components.css` | Reusable web component source | CSS |
| `DesignSystem/SwiftUI/` | Reusable macOS component package | Swift Package |
| `design/index.html` | Complete website + macOS design-system reference | HTML/CSS/JS |
| `design/reference.css` | Live component and responsive specimens | CSS |
| `design/reference.js` | Reference-page menu and motion demo behavior | JavaScript |
| `Scripts/build_final_brand.swift` | Reproducible wordmark/icon/favicons exporter | Swift |
| `Scripts/check_contrast.py` | WCAG text/background contrast gate | Python |
| `docs/reviews/BRAND.1/finalists/index.html` | Final selection record | HTML/CSS |
| `docs/design/EXPERIENCE_MODEL.md` | Interview-backed website and application journeys | Markdown |
| `docs/design/AUDIT-COMPONENT-LIBRARY-2026-08-14.md` | Current design-system and component-library validation | Markdown |

## Fonts

| File | Use | License |
|---|---|---|
| `brand/fonts/AlumniSans.ttf` | Display, identity source outlines | SIL Open Font License 1.1 (`brand/fonts/licenses/AlumniSans-OFL.txt`) |
| `brand/fonts/PTSans.ttc` | Body and functional copy | SIL Open Font License 1.1; bundled project font |

## RN.1 handoff

Install `brand/icon/Uzume-1024.png` or the prepared `brand/icon/Uzume.iconset` / `brand/icon/Uzume.icns` during RN.1 Task 3. BRAND.1 does not modify the application repository, bundle identifiers, Info.plist, or in-app strings.
