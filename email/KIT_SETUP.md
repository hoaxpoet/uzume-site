# Kit setup — the confirmation (double opt-in) email

Every setting here lives in Kit's dashboard, not in this repo. It is written
down because nothing in CI can reach it: the previous configuration shipped a
call-to-action below WCAG AA and a stock subject line, and the correct values
existed only in an HTML comment that Kit never renders.

Form: **9918547** (the id is public — it ships in the page HTML either way).

## Block order — this is not optional

The card is deliberately split so the confirm button sits *inside* it. Kit's
block list for this email must read, top to bottom:

| # | Block | Content |
|---|-------|---------|
| 1 | HTML | `email/incentive-top.html` |
| 2 | **Button** | the confirm button — settings below |
| 3 | HTML | `email/incentive-bottom.html` |

The button carries Kit's own confirmation URL, so it cannot be written into the
HTML: a hand-authored merge tag would be a link that silently goes nowhere.
Placing it between the halves is the design — the light gap it opens between two
fields of midnight is `BRAND.md`'s First Opening, and it puts the one action
this email exists for on the card's own dark ground rather than on Kit's light
one, where it measured 3.38:1 against the background.

If the blocks are ever reordered, the design breaks but the copy still reads:
no sentence in either fragment refers to the button's position.

## Button block settings

| Field | Value | Why |
|-------|-------|-----|
| URL | `{{ confirm_url }}` | Kit's own merge tag |
| Background colour | `#7f6aff` | `--color-accent` |
| **Text colour** | **`#0b0c10`** | `--color-on-accent`. **Not `#FFFFFF`** — white on this violet measures **3.88:1** and fails WCAG AA for normal text. `#0b0c10` measures **5.03:1** and passes. |
| Label | `Tell me when I can download it` | `BRAND.md`: buttons name the reader's outcome, not the sender's. "Confirm your email" names ours. |
| Size | Large | Medium risks falling under the 44px minimum target `DESIGN.md` requires |
| Width | **Full width** | "Fit content" renders a chip; the CTA should read as a slab spanning the card |
| Rounded corners | Large | matches the card's 16px |
| Alignment | Centre | |
| Margin | None | the two HTML blocks supply their own padding; extra margin widens the seam |

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
- [ ] **The seam.** Confirm the two dark halves meet the button cleanly and that
      Kit adds no unexpected gap or background between blocks.
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
