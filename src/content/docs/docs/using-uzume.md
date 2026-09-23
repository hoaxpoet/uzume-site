---
title: Using Uzume
description: What happens while a Uzume session runs — starting it, steering it, reduced motion, and what to do when the visuals stop answering the music.
---

Uzume is not a screensaver with a microphone attached. It prepares before it
performs: it hears the music first, decides what will accompany what, and then
adapts as the music actually unfolds. Most of that is deliberately invisible.
This page is the visible part.

## Starting a session

**From local files.** Open a file, a folder, or an M3U playlist. Uzume is the
player here, so there is nothing to coordinate: a count of three runs over an
opening full of light, and the session begins when it reaches zero.

**From another app.** Connect a playlist — or choose to listen without one —
then press play in Apple Music, Spotify, or wherever the music is. Uzume waits
on a ready screen and starts on its own within a moment of hearing audio. There
is a **Begin now** button if you would rather it started ahead of the music, and
if it has heard nothing for a minute and a half it asks whether the music is
actually playing.

**While it prepares.** Handing Uzume a playlist buys it the chance to listen
ahead, and that takes a little time. The wait shows you one of two things: a
dark opening that widens as more of the playlist is heard, or — if you press
**Show track info** — the list itself, each track reporting what Uzume found in
it as it goes. Once the first few tracks are ready you can start without waiting
for the rest; preparation carries on behind the session.

What it will not show you is what is coming. Which scene accompanies which
track, and where the transitions land, stay a surprise on purpose.

## While it plays

The chrome appears for about three seconds and then goes away completely, so
there is nothing between you and the visuals. Move the mouse, click, or press
any key and it comes back. It returns briefly at every track change, too.

- **Top left** — what is playing now: title, artist, artwork where the source
  provides it, and the name of the scene currently drawing it.
- **Top right** — one dot per track in the session, filled as they play; a
  show/hide switch for the track card; settings; and end session.
- **Bottom center, local files only** — stop, previous, play/pause, next.
  Sessions driven by another app have no transport, because Uzume does not
  control that app and a pause button there would be a lie.

## Steering it

Every one of these is a keystroke, which means nobody watching knows you used
it. The ones that change the visuals wait for a musical boundary rather than
cutting mid-phrase.

| Key | What it does |
|---|---|
| `+` | More like this — stay with this kind of scene, and stay on this one longer |
| `-` | Less like this — leave early, and hold this family back for a while |
| `.` | Reshuffle what has not played yet |
| `←` `→` | Move to a different scene at the next boundary |
| `⇧←` `⇧→` | Move now, accepting the cut |
| `M` | Hold the mood where it is |
| `Space` | Show or hide the chrome |
| `⌘F` | Fullscreen |
| `⌘⇧F` | Send it to the other display |
| `Esc` | Leave fullscreen, or end the session |
| `⇧?` | The list of these, on screen |

For a room, put Uzume fullscreen on the television and keep the laptop for
yourself — the keys work from wherever the window has focus. Uzume never plays
audio, only listens to it, so speakers, HomePods and AirPlay stay your music
app's business.

## Reduced motion

If your Mac asks for reduced motion, Uzume gives it: the feedback blur that
smears one frame into the next is switched off, color shifts take seconds
instead of moments, and beat pulses run at half strength. The visuals are
deliberately less spectacular. That is the trade, and it is the right one.

## When the visuals stop answering the music

Silence itself is fine. Scenes are written to stay alive with nothing coming in,
and after a few quiet seconds a small **Listening…** badge appears until sound
returns.

What is not fine is Uzume hearing nothing while music is plainly playing. After
about ten seconds of that, a card appears over the visuals with the things to
try. In order of how often they are the answer:

**The Screen Recording permission has gone stale.** This is the trap worth
knowing about, because it gives no error: macOS quietly invalidates the grant
when your Mac's default output device changes — plugging in an interface,
unplugging headphones — and after every rebuild of the app. Uzume goes on
capturing successfully and receives nothing but silence. Fix it in System
Settings → Privacy & Security → Screen Recording: toggle Uzume off, then on
again, and relaunch.

**You scrubbed in Spotify or Apple Music.** Dragging the playhead tears down the
audio Uzume was attached to. It notices and reattaches on its own, after a few
seconds and then a few more.

**The track is protected.** Apple Music lossless and some Spotify content hand
any listener process digital silence. Nothing is broken and nothing can be done
about it; Uzume falls back to its quiet baseline and picks up again on the next
track that is not protected.

And if the music is clearly arriving but the visuals feel flat, Uzume is
probably being fed a quiet, flattened signal:

- Spotify → Settings → Playback → turn **Normalize volume** off.
- Apple Music → Settings → Playback → turn **Sound Check** off.
- Pin streaming quality high; low bitrates flatten exactly the transients the
  visuals are reading.
- In Audio MIDI Setup, set your output device to 48 kHz.

---

**Drawn from** the app repository:
[docs/UX_SPEC.md](https://github.com/hoaxpoet/uzume/blob/main/docs/UX_SPEC.md),
[docs/RUNBOOK.md](https://github.com/hoaxpoet/uzume/blob/main/docs/RUNBOOK.md),
[docs/PRODUCT_SPEC.md](https://github.com/hoaxpoet/uzume/blob/main/docs/PRODUCT_SPEC.md)
and [README.md](https://github.com/hoaxpoet/uzume/blob/main/README.md). Those are
written maintainers-first and stay canonical; this page is a rewrite of the
parts that face outward.
