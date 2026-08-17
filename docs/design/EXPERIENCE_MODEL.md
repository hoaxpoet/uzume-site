# Uzume Experience Model

This document records the product decisions established by inspection of the Phosphene repository and the August 2026 design-system interview. It governs representative screens and component priorities; it does not modify the application repository.

## Product truth

Machine-learning models analyze audio. Preset selection, sequencing, and transition planning are deterministic and rules-based. Uzume does not currently offer generative AI orchestration and must not be marketed as doing so.

The Curator is usually also the Viewer. Design must preserve the surprise of the playlist sequence, preset selection, and transitions rather than exposing the plan during preparation.

## macOS journey

### Configure

Before adding music, the Curator may configure the audio source, visual output, display behavior, quality, accessibility, and which presets or preset families are eligible. The Curator may define the eligible repertoire but may not assign presets to tracks, reveal assignments, place transitions, or edit the planned sequence.

Durable preferences live in a native Settings window. Session-variable choices appear in a compact preflight surface titled around the performance being prepared—not in a permanent dashboard.

### Add music

The Curator selects local files, folders, or playlists, or connects a supported streaming playlist. Source selection states requirements before commitment, including the macOS system-audio permission for streaming capture.

### Prepare

Preparation is a principal product experience. It must remain informative and atmospheric for waits that may last minutes while preserving mystery.

Show overall progress, completed track count, elapsed time, a credible estimate when one exists, plain-language work stages, an evolving abstract field of light tied to verified progress, and clear cancellation or recovery.

Do not show track names or ordering, artwork, selected presets or families, transitions, plan structure, mood classifications, analysis charts, or diagnostic detail.

“Start now” is not part of the normal path because the whole-session plan is incomplete. It may appear after an exceptional delay only if the product can explain the compromise honestly. Until perceptual equivalence is validated, waiting remains the recommended action.

### Handoff

Local-file playback begins automatically when preparation completes. A streaming integration may start playback only when the service and user authorization support it legitimately. Otherwise preparation resolves into a clear instruction—“Start the playlist in Spotify”—and waits for detected audio.

The first detected audio cuts directly from preparation into the first preset. There is no plan preview and no separate ceremonial Ready screen.

### Perform

The visual output is full screen. When a second display is available, the preferred mode is clean output on the external display with a compact Curator surface on the Mac. Mirrored full-screen output remains an acceptable fallback.

The always-discoverable control surface is minimal: show or hide track information and End Session. Listening state may be visible but is not a control. Preset nudges, track-level assignment, transition editing, and re-planning are not primary product controls. Developer diagnostics remain outside the user surface.

### End

End the performance gently. Preserve a useful summary and offer a new session without turning reflection into analytics.

## Website journey

The website’s primary job is to convince listeners to download Uzume. Recruiting preset contributors is secondary.

The landing path is:

1. Real performance footage, a plain explanation, requirements, and download action
2. Evidence of the prepared-performance difference
3. Permission, privacy, compatibility, beta, reduced-motion, and flash-safety trust
4. A gallery of real certified preset footage
5. A short explanation of the Uzume myth and First Opening identity
6. A contributor invitation showing Metal + JSON and hot reload

Open source is a trust and contribution fact, not an alternate product identity. AI is not part of the public story.

## Validation questions

- Does preparation remain compelling for two minutes without revealing the show?
- Can a first-time user explain what is happening and how long remains?
- Does the transition into the first preset feel immediate when audio begins?
- Can the Curator find track-information visibility and End Session without knowing a shortcut?
- Does an external display remain free of operator messages and errors?
- Can a visitor understand and choose to download Uzume within the first viewport?
