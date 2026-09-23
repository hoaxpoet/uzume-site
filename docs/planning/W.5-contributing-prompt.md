## Increment W.5, session 2 — Docs: Contributing

**Type:** content (**site repo**).

**Objective.** After this session `/docs` carries the third page the plan asks for, and
the contributor path is whole: someone who can write a fragment shader can find out what a
scene is on disk, get one rendering on their own machine, understand what the project's
gates will check, and know what happens between opening a pull request and seeing their
name on `/gallery`. Curated for the web, not mirrored. Every fact traces to the app repo.

**What exists now.** Session 1 landed as `5ba6574` (PR #62). `/docs` has three pages —
`index.md` (overview, routing, and the one-sentence scene/preset disclosure),
`getting-started.md` (seven question-shaped headings carrying `FAQPage` JSON-LD through
Starlight's frontmatter `head`), and `using-uzume.md`. Each ends in a visible **Drawn
from** line of links to the app repo, which is what `lychee` checks (decision 4 →
A). `src/styles/docs.css` now carries the reduced-motion guard `Base.astro` never passes
to a Starlight layout. The sidebar has one group, three entries. `/docs` is indexed and
stays that way.

**The decisions session 1 already made, which this session inherits rather than reopens.**
"Scene" throughout, with the repo's word named once early (decision 2 → A) — it is
disclosed on the overview and again inside the answer to "how do I write a scene?", which
is exactly where this page picks the reader up. `[W.5]` stays the commit prefix. American
spelling. GitHub stays out of the top nav and belongs on this page, where scene-writers
are (W.5a).

**One fact that shapes the whole session.** The lifecycle a submitted scene goes through
is called **certification** upstream — `certified: false` is how you ship, a maintainer
runs a live review with real music, and on sign-off the flag flips and the scene joins the
rotation the planner draws from. W.5a removed the word "certified" from this site
deliberately: it is the project's internal badge and means nothing to a listener. The
mechanism is fully sourced (`CONTRIBUTING.md` §Gates, §Certification lifecycle;
`docs/GLOSSARY.md`); the vocabulary for it is not. This is DECISION-NEEDED 1 and it
governs roughly a third of the page. Do not improvise it.

**A disagreement resolved before this prompt was written — do not re-derive it.** Session
1 flagged that `docs/UX_SPEC.md` §4.4 ("URL-paste only, no OAuth, public playlists only in
v1") and `docs/RUNBOOK.md` §U.11 (Authorization Code + PKCE, refresh token in the
Keychain) describe different Spotify connectors. The implementation settles it: the app
wires `SpotifyOAuthPlaylistConnector` around `SpotifyWebAPIConnector(tokenProvider: oauth)`
in `UzumeApp/Views/ConnectorPickerView.swift:235`, `SpotifyOAuthTokenProvider.swift`
implements PKCE with scopes `playlist-read-private playlist-read-collaborative`, and
`SpotifyConnectionViewModel.swift` opens with "Increment U.11: OAuth Authorization Code +
PKCE replaces client-credentials." **RUNBOOK is current; UX_SPEC §4.4 is stale**, and
private and collaborative playlists do work, contrary to what §4.4 says. Two consequences,
both in the tasks below: this page may rely on the RUNBOOK account, and Getting Started's
Spotify sentence gains the login step it was missing. Filing the stale section upstream is
app-side work and is **not** this session's (see Do NOT).

## Skill invocations

None. This repo carries none of the app repo's skills. Closeout is inline, below.

## Read first, in order

1. `docs/planning/WEBSITE_ROADMAP.md` — §3 **W.5 — Docs, first session**. Its claims table
   is the source list this session extends, and its gap list is what it is expected to
   close or restate.
2. `docs/planning/WEBSITE_PLAN.md` §3, the **Docs (`/docs`)** paragraph — the governing
   spec, and the sentence naming what the Contributing page owes.
3. `docs/planning/W.5-prompt.md` — session 1's prompt, for the standard this one inherits
   (claims-table-before-drafting, visible upstream references, verification shape).
4. `CLAUDE.md` and `PRODUCT.md` — the source-of-truth boundary and copy law in full.
5. The three live pages: `src/content/docs/docs/index.md`, `getting-started.md`,
   `using-uzume.md`. Read them for voice and for the **Drawn from** shape; the new page
   must be indistinguishable in both.
6. `.github/workflows/site.yml` — the `lychee` step the upstream references ride on.
7. App repo, read-only, at `~/Documents/Projects/uzume`: `CONTRIBUTING.md` (the spine of
   this page), `docs/presets/YOUR_FIRST_PRESET.md`, `docs/presets/NEW_PRESET_CHECKLIST.md`,
   `docs/PRESET_SESSION_CHECKLIST.md`, `docs/SHADER_CRAFT.md` §17 (the sidecar schema),
   `docs/CREDITS.md` (the Milkdrop posture), `docs/GLOSSARY.md`.

## Pre-flight invariants — stop if any fails

1. Clean working tree, branched from an up-to-date `main` containing `5ba6574`.
2. `npm ci` has been run in this worktree *and* in the main checkout (CLAUDE.md's
   `tsconfig` note). `npx astro check` and `npm run build` pass **before any edit**.
3. The app repo is readable locally, and is a **source to verify against, never a build
   dependency** — the site must build with it absent.
4. The built docs are still clean and still carry exactly one FAQ:
   ```bash
   npm run build
   grep -roi 'certified\|flashes per second' dist/docs/ | sort | uniq -c   # expect nothing
   ```
   plus the `FAQPage` script from session 1's verification block — **exactly one block,
   seven entries**. If a second `FAQPage` has appeared, stop and ask.
5. `python3 Scripts/generate_presets.py --check` is **red before you start**, on four
   sidecars, for a reason unrelated to docs: W.5a's American-spelling pass means
   regenerating re-imports "colour" from the app repo. Confirm it is the same four files
   and leave them alone. If it is a different set, stop and report — something else moved.

## Tasks

**1. Branch.** `git checkout -b w5-contributing`.

**2. Answer DECISION-NEEDED 1 before writing a word of the lifecycle section**, and record
all three decisions in the roadmap entry. If Matt has not answered, take the defaults
below and say so in closeout.

*Done-when:* all three recorded.

**3. Verify every fact first, then write.** Extend session 1's claims table: each new
assertion, and the app-repo file and line it comes from. What a scene is on disk; where
the two files go for hot reload and in-repo; what the hot-reload loop actually does on a
broken save; what each gate checks; what a submission needs to carry; what the maintainer
step is; the Milkdrop posture. **Anything you cannot source, do not write** — list it in
closeout as a gap instead.

*Done-when:* the extended table is in the roadmap entry and every claim on the page has a
row.

**4. Write the page.** `src/content/docs/docs/contributing.md`. Outsider-first prose, no
increment IDs, no `D-###`, no "M7", no internal shorthand. The shape the plan asks for:

- **What a scene is** — two files, a shader and a JSON file beside it, discovered
  automatically. The vocabulary disclosure already exists twice; do not make a third
  meal of it, but this is the page where the reader will actually meet `presets/` in a
  path, so one clause acknowledging that is right.
- **Getting one rendering** — the hot-reload directory and the in-repo path; what happens
  on a save that does not compile; that none of this needs an account, a streaming
  service, or the Screen Recording permission.
- **The one design rule**, per DECISION-NEEDED 2 — the thing the app repo calls the most
  important rule it learned empirically: drive from continuous energy rather than raw beat
  detections. In plain words, not the primitives' names.
- **What the gates check** — in the reader's terms: that every audio route the scene
  declares is exercised by real music; that it clears the project's visual floor; the
  photosensitivity gate (**"steady luminance"**, never a flashes-per-second figure); lint
  and the test suite.
- **What happens after you open the pull request** — per decision 1. Do not promise a
  turnaround time; no upstream doc states one.
- **The payoff** — a merged scene joins what every listener sees and keeps its author's
  name, and `/gallery` is where it shows up. Link it.
- **Porting a Milkdrop idea** — welcome, authored from scratch on Uzume's own primitives,
  attribution in the sidecar and in the credits file, and **never commit a `.milk` file**.
- **Where to ask** — GitHub issues, and the app repo link that belongs on this page rather
  than in the nav.

Close with the **Drawn from** line, in the established shape.

*Done-when:* the page builds, reads as written for someone who has never seen this project,
and contains no claim absent from the table.

**5. Getting Started's Spotify sentence gains the login step.** It currently says a
Spotify session needs a client ID of your own registered against the copy you built, which
is true and incomplete: there is also a one-time browser login, and private and
collaborative playlists are in scope. One sentence, sourced to the RUNBOOK and the
implementation named above. Do not touch the seven questions, their order, or the JSON-LD
— and if the sentence you add changes an answer's text, the `FAQPage` `acceptedAnswer`
must change with it, verbatim.

*Done-when:* the FAQ still parses, still holds seven entries, and every `acceptedAnswer`
still appears verbatim in the rendered prose.

**6. Sidebar.** Add the page as the fourth entry. `/docs` stays pinned dark with no theme
picker; the landing nav is unchanged; GitHub stays out of it.

*Done-when:* every page is reachable from the sidebar and `/` is untouched.

**7. Verify rendered, on the preview URL** — not in diff form. Phone width,
`prefers-reduced-motion`, the contrast gate, and that Starlight still inherits `tokens.css`
rather than shipping its own palette.

**8. Record the decisions** in `docs/planning/WEBSITE_ROADMAP.md`, as a **W.5, session 2**
entry in the style of the first — what was decided, by whom, what was cut and why, the
extended claims table, and the gaps.

## Do NOT

- **Do not mirror `CONTRIBUTING.md`.** If the page is turning into a rewrite of it with the
  same headings in the same order, the page is wrong. Upstream stays canonical and is one
  click away.
- **Do not assert a product fact the app repo does not support**, however obvious.
- **Do not use "certified"** unless DECISION-NEEDED 1 comes back as B, and do not
  reintroduce jargon or any count of scenes.
- **Do not state a flashes-per-second figure.** "Steady luminance" is the phrasing; the
  sentence already exists on `/gallery` and on Getting Started.
- **Do not add a second `FAQPage` block.** The verification asserts exactly one across
  `dist/docs/**`, and a question-shaped Contributing page was considered and rejected — the
  FAQ lives on Getting Started (W.5 decision, W.6 handoff).
- **Do not promise a review turnaround**, a release date, or that a submitted scene will be
  accepted.
- **Do not write the beta in the present tense** or imply the app is installable. `/download`
  and the CTA flip are W.7 and blocked app-side.
- **Do not add client-side JS**, fork `tokens.css`, or hardcode a color or type size.
- **Do not edit the app repo.** Read-only, always — including the stale `UX_SPEC.md` §4.4
  identified above. Recording it for Matt to file app-side is the whole of this session's
  responsibility for it.
- **Do not build `/download` or `/credits`**, and do not touch the held captures in
  `docs/captures/W3a-capture-log.json`.

## Verification commands — all must pass before closeout

```bash
node --check DesignSystem/Web/catalogue.js
node --check DesignSystem/Web/uzume-components.js
python3 Scripts/check_web_catalogue.py
python3 Scripts/check_contrast.py tokens.css
python3 Scripts/check_copy_spacing.py
npx astro check
npm run build
```

`python3 Scripts/generate_presets.py --check` stays red on the same four sidecars, for the
spelling reason recorded in W.5 session 1. It runs in neither workflow. Confirm the file
set is unchanged; do not "fix" it here.

Then, on the built output:

```bash
# No forbidden vocabulary reached the built docs.
grep -roi 'certified\|flashes per second' dist/docs/ | sort | uniq -c
# All three sub-pages carry a visible upstream reference (decision 4 → A). Expect 3.
grep -rlo 'github.com/hoaxpoet/uzume' dist/docs/*/index.html | wc -l
# Still exactly one FAQ, still seven questions, still no raw '<'.
python3 - <<'EOF'
import json, re, pathlib
hits = [m for f in pathlib.Path("dist/docs").rglob("index.html")
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                            f.read_text(), re.S)]
faq = [h for h in hits if json.loads(h).get("@type") == "FAQPage"]
assert len(faq) == 1, f"expected one FAQPage, found {len(faq)}"
assert "<" not in faq[0], "raw '<' leaked into the script element"
d = json.loads(faq[0])
assert len(d["mainEntity"]) == 7, len(d["mainEntity"])
body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "",
      pathlib.Path("dist/docs/getting-started/index.html").read_text()))
import html
body = html.unescape(body)
for q in d["mainEntity"]:
    a = re.sub(r"\s+", " ", q["acceptedAnswer"]["text"])
    assert a in body, q["name"]
print("FAQ intact: 7 answers, all verbatim in the prose")
EOF
```

`lychee` runs in CI on the PR and must be green.

## Commits

`[W.5] site: <description>`, small and per logical step — the page, the Getting Started
sentence, and the roadmap entry are three. **Push only on Matt's explicit "yes, push."**

## Closeout (inline — this repo has no closeout skill)

1. Files changed.
2. Verification output, verbatim.
3. The preview URL, and what Matt should read on it first.
4. The extended claims table, and **every gap** — each fact the page wanted to state that
   the app repo could not support.
5. Contrast and reduced-motion results, with numbers.
6. The three decisions, as answered.
7. Confirmation that the FAQ is untouched: one block, seven entries, every answer still
   verbatim in the prose.
8. **For Matt to file app-side:** `docs/UX_SPEC.md` §4.4 is stale — it describes a
   client-credentials, public-playlists-only Spotify connector that U.11 replaced with
   OAuth PKCE. Restate it in closeout so it does not get lost with this session.
9. **Handoff:** what W.6 (launch polish) and W.7 (download flip) now depend on, and
   whether `/docs` should stay indexed (it should, unless something on this page argues
   otherwise).

## DECISION-NEEDED

**1. What does the site call the step between a merged scene and a scene listeners
actually see?** Upstream calls it certification: a maintainer plays the scene against real
music, and on sign-off it joins the rotation the planner draws from. W.5a deleted
"certified" from the site as an internal badge that means nothing to a listener.

- **A — Name no badge; describe the step.** "A maintainer plays it against real music. If
  it holds up, it joins the rotation every listener sees." The reader learns the truth and
  the site keeps one vocabulary.
- **B — Use "certified" on this page only**, because a contributor will meet
  `certified: false` in the sidecar within minutes and a site that hides the word makes
  them decode it alone.
- **C — Coin a site word** ("accepted", "in rotation") and use it everywhere, including a
  future gallery caption.

*Recommendation and default:* **A**, with the literal `certified: false` line shown once as
what you type in the file rather than as a status the site names. It keeps W.5a's decision
intact and still puts the word in front of the reader at the moment they need it.

**2. How much of the craft does this page carry?** The app repo has a long authoring
discipline and a quality bar behind it.

- **A — None.** Link the two upstream documents and let them do it.
- **B — One rule, in plain words** — drive the visuals from the music's continuous energy
  rather than from raw beat detections — plus the links. It is the single rule upstream
  says it learned the hard way, and a page that omits it sends people into the mistake it
  exists to prevent.
- **C — A full quickstart**, restating the sidecar schema and the authoring checklist.

*Recommendation and default:* **B**. **C** becomes a second copy of a document that changes
app-side, which is the drift the boundary exists to prevent.

**3. Does the page show code?**

- **A — No code**, prose and links only.
- **B — The file shape only** — the two filenames side by side, and the directory a
  hot-reloaded pair goes in. No shader source.
- **C — The whole working pair inline**, as the upstream first-preset walkthrough has it.

*Recommendation and default:* **B**. It answers "what am I actually making" in four lines
and cannot go stale the way a copied shader would; **C** is a sixty-line file that the app
repo gate-verifies to compile and this repo could not.
