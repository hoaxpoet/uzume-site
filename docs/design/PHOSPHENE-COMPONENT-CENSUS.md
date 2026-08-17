# Phosphene → Uzume Component Census

Status: source audit complete, migration not started  
Source inspected: `/Users/braesidebandit/Documents/Projects/phosphene/PhospheneApp`  
Design-system target: `DesignSystem/SwiftUI`

## Why this exists

Uzume must not acquire a parallel component architecture that ignores the application it will replace. The current Phosphene implementation is evidence: it contains working composition, state ownership, accessibility identifiers, recovery behavior, and test seams. It is not automatically the desired visual design, naming model, or final product behavior.

The migration rule is therefore:

1. Preserve proven behavior and state boundaries.
2. Consolidate repeated intent before introducing another abstraction.
3. Redesign presentation where the current surface is visually unsuccessful.
4. Replace behavior only where the agreed Uzume experience explicitly differs.
5. Add a component only when the current application has no equivalent responsibility.

## Audit method

The census inspected all 49 Swift files under `PhospheneApp/Views`, plus `ContentView.swift`, `LocalFileErrorStore.swift`, related view models, `PRODUCT_SPEC.md`, and `UX_SPEC.md`. Static tracing found 57 named `View` or `ViewModifier` types including private helpers. Construction sites, state ownership, environment dependencies, and repeated hard-coded presentation values were checked directly.

The counts below are architectural evidence, not a reuse score. A one-consumer view can still be a valid component when it owns a stable responsibility; a frequently constructed helper can still be private when its meaning is local.

## Current composition

```text
ContentView
├── PermissionOnboardingView
└── session state
    ├── IdleView
    │   ├── PhotosensitivityNoticeView
    │   ├── LocalFileErrorBanner
    │   └── ConnectorPickerView
    │       ├── ConnectorTileView
    │       ├── AppleMusicConnectionView
    │       ├── SpotifyConnectionView
    │       └── LocalSourceConnectionView
    │           ├── LocalSourceActionTile
    │           └── LocalFileErrorBanner
    ├── ConnectingView
    ├── PreparationProgressView
    │   ├── TopBannerView
    │   ├── TrackPreparationRow
    │   │   └── TrackPreparationStatusIcon
    │   └── PreparationFailureView
    ├── ReadyView
    │   ├── ReadyPulsingBorder
    │   └── PlanPreviewView
    │       ├── PlanPreviewRowView
    │       └── PlanPreviewTransitionView
    ├── PlaybackView
    │   ├── MetalView
    │   ├── TrackChangeAnimationView
    │   ├── PlaybackChromeView
    │   │   ├── TrackInfoCardView
    │   │   ├── PlaybackControlsCluster
    │   │   │   └── SessionProgressDotsView
    │   │   ├── ListeningBadgeView
    │   │   ├── LocalFileTransportBar
    │   │   └── ToastContainerView → ToastView
    │   ├── AudioStallOverlayView
    │   ├── ShortcutHelpOverlayView
    │   ├── DebugOverlayView
    │   └── DashboardOverlayView
    └── EndedView

SettingsView
├── LocalFilesSettingsSection
├── VisualsSettingsSection
│   └── PresetCategoryBlocklistPicker
├── DiagnosticsSettingsSection
└── AboutSettingsSection
```

## Classification

### Application shells and state screens

These remain app-owned compositions. The design system supplies their smaller components and layout contracts; it should not absorb their session logic.

| Current surface | Current responsibility | Decision | Uzume target |
|---|---|---|---|
| `ContentView` | Permission gate and session-state routing | Retain | `AppRouter`; no design-system component |
| `IdleView` | Entry state, source selection, ad-hoc fallback | Redesign | `SessionHome`, composed from source and settings components |
| `ConnectorPickerView` | Source navigation and connector VM lifetime | Retain behavior, redesign composition | `SourcePicker` screen using `SourceChoice` |
| `AppleMusicConnectionView` | Apple Music connection states and recovery | Retain behavior | Source-specific flow using shared connection-state components |
| `SpotifyConnectionView` | URL/OAuth input, validation, connection recovery | Retain behavior | Source-specific flow using shared fields and connection states |
| `LocalSourceConnectionView` | File, folder, and playlist actions | Retain behavior, consolidate tiles | Local-source branch of `SourcePicker` |
| `ConnectingView` | Source-aware transitional state | Consolidate | `ConnectionProgress` shared by connector flows |
| `PreparationProgressView` | Preparation orchestration, rows, recovery, cancel/start | Retain state boundary, redesign presentation | `PreparationStage` app composition |
| `ReadyView` | Streaming playback handoff and first-audio detection | Retain detection, replace presentation | `StreamingHandoff` |
| `PlaybackView` | Render and overlay-layer composition | Retain | `PerformanceView`; consumes `PerformanceChrome` |
| `EndedView` | Session summary and next action | Redesign | `SessionSummary` |
| `SettingsView` | Native settings navigation and durable preferences | Retain | `SettingsView`; native `Form` and `NavigationSplitView` |
| `PermissionOnboardingView` | Screen-audio permission explanation | Retain behavior, redesign copy/presentation | `PermissionExplanation` screen |
| `PhotosensitivityNoticeView` | One-time safety acknowledgement | Retain | `PhotosensitivityNotice` sheet |

### Reusable product components

| Current component | Evidence and use | Decision | Uzume component |
|---|---|---|---|
| `ConnectorTileView` | Four constructions; enabled, disabled, and recovery action states | Consolidate with `LocalSourceActionTile` | `SourceChoice` with navigation/action affordance and disabled recovery |
| `LocalSourceActionTile` | Three constructions in one source screen; deliberately parallels connector tile | Consolidate | `SourceChoice` action variant |
| `TrackPreparationRow` | Stable per-track status, progress, ETA, and accessibility contract | Retain and restyle | `PreparationTrackRow` |
| `TrackPreparationStatusIcon` | Central mapping from preparation state to symbol/progress | Retain | `PreparationStatusIndicator` |
| `TopBannerView` | Non-blocking preparation degradation | Consolidate visual primitive, retain placement semantics | `NoticeBanner` |
| `LocalFileErrorBanner` | Shared by two screens; inline, auto-clearing local-file errors | Consolidate visual primitive | `InlineNotice` |
| `ToastView` + `ToastContainerView` | Playback-only ephemeral notification queue with action and dismissal | Retain, restyle | `PerformanceToast` + `ToastRegion` |
| `FullScreenErrorView` | Generic blocking recovery layout but currently unused | Consolidate | Base for `RecoveryScreen` |
| `PreparationFailureView` | Active duplicate of full-screen recovery layout with preparation actions | Consolidate into `RecoveryScreen` | `RecoveryScreen` with context-specific actions |
| `AudioStallOverlayView` | Total loss-of-function recovery during playback | Retain responsibility, rewrite public copy | `AudioRecoveryOverlay` |
| `OverlayBackdropStyle` | Shared contrast treatment for UI over arbitrary visuals | Retain contract, replace decorative material where necessary | `PerformanceBackdrop` modifier |
| `TrackInfoCardView` | Stable current-track, artwork, preset, and mode composition | Redesign content policy | `TrackInformation` |
| `PlaybackControlsCluster` | Settings, session end, and progress composition | Retain responsibility | `PerformanceControls` |
| `SessionProgressDotsView` | Planned, reactive, and large-session variants | Retain only if future-track count does not weaken mystery | `SessionPosition` |
| `ListeningBadgeView` | Sustained-silence state during playback | Retain | `ListeningStatus` |
| `LocalFileTransportBar` | Source-conditional transport with tested callbacks | Retain behavior, retokenize | `LocalPlaybackTransport` |
| `ShortcutHelpOverlayView` | Keyboard-command reference | Retain | `ShortcutReference` |
| `PresetCategoryBlocklistPicker` | Existing include/exclude preference control | Redesign and expand | `PresetEligibilityPicker` |
| `QualityGradeIndicator` | Repeated diagnostic quality representation | Keep diagnostic-only | `DiagnosticQualityIndicator`, outside product chrome |
| `DashboardCardView` + `DashboardRowView` | Developer telemetry composition using existing `DashboardTokens` | Keep separate | Developer instrumentation system, not consumer UI |

### Replace or remove

| Current component | Why it does not carry forward unchanged | Decision |
|---|---|---|
| `PlanPreviewView` | Reveals the planned track/preset sequence and supports regeneration, conflicting with the agreed surprise model | Remove from the normal Uzume flow |
| `PlanPreviewRowView` | Exposes per-track preset assignment and dormant manual-swap plumbing | Remove with plan preview |
| `PlanPreviewTransitionView` | Exposes future transition choreography | Remove with plan preview |
| `TrackChangeAnimationView` | The current literal information animation should be evaluated against the quieter track-information policy | Replace unless validated in the redesigned performance scene |
| `ReadyBackgroundPresetView` | Placeholder gradient rather than a real product state | Replace with `StreamingHandoff` performed-light treatment |
| `ReadyPulsingBorder` | Attention device tied to the discarded ready presentation | Fold into the handoff’s state language or remove |

### Missing responsibilities

These are justified additions because no existing component owns the responsibility.

| Missing responsibility | Component | Reason |
|---|---|---|
| Pre-session summary of audio, output, repertoire, and accessibility | `PerformancePreflight` | Settings exist, but there is no concise session boundary before music is added |
| Shared source-choice visual and behavioral contract | `SourceChoice` | Two near-duplicate tile implementations currently encode the same family separately |
| Shared status semantics across inline, banner, toast, and blocking placements | `StatusTone` + placement components | Existing status surfaces repeat severity mapping and presentation decisions |
| Viewer/curator output separation | `PerformanceOutputRole` layout contract | Current `PlaybackView` assumes one combined output surface |

## State ownership rules to preserve

- `ContentView` owns routing; design-system views must not introduce a second session state machine.
- Views that own asynchronous work keep their view models in `@StateObject` for the view lifetime. The connector wrapper pattern exists specifically to prevent OAuth and Apple Music tasks from being orphaned during parent re-evaluation.
- Application-wide stores such as `SettingsStore` remain injected environment objects. A design-system component must not construct a parallel store.
- Publisher adapters belong at the application composition boundary. Presentational components receive stable display models or bindings rather than the engine.
- Source capability remains explicit. Local playback owns transport; streaming handoff listens for external audio and must not promise transport control.
- Reduced motion is a behavior input, not a purely visual theme toggle.

## Token findings

Phosphene already contains `DashboardTokens` with type, spacing, surface, text, brand, and status values. It is consumed by the dashboard, local transport, local-file error banner, and ended state, but most application views still hard-code `Color.black`, `Color.white.opacity(...)`, corner radii, and spacing. Twenty-six view files contain direct color/shape values.

`DashboardTokens` should not be adopted wholesale: it encodes the former purple/coral visual direction and a telemetry-specific type scale. Its useful precedent is architectural—a shared token source already works across renderer and SwiftUI code. During migration, `UzumeTokens` should become the consumer-interface source of truth, while diagnostic-only measurements can retain a separate dense scale.

## Migration order

1. Introduce `UzumeTokens` and `PerformanceBackdrop` without changing behavior.
2. Consolidate `ConnectorTileView` and `LocalSourceActionTile` into `SourceChoice`; migrate both consumers.
3. Consolidate `FullScreenErrorView` and `PreparationFailureView`; introduce shared status semantics while keeping banner, inline, toast, and blocking placements distinct.
4. Rebuild `PreparationProgressView` in place from `PreparationTrackRow`, `PreparationStatusIndicator`, `NoticeBanner`, and the performed-light background.
5. Rebuild `ReadyView` in place as `StreamingHandoff`; remove plan-preview entry points from the normal flow.
6. Retokenize the existing playback chrome composition. Do not replace it with a parallel `CuratorControlSurface` tree.
7. Add `PerformancePreflight` only after its integration point and settings summary model are defined in the application.

No Phosphene source files were changed by this audit.
