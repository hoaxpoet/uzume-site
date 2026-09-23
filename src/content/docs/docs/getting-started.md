---
title: Getting started
description: What Uzume needs, how to build and run it from source today, what the Screen Recording permission is for, and the questions people ask before they try it.
head:
  - tag: script
    attrs: { type: application/ld+json }
    content: '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Does it work with Apple Music and Spotify?","acceptedAnswer":{"@type":"Answer","text":"Yes, though not by controlling them. Uzume listens to the audio coming out of your Mac, so anything that plays on it can be accompanied — Apple Music, Spotify, a browser tab. You press play in your own app, and Uzume follows. Capturing that audio needs the macOS Screen Recording permission. Local files are the exception: open one in Uzume and it plays the file itself, with no permission and no account."}},{"@type":"Question","name":"Does it need the Screen Recording permission?","acceptedAnswer":{"@type":"Answer","text":"Only to hear music playing in another app. On macOS, permission to capture system audio is bundled with screen recording permission — Apple groups them together, and Uzume uses only the audio portion. Nothing it hears leaves your Mac. Playing a local file in Uzume needs no permission at all."}},{"@type":"Question","name":"Is it free?","acceptedAnswer":{"@type":"Answer","text":"Yes. The source is public and MIT-licensed, so you can build and run it today at no cost, and the public beta will be free and open source when it arrives."}},{"@type":"Question","name":"Does it run on Intel Macs?","acceptedAnswer":{"@type":"Answer","text":"No. Uzume is Apple silicon only — an M1 Mac or newer. A few features are reserved for M3 and newer."}},{"@type":"Question","name":"Which version of macOS does it need?","acceptedAnswer":{"@type":"Answer","text":"macOS 14 Sonoma or later. Building it yourself also needs Xcode 26.5, the version the repository pins."}},{"@type":"Question","name":"Is it safe to watch if I am sensitive to flashing light?","acceptedAnswer":{"@type":"Answer","text":"Every scene in the gallery is tested for steady luminance: a bounded change in brightness from frame to frame, with beat-locked motion confined to parts of the frame rather than thrown across all of it. The app says the rest plainly before your first session: it renders high-contrast, fast-changing visuals, and if you are sensitive to flashing lights or strobe patterns you should turn on Reduce motion in Settings before you start."}},{"@type":"Question","name":"How do I write a scene?","acceptedAnswer":{"@type":"Answer","text":"A scene is two files — a Metal shader and a JSON file beside it — and the app picks the pair up on its own. The code and the repository call these presets, so that is the word you will meet in filenames and JSON keys; on this site they are scenes. The walkthrough is in the app repository contributing guide today, and a page here comes next."}}]}'
---

There is no build to download yet. Nothing is signed or notarized, so there is
nothing a Mac will install — but the source is public and MIT-licensed, and it
builds and runs on a Mac you already have. That is the install story today, and
the whole of it.

You will need an Apple silicon Mac running macOS 14 Sonoma or later, and
Xcode 26.5, the version the repository pins.

```bash
git clone https://github.com/hoaxpoet/uzume.git
cd uzume

# The audio-analysis model weights are about 167 MB and ship as a release
# asset rather than repository content, so they are fetched separately.
Scripts/fetch_weights.sh

xcodebuild -scheme UzumeApp -destination 'platform=macOS' build
```

Then run it, and open a music file with **File → Open Local File** (⌘O). That
path needs no permission and no account, and it is the quickest way to see
whether any of this is for you. Everything below is the questions people ask
before they get that far.

## Does it work with Apple Music and Spotify?

Yes, though not by controlling them. Uzume listens to the audio coming out of
your Mac, so anything that plays on it can be accompanied — Apple Music,
Spotify, a browser tab. You press play in your own app, and Uzume follows.
Capturing that audio needs the macOS Screen Recording permission. Local files
are the exception: open one in Uzume and it plays the file itself, with no
permission and no account.

Uzume can also be handed the playlist in advance, which is what lets it hear a
track before it plays rather than while it plays. Apple Music playlists are read
from the running app, which macOS will ask you to allow the first time; Spotify playlists are pasted in as a link, and because
there is no signed build yet, a Spotify session needs a Spotify client ID of
your own registered against the copy you built — the repository's runbook covers
that setup.

Local files it plays for you: `.m4a`, `.mp3` and `.flac`, single files, whole
folders, or an M3U playlist.

## Does it need the Screen Recording permission?

Only to hear music playing in another app. On macOS, permission to capture
system audio is bundled with screen recording permission — Apple groups them
together, and Uzume uses only the audio portion. Nothing it hears leaves your
Mac. Playing a local file in Uzume needs no permission at all.

The app asks for it on first launch and explains it there in the same terms. If
you would rather not grant it, the local-file path is complete without it: the
full analysis and the full visual pipeline run either way.

## Is it free?

Yes. The source is public and MIT-licensed, so you can build and run it today at
no cost, and the public beta will be free and open source when it arrives.

## Does it run on Intel Macs?

No. Uzume is Apple silicon only — an M1 Mac or newer. A few features are
reserved for M3 and newer.

## Which version of macOS does it need?

macOS 14 Sonoma or later. Building it yourself also needs Xcode 26.5, the
version the repository pins.

## Is it safe to watch if I am sensitive to flashing light?

Every scene in the gallery is tested for steady luminance: a bounded change in
brightness from frame to frame, with beat-locked motion confined to parts of the
frame rather than thrown across all of it. The app says the rest plainly before
your first session: it renders high-contrast, fast-changing visuals, and if you
are sensitive to flashing lights or strobe patterns you should turn on Reduce
motion in Settings before you start.

Uzume honors your system's reduced-motion setting as well, and so does this
site — [the gallery](/gallery/) holds still until you ask it not to.

## How do I write a scene?

A scene is two files — a Metal shader and a JSON file beside it — and the app
picks the pair up on its own. The code and the repository call these presets, so
that is the word you will meet in filenames and JSON keys; on this site they are
scenes. The walkthrough is in the app repository contributing guide today, and a
page here comes next.

If a scene is merged it joins what every listener sees, and it keeps your name
on it — the [gallery](/gallery/) is where they end up.

---

**Drawn from** the app repository:
[README.md](https://github.com/hoaxpoet/uzume/blob/main/README.md),
[docs/UX_SPEC.md](https://github.com/hoaxpoet/uzume/blob/main/docs/UX_SPEC.md),
[docs/RUNBOOK.md](https://github.com/hoaxpoet/uzume/blob/main/docs/RUNBOOK.md),
[docs/PRODUCT_SPEC.md](https://github.com/hoaxpoet/uzume/blob/main/docs/PRODUCT_SPEC.md)
and [CONTRIBUTING.md](https://github.com/hoaxpoet/uzume/blob/main/CONTRIBUTING.md).
Those are written maintainers-first and stay canonical; this page is a rewrite
of the parts that face outward.
