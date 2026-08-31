# UzumeDesignSystem

SwiftUI migration prototypes and tokens for the Uzume macOS application. This package is not yet a drop-in replacement for the Uzume app’s existing view tree. Integration must follow the source mapping in `../COMPONENTS.md` and `../../docs/design/PHOSPHENE-COMPONENT-CENSUS.md`, preserving current state ownership and behavior while the presentation is refactored in place.

The package deliberately keeps controls native. Uzume violet adapts between `#6753D7` in light appearance and `#7F6AFF` in dark appearance; system yellow, red, green, and blue retain their conventional adaptive meanings. Warning symbols use a black detail on the yellow field so the symbol remains legible in light appearance. The full violet/cyan/gold/ember spectrum is reserved for performed-light surfaces such as `PreparationStage`.

Current prototype status:

- `PreparationStage` is the visual target for the existing `PreparationProgressView`; it does not replace that view’s track rows, recovery, progressive-readiness, or publisher wiring.
- `StreamingHandoff` is the presentation target for `ReadyView`; the existing first-audio detector and source-aware state remain authoritative.
- `PerformancePreflight` is genuinely new and requires an application integration point plus a summary model backed by current Settings.
- `UzumeSystemNotice` is a shared semantic primitive for consolidating existing banner, inline, toast, and blocking recovery treatments without making those placements behaviorally identical.
- `CuratorControlSurface` is an early sketch and is not the target architecture. Uzume should retokenize and reorganize the existing `PlaybackChromeView` composition instead.
