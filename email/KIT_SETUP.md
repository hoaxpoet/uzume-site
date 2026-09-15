# Kit setup — the confirmation (double opt-in) email

Every setting here lives in Kit's dashboard, not in this repo. It is written
down because nothing in CI can reach it: the previous configuration shipped a
call-to-action below WCAG AA and a stock subject line, and the correct values
existed only in an HTML comment that Kit never renders.

Form: **9918547** (the id is public — it ships in the page HTML either way).

## Blocks — one, and only one

Paste `email/incentive.html` into a **single HTML block**. Add nothing else: no
Button block, no Divider, no text blocks.

**The confirm button is inside the HTML.** `{{ confirm_url }}` is the same merge
tag Kit's own Button block uses — it is visible in that block's URL field — so an
`<a href="{{ confirm_url }}">` resolves to exactly the same link with none of the
constraints. That is what lets the button sit on the card's own dark ground.

An earlier version used Kit's Button block below the card. Two things were wrong
with it, and both are visible rather than theoretical: the violet dropped to
**3.38:1** against Kit's light background, and the button's rounded corners cut
four pale wedges out of the design where the light ground showed through. A
button inside the card rounds against midnight instead, and reads as part of the
message rather than part of Kit's footer chrome.

The label is **"Confirm my email"** — the approved wording in
`WEBSITE_ROADMAP.md` W.2. The button's `#0b0c10` on `#7f6aff` measures **5.03:1**
and passes AA; white on that violet is **3.88:1** and fails. Do not "fix" it to
white.

## Subject, sender, reply-to

| Field | Value |
|-------|-------|
| Subject | `Confirm your email for the Uzume beta` |
| From name | `Uzume` |
| From address | `hello@uzume.io` once the domain is authenticated — see below |
| Reply-to | `hello@uzume.io` (routable immediately, see below) |

Kit's own double opt-in setting is what sends this email; the HTML block lives in
the form's confirmation-email editor, reached from form `9918547`.

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
`uzume.io` it has to be authorised to. Kit's email-authentication / sending-domain
setting issues DKIM records (usually plus a CNAME or two) which get pasted into
Cloudflare DNS. Cloudflare is only the DNS host in that exchange; it is not
sending anything. **Check whether custom sending-domain authentication is
included on the current Kit plan before planning around it** — if it is not, the
From name fix above still stands on its own.

Until the domain is authenticated, do not spoof `From: hello@uzume.io` — an
unauthenticated From on a domain that publishes SPF is a deliverability problem,
not a branding win.

## Before turning double opt-in on

`consent.enabled` and the site copy must ship together. The form's success
message used to read *"You're on the list"*, which stops being true the moment
double opt-in is enabled — the subscriber is pending, and a page that says they
are finished removes their reason to go and find the email.
`NotifyForm.astro` now answers *"Almost — check your email and confirm."*
That change is in this same branch. Do not enable one without the other.

## Test send — what a preview cannot tell you

Kit's editor preview is not a rendering engine. Send a real test to at least
Gmail web, the Gmail Android or iOS app, Apple Mail in dark mode, and Outlook
for Windows, and check:

- [ ] **Images off.** The first legible word must be "Confirm", not "Click", and
      the wordmark's alt text must read as ivory, not black. This was measured at
      1.07:1 before the fix; both `<img>` and its `<td>` now declare the colour
      because webmail reads one and Outlook reads the other.
- [ ] **Outlook width.** The MSO ghost table should hold the card at 520px. Without
      it Word ignores `max-width` and the measure runs past 140 characters.
- [ ] **Outlook corners.** `border-radius` is unsupported in Word's engine, so the
      card will be a hard-cornered slab there. Expected, not a defect.
- [ ] **The button.** Confirm `{{ confirm_url }}` resolved to a real link and that
      clicking it actually confirms the subscriber. This is the one thing that
      must be proven with a live send before the list is trusted.
- [ ] **Button in Outlook.** `border-radius` is unsupported there, so expect a
      square violet block — on the dark card that is fine, and it is why the
      button is not a rounded pill.
- [ ] **Kit's preview showed square corners** while a browser renders the 16px
      radius correctly. Unexplained. Confirm which is true in a real send.
- [ ] **Dark mode.** Gmail's apps and Outlook.com may apply their own colour
      transforms. The fragment cannot declare `color-scheme` — that is a
      `<head>` mechanism and Kit owns the head — so this is a risk to observe,
      not one that can be fixed from here. Watch for the wordmark PNG becoming a
      mismatched rectangle: its `#0b0c10` ground is baked in opaquely and cannot
      follow an inversion.
- [ ] **Mobile gutter.** The fragment supplies no side padding of its own, so at
      375px the card may run edge-to-edge depending on whether Kit's wrapper cell
      pads it. If it does go edge-to-edge, the rounded corners become notches.

## Blocks to leave empty, and why

Kit offers Video, Spotify, TikTok and X embeds. None belong in this email:

- **Video** needs footage that does not exist yet (W.3), and `PRODUCT.md`
  forbids fabricating it.
- **Spotify would be actively misleading.** `PRODUCT.md` is explicit that Uzume
  controls playback only for local files and *listens* to streaming sources. A
  Spotify block in a Uzume email implies a playback integration the product does
  not have.
- **TikTok / X** have no account to embed and no content to show.
