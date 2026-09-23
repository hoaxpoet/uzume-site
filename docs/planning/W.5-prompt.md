## Increment W.5 — Docs: the outsider-facing subset

**Type:** content + feature (**site repo**).

**Objective.** After this session `/docs` is a real section rather than a placeholder: a
visitor who has never seen this project can find out what Uzume needs, get it running from
source, understand what it does while it runs, and — if they want — write a scene and
submit it. Curated for the web, not mirrored from the repo. Every product claim traces to
the app repo, and every page says which upstream doc it was drawn from.

**What exists now.** `src/content/docs/docs/index.md` is a four-line placeholder that says
documentation "arrives in a later increment". The Starlight integration is configured in
`astro.config.mjs`: title "Uzume", `disable404Route: true`, `customCss` of
`src/styles/fonts.css` and `src/styles/docs.css`, a GitHub social link, and two component
overrides (`DocsThemeProvider`, `DocsThemeSelect`) that pin `/docs` to dark and remove the
theme picker. The sidebar has exactly one entry: `{ label: "Docs", items: [{ label:
"Overview", slug: "docs" }] }`. Built routes today are `/`, `/gallery/`, `/docs/`,
`/design/`, `/confirmed/`. There is no `/download` and no `/credits`; plan §3 lists both,
and neither is this session's job.

**One fact that shapes the whole session.** W.5a rewrote the landing page and changed the
vocabulary: the visitor-facing noun is now **scene**, not "preset". Verified on the current
build — `dist/gallery/index.html` has eight visible "scene" and zero "preset"; `dist/index.html`
has zero visible "preset" (its 44 raw matches are all CSS class names like
`uz-preset-card`). "Certified" appears nowhere on either page, and no page states a count.
But the app repo has not followed: `README.md` §Contributing presets, `CONTRIBUTING.md`,
every sidecar filename, the `presets` content collection, `Scripts/generate_presets.py` and
the JSON keys all say **preset**. The Contributing page is where those two vocabularies
collide, and a reader who follows it will be reading app-repo files within one click. This
is DECISION-NEEDED 2; do not improvise it.

## Skill invocations

None. This repo carries none of the app repo's skills. Closeout is inline, below.

## Read first, in order

1. `docs/planning/WEBSITE_ROADMAP.md` — §3 **W.5a** (the homepage rewrite: its decisions
   bind this session's copy) and §3 **W.5 — Docs** (the scope this prompt executes).
2. `docs/planning/WEBSITE_PLAN.md` §3, the **Docs (`/docs`)** paragraph. It is the
   governing spec: curated not mirrored, three page groups, frontmatter naming the upstream
   repo doc, CI link-checking those references, manual curation first.
3. `CLAUDE.md` — source-of-truth boundary, copy law, tokens-first, the checks list.
4. `PRODUCT.md` — copy law in full. The beta is **future tense**. "Open source and
   buildable" and "available to install" are different claims and only the first is true
   today. Flash safety is "steady luminance", never a flashes-per-second figure.
5. `astro.config.mjs` (the `starlight({...})` block), `src/styles/docs.css`,
   `src/components/DocsThemeProvider.astro`, `src/components/DocsThemeSelect.astro`.
6. `.github/workflows/site.yml` — the existing `lychee` step, including why `uzume.io` and
   `/dist/gallery#` are excluded. DECISION-NEEDED 4 builds on it.
7. App repo, read-only, at `~/Documents/Projects/uzume`:
   `README.md` (§Requirements, §Getting started, §Running it, §Contributing presets,
   §Documentation map), `CONTRIBUTING.md`, `docs/PRODUCT_SPEC.md`, `docs/ARCHITECTURE.md`,
   `docs/GLOSSARY.md`, `docs/Preset_Development_Protocol.md`,
   `docs/PRESET_SESSION_CHECKLIST.md`, `docs/PUBLISHING.md`, `docs/CREDITS.md`.

## Pre-flight invariants — stop if any fails

1. Clean working tree, branched from an up-to-date `main` containing W.5k (`b93a7e4`).
2. `npm ci` has been run in this worktree *and* in the main checkout (CLAUDE.md's
   `tsconfig` note). `npx astro check` and `npm run build` pass **before any edit**.
3. The app repo is readable locally. It is a **source to verify against, never a build
   dependency** — the site must build with it absent.
4. `https://github.com/hoaxpoet/uzume` returns 200. The upstream-reference scheme in Task 5
   depends on the app repo being publicly reachable; it was when this prompt was written.
5. Re-run the vocabulary check before writing copy, because it is the thing most likely to
   have moved since:
   `npm run build && grep -oi 'preset\|certified' dist/gallery/index.html | sort | uniq -c`
   Expect zero. If "preset" or "certified" is back in visible copy, stop and ask.

## Tasks

**1. Branch.** `git checkout -b w5-docs`.

**2. Record the decisions.** All four are answered below (Matt, 2026-09-23) — every one on
its default. This task records them in the session log; it does not ask again. If anything
in the repo contradicts an answer, stop and raise it rather than reinterpreting.

*Done-when:* all four recorded in the session log.

**3. Verify every product fact first, then write.** Build a claims table before drafting:
each factual assertion a page will make, and the app-repo file and line it comes from.
Requirements, the build steps, what the Screen Recording permission is actually for, what
works with local files versus a streaming source, what a scene consists of on disk, and
what happens to a submission. **Anything you cannot source, do not write.** If a claim
matters and the app repo does not support it, list it in closeout as a gap rather than
filling it in.

*Done-when:* the table exists in the session log and every later page cites it.

**4. Write the pages.** Per plan §3, three groups. **This session writes Getting Started
and Using Uzume** (decision 3); Contributing is described below because its shape governs
what the first two must set up, but it is the next session's to write.

- **Getting Started** — requirements; building from source (the only install story today,
  written in the future tense for the beta per PRODUCT.md); the Screen Recording permission
  explainer, saying plainly what it is for and that local files need no permission at all;
  local files versus streaming.
- **Using Uzume** — what the app does while it runs, in a listener's terms. The
  troubleshooting the plan calls for, including the silent-tap gotcha, if the app repo
  documents it well enough to state.
- **Contributing** *(next session)* — what a scene is as two files, the hot-reload loop if it exists
  upstream, a first walkthrough, what the gates check and what happens after a merge. The
  gallery is the payoff: a merged scene ends up on `/gallery` with its author's name on it,
  which is already true and already visible.

Write outsider-first prose. No increment IDs, no `D-###`, no "M7", no internal shorthand —
that is exactly what makes the repo docs unsuitable to mirror. American spelling (W.5a).

*Done-when:* each page builds, reads as written for someone who has never seen the project,
and contains no claim absent from the Task 3 table.

**5. Upstream references, and make CI check them.** Every page carries frontmatter naming
its upstream app-repo doc. Note the wiring problem: frontmatter is not emitted into the
built HTML, and the existing `lychee` step scans `dist/**/*.html`, so a bare frontmatter
field is checked by nothing. Resolve per DECISION-NEEDED 4 — the default renders the
reference visibly on the page as a link to the app repo on GitHub, which both credits the
source and puts a real href in front of `lychee`.

*Done-when:* `lychee` passes and would fail if an upstream path were renamed. Prove the
second half by temporarily breaking one reference and showing CI red, then reverting.

**6. Sidebar and navigation.** Replace the single-entry sidebar with the real structure.
Keep `/docs` pinned dark and the theme picker absent — that is a deliberate W.5-era
decision recorded in those two component overrides, not an accident. GitHub stays out of
the top nav (W.5a) but belongs on the Contributing page, where scene-writers are.

*Done-when:* every page is reachable from the sidebar, and the landing nav is unchanged.

**7. Verify rendered, on the preview URL.** Not in diff form (CLAUDE.md working
conventions). Check at phone width; check `prefers-reduced-motion`; run the contrast gate;
confirm Starlight's own components inherit `tokens.css` rather than shipping their own
palette.

**8. Record the decisions.** Per CLAUDE.md, decisions land in
`docs/planning/WEBSITE_ROADMAP.md` — a W.5 entry in the style of W.5a: what was decided,
by whom, and what was cut with reasons.

## Do NOT

- **Do not mirror the repo docs.** Curated subset, rewritten for outsiders. If a page is
  turning into a copy of an upstream file, the page is wrong.
- **Do not assert a product fact the app repo does not support**, however obvious it seems.
  This is the one rule in CLAUDE.md with its own table in `README.md`.
- **Do not write the beta in the present tense**, and do not imply the app is installable.
  There is no signed artifact; `/download` and the CTA flip are W.7 and blocked app-side.
- **Do not state a flashes-per-second figure.** "Steady luminance" is the phrasing.
- **Do not reintroduce "certified", jargon, or any count of scenes** — W.5a removed all
  three deliberately, and a count is wrong within the month.
- **Do not add client-side JS.** Zero by default; components earn it.
- **Do not fork `tokens.css`** or hardcode a color or a type size to make a docs page look
  right. Starlight themes through custom properties; that is why `/docs` inherits the
  identity for free.
- **Do not edit the app repo.** Read-only, always.
- **Do not build `/download` or `/credits`.** Plan §3 lists them; they are not W.5.
- **Do not touch the held captures.** Nacre and Dragon Bloom are held in
  `docs/captures/W3a-capture-log.json` for stated reasons; Dragon Bloom's is a flash-safety
  block, not an encoding one.

## Verification commands — all must pass before closeout

```bash
node --check DesignSystem/Web/catalogue.js
node --check DesignSystem/Web/uzume-components.js
python3 Scripts/check_web_catalogue.py
python3 Scripts/check_contrast.py tokens.css
python3 Scripts/check_copy_spacing.py
python3 Scripts/generate_presets.py --check
npx astro check
npm run build
```

Then, on the built output:

```bash
# No forbidden vocabulary reached the built docs.
grep -roi 'certified\|flashes per second' dist/docs/ | sort | uniq -c
# Every docs page carries a visible upstream reference (per DECISION-NEEDED 4).
grep -rlo 'github.com/hoaxpoet/uzume' dist/docs/*/index.html | wc -l
```

`lychee` runs in CI on the PR and must be green.

## Commits

`[W.5] site: <description>`, small and per logical step — one per page group reads well
here. **Push only on Matt's explicit "yes, push."**

## Closeout (inline — this repo has no closeout skill)

1. Files changed.
2. Verification output, verbatim.
3. The preview URL, and what Matt should read on it first.
4. The claims table from Task 3, and **every gap** — each fact a page wanted to state that
   the app repo could not support. This list is the session's most useful output after the
   pages themselves.
5. Proof the upstream-reference check actually fails when a reference breaks.
6. Contrast and reduced-motion results, with numbers.
7. The four decisions, as answered.
8. **Handoff:** what the second docs session inherits, and anything W.6 (launch polish)
   or W.7 (download flip) now depends on.

## DECISION-NEEDED (answered in advance — Matt, 2026-09-23)

**All four went to their defaults. Task 2 records them rather than asking again.**

- **1 → A.** Keep **W.5** for docs, as the roadmap has it. The homepage rewrite keeps its
  `W.5a`–`W.5k` labels; note the collision in closeout so the log stays readable later.
- **2 → A.** **"Scene" throughout**, naming the repo's term once, early, in plain words:
  the code and the repo call these presets, and you will see that word in filenames and
  JSON keys. One voice across the site; the reader is told before it bites them.
- **3 → A.** **Getting Started + Using Uzume this session; Contributing next.** The
  listener path ships whole.
- **4 → A.** **Render the upstream reference visibly** on each page as a link to the file
  on `github.com/hoaxpoet/uzume`. No CI change; readers get a citation; a renamed upstream
  file turns CI red.

The options each decision was chosen from are kept below, because the reasoning is the part
worth re-reading if one of them starts to hurt.

**1. What is this increment called?** The roadmap says "W.5 — Docs", but `W.5a` through
`W.5k` are already spent on the homepage rewrite, so "W.5" now reads as that work in the
commit log.

- **A — Keep W.5 for docs, as the roadmap has it.** The homepage work becomes the odd one
  out, and `git log --oneline --grep '\[W\.5'` returns two unrelated bodies of work.
- **B — Relabel this W.8** and leave the homepage in sole possession of W.5. Cleanest to
  read later; costs an edit to the roadmap's §3 and §4 ordering.
- **C — `W.5-docs` as the commit prefix**, keeping the roadmap heading. Unambiguous in the
  log, mildly ugly.

*Default if unanswered:* **A**, because the roadmap is the governing document and this
prompt is filed as `W.5-prompt.md`. Flag the collision in closeout either way.

**2. What does the Contributing page call the thing?** The site says *scene*; the app repo,
`CONTRIBUTING.md`, every filename and every JSON key say *preset*. A reader following this
page is in app-repo files within a click.

- **A — "Scene" throughout, naming the repo's term once.** One sentence early: the code and
  the repo call these presets, and you will see that word in filenames and JSON. Keeps the
  site in one voice and tells the reader the truth before it bites them.
- **B — "Scene" on Getting Started and Using, "preset" on Contributing.** Contributing is a
  technical page about files that are literally named `presets/`; matching the repo reduces
  friction for the person actually doing the work.
- **C — Wait for the app repo to rename.** Correct end state, but it is app-side work that
  is not scheduled, and W.5 would block on it indefinitely.

*Default if unanswered:* **A**. W.5a chose the vocabulary deliberately and splitting it by
page rebuilds the "split vocabulary between listeners and contributors" that W.5a rejected.

**3. How do the two sessions split?** The roadmap budgets about two.

- **A — Getting Started + Using Uzume first; Contributing second.** Ships the listener path
  whole; Contributing is the longest page and the one most exposed to decision 2.
- **B — Getting Started + Contributing first; Using second.** Serves the two audiences the
  landing page actually sends here, and Using is the page most dependent on app-repo
  troubleshooting detail that may not exist yet.
- **C — All three, thin, in one session**, deepened in the second.

*Default if unanswered:* **A**.

**4. How do upstream references get checked?** Frontmatter alone is checked by nothing —
`lychee` scans `dist/**/*.html` and frontmatter never reaches it.

- **A — Render the reference visibly** on each page as a link to the file on
  `github.com/hoaxpoet/uzume`. `lychee` checks it with no CI change; readers get a source
  citation; a renamed upstream file turns CI red. Costs a visible line per page.
- **B — Keep it in frontmatter and add a second `lychee` pass** over
  `src/content/docs/**/*.md`, resolving the field to a URL. Invisible to readers, more CI
  machinery, and the reference stops being a reader-facing credit.
- **C — Frontmatter only, unchecked.** What the plan's wording literally describes, minus
  the checking it promises. Drift is the documented risk in §6.

*Default if unanswered:* **A**. It is the only option that satisfies both halves of the
plan's sentence — the page names its upstream doc *and* CI catches drift — and it needs no
new CI configuration.
