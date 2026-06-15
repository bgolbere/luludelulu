# LULUDELULU

> A two-player cooperative card game about how well you *actually* know each other.
> Answer weird questions with numbers. Try to match. Discover where you sync.
>
> **Play it: [luluthegame.com](https://luluthegame.com)**

*Delulu is the solulu.*

---

This repository hosts the public site for **luluthegame.com**, deployed on
**Cloudflare Pages** (fast deploys, automatic SSL).

## What's here

```
index.html        Landing page — how to play, get the game, QR, feedback
randomizer/        The full game, playable in a browser (offline-capable, all prompts inlined)
site-assets/       Printable rules PDF, QR code, print-ready QR poster, social preview image
```

## Run it locally

It's a static site — no build step. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## How the game works

You play in your browser with a regular deck of cards (Ace–10 of two suits) and
some chips. The site reads out the prompts and keeps score; the cards are how you
each secretly lock in a number 1–10. Lay them face down, flip together — match or
come close and you earn chips together. The game runs four phases (concrete,
social, esoteric, then a blind "Delulu" round) with a halftime Drift Check to talk
about your misses. ~15 minutes, two players.

Prefer a table reference instead of glancing at the screen? Print the
[rules card](site-assets/luludelulu-rules.pdf).

## Feedback

Playtesting now — feedback welcome at **hello@luluthegame.com**.

---

*Delulu is the solulu.*
