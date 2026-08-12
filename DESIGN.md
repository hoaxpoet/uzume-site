---
name: Uzume
description: A quiet theater for music performed as light.
colors:
  canvas: "#09090B"
  surface: "#111114"
  surface-raised: "#19191D"
  line: "#323238"
  text-primary: "#F4F1EA"
  text-secondary: "#C4BFB5"
  text-tertiary: "#969188"
  first-light: "#F2A64A"
  first-light-hover: "#FFC06B"
  first-light-dim: "#7A4A1E"
typography:
  display:
    fontFamily: "STIX Two Text, serif"
    fontSize: "clamp(3rem, 10vw, 8rem)"
    fontWeight: 500
    lineHeight: 0.94
    letterSpacing: "-0.035em"
  body:
    fontFamily: "PT Sans, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  label:
    fontFamily: "PT Sans, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.12em"
rounded:
  sm: "6px"
  md: "12px"
  lg: "20px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"
  2xl: "64px"
components:
  button-primary:
    backgroundColor: "{colors.first-light}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.sm}"
    padding: "12px 18px"
  button-primary-hover:
    backgroundColor: "{colors.first-light-hover}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.sm}"
    padding: "12px 18px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "24px"
---

# Design System: Uzume

## Overview

**Creative North Star: “The Darkened Theater”**

Uzume's visual system is the room around the performance: near-black, typographic, materially quiet, and precise enough that the engine's footage can become the only spectacle. The identity borrows structure—not imagery—from Ama-no-Iwato: darkness held in reserve, a deliberate plan, and one first line of warm light.

Restraint is law. Brand surfaces use near-black canvas, neutral text, exactly one amber accent family, and no other saturated color. Footage is the only saturation source; when footage appears, the chrome recedes further.

**Key characteristics:**

- Near-black tonal layers, separated by value and hairlines rather than glow.
- One display face with literary gravity; one highly legible sans serif for everything functional.
- Spacious compositions with one decisive interruption: a crack, gleam, or lit beat.
- Motion belongs to the engine; surrounding brand chrome stays nearly still.

## Colors

The palette is a dark neutral theater with one warm, first-light amber accent.

### Primary

- **First Light** (`#F2A64A`): the sole accent, used sparingly for the primary action, focus, a selected state, or the single mythic signal in a mark.
- **First Light Hover** (`#FFC06B`): the same amber made lighter for hover and high-emphasis interaction.
- **First Light Dim** (`#7A4A1E`): the same amber reduced for non-text ornament and quiet selected surfaces.

### Neutral

- **Canvas** (`#09090B`): the default field.
- **Surface** (`#111114`): cards and inset regions.
- **Raised Surface** (`#19191D`): the highest tonal layer; never glass.
- **Line** (`#323238`): rules and boundaries.
- **Primary Text** (`#F4F1EA`): titles and essential copy.
- **Secondary Text** (`#C4BFB5`): body copy and supporting information.
- **Tertiary Text** (`#969188`): labels and metadata only where verified against its background.

**The Single-Accent Law.** First Light and its hover/dim states are one hue family, not three colors. No second accent is introduced. Engine footage may contain any color because it is the work, not the chrome.

## Typography

**Display Font:** STIX Two Text (SIL Open Font License 1.1; serif fallback)

**Body Font:** PT Sans (SIL Open Font License 1.1; sans-serif fallback)

**Character:** The display voice feels measured and performance-minded without becoming theatrical costume. The text face is neutral, open, and practical; it explains permissions, requirements, and contribution steps without fanfare.

### Hierarchy

- **Display** (500, fluid 48–128 px, 0.94): the name, one-line statements, and major specimens.
- **Headline** (500, fluid 32–56 px, 1.05): section openings and campaign lines.
- **Title** (500, 20–28 px, 1.2): cards and grouped content.
- **Body** (400, 16–18 px, 1.6): explanatory copy.
- **Label** (600, 12 px, 1.3, tracked): short metadata and specimen annotation, never long prose.

The wordmark is always vector artwork, never live text. Do not fake its letterforms with the display face.

## Layout

Use generous negative space and a clear reading edge. Pages use a 4 px base spacing scale with meaningful stops at 8, 16, 24, 40, 64, 96, and 128 px. Dense technical material may use the smaller stops; brand statements and artwork need the larger ones.

The preferred composition is asymmetrical but calm: a dominant field, one narrow axis of metadata, and one interruption of first light. Cards are not the default container. Use grouping and whitespace first, tonal surfaces second, and borders only when they clarify a real boundary.

## Elevation & Depth

Depth is tonal, not glossy. Canvas, surface, and raised surface provide three quiet planes. No glassmorphism, colored shadow, bloom, glow edge, or simulated hardware panel is part of the system.

## Shapes

Small controls use 6 px corners, cards use 12 px, and large media frames may use 20 px. The app icon follows the macOS continuous rounded-square silhouette, but the inner motif remains geometric and abstract. Circles, lines, wedges, and repeated strokes may carry the myth; literal doors, mirrors, deities, or ritual objects may not.

## Components

- **Primary button:** First Light fill, Canvas text, 6 px radius, compact horizontal padding. It is the only filled accent control in a region.
- **Secondary action:** text or neutral outline; never a differently colored fill.
- **Card:** Surface background, Primary Text, 12 px radius. Avoid card-on-card nesting.
- **Focus:** a clear First Light outline with sufficient offset; focus is never communicated by color alone.
- **Footage frame:** plain crop on Canvas, with minimal controls. Footage owns all saturation within it.

Motion tokens are 120 ms (immediate), 240 ms (standard), and 480 ms (deliberate). They are reserved for state communication, not ambient brand animation. Under `prefers-reduced-motion: reduce`, all three collapse to 1 ms and nonessential transforms are removed.

## Do's and Don'ts

**Do:**

- Let footage lead and dim the interface around it.
- Use First Light once, decisively.
- Keep copy plain, warm, unhurried, and specific.
- Show and state reduced-motion support and certified 0-flashes-per-second care.
- Refer to the myth through abstract light, reflection, rhythm, and emergence.

**Don't:**

- Do not use vaporwave or synthwave neon kitsch.
- Do not imitate DAW-plugin skeuomorphism.
- Do not use crypto-glow gradients or generic “AI shimmer.”
- Do not add a second accent, identity gradient, or decorative motion loop.
- Do not depict Ame-no-Uzume, shrine iconography, torii, shimenawa, or any Shinto ritual object.
- Do not place the wordmark directly over photography or visually busy footage.
