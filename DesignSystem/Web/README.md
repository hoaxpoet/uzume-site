# Uzume Web Components

Import the semantic tokens first, followed by the component stylesheet:

```html
<link rel="stylesheet" href="/tokens.css">
<link rel="stylesheet" href="/DesignSystem/Web/uzume-components.css">
<script type="module" src="/DesignSystem/Web/uzume-components.js"></script>
```

The library is framework-neutral and uses semantic HTML rather than custom elements. Astro or server-rendered templates can emit the documented class structure without requiring a component runtime. JavaScript is limited to the Button busy-state helper until real media behavior is integrated.

Components follow the operating-system appearance through `prefers-color-scheme`. Apply `data-theme="light"` or `data-theme="dark"` to a root or component subtree for an explicit scope. Status components consume separate foreground, background, and border tokens for every tone; do not substitute the raw brand spectrum.

Implemented components, each with named consumers in the launch website plan:

- `uz-button`: primary, secondary, and quiet landing, download, and contributor actions at one 44 px-minimum size
- `uz-icon-button`: one 44 × 44 px play, pause, and mute presentation for hero and gallery media
- `uz-link`: default and quiet navigation, documentation, credit, and supporting-link treatments
- `uz-banner`: beta availability plus permission and installation guidance
- `uz-definition-list`: requirements and factual metadata
- `uz-media-frame`: image, video, or explicit-fallback hero and prepared-performance evidence
- `uz-preset-card`: certified preset gallery and landing teaser with identity preserved when media is unavailable

Documented composition patterns—not component APIs:

- `uz-site-navigation`: global site-header composition
- `uz-download-decision`: Definition List, Link, and Button in one decision region
- `uz-trust-explanation`: content structure for sensitive dependencies
- `uz-contributor-invitation`: subordinate website conversion section
- `uz-preset-gallery`: certified preset collection and landing teaser

Disabled controls keep at least 4.5:1 text contrast in both appearances even though WCAG exempts inactive controls. A nearby reason remains required.

Open `index.html` for the system inventory. Detailed reference material is separated by layer:

- `foundations/`
- `components/`
- `patterns/`
- `native/controls/`
- `native/components/`
- `native/screens/`
