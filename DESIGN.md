---
name: Uzume
description: A dark theater opened by performed, prismatic light.
colors:
  canvas: "#0b0c10"
  surface: "#14151a"
  surface-raised: "#1d1f25"
  surface-selected: "#292b33"
  line: "#34363f"
  text-primary: "#f4f6f1"
  text-secondary: "#c5c9c3"
  text-tertiary: "#a4a8a2"
  accent: "#7f6aff"
  accent-hover: "#a99bff"
  accent-pressed: "#7865ee"
  on-accent: "#0b0c10"
  opening-violet: "#7f6aff"
  opening-cyan: "#37d6c0"
  opening-ember: "#ff6b4a"
  success: "#67d6a2"
  warning: "#ffd60a"
  danger: "#ff8a75"
typography:
  display:
    fontFamily: "Alumni Sans, Arial Narrow, sans-serif"
    fontSize: "clamp(3.5rem, 8vw, 6rem)"
    fontWeight: 600
    lineHeight: 0.92
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Alumni Sans, Arial Narrow, sans-serif"
    fontSize: "2.5rem"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  body:
    fontFamily: "PT Sans, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "PT Sans, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 700
    lineHeight: 1.45
rounded:
  compact: "6px"
  standard: "12px"
  prominent: "16px"
  pill: "999px"
spacing:
  x1: "4px"
  x2: "8px"
  x3: "12px"
  x4: "16px"
  x5: "20px"
  x6: "24px"
  x8: "32px"
  x10: "40px"
  x12: "48px"
  x16: "64px"
  x20: "80px"
  x24: "96px"
  x32: "128px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.standard}"
    padding: "10px 18px"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.standard}"
    padding: "10px 18px"
    height: "44px"
  button-secondary:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.standard}"
    padding: "10px 18px"
    height: "44px"
---

# Design System: Uzume

## Overview

**Creative North Star: "First Opening"**

Uzume is a dark theater at the instant a tiny opening admits performed, prismatic light. Darkness is the condition, the opening is the event, and color is the consequence. The First Opening identity and the visualizer's real output provide spectacle; interface chrome remains restrained, specific, and calm.

This is one system expressed in two platform languages. The website persuades with editorial scale, Alumni Sans, and large fields of real engine footage. The macOS app operates through native structure, San Francisco, system colors, and minimal controls. They share intent, hierarchy, rhythm, state language, and accessibility—not pixel-identical controls.

The implementation model has four layers: primitives, semantic roles, platform mappings, then named components and patterns. Website product code consumes semantic roles from `tokens.css`; native work maps intent through SwiftUI/AppKit semantics, with `DesignSystem/UzumeTokens.swift` as the current reference.

**Key Characteristics:**

- Performance output receives the largest and richest visual field.
- Midnight and ivory make the stage; violet communicates action; the spectrum communicates light.
- Preparation is informative and atmospheric while preserving mystery.
- Marketing is expressive; native controls remain recognizably macOS.
- Voice and motion are plain, warm, unhurried, and specific.

## Colors

Midnight and ivory hold the stage. Violet is the interaction accent. Violet, cyan, gold, and ember also appear together as the light brought through the opening; isolated gold is never control chrome.

### Primary

- **Action Violet:** Primary actions, focus relationships, and app tint. In identity artwork it appears only as part of the full performed-light spectrum, never as a status color.

### Secondary

- **Opening Violet:** Identity artwork, real performance footage, and meaningful visual metadata.
- **Opening Cyan:** Identity artwork, real performance footage, information status where the semantic token is used.

### Tertiary

- **Opening Ember:** Identity artwork and performed-light fields; danger uses its separate semantic red.

### Neutral

- **Midnight Canvas:** The website ground and the dark preparation-to-performance environment.
- **Tonal Surfaces:** Grouping, selection, and genuine elevation without card proliferation.
- **Ivory Text:** Essential content and the bright edge of First Opening.
- **Muted Ivory:** Supporting copy and metadata that must still meet contrast requirements.

Status colors retain conventional meanings and are always paired with text and an icon: green success, yellow warning, red error, and blue information. On macOS, use the corresponding adaptive system colors and standard alert/control structures without bending them toward the brand palette.

Web status components use four tokens per tone: `foreground`, `background`, `border`, and neutral component text. Dark appearance uses bright status marks on deep chromatic fields; light appearance uses dark status marks on pale chromatic fields. Warning is deliberately asymmetric: bright yellow carries the warning mark in dark appearance, while dark amber and black detail sit on a pale-yellow field in light appearance. The same bright yellow is never reused as light-mode text.

The website follows `prefers-color-scheme` unless an explicit `data-theme="light|dark"` scope is present. Both appearances are authored independently rather than inverted. Component typography keeps the same semantic size, weight, line height, and typeface across appearances; only color roles adapt. Normal text must remain at least 4.5:1; meaningful icons, borders, and focus indicators must remain at least 3:1. Increased-contrast mode strengthens boundaries without changing semantic hue.

**The Violet Acts Rule.** Violet marks the primary action and branded app tint. Filled controls and focus treatment distinguish that semantic role from violet appearing inside performed-light artwork.

**The System Status Rule.** Do not recolor notifications to fit the brand. Yellow warns, red fails, green succeeds, and blue informs; icons and explicit language remain mandatory.

**The Gold Performs Rule.** Gold belongs to First Opening, real visual output, and atmospheric light. It never identifies an action, focus state, selection, progress state, or notification.

**The Spectrum Performs Rule.** Use the full spectrum for the identity, actual engine output, atmospheric progress, and distinctions with real meaning—never as equal-colored tabs or arbitrary chart categories.

## Typography

- **Display Font:** Alumni Sans SemiBold (with Arial Narrow and sans-serif fallbacks)
- **Body Font:** PT Sans (with system-ui and sans-serif fallbacks)
- **Native UI Font:** San Francisco through SwiftUI/AppKit semantic styles
- **Code Font:** Platform monospace

**Character:** Alumni Sans is commanding and performative without becoming ceremonial. PT Sans is warm, compact, and legible. Native UI uses the platform's own typography so branded moments never compromise operation.

### Hierarchy

- **Display** (600, responsive 56–96 px, 0.92 line height): Short website statements and branded editorial moments.
- **Headline** (600, 40 px, 1.08 line height): Major web section headings.
- **Title** (600, 28 px, 1.08 line height): Component and subsection titles.
- **Body** (400, 16 px, 1.55 line height): Product explanation, forms, navigation, and documentation; keep prose between 45 and 75 characters per line.
- **Label** (700, 14 px, 1.45 line height): Compact control labels and metadata. Uppercase tracking is reserved for compact metadata, never section headings.
- **Native** (semantic system styles): Settings, controls, preparation copy, and all dense application content. Alumni Sans may appear only in branded first-run, empty, or About moments.

Sentence case is the default. Controls use verbs and outcomes. Status copy uses present participles only for work genuinely in progress.

**The Native Means Native Rule.** Do not force Alumni Sans or PT Sans into macOS control surfaces.

## Layout

The shared spatial rhythm is four points: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, and 128. Group labels more tightly with their controls than one group with the next. Whitespace and separators come before cards.

Website content widths are 48 rem for reading, 72 rem by default, and 90 rem for immersive media. Page gutters scale from 16 to 48 px. Sections use 64–128 px of vertical separation based on viewport and content change. Marketing composition may be asymmetric; documentation retains a stable reading column and persistent wayfinding. Web interactive targets are at least 44×44 px.

The first website viewport contains real performance footage, a plain product sentence, Apple Silicon/macOS 14+ requirements, and “Download the beta.” The visitor must understand the product and act without first reading the icon, myth, open-source model, or architecture. The remaining landing sequence is: prepared-performance difference, trust, certified preset gallery, brief myth and identity, then contributor invitation.

macOS layouts are task-shaped: sidebar for durable destinations, toolbar for window-level actions, split view for selection/detail, inspector for editable secondary attributes, sheets for focused tasks, and popovers for transient choices. With two displays, the external display receives clean full-screen output and the Mac receives a compact Curator surface; mirrored full-screen output is the fallback.

## Elevation & Depth

The system is tonal by default. Canvas, surface, raised surface, and selected surface establish hierarchy before shadow is considered. Shadows appear only where content genuinely floats, such as a popover, compact Curator surface, or isolated native window specimen. Performance footage and prismatic light create visual depth through content, not glass effects or ambient glow.

### Shadow Vocabulary

- **Raised:** A broad, low-contrast shadow for truly floating content (`0 16px 42px rgb(0 0 0 / 32%)`).
- **Focus:** A two-stage ring that separates violet from the canvas (`0 0 0 3px canvas, 0 0 0 5px focus`).

**The Tonal-First Rule.** A surface stays flat at rest unless its behavior requires it to float above another surface.

## Shapes

On the website, Uzume uses gently curved, geometric surfaces: compact controls at 6 px, standard components at 12 px, and prominent media or grouped regions at 16 px. The native mapping follows tighter macOS metrics—6, 10, and 14 pt—when custom compositions need a radius; standard controls retain their system shape. Pills are reserved for tags and compact segmented choices. The First Opening silhouette belongs to identity artwork and authored atmospheric fields; it is not a generic container shape.

Website icons use one consistent set with a 1.75–2 px stroke at 24 px. Native controls use SF Symbols and system-provided icons. The full First Opening icon is used at 64 px and above; the supplied art-directed crop is used at 16–32 px. The outlined wordmark is never recreated with live text and is at least 96 px wide.

## Components

Detailed anatomy, variants, states, and accessibility requirements live in `DesignSystem/COMPONENTS.md`. Working implementations live in `DesignSystem/Web/` and the `DesignSystem/SwiftUI/` package. The platforms share intent without sharing literal control rendering.

### Website

The launch web library contains seven stateless, composable components with named consumers in the website plan: Button, Icon Button, Link, Banner, Definition List, Media Frame, and Preset Card. It does not duplicate Starlight controls or invent form, overlay, filtering, and preference components for surfaces that are not planned.

- **Actions:** Button, Icon Button, and Link cover downloads, supporting navigation, contributor routing, and media playback. Loading preserves Button label meaning and width. Disabled controls use an opaque neutral surface, retain 4.5:1 text contrast by Uzume policy, and include a nearby reason.
- **Feedback:** Banner covers beta availability plus permission and installation guidance. Status colors retain conventional meaning and every failure names a recovery or supporting resource.
- **Content:** Definition List covers repeated requirements and factual metadata. Media Frame presents real engine footage with poster fallback, attribution, controls where needed, lazy loading, and a still experience under reduced motion. Preset Card retains identity and contributor credit when media fails.

Website patterns compose these components without becoming component APIs: Site Header, Download Decision, Trust Explanation, Preset Gallery, and Contributor Invitation.

### macOS Application

The user journey is **Configure → Add music → Prepare → Handoff → Perform → End**. Viewer output never includes settings, diagnostics, errors, or operator controls.

- **Performance Preflight:** Before music is added, summarizes audio source, visual output/display, eligible repertoire, quality, and accessibility. Deep durable preferences open the native Settings scene.
- **Source Picker:** Names the actual capabilities of local files, folders, playlists, Apple Music, Spotify, and any retained reactive source. Streaming never promises playback control the integration cannot honor.
- **Preset Eligibility Picker:** Includes or excludes families and individual presets with author and certification metadata. It never exposes track assignments, future selections, ordering, transition placement, or plan editing.
- **Permission Explanation:** Before the macOS Screen Recording dialog, explains that Uzume uses system audio, captures neither screen nor microphone, processes locally, and does not need the permission for local-file playback.
- **Preparation Stage:** A signature dark surface with progress-linked abstract light, a plain-language stage, completed/total count, elapsed time, credible estimate, and Listening → Separating → Understanding → Composing trace. It never reveals track names/order, artwork, selected presets/families, transitions, moods, or plan structure. “Start now” is exceptional-only while whole-session equivalence remains unvalidated.
- **Streaming Handoff:** Authorized integrations may start legitimately. Otherwise it gives a source-specific instruction such as “Start the playlist in Spotify,” waits for sustained audio, then cuts directly to the first preset without a plan preview or Ready ceremony.
- **Curator Control Surface:** Always discoverable on the Curator display and absent from separated Viewer output. It contains listening status, Show/Hide Track Information, and End Session; local-file transport appears only because Uzume owns that playback.
- **Settings:** Native sidebar and form controls for Audio, Visual Output, Presets, Accessibility, Diagnostics, and About. Session-affecting changes state when they will apply.

### Shared States and Motion

Every relevant component handles ready, focus/selection, loading, empty, permission blocked, offline/unavailable, error, disabled, and consequential success. Errors state problem, consequence, and recovery while preserving user work.

Control feedback lasts 120 ms, standard state changes 240 ms, and authored opening 480 ms using exponential ease-out. Reduced motion removes scale, parallax, autoplay, continuous animation, and large spatial transitions; content appears immediately or through a native crossfade.

## Do's and Don'ts

### Do:

- **Do** let real engine footage carry the largest color field on product and website surfaces.
- **Do** use semantic tokens from `tokens.css` and adaptive SwiftUI/AppKit colors rather than raw values in components.
- **Do** preserve mystery during preparation while showing truthful progress, elapsed time, credible estimates, and understandable stages.
- **Do** lead the website with the listener's download decision; contributor recruitment is secondary.
- **Do** use plain, specific copy for permissions, beta limits, failures, and recovery.
- **Do** meet WCAG AA, support keyboard and VoiceOver operation, expose progress semantically, and honor reduced motion, increased contrast, and transparency reduction.
- **Do** add tokens only for reusable decisions and components for repeated intent or centralized accessibility behavior.

### Don't:

- **Don't** describe Uzume as AI-powered or claim AI orchestration. Machine learning analyzes audio; deterministic rules plan the session.
- **Don't** reveal the planned track sequence, preset choices, transitions, or moods before performance.
- **Don't** make the native app look like the marketing website; brand it through tint, display moments, language, and the performance itself.
- **Don't** draw a camera iris, lens, eye, prism object, cave, door, or religious object as the core identity.
- **Don't** redraw the spectrum as hard parallel rainbow stripes or use all identity colors as decorative controls.
- **Don't** use vaporwave glow, generic AI shimmer, DAW skeuomorphism, stock music imagery, generic waveforms, or looping brand chrome.
- **Don't** fabricate footage, customer claims, testimonials, service control, or production readiness.
