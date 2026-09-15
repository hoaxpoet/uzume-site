# Kit setup — the confirmation (double opt-in) email

Every setting here lives in Kit's dashboard, not in this repo. It is written
down because nothing in CI can reach it: an earlier configuration shipped a
call-to-action below WCAG AA and Kit's stock subject line, and the correct
values existed only in an HTML comment Kit never renders.

Form: **9921149** (the id is public — it ships in the page HTML either way).

## Why this email is light

Kit owns `<body>`, the email background, and a footer carrying the unsubscribe
link, the postal address and the "Built with Kit" badge. On the free plan none
of it can be removed or restyled.

That is not worth fighting, for three reasons:

1. **The unsubscribe link and the postal address are legally required** under
   [CAN-SPAM](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business),
   whatever service sends the mail. They are not going away by switching
   providers or by self-hosting. Only the "Built with Kit" line is optional.
2. **Every free tier brands its footer.** MailerLite, Buttondown and Resend all
   put their own badge on free-plan mail and charge roughly $9–20/month to
   remove it. Switching trades one badge for another.
3. **The jank was never the footer.** It was a dark `#0b0c10` card dropped onto
   Kit's light ground — a black slab on a white page, with a seam everywhere the
   two met. Any footer under that would have looked pasted on.

So the email shares Kit's ground instead of opposing it. This is the brand's
other half, not a retreat from it: `tokens.css` ships a complete light theme,
and `BRAND.md` names **"midnight on ivory"** an approved inverse of the
wordmark. The one dark element is the app icon, which is supposed to read as an
app icon.

The fragments declare **no background colour at all**. Kit's exact ground is not
ours to know, so nothing assumes one — the wordmark PNG is transparent, the icon
is masked to its squircle, and every colour declared is ink on whatever Kit
supplies. There is no edge for the footer to clash with.

Measured against Kit's ground: body ink `#4f525a` **6.80:1**, small print
`#64676f` **4.92:1**, lede `#111217` **16.27:1**, button `#6753d7` **4.81:1**.

## Blocks — three, in this order

| # | Block | Content |
|---|-------|---------|
| 1 | HTML | `email/incentive-top.html` |
| 2 | **Confirmation button** | Kit's own — settings below |
| 3 | HTML | `email/incentive-bottom.html` |

**Kit requires its own confirmation button** and refuses to publish without one
("A confirmation button is required on this email"). Use the **Add confirmation
button** action in that warning banner — do not hand-write an `<a>` with a merge
tag and expect it to count. An earlier revision tried exactly that and Kit
rejected it.

Because the whole email is light, the button sitting on Kit's ground between the
two HTML blocks is simply a button in a message. Nothing shows through its
corners, which is what went wrong when the same arrangement was tried against a
dark card.

### Button settings

| Field | Value | Why |
|-------|-------|-----|
| Background colour | `#6753d7` | `--color-accent`, light theme. **Not** `#7f6aff`, which is the dark-theme accent and too pale on a light ground. |
| Text colour | `#ffffff` | `--color-on-accent`, light theme. Measures **5.53:1** and passes AA. |
| Label | `Confirm my email` | the approved wording in `WEBSITE_ROADMAP.md` W.2 |
| Size | Large | keeps the target above the 44px minimum `DESIGN.md` requires |
| Rounded corners | Small | matches the 8px the fragments assume |
| Alignment | Centre | |

## Brand settings (Settings → Brand)

Kit's brand panel feeds its own surfaces — broadcasts, sequences, landing pages,
forms, the unsubscribe page — and its swatches are a quick-pick palette, not a
theme. Changing them does not restyle anything already built, and it does not
touch the HTML blocks, which carry their own inline values.

**One thing here does reach this email: the email-safe font sets the confirmation
button's label and the footer.** Those are Kit's blocks, not ours.

### Business Name

`Uzume` — already correct. Worth noting it is not cosmetic: Kit puts it on the
public unsubscribe page, which is a trust surface for someone who has just
decided they do not trust you.

### Colours

The slot already holding `#7F6AFF` is the **dark-theme** accent. It is the wrong
primary for anything on a light ground — this email included — so add the light
accent and keep both, labelled by where they belong.

| Hex | Token | Use |
|-----|-------|-----|
| `#6753D7` | `--color-accent` (light) | **primary CTA on light surfaces** — this email's button, Kit landing-page buttons |
| `#5946C2` | `--color-accent-hover` (light) | link and button hover on Kit pages |
| `#7F6AFF` | `--color-accent` (dark) | accent on midnight surfaces only *(already set)* |
| `#0B0C10` | Midnight | the stage; dark grounds and display type |
| `#F4F6F1` | Ivory | the paired light of the identity pair |
| `#111217` | `--uzume-ink-900` | headings and lede on light |
| `#4F525A` | `--uzume-ink-700` | body copy on light |
| `#64676F` | `--uzume-ink-600` | small print on light |
| `#C9C9C5` | `--color-line` (light) | rules and dividers on light |
| `#F7F7F5` | `--uzume-paper-100` | light page ground |

That is ten of the twelve slots. **Leave the last two empty rather than filling
them with cyan `#37D6C0`, gold `#F5C84C` and ember `#FF6B4A`.** Those are real
identity colours, but `BRAND.md` scopes them as "the light brought through the
opening" and `DESIGN.md` explicitly forbids using all identity colours as
decorative controls. A quick-pick palette is precisely the mechanism that turns
them into decorative controls — they belong in rendered output, not in a button
picker.

### Fonts

**Email-safe → add `Arial`.** Kit renders the confirmation button's label and
the footer in this face, so it is the one font choice that shows up in this
email. The HTML fragments now declare `Arial, Helvetica, sans-serif` to match;
they previously led with a system stack (SF on macOS, Segoe UI on Windows),
which would have set the body in one face and Kit's button in another on the
same screen. If Kit offers `Helvetica` as a separate entry, either is fine —
they resolve to each other on almost every client.

Neither brand face is available here and neither can be: Alumni Sans and PT Sans
are webfonts, and mail clients do not load webfonts. That is not a loss worth
fighting — the brand is carried by the wordmark image, the copy, and the colour,
not by the body face.

**Web fonts → add `PT Sans`, and nothing else.** Webfonts do work on Kit's
web-based pages (the unsubscribe page, the update-profile page, any hosted form),
and PT Sans is in Kit's picker.

**Alumni Sans is not in Kit's list (checked 2026-09-15), and it does not need to
be.** `BRAND.md` assigns PT Sans "body copy, navigation, labels, forms, help, and
documentation" and scopes Alumni Sans to "page-level statements, campaign
headlines, and short editorial moments". Every Kit-hosted surface here is the
former: functional pages a subscriber passes through. The campaign surfaces are
uzume.io, which serves the real font itself. So PT Sans alone is the correct
assignment, not a fallback.

**Do not substitute a lookalike** — Oswald, Archivo Narrow, Barlow Condensed or
any other condensed grotesque. `BRAND.md`: *"do not typeset a substitute
lockup."* The first Kit heading that renders the word "Uzume" in a near-miss face
is a typeset substitute lockup on a public page, and it reads as a slightly wrong
Uzume rather than an honest one. Plain PT Sans is the better failure mode. Where
a page genuinely needs the identity, use the wordmark image.

**Custom fonts → skip.** Paid-plan only, and there is nothing to upload: the
Google-hosted versions of both faces cover every Kit surface that can use them.

### Favicon

Paid-plan only. When that changes, `brand/favicon/favicon-512.png` is the asset
to upload — it is the art-directed crop, already square and production-ready.
Note the upsell also bundles removing Kit branding from subscriber-facing pages,
which is the same paid tier that would remove "Built with Kit" from the email
footer.

### Links

Add `https://uzume.io` and the repository, `https://github.com/hoaxpoet/uzume`.
These appear in Kit's recommendations profile and on subscriber-facing pages,
and they are the two places a suspicious recipient would go to check that this
is real. Nothing else exists yet — no social accounts — so add nothing else.

## Subject, sender, reply-to

| Field | Value |
|-------|-------|
| Subject | `Confirm your email for the Uzume beta` |
| From name | `Uzume` |
| From address | `hello@uzume.io` once the domain is authenticated — see below |
| Reply-to | `hello@uzume.io` (routable immediately, see below) |

**Do not leave Kit's stock subject, `Important: confirm your subscription`.** It
names no product, and "Important:" is a textbook phishing opener. The recipient
typed their address on uzume.io seconds earlier; nothing in a stock subject
connects the two, and an unopened confirmation is someone who wanted the app and
will never get the launch mail.

The **From name is a plain text field on any plan** and is the single
highest-leverage fix here. Set it to `Uzume` today, even before the address
moves off `matt@plaitandpattern`.

## Email addresses on uzume.io

Two different problems. Cloudflare solves only the first.

**Receiving — Cloudflare Email Routing, free.** Dashboard → `uzume.io` → Email
Routing. Create `hello@uzume.io` and forward it to an existing mailbox.
Cloudflare writes the MX and SPF records itself. This is **inbound only** — it
can forward mail, it cannot send it. It is enough to make `hello@uzume.io` a
working reply-to straight away.

**Sending — Kit, authenticated against the domain.** For Kit to send *as*
`uzume.io` it must be authorised to. Kit's email-authentication / sending-domain
setting issues DKIM records (usually plus a CNAME or two) which get pasted into
Cloudflare DNS. Cloudflare is only the DNS host in that exchange; it is not
sending anything. **Check whether custom sending-domain authentication is
included on the current Kit plan before planning around it** — if it is not, the
From name fix above still stands on its own.

Until the domain is authenticated, do not spoof `From: hello@uzume.io` — an
unauthenticated From on a domain that publishes SPF is a deliverability problem,
not a branding win.

## Before turning double opt-in on — now a merge blocker

**`consent.enabled` is `false` on form 9921149**, verified against the live
endpoint on 2026-09-15. That makes the ordering constraint sharper than it was:

The form's success message used to read *"You're on the list"*, which stops being
true the moment double opt-in is enabled. `NotifyForm.astro` now answers
*"Almost — check your email and confirm."* — which is **false while consent is
off**, because Kit sends no confirmation and no email ever arrives.

The copy was wrong in one direction before and is wrong in the other direction
now. So this is no longer a follow-up: **turn double opt-in on before this branch
merges**, or the deployed site tells people to check an inbox nothing was sent
to. Confirm it flipped by re-running the probe below; `consent.enabled` must read
`true`.

```bash
curl -s -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
  --data '{"email_address":""}' https://app.kit.com/forms/9921149/subscriptions
```

An empty address subscribes no one — Kit rejects it on validation — but the
response still reports the form's own `consent` state. A form that does not exist
answers `"consent":null` with "Couldn't find a form for this request", so the
same probe also distinguishes a live form from a deleted one.

### The original constraint

`consent.enabled` and the site copy must ship together. The form's success
message used to read *"You're on the list"*, which stops being true the moment
double opt-in is enabled — the subscriber is pending, and a page that says they
are finished removes their reason to go and find the email.
`NotifyForm.astro` now answers *"Almost — check your email and confirm."*
That change is on this same branch. Do not enable one without the other.

## The email depends on a deploy — build it in this order

The fragments reference `https://uzume.io/email/...` for both images, so **the
confirmation email cannot be finished before this branch is on `main` and
deployed.** Until then Kit renders a broken-image box and falls back to the
wordmark's alt text. That happened once already, on 2026-09-15, when
`uzume-wordmark-ink.png` existed only on the branch.

This is the ordering, and the two steps in the middle should be minutes apart:

1. **Merge and deploy.** Both assets go live; the wordmark resolves.
2. **Turn double opt-in on** in Kit, immediately.
3. **Re-run the probe** and confirm `consent.enabled` is `true`.
4. **Finish the confirmation email** and send the test.

Between 1 and 2 the site says "check your email" while Kit sends nothing. That
window is unavoidable — the site copy and the Kit toggle cannot change in the
same commit — so keep it short and do not start it unattended.

**Before touching the email in Kit, confirm the assets are actually live:**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://uzume.io/email/uzume-wordmark-ink.png
curl -s -o /dev/null -w "%{http_code}\n" https://uzume.io/email/uzume-icon.png
```

Both must be `200`. If either 404s, the deploy has not landed and the email will
render broken no matter how it is configured.

Renaming or re-deriving an email asset re-opens this every time: the old name
keeps serving, the new one 404s until deploy, and Kit shows the failure rather
than the design. Change the file in place where possible.

## Test send — what a preview cannot tell you

Kit's editor preview is not a rendering engine. Send a real test to at least
Gmail web, the Gmail Android or iOS app, Apple Mail in dark mode, and Outlook
for Windows, and check:

- [ ] **The button actually confirms.** Click it from a real test subscriber and
      verify the subscription moves from pending to confirmed. Nothing else in
      this list matters if that fails.
- [ ] **Images off.** The wordmark's alt text must read as dark ink, legible.
      Both the `<img>` and its `<td>` declare the colour, because webmail reads
      one and Outlook reads the other.
- [ ] **The icon in Outlook.** Word drops `border-radius`, so the icon becomes a
      hard black square on a light ground. This is the one place the design
      visibly degrades and the reason the icon is only 72px. If it looks bad
      enough to matter, the fix is a pre-masked PNG with transparency, which
      means deriving a new asset from `brand/icon/Uzume-1024.png`.
- [ ] **Outlook width.** The MSO ghost table should hold the column at 520px.
      Word ignores `max-width`.
- [ ] **Dark mode.** Gmail's apps and Outlook.com may apply their own colour
      transforms. The fragments cannot declare `color-scheme` — that is a
      `<head>` mechanism and Kit owns the head — so this is a risk to observe,
      not one fixable from here. A light email inverted to dark is a much softer
      failure than the dark card was, but check that the transparent wordmark
      does not end up dark-on-dark.
- [ ] **The seams.** Confirm Kit adds no unexpected background or rule between
      the three blocks.

## Blocks to leave empty, and why

Kit offers Video, Spotify, TikTok and X embeds. None belong in this email:

- **Video** needs footage that does not exist yet (W.3), and `PRODUCT.md`
  forbids fabricating it.
- **Spotify would be actively misleading.** `PRODUCT.md` is explicit that Uzume
  controls playback only for local files and *listens* to streaming sources. A
  Spotify block in a Uzume email implies a playback integration the product does
  not have.
- **TikTok / X** have no account to embed and no content to show.
