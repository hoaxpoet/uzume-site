# Uzume Brand Guidelines

## Brand idea

**First Opening** is the selected identity. Two shadows nearly meet, leaving a tiny irregular opening through which prismatic light enters the dark. It is a play of shadow and light rather than a pictured aperture: darkness is the condition, the opening is the event, and color is the consequence.

Uzume should be remembered as **the performer who brings light**. The brand does not picture every beat of the myth. It captures its decisive change: planned performance creates curiosity, the world opens, and light returns.

## Name, pronunciation, and story

**Uzume** is pronounced **oo-ZOO-meh**. Show pronunciation once in introductory or press contexts; do not append it to every lockup.

In the Ama-no-Iwato myth, the world darkens when Amaterasu withdraws into the heavenly rock-cave. Omoikane prepares a plan; Ame-no-Uzume performs with such force and joy that the assembled gods erupt in laughter. Curious, Amaterasu looks out, the prepared mirror catches her radiance, and light returns. The product mapping is direct: a session is planned, a visual performance unfolds, and music is answered in light.

Use the myth with care. Describe Ame-no-Uzume as an active, commanding performer—not a mascot. Respectful, research-grounded depiction is permitted in editorial work; avoid caricature, sexualization, invented “Japanese” costume, and decorative shrine imagery.

## Positioning

Uzume is a native macOS music visualizer that performs light to whatever the listener is already playing. It is not a playback controller and not a generic reactive waveform. Whole-playlist analysis informs an orchestrated visual arc; live listening refines it; contributor-written presets form the performance vocabulary.

### Core message hierarchy

1. **What it is:** visual performances for the music already playing.
2. **Why it is different:** it plans a session, then refines it live.
3. **Why it is trustworthy:** local-first explanation, clear permissions, reduced-motion support, and certified presets measured at 0 flashes per second.
4. **Why it can grow:** the visual repertoire is open to shader-writing contributors.

## Tagline

*“A light in sound, a sound-like power in light.”* — Samuel Taylor Coleridge, *The Eolian Harp* (1795, public domain).

The tagline is an atmospheric close, not the primary product explanation. Pair it with plain language that says what Uzume does.

## Voice

Uzume is **plain, warm, unhurried, and specific**.

- Lead with the action or answer: “Choose a folder,” not “Let’s get started!”
- Describe preparation and planning concretely; avoid mystical language where a product mechanism will do.
- State beta limitations, permissions, and recovery paths before users encounter them.
- Do not describe Uzume as AI-powered or claim AI orchestration. Machine learning analyzes audio; deterministic rules plan the session.
- Prefer “Uzume listens” and “Uzume performs” to treating the app as a passive display.
- Buttons name outcomes: “Download the beta,” “Open System Settings,” “Retry analysis.”
- Errors name the problem and next action: “System audio is unavailable. Allow Screen Recording in System Settings, then try again.”

## Identity system

### App icon and favicon

- Use `brand/icon/Uzume-1024.png` for the macOS app icon and large identity display.
- Use the full composition at **64 px or larger**.
- Use the supplied art-directed crop in `brand/favicon/` at **16–32 px**. It is the same artwork reframed, not a second mark.
- Maintain clear space of at least one-eighth of the icon width around the squircle outside system-owned icon containers.
- Keep the ivory opening brighter than the surrounding spectrum.
- Do not recolor, sharpen, add type or glow, flatten the spectrum into bands, or place the icon over photography.
- A monochrome substitute is not approved.

### Wordmark

- Use the outlined files in `brand/wordmark/`; do not typeset a substitute lockup.
- Minimum digital width: **96 px** without pronunciation, **144 px** with pronunciation.
- Clear space: at least the cap height of the initial **U** on every side.
- Primary treatment: ivory on midnight. Approved inverse: midnight on ivory.
- Do not place the wordmark directly over engine footage or competing imagery.

## Typography

**Alumni Sans SemiBold** is the identity and display voice. It carries page-level statements, campaign headlines, and short editorial moments. Do not use it for settings, form controls, dense data, or paragraphs.

**PT Sans** is the website text and functional voice. It carries body copy, navigation, labels, forms, help, and documentation. The native macOS app uses the system typeface for controls and content; Alumni Sans may appear only in branded first-run, empty, or about moments.

Keep display lines short, sentence case, and tightly composed. Body copy should stay between 45 and 75 characters per line.

## Color

### Core identity palette

- Midnight `#0B0C10`
- Ivory `#F4F6F1`
- Violet `#7F6AFF`
- Cyan `#37D6C0`
- Gold `#F5C84C`
- Ember `#FF6B4A`

Midnight and ivory form the stage. Violet, cyan, gold, and ember are the light brought through the opening.

### Usage model

- **Violet is the interaction accent.** It marks primary actions, focus, and branded app tint; within identity artwork it appears only as part of the complete performed-light spectrum.
- **Gold is performed light, never interface state.** Do not use it for actions, focus, selection, progress, or notifications.
- **The full spectrum is content color.** Use it for First Opening artwork, actual engine footage, editorial light fields, and meaningful contributor/preset metadata.
- **Status colors are semantic.** Success, warning, error, and information use dedicated roles in `tokens.css`; do not assign violet/cyan/ember arbitrarily to statuses.
- **Status colors adapt by appearance.** Preserve the hue category, then change lightness and surrounding field for contrast. Light mode uses dark semantic marks on pale fields; dark mode uses bright marks on deep fields.
- **The app follows macOS semantic surfaces.** System background, label, separator, selection, and disabled colors adapt automatically. Brand colors theme only the layer the platform leaves open.
- Never use all five identity colors as a decorative set of controls, navigation tabs, or equal chart categories when no meaning exists.

## Image and footage direction

The engine’s output is the principal image language. Prefer a few large, immersive frames to galleries of tiny thumbnails. Crop for rhythm and scale, but never place explanatory copy over a visually busy region without a solid scrim or separate field.

Published footage must be real or clearly labeled as illustrative. Show the interface only when explaining a task; show engine output when making the emotional case. Do not add stock music imagery, generic waveforms, lens flares, or AI shimmer around the footage.

## Motion behavior

The brand’s authored movement is **opening**: content begins legible, darkness yields, and light becomes visible. Keep control transitions short (120–240 ms) and authored reveals deliberate (480 ms). Avoid looping brand chrome, synchronized section entrances, parallax, and decorative pulsing.

Under reduced motion, remove spatial travel, scale, looping autoplay, and decorative reveals. Preserve all content as an immediate state or restrained crossfade.

## Pythagoras

Pythagoras is a future in-app onboarding and help guide who connects sound, number, and visible form. He explains what the listener is seeing without pretending the performance can be reduced to a formula. He is not part of the core mark, decorative chrome, or routine error messaging.

## Selection record

Matt’s Task-5 decision: **“First Opening wins.”** Negative Dance remains an archived runner-up study. All earlier directions and simplified favicon experiments are rejected and are not part of the production identity.
