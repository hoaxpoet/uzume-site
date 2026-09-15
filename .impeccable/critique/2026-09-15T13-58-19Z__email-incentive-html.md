---
target: the Kit confirmation email
total_score: 19
max_score: 40
na_heuristics: 
p0_count: 2
p1_count: 4
timestamp: 2026-09-15T13-58-19Z
slug: email-incentive-html
---
Method: dual-agent (A: design review · B: detector + rendered evidence)

Target: `email/incentive.html` — Kit double opt-in confirmation email (HTML-block fragment). Mode: Persuade.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | States the outcome, never states where the reader is: no "step 2 of 2", no mention of uzume.io, nothing about what follows the click. |
| 2 | Match System / Real World | 3 | Plain, concrete language throughout. Docked for the subject line's system vocabulary ("subscription") over the reader's ("the Uzume beta"). |
| 3 | User Control and Freedom | 2 | "Ignore this and you'll hear nothing" is real control. But "Unsubscribe any time." was dropped, and there is no path to fix a mistyped address. |
| 4 | Consistency and Standards | 1 | Three visual identities stacked (card / violet pill / Kit chrome). Button label contradicts the file's own comment and `--color-on-accent`. Detector confirms off-scale radius and type; 28px/36px spacing is off the 4pt rhythm. |
| 5 | Error Prevention | 3 | "nothing happens without the button below" is a mechanical guarantee, not a reassurance. Docked because it is the last line of the third paragraph. |
| 6 | Recognition Rather Than Recall | 1 | Recognition rides entirely on two images. With images blocked, the product name renders at a measured 1.07:1 — invisible. Sender says "plaitandpattern". |
| 7 | Flexibility and Efficiency | 1 | No plain-text confirm URL, no "if the button doesn't work" fallback, no echo of the address they typed. One brittle route. |
| 8 | Aesthetic and Minimalist Design | 3 | Genuinely restrained; colour-token fidelity is exact; measure ~57 chars. Docked because two of three paragraphs are marketing placed between the instruction and the action. |
| 9 | Error Recovery | 2 | Wrong-recipient handled well. Expired link, failed click, "I clicked and nothing happened" have no path. |
| 10 | Help and Documentation | 1 | No link to uzume.io, no repo link, no reply-to invitation. A cautious reader's only route is the button they distrust. |
| **Total** | | **19/40** | **Needs significant work** |

No heuristic scored n/a. #7 and #10 were considered for exemption and kept: a transactional email's accelerator is the plain-text URL and its recovery path is the expired-link route. Both are standard, both absent.

## Design Specificity Verdict

**The copy is unmistakably Uzume. The design is a competent generic dark confirmation email wearing Uzume's colours.**

Swap the two PNGs and six hex values and nothing in the composition, type, or rhythm resists the transplant. What is authentically Uzume: the `#0b0c10` ground (exact `--uzume-midnight-950`), the ivory ramp at 17.96:1 and 11.65:1, and paragraph 1 — 37 words that carry two levels of BRAND.md's hierarchy, translate the deterministic planner into plain language, and claim no AI. No template produces that sentence.

What is generic: the centred-icon → wordmark → one-liner → rule → body layout is the Postmark/Stripe/Mailchimp default. The type surrenders rather than adapts — 20px headline over 16px body is a **1.25x scale ratio, the flattest available**, with no weight, tracking, or case contrast standing in for the unloadable Alumni Sans. And **no spectrum colour appears in the card at all**. Violet, cyan, gold, ember live only inside the 88px icon — the element most likely to be blocked. BRAND.md: *"darkness is the condition, the opening is the event, colour is the consequence."* The card has the condition and no event.

The email never performs its own thesis. The one bright element available is the violet button, and it has been placed outside the dark.

**Deterministic scan:** `detect.mjs` exit 2, 6 findings on the target. Two real — `border-radius:20px` on the icon (line 49, off DESIGN.md's 6/12/16/999 scale, and 4px from the card's own 16px) and `font-size:20px` (line 69, absent from the ramp: 16 / 18 / 22). Four false positives, all the same rule: `Helvetica` as the 4th fallback in the system stack, which mail clients require and DESIGN.md cannot govern. `NotifyForm.astro` and `index.astro` both scan clean — the email is the only file in the chain that hand-copies values instead of consuming tokens.

Drift the detector missed, measured by hand: colours are **exact, zero drift**, but `28px`/`36px` padding is off the 4pt scale (six sites) and `line-height:1.6` misses `--leading-body: 1.55`.

**Rendered evidence:** harness reproducing Kit's shell, served over HTTP, captured at 1280 and 375, with and without images.

## Overall Impression

The email-HTML craft is real and the copy is the best listener-facing writing in the repo. Two things undo it. First, the single element the email exists to get clicked is outside the composition, on the lightest ground available to it, at 3.88:1, at the end of a message whose opening instruction points at it from 250px away. Second, the file's own comment claims *"read this with images off and it still makes sense"* — and the rendered proof says otherwise.

The biggest opportunity is also the cheapest: BRAND.md already prescribes the fix. Put the light in the gap between the shadows.

## What's Working

1. **The dark card inside a light host is the right structural idea, competently built.** `bgcolor` plus inline `background-color`, `role="presentation"` on all three tables (verified, none missing), `border-collapse:collapse`, zero `<head>` dependency, every rule inline. Colour fidelity is exact against `tokens.css`. It does the hard thing rather than surrendering to Kit's defaults.

2. **Paragraph 1 is unforgeable.** Two levels of message hierarchy in 37 words, the planner translated without jargon or AI implication, the brand's own verb earned. Warm, unhurried, specific.

3. **"Didn't sign up? Ignore this — nothing happens without the button below."** This improves on the approved copy: it converts passive reassurance into a mechanical guarantee about what inaction does. Right sentence, wrong position.

Honourable mention: the authoring comment (lines 1–22) is exemplary — it is the reason these failures are diagnosable at all. It is also the document whose instruction was not followed.

## Priority Issues

### [P0] The site tells the subscriber they are done, seconds before this email asks them to finish
`NotifyForm.astro:88` answers success with *"You're on the list. We'll write when there's a build to download."* With double opt-in on, that is false — they are pending. `WEBSITE_ROADMAP.md:141` recorded this as a ship-together constraint and it has not been done.

**Why it matters:** it removes the reader's reason to go find the email at all, and every unconfirmed address is a person who wanted the app and won't get the launch mail. This is the flow defect, not a design defect, and it gates turning `consent.enabled` on.

**Fix:** success copy becomes "Check your email — there's a link to confirm." Ship it in the same change as the Kit setting. Suggested: `/impeccable clarify`

### [P0] The sender and subject are not Uzume
From: `"matt@plaitandpattern"`. Subject: `"Important: confirm your subscription"` — Kit's stock default. Approved was *"Confirm your email for the Uzume beta."*

**Why it matters:** the card's whole achievement is recognition, and recognition is spent before the email is opened. "Important:" is a textbook phishing opener carrying no product name. This is the highest-leverage change in the review and it is not in the HTML file — it is two fields in Kit. Ideally a `uzume.io` sending domain with SPF/DKIM.

**Fix:** From name contains "Uzume"; subject set to the approved line. Suggested: `/impeccable clarify`

### [P1] The CTA is outside the card, and it is the least-emphasised element in an email that exists to get it clicked
Emphasis runs 88px icon > 160px wordmark > 20px headline > 16px body > **small violet pill**. The pill sits on Kit's `#EFEFEF` at **3.38:1**, sharing a background with the unsubscribe link and the PMB address — grouped with the chrome, not the message. This is also a **structural drift**: `WEBSITE_ROADMAP.md:119–133` placed the button directly beneath its own instruction, before the three paragraphs.

**Why it matters:** it causes four of six cognitive-load failures at once (single focus, grouping, hierarchy, working memory). It strands "Click below" ~250px from its referent across a container boundary, where in a standard preview pane the two are never co-visible. And it leaves the card ending on a body paragraph with no terminal element — a dark slab whose last line asserts a button it does not contain.

**Fix:** split at the divider — HTML block (icon, wordmark, headline) → **Kit Button block** → HTML block (paragraphs, close). Take the visible seam: a violet button in a light gap between two fields of midnight *is* BRAND.md's First Opening. Set the button to full width, not "Fit content". Suggested: `/impeccable layout`

### [P1] With images blocked, the card has no visible brand at all
Measured: the `<td>` at line 55 and the `<img>` at line 56 declare **no `color`**, so `alt="Uzume"` inherits black and renders at **1.07:1** on `#0b0c10`. The `alt=""` icon does not collapse — fixed width/height reserve the full 88x88 box and paint a broken-image glyph. Every other text cell in the file (69, 100, 110, 120) sets `color`; these two do not.

Confirmed visually in the images-off screenshot: roughly 380px of empty card, a smudge where the name should be, and **"Click" as the first legible word in the email.** Combined with P0 that is a complete phishing profile.

**Why it matters:** it directly falsifies the file's stated contract at lines 14–17. There is no `<h1>`–`<h6>` anywhere in the fragment, so the image alt is the only title the email has — semantically absent from the rotor and visually invisible when blocked.

**Fix:** inline `color:#f4f6f1` plus the system font stack, `font-size:34px`, `font-weight:700`, `line-height:81px` **on the `<img>`** (webmail reads it) **and repeat `color:#f4f6f1` on the parent `<td>`** (Outlook reads it). Same defensive colour on the icon cell. Ten minutes. Suggested: `/impeccable harden`

### [P1] The button label fails AA, and the correct value was already written down
Live config is `#FFFFFF` on `#7F6AFF` = **3.88:1**. A 16px medium button label is not large text, so 4.5:1 applies. `tokens.css:55` declares `--color-on-accent: var(--uzume-midnight-950)`; the file's own comment at line 21 instructs `#0b0c10`, which measures **5.03:1 and passes**.

**Why it matters:** the one interactive element in the email is the one that fails, DESIGN.md names AA a commitment, and the instruction lives in an HTML comment Kit never renders — so nothing enforces it and no repo gate catches it.

**Fix:** one field in Kit — text colour `#0b0c10`. Suggested: `/impeccable audit`

### [P1] In Outlook the card has nothing holding its width
`max-width:520px` is absent from Word's supported CSS, and `grep` confirms **no `<!--[if mso]>` conditional, no `width="520"` attribute, no `mso-` property anywhere**. Only `width="100%"` survives.

**Why it matters:** in a maximised Outlook reading pane the card runs 800–1000px with 32px padding — roughly **140–180 characters per line**. The file's comment claims Outlook-awareness while relying on a property Word ignores, unmitigated. `border-radius` goes too, so the card is a hard-cornered slab there.

**Fix:** MSO-conditional ghost table at `width="520"`, or `width="520" align="center"` with `max-width` as the responsive escape. Also swap the `height="1"` divider for `border-top:1px solid #34363f` — Word honours `border` but floors the cell height on the `font-size:0` trick. Suggested: `/impeccable harden`

### [P2] Copy drift from the approved draft, one piece consent-bearing
**"Unsubscribe any time." was dropped** from paragraph 2. `NotifyForm.astro:38–41` ends its terms on exactly that sentence, and the roadmap states the email's copy *"must keep the same scope as the form, or the two promises drift apart."* Kit's footer satisfies the law; the symmetry the roadmap demanded is what breaks. Also: button label reads "Confirm your email" against approved "Confirm my email". Restore the first; either restore or record the second.

## Persona Red Flags

**The suspicious recipient who doesn't remember signing up.** Sender `matt@plaitandpattern` has no relationship to uzume.io or the word Uzume — the strongest legitimacy signal in email points somewhere else. "Important:" is the phishing opener. Images off gives them a black rectangle with an invisible name whose first legible word is "Click". The reassurance they need is the *third paragraph*, ~400px down, behind two paragraphs of marketing. And **the email contains zero links** — their natural move is "let me check the site myself," and there is no way to do that except by clicking the thing they are afraid of.

**The listener who signed up four seconds ago and wants this over with.** The button is not visible without scrolling past ~500px of card. "Click below" cannot be obeyed when it is read. Three paragraphs re-explain what they read 30 seconds ago on the landing page. The card's bottom edge with no button reads as broken for a beat. And nothing confirms the address they typed — the one personalisation Kit merges for free.

**The privacy-conscious Mac user weighing whether to let this near their audio.** BRAND.md message 3 — trustworthiness — is **entirely absent**. No "runs locally", no "no account", no "sends no audio anywhere", though all three exist as approved copy in `index.astro:97–114`. "Listens to whatever music you're already playing" with no local-first sentence beside it invites exactly the wrong inference from the verb "listens". And "free, open source, MIT" — the most persuasive PRODUCT.md-safe sentence available — appears nowhere.

## Minor Observations

- **Mobile: the side gutter is exactly 0px, both sides.** `max-width:520px;width:100%` with no self-supplied padding resolves to the full 375px viewport. The 16px radius still computes, so the corners become notches with page ground bleeding through triangular slivers. Depends on whether Kit's wrapper cell supplies padding — unverified, and not something this repo controls.
- **The masthead is top-heavy.** ~225px of the card's 649px passes before the first word. The wordmark PNG carries asymmetric baked padding — 55px above the ink, 16px below (352x178 canvas, 333x107 ink) — so the rendered gap above is more than twice the gap below, and BRAND.md clear space is violated on all four sides.
- **Kit's editor preview shows square corners; the browser measures `16px` and renders them.** The two assessments disagree here, and neither explains Kit's preview. Resolve it with a real test send, not a preview.
- **Dark-mode clients have no defence and cannot be given one.** `color-scheme` / `supported-color-schemes` are `<head>`-scoped and Kit owns the head. Apple Mail leaves dark backgrounds alone; Gmail app and Outlook.com may partially invert, lightening the card while leaving declared text colours — near-white on near-white. Aggravated by the wordmark PNG having `#0b0c10` baked in opaquely rather than transparent, so it cannot follow an inversion.
- **The images are live, not broken.** `uzume.io/email/uzume-icon.png` and `uzume-wordmark.png` both return 200 with byte counts matching `public/email/` exactly. `cache-control: max-age=0, must-revalidate` on immutable email art is wasteful but harmless. ~44 KB total, fine for email; the 39.6 KB icon is heavy for 192px but not a problem.
- **The icon PNG's corners are pure `#000000`, opaque** — its silhouette comes entirely from CSS. In Outlook it becomes an 88px hard square, saved only by measuring 1.07:1 against the card.
- **No preheader.** Gmail's snippet defaults to the headline. Given how far the stock subject can be improved, the second inbox-row signal is unclaimed.
- **The `#34363f` hairline at 1.62:1 is correct, not a defect** — decorative, so 1.4.11 does not apply. Noting it so nobody "fixes" it. Ironically it would get *more* visible in the clients where the 1px trick fails.
- **Axis break:** centred (icon, wordmark, headline) → left (body) → centred again outside the card.

## Questions to Consider

1. If the card's job is recognition, why is the largest element the one that disappears when images are blocked, while the sender name — which can never be blocked — says "plaitandpattern"?
2. Is double opt-in the right instrument for a list whose first send may be months away? Every unconfirmed address is someone who wanted this app. Was the deliverability threat quantified, or is this Kit's default?
3. Why does the email spend 84 words re-explaining a product the reader saw 30 seconds ago, and zero words on the thing the landing page couldn't say — that they are one click from the only email that will matter? Kit's post-click confirmation page is stock, untouched, and is where the explanation belongs.
4. "Click below" is a location instruction in a medium where you control neither layout nor client. If the button moved again tomorrow, how many words would break? (Two phrases. Both load-bearing.)
5. The peak is the first 200px and the end is an administrative pill on grey. If peak-end is what's remembered, is the brand investment in the wrong half?

## Untaken Opportunities

Holding PRODUCT.md absolutely — no footage, no downloadable claim, no fabrication.

- **The Button block is doing the least work of any block available.** "Fit content" makes a chip; full width makes a slab. And per BRAND.md buttons name the *reader's* outcome: "Tell me when I can download it" moves the ending from compliance to anticipation.
- **A plain link to uzume.io below the CTA.** Asserts nothing; the landing page makes no downloadable claim. It is the cheapest fix for the suspicious reader, who currently has exactly one way to verify the email. Add the repo link and the privacy-conscious reader is served too.
- **Move "Didn't sign up?" and the restored "Unsubscribe any time." below the button.** One restructure fixes cognitive-load items 5, 7 and 8 at once: small print lands after the decision, and the self-doubt beat stops arriving immediately before the click.
- **One trust sentence.** *"Analysis and rendering run locally. Uzume has no account, sends no audio anywhere."* Already approved, already live on the landing page. Highest-value sentence not present.
- **The Coleridge line as the card's close.** Public domain, asserts nothing, gives the card an end instead of a stop.
- **Use the Image block once, for First Opening — not footage.** The artwork is a real production artifact, not a capture, so it makes no product claim. It would put the spectrum into a composition that currently has none.
- **Leave Video, Spotify, TikTok and X empty, and write down why.** A Spotify embed would be actively misleading: PRODUCT.md is explicit that Uzume controls playback only for local files and *listens* to streaming sources. That reason deserves a line in the roadmap so nobody reaches for the block later.
- **Kit's post-click confirmation page is the real end of this journey and it is stock** — the one surface where the reader has already committed and is maximally receptive.
