# Uzume Design System Catalogue Audit

Date: 2026-08-17
Scope: `DesignSystem/Web/` inventory and all seven routed catalogue pages

## Audit health score

| Dimension | Score | Key finding |
| --- | ---: | --- |
| Accessibility | 4/4 | Shared navigation, controls, states, focus, names, and live feedback now satisfy the catalogue contract. |
| Performance | 3/4 | Runtime code is small and stable; the 2.8 MB PT Sans TTC and 1.1 MB identity raster remain heavier than necessary. |
| Responsive design | 4/4 | Mobile comparison records preserve row subjects and cell labels without horizontal scrolling; navigation retains route and system-layer context. |
| Theming | 4/4 | System, dark, and light appearances are globally inspectable; the fixed-dark top bar remains legible in every mode. |
| Implementation integrity | 4/4 | Seven routes, seven documented web components, and implementation-backed contracts remain coherent and product-specific. |
| **Total** | **19/20** | **Excellent — only asset-transfer optimization remains.** |

## Implementation integrity verdict

**Pass.** The catalogue expresses Uzume’s actual website and macOS layers, uses the First Opening identity without presenting it as performance footage, and keeps component claims tied to implementation and named consumers. The detector reports one advisory for em-dash saturation in `components/index.html`; verification shows this is a false positive caused by CSS custom-property names such as `--color-accent` inside code specimens.

## Corrected in this increment

- Hidden mobile navigation is now removed from keyboard and accessibility traversal with `inert`, `aria-hidden`, and a tabindex fallback.
- Navigation opens with focus inside, closes with Escape, restores focus to the menu button, and exposes an updated accessible name and expanded state.
- Escape clears an active component filter before it closes mobile navigation.
- Filtering reports exact result counts through a polite live region and has an explicit accessible input name.
- The catalogue now provides a persistent global Appearance control for system, dark, and light inspection.
- The fixed-dark top bar owns stable local tokens, preventing light-theme contrast failures.
- Catalogue links and controls meet the 44 px minimum target and retain visible focus.
- Mutually exclusive specimen controls expose a named group role and pressed state.
- Unavailable destinations render as styled plain text rather than disabled or placeholder links.
- Copy controls announce success and failure and include a fallback for file-based catalogue viewing.
- Every rendered button declares its type; every route retains one `h1`, named landmarks, and valid internal navigation.
- Mobile tables now recompose into single-axis labelled records while retaining table, row, and header semantics in the DOM.
- Mobile navigation now identifies the current route, exposes every system layer, adds a dismissible scrim, and responds safely when the viewport changes.
- Catalogue layouts account for mobile safe-area insets and remain free of page, table, and top-bar overflow from 320 px upward.

## Remaining findings

### [P2] Font and identity specimens are heavier than necessary

- **Location:** `brand/fonts/PTSans.ttc` (2.8 MB), `brand/icon/Uzume-1024.png` (1.1 MB)
- **Category:** Performance
- **Impact:** First visits transfer more data than the documentation interface requires, especially when media specimens enter the viewport.
- **Recommendation:** Subset and convert web fonts to WOFF2, and add appropriately sized responsive derivatives for catalogue specimens.
- **Suggested command:** `$impeccable optimize`

## Positive findings

- All tested semantic text and status pairings exceed 4.5:1 in dark and light appearances; disabled text measures 5.85:1 dark and 4.87:1 light.
- No route produced console warnings or errors.
- All seven routes rendered at 390 px without page-level horizontal overflow.
- All seven comparison tables render as labelled records at 700 px and below with complete column and row header relationships.
- Status communication consistently combines text, conventional color, and iconography.
- Reduced-motion rules preserve state changes while removing nonessential movement.

## Recommended actions

1. **[P2] `$impeccable optimize`:** Reduce the font and identity-specimen transfer weight.
2. **[P3] `$impeccable polish`:** Run the final catalogue coherence pass after the remaining planned increments.
