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

Uzume is a native macOS music visualizer that performs light to whatever the listener is already playing. It pre-analyzes a playlist, lets an AI orchestrator plan the session and its transitions, then refines that plan with live analysis while the music unfolds. Success means the visual performance feels intentional rather than merely reactive, while remaining approachable to listeners and genuinely extensible by contributors.

## Positioning

Uzume is not a playback controller and not a generic reactive waveform. Its distinctive mechanism is an authored-performance model: whole-playlist analysis informs an orchestrated visual arc, live listening refines it, and contributor-written presets form the performance vocabulary.

## Operating Context

Uzume is a free, open-source public beta for Apple Silicon Macs running macOS 14 or later. Listeners keep using their preferred playback source; system-audio capture requires macOS Screen Recording permission, while local-file playback does not. Contributors work in Metal and JSON with hot reload and repository test/certification gates.

## Capabilities and Constraints

- Native macOS application; this repo must not modify the application or its rename implementation.
- Public beta, free, open source, with GitHub Issues as the feedback path.
- Certified presets are measured at 0 flashes per second.
- The in-app onboarding/help persona is **Pythagoras**; this brand increment defines the future persona in two sentences only.
- The AI orchestrator's internal codename is **Omoikane**.
- The canonical public name is **Uzume**, pronounced **oo-ZOO-meh**.

## Brand Commitments

- **Identity principle:** the engine's output is the brand. Brand chrome is a restrained, dark, typographic frame; rendered footage supplies the saturation and spectacle.
- **Story:** the Ama-no-Iwato myth—a dark world, a planned performance, a mirror prepared before light exists, and light returning to watch.
- **Tagline:** “a light in sound, a sound-like power in light,” from Samuel Taylor Coleridge's 1795 poem *The Eolian Harp* (public domain).
- **Voice:** plain, warm, unhurried, and never breathless.
- Myth references remain abstract. Never depict Ame-no-Uzume, shrine iconography, torii, shimenawa, or Shinto ritual objects.

## Evidence on Hand

- Naming decision, pronunciation, collision review, and sensitivity posture: `docs/planning/NAMING_REPORT.md`.
- Myth retelling and copy vault: `docs/planning/MYTH_RESEARCH.md`.
- Audience, information architecture, design-system constraints, and accessibility commitments: `docs/planning/WEBSITE_PLAN.md`.
- No application footage, customer claims, testimonials, or production website assets exist in this repository yet; future work must not fabricate them.

## Product Principles

1. **Plan, then perform.** The orchestration model—not reactive decoration—is the product's center.
2. **The engine gets the stage.** Brand and interface recede so the visual output can lead.
3. **Make contribution visible.** Presets and their authors are a first-class product surface.
4. **Explain trust before requesting it.** Permission, local processing, beta status, and requirements are stated plainly.
5. **Care is a feature.** Reduced-motion behavior and measured flash safety are named, visible commitments.

## Accessibility & Inclusion

Honor `prefers-reduced-motion` absolutely. Brand chrome becomes effectively still under reduced motion, and the product's certified-preset standard of 0 flashes per second is communicated explicitly. All brand text/background pairings must meet WCAG AA. The Japanese religious reference is treated as respectful homage within Uzume's domain of performance and is never rendered as costume or literal sacred imagery.
