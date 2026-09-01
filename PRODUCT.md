# Product

<!-- impeccable:product-schema 1 -->

## Platform

adaptive

## Stack

The product is a native macOS application. This repository is its separate public website and brand workspace; the planned website stack is Astro 7 with Starlight, deployed as static assets on Cloudflare. BRAND.1 creates framework-free brand artifacts that the native app and future website can both consume.

## Users

Uzume serves two audiences:

- **Listeners who want their music made visible.** They play music in their existing player while Uzume listens, plans, and performs a visual accompaniment.
- **Shader-writing contributors.** They author Metal presets, use a hot-reload loop, and contribute the visual repertoire that listeners see.

## Product Purpose

Uzume is a native macOS music visualizer that performs light to music. It analyzes a playlist before playback, uses a deterministic session planner to select and sequence eligible presets, then adapts the performance with live audio analysis as the music unfolds. Success means the visual performance feels intentional rather than merely reactive, while remaining approachable to listeners and genuinely extensible by contributors.

## Positioning

Uzume is not a generic reactive waveform. Its distinctive mechanism is a prepared-performance model: playlist analysis informs a visual sequence, live listening refines it, and contributor-written presets form the performance vocabulary. Uzume controls playback for local files; for streaming sources it listens to the external player unless a supported integration can start it legitimately.

## Operating Context

Uzume will launch as a **free, open-source public beta** for Apple Silicon Macs running macOS 14 or later, MIT-licensed. That is the intended shape of the release and the right thing to write copy toward. **It has not launched yet.** The source repository [`hoaxpoet/uzume`](https://github.com/hoaxpoet/uzume) *is* public — contributors can already clone, build and run it — but there is **no release**: no signed or notarized build exists (Developer ID signing and notarization are blocked on a paid Apple Developer Program membership the project does not have), and nothing is downloadable. "Open source and buildable" and "available to install" are different claims; only the first is true today. Write the beta in the future tense until those land — describe what the beta will be, not something a visitor can download today. Listeners keep using their preferred playback source; system-audio capture requires macOS Screen Recording permission, while local-file playback does not. Contributors work in Metal and JSON with hot reload and repository test/certification gates.

## Capabilities and Constraints

- Native macOS application; this repo must not modify the application or its rename implementation.
- Public beta at launch: free, open source (MIT), with GitHub Issues as the feedback path once the repository is public — it is not yet.
- Certified presets are gated on **steady luminance** (D-157): per-preset tests assert a bounded maximum per-frame brightness change across a rendered sequence, and beat-locked motion is confined to bounded regions rather than global flashes. State it that way — the app does not measure a "flashes per second" figure, so do not publish one.
- The in-app onboarding/help persona is **Pythagoras**; this brand increment defines the future persona in two sentences only.
- The session planner is deterministic and rules-based. Machine learning is used for audio analysis, not generative planning. AI is not a current product or marketing claim.
- The canonical public name is **Uzume**, pronounced **oo-ZOO-meh**.

## Brand Commitments

- **Identity principle:** the engine's output is the brand. Brand chrome is a restrained, dark, typographic frame; rendered footage supplies the saturation and spectacle.
- **Story:** the Ama-no-Iwato myth—a dark world, a planned performance, a mirror prepared before light exists, and light returning to watch.
- **Tagline:** “a light in sound, a sound-like power in light,” from Samuel Taylor Coleridge's 1795 poem *The Eolian Harp* (public domain).
- **Voice:** plain, warm, unhurried, and never breathless.
- Treat Ame-no-Uzume as the commanding performer who brings light. A respectful, research-grounded depiction is permitted; avoid caricature, sexualization, invented “Japanese” costume, and decorative shrine iconography.

## Evidence on Hand

- Naming decision, pronunciation, collision review, and sensitivity posture: `docs/planning/NAMING_REPORT.md`.
- Myth retelling and copy vault: `docs/planning/MYTH_RESEARCH.md`.
- Audience, information architecture, design-system constraints, and accessibility commitments: `docs/planning/WEBSITE_PLAN.md`.
- Verified application behavior: the app repository [`hoaxpoet/uzume`](https://github.com/hoaxpoet/uzume) — `docs/PRODUCT_SPEC.md`, `docs/UX_SPEC.md`, and the SwiftUI implementation inspected in August 2026 (pre-rename, when the tree was still named Phosphene).
- Interview-backed cross-surface decisions: `docs/design/EXPERIENCE_MODEL.md`.
- No application footage, customer claims, testimonials, or production website assets exist in this repository yet; future work must not fabricate them.

## Product Principles

1. **Prepare, then perform.** Playlist analysis and deliberate sequencing—not reactive decoration—are the product's center.
2. **The engine gets the stage.** Brand and interface recede so the visual output can lead.
3. **Make contribution visible.** Presets and their authors are a first-class product surface.
4. **Explain trust before requesting it.** Permission, local processing, beta status, and requirements are stated plainly.
5. **Care is a feature.** Reduced-motion behavior and measured flash safety are named, visible commitments.

## Accessibility & Inclusion

Honor `prefers-reduced-motion` absolutely. Brand chrome becomes effectively still under reduced motion, and the product's certified-preset steady-luminance standard (D-157) is communicated explicitly, in the terms the app actually gates. All brand text/background pairings must meet WCAG AA. The Japanese religious reference is treated as respectful homage within Uzume's domain of performance and is never rendered as costume or literal sacred imagery.
