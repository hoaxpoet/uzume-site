# Kit setup — the confirmation (double opt-in) email

Every setting here lives in Kit's dashboard, not in this repo. It is written
down because nothing in CI can reach it: an earlier configuration shipped a
call-to-action below WCAG AA and Kit's stock subject line, and the correct
values existed only in an HTML comment Kit never renders.

Form: **9918547** (the id is public — it ships in the page HTML either way).

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

## Before turning double opt-in on

`consent.enabled` and the site copy must ship together. The form's success
message used to read *"You're on the list"*, which stops being true the moment
double opt-in is enabled — the subscriber is pending, and a page that says they
are finished removes their reason to go and find the email.
`NotifyForm.astro` now answers *"Almost — check your email and confirm."*
That change is on this same branch. Do not enable one without the other.

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
