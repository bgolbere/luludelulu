# LULUDELULU

> A two-player cooperative card game about how well you *actually* know each other.
> Answer weird questions with numbers. Try to match. Discover where you sync.
>
> **Play it: [luluthegame.com](https://luluthegame.com)**

*Delulu is the solulu.*

---

This repository hosts the public site for **luluthegame.com** via GitHub Pages.

## What's here

```
index.html        Landing page — how to play, get the game, QR, feedback
randomizer/        The full game, playable in a browser (offline-capable, all prompts inlined)
site-assets/       Printable rules PDF, QR code, print-ready QR poster
CNAME              Custom domain config for GitHub Pages
```

## Run it locally

It's a static site — no build step. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## How the game works

Someone reads a prompt. Both players secretly pick a number 1–10 and lay a card
face down. Flip together. Match or come close, you earn chips together. The game
runs four phases — concrete, social, esoteric, then a blind "Delulu" round — with
a halftime Drift Check to talk about your misses. ~15 minutes, two players.

Play in your browser, or print the [rules card](site-assets/luludelulu-rules.pdf)
and use a regular deck (Ace–10 of two suits) plus some chips.

## Feedback

Playtesting now — feedback welcome at **bgolbere@gmail.com**.

---

*Delulu is the solulu.*
