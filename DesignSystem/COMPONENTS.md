# Uzume Component Library

These are the components justified by the website, the agreed Uzume experience, and the Uzume macOS app's current SwiftUI implementation. This document defines target intent, anatomy, variants, states, accessibility, and migration ownership; the source implementations live beside it.

- Web catalogue home: `DesignSystem/Web/index.html`
- Web component reference: `DesignSystem/Web/components/index.html`
- Web pattern reference: `DesignSystem/Web/patterns/index.html`
- Native reference: `DesignSystem/Web/native/`
- Web source: `DesignSystem/Web/uzume-components.css` and `uzume-components.js`
- Native package: `DesignSystem/SwiftUI/`
- App source census (taken pre-rename, when the tree was named Phosphene): `docs/design/PHOSPHENE-COMPONENT-CENSUS.md`

## Source reconciliation

The SwiftUI package is a migration target, not a parallel replacement application. The app's existing components remain the behavioral source until each migration is implemented and tested.

| Uzume target | Existing app source | Migration posture |
|---|---|---|
| `SourcePicker` | `ConnectorPickerView`, `AppleMusicConnectionView`, `SpotifyConnectionView`, `LocalSourceConnectionView` | Preserve connector state and task lifetime; redesign the composition |
| `SourceChoice` | `ConnectorTileView`, private `LocalSourceActionTile` | Consolidate navigation, action, disabled, and recovery variants |
| `PreparationStage` | `PreparationProgressView` | Rebuild in place; preserve progress publishers, recovery, cancel, and progressive readiness |
| `PreparationTrackRow` | `TrackPreparationRow`, `TrackPreparationStatusIcon` | Retain state vocabulary and accessibility; retokenize presentation |
| `StreamingHandoff` | `ReadyView`, `ReadyViewModel`, first-audio detection | Replace ready presentation; preserve source-aware instructions and audio gate |
| `PerformanceChrome` | `PlaybackChromeView` and its child views | Retokenize and reorganize the existing composition; do not create a second control tree |
| `TrackInformation` | `TrackInfoCardView` | Preserve current-track data; remove future-plan disclosure |
| `LocalPlaybackTransport` | `LocalFileTransportBar` | Preserve local-only transport capability and callbacks |
| `StatusTone` placements | `TopBannerView`, `LocalFileErrorBanner`, `ToastView`, `FullScreenErrorView`, `PreparationFailureView` | Share semantics and primitives while retaining distinct interruption levels |
| `PresetEligibilityPicker` | `PresetCategoryBlocklistPicker` | Expand the existing include/exclude control rather than inventing a separate settings model |
| `PerformancePreflight` | No existing equivalent | New component; integrate with existing Settings and source entry points |

`PlanPreviewView`, `PlanPreviewRowView`, and `PlanPreviewTransitionView` are not design-system foundations. They reveal future track/preset choreography and conflict with the agreed surprise model, so they are removal candidates during the Ready/Playback refactor.

## Naming and ownership

- Web implementation consumes semantic roles from `tokens.css` and can be wrapped by future Astro components without changing its contract.
- Native implementation ships as the local `UzumeDesignSystem` Swift package. The application can adopt it during the rename/product-integration increment.
- Component names describe stable UI responsibility; screen and pattern names describe product tasks.
- A component variant changes behavior or hierarchy. One-off layout differences remain composition.
- Existing state ownership is preserved: screen-level views own `@StateObject` view models; app stores stay environment-injected; design-system components receive display models, bindings, and actions.
- Native SwiftUI controls remain native. Tokens and composition provide Uzume identity without rebuilding standard macOS control behavior.

## Web components

Morningstar’s composable model informs these contracts, but its breadth does not define Uzume’s inventory. A website component is admitted only when the launch plan names a consumer. The planned website has no accounts, submissions, contact forms, or preference editing; Starlight owns docs search and code-interface controls.

| Component | Named website consumers | Required contract |
|---|---|---|
| `Button` | Landing download, Download page, contributor invitation | Primary, secondary, quiet; one 44 px-minimum size; loading and disabled reason |
| `IconButton` | Hero and gallery media controls | One 44 × 44 px presentation; play, pause, and mute; accessible name; disabled reason when needed |
| `Link` | Site navigation, documentation, credits, supporting download links | Default and quiet treatments; internal or external destination; unavailable copy is rendered without `href` |
| `Banner` | Download availability, Getting Started permission/install guidance | Info/success/warning/error; explicit language; optional supporting link |
| `DefinitionList` | Landing requirements, Download requirements, preset facts | Two-column and stacked responsive layouts |
| `MediaFrame` | Landing hero reel and prepared-performance evidence | Image, video, or explicit fallback; caption and attribution; playback controls compose `IconButton` |
| `PresetCard` | Certified preset gallery and landing teaser | Preview available/unavailable; name, author, certification, attribution; playback controls compose `IconButton` |

The following were explicitly removed as speculative: Input, Textarea, Select, Checkbox, Radio Button, Switch, Search Field, Fieldset, Inline Message, Progress, Spinner, Empty State, Tabs, Disclosure, Tag, Dialog, and Tooltip. If a future approved surface introduces a named consumer, that component can be added then.

### Shared component requirements

- Components use native HTML elements before ARIA and consume semantic roles from `tokens.css`.
- Components are stateless except for local media state and the Button loading state. `Button` is the only web component with a scripted state helper in this increment.
- All interactive controls have visible focus, keyboard operation, and a 44 × 44 px minimum target.
- Disabled controls retain readable text by Uzume policy and require a nearby associated reason when the user needs to understand why.
- `prefers-reduced-motion` removes nonessential transitions and indeterminate rotation without hiding status.
- Light and dark appearances map component roles independently; status colors retain conventional meaning.

## Web patterns

Patterns document how components and content are assembled for Uzume tasks. They are not interchangeable component APIs.

### Site header

Composes the wordmark, Links, current-location treatment, and Button. Its behavior belongs to the website shell.

### Download decision

Keeps product outcome, compatibility, availability, primary Button, supporting Link, and disabled reason in one decision region. Uses `DefinitionList`, `Button`, and `Link`.

### Trust explanation

**Purpose:** Explain a potentially alarming dependency before the user encounters it.

**Variants:** Permission, local processing/privacy, reduced motion/photosensitivity, beta expectations.

**Anatomy:** Specific heading, plain explanation, consequence, optional documentation link. Status color may support but never replace text or icon.

**Appearance:** Every status maps foreground, background, and border separately in light and dark themes. Warning uses dark amber/black detail on pale yellow in light appearance and bright yellow on a deep field in dark appearance. Neutral text carries the message in both.

### Contributor invitation

**Purpose:** Recruit preset contributors without competing with the listener download path.

**Anatomy:** One outcome-led statement, concise invitation, and documentation action. It never appears before the primary download decision.

### Preset gallery

Composes certified `PresetCard` entries into the full gallery and landing-page teaser. Entries are generated from the preset content collection and retain identity and contributor credit when media fails.

## Native platform controls

Standard macOS controls are components in the Uzume system even though Uzume does not redraw them. Their shared contract specifies when to use each native family, which roles and control sizes are allowed, how brand tint is applied, and which accessibility behavior must remain intact.

| Native family | App evidence | Uzume direction |
|---|---:|---|
| `Button` | 56 construction sites | Preserve native roles/styles; tint primary actions violet; retain system destructive treatment |
| `Toggle` | 4 construction sites | Immediate binary settings; use native switch or checkbox style by context |
| `Picker` | 4 construction sites | Choose menu, segmented, or radio presentation from option count and task |
| `TextField` | Spotify playlist entry | Visible label, prompt, help/error relationship, native focus behavior |
| `ProgressView` | 8 construction sites | Determinate when measurable; spinner only for indeterminate work |
| `DisclosureGroup` | Permission onboarding | Supporting detail only; never hide a required action |
| `List` / `Form` / `Section` | Settings navigation and four form sections | Preserve native macOS settings structure; no bespoke card stack |
| Sheet / confirmation dialog | Five sheets and four confirmation dialogs | Sheet for focused subtasks; confirmation only for consequential actions |

## Native product component extraction

These are reusable units justified by the app's current source. Extraction happens while their existing consumers are refactored; this document does not authorize parallel replacements.

### `SourceChoice`

**Source:** `ConnectorTileView` and private `LocalSourceActionTile`.

**Variants:** Navigation, immediate action, unavailable with reason, unavailable with recovery action.

### `PreparationTrackRow`

**Source:** `TrackPreparationRow` and `TrackPreparationStatusIcon`.

**Content:** Track identity, preparation state, optional determinate sub-progress, and honest ETA. The row preserves the existing accessible combined label/value contract.

### Status placements

`NoticeBanner`, `InlineNotice`, `PerformanceToast`, and `RecoveryScreen` share status tone and icon rules but remain separate components because interruption, lifetime, and action behavior differ.

**Source:** `TopBannerView`, `LocalFileErrorBanner`, `ToastView`, `FullScreenErrorView`, and `PreparationFailureView`.

### `TrackInformation`

**Source:** `TrackInfoCardView`.

**Content:** Current title, artist, and available artwork. Preset name is omitted by default if it weakens surprise. Never exposes upcoming content.

### `PerformanceControls`

**Source:** `PlaybackControlsCluster`.

**Content:** Settings and End Session with optional session position. Local transport is not included because it is source-conditional.

### `SessionPosition`

**Source:** `SessionProgressDotsView`.

**Behavior:** Planned, reactive, and large-session variants. Retained only if aggregate position does not weaken the surprise model.

### `ListeningStatus`

**Source:** `ListeningBadgeView`.

**Behavior:** Announces sustained silence without implying failure; respects reduced motion and does not intercept input.

### `LocalPlaybackTransport`

**Source:** `LocalFileTransportBar`.

**Behavior:** Stop, previous, play/pause, and next are available only when Uzume owns local playback.

### `PresetEligibilityPicker`

**Source:** `PresetCategoryBlocklistPicker`.

**Behavior:** Expands the existing include/exclude preference to support family and individual eligibility. It never edits track assignments or future plan order.

## Native screens and compositions

The following own routed product states or assemble multiple components. They belong in experience documentation, not the component inventory.

### `PerformancePreflight`

**Purpose:** Confirm the session boundaries before music is added.

**Anatomy:** Audio source summary, output/display summary, eligible repertoire summary, accessibility/quality summary, Add Music primary action, Settings access.

**Behavior:** High-frequency choices may be changed in place; deeper durable choices open the appropriate Settings section. Preflight never exposes plan editing.

**States:** Ready, source unavailable, permission needed, external display disconnected, no eligible presets.

### `SourcePicker`

**Purpose:** Choose local files/folders/playlists or a supported streaming source.

**Variants:** Local file, local folder, local playlist, Apple Music, Spotify, reactive fallback when retained.

**Behavior:** Each source names its actual capabilities. A streaming source never promises playback control until the integration can honor it.

**Accessibility:** Native picker/list controls, keyboard operation, source availability in label and description rather than color alone.

### `PreparationStage`

**Purpose:** Make minutes of hidden work understandable and atmospheric without spoiling the performance.

**Anatomy:** Abstract progress-linked light field, stage statement, completed/total count, determinate progress when honest, elapsed/estimated time, four-step trace, Cancel, recovery slot.

**Stages:** Listening, Separating, Understanding, Composing. These are user language, not one-to-one promises about internal threads.

**Behavior:** Changes in light correspond to verified progress milestones. Motion begins from a complete, legible default and never blocks information. No selected content is previewed.

**States:** Active, estimate unavailable, exceptional delay, offline, partial failures, no analyzable tracks, cancelling, complete-awaiting-streaming-audio.

**Accessibility:** Progress has an accessible label and value; stage changes announce politely; time estimates do not announce on every small update; reduced motion keeps the field still while progress and copy update.

### `StreamingHandoff`

**Purpose:** Bridge completed preparation to externally controlled playback.

**Anatomy:** “Performance ready” statement, source-specific instruction, listening state, source recovery action when needed.

**Behavior:** If authorized integration can start playback, do so and bypass the instruction. Otherwise wait for sustained detected audio. On detection, remove the handoff and cut directly to the first preset.

**States:** Waiting for user, listening for audio, audio detected, source unavailable, timeout/retry.

### `PerformanceChrome`

**Purpose:** Compose the existing in-performance information, status, and controls without creating a parallel control tree.

**Existing source:** `PlaybackChromeView`, `TrackInfoCardView`, `PlaybackControlsCluster`, `ListeningBadgeView`, `SessionProgressDotsView`, `LocalFileTransportBar`, `ToastContainerView`.

**Anatomy:** Listening status, optional current-track information, session position, Settings, End Session, toast region, and source-conditional local transport.

**Behavior:** Present on the Curator display; absent from separated Viewer output. It may reduce to quiet edge controls after inactivity but cannot become undiscoverable.

**States:** Listening, temporarily silent, track information shown/hidden, end confirmation, local-file paused.

**Migration:** Retokenize and reorganize `PlaybackChromeView` in place. The package’s early `CuratorControlSurface` prototype is not the migration target because it omits the existing chrome’s state, source capability, and notification behavior.

### `PermissionExplanation`

**Purpose:** Explain system-audio capture before opening System Settings.

**Required copy facts:** macOS groups system-audio capture with Screen Recording; Uzume uses the audio portion; it does not capture the screen or microphone; processing remains local; local-file playback does not require this permission.

**Actions:** Open System Settings; choose local music where appropriate; dismiss only when a viable alternative remains.

## Release contract

Every component implementation must demonstrate:

- Real content at minimum and maximum supported sizes
- Keyboard and VoiceOver behavior
- Focus, disabled, loading, empty, error, and recovery states where applicable
- Reduced motion and increased contrast
- Light and dark appearance with semantic foreground/background/border mappings
- Localization expansion and long labels
- Viewer/Curator separation when the component can appear during performance
