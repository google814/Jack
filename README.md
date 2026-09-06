# Jack's Games

Browser games for Jack. No build tools needed — every game is a single self-contained HTML file.

## Games

| Game | Path | What it is |
|------|------|------------|
| ⚽📖 Jack's Words | [`reading-game/`](reading-game/) | English reading game for Year 1: hear a word, click letters to hear them, build the word from scrambled tiles, then see it rainbow-highlighted in a simple sentence. Every finished word earns a football ⚽. Spoken with a pre-rendered neural English voice (see “Voice” below). |
| ⚽🔢 Jack's Numbers | [`math-game/`](math-game/) | English maths game for Year 1: counting, adding, and taking away up to 10. Every sum is shown with clickable footballs that count out loud; the answer is picked from number tiles and celebrated with a rainbow result and a football ⚽. |
| ⚽💯 Jack's Big Numbers | [`big-numbers/`](big-numbers/) | The harder sequel to Jack's Numbers: two-digit maths to 100 in six steps — reading tens and ones off nets of ten footballs, adding ones without bridging, a whole ten more or less, bridging over the ten, whole tens, and counting on in twos, fives and tens. Sixty sums in a fixed order; the wrong tiles are the mistakes a six-year-old really makes (one out, ten out, digits swapped). |
| 🥅✍️ Jack's Match | [`match-game/`](match-game/) | Two halves. First half is the phonics screening check idea: a word appears and he decides GOAL (real word) or ALIEN (made-up but decodable — `zat`, `shob`). Nothing is read out first, so he has to sound it out. Second half he hears a word and writes it on an ABC keyboard with no letters given. |
| ✏️ Jack's Letters | [`letters-game/`](letters-game/) | Trace lowercase letters with a finger. Each letter is SVG stroke paths; the checker samples points along each stroke with `getPointAtLength()` and requires them to be hit in order, so the letter has to be formed the way it is written. Taught in movement families (`c a d g o q`, `i l t u`, …), not a–z. An accuracy meter under the board scores how closely the finger hugged the line, red to green; 95% or more pays a bonus football and leaves a ⭐ on that letter. |
| 🍎 Jack's Apples | [`apples-game/`](apples-game/) | Trace the numbers 1–20 with a finger, then fill the missing numbers into a 4×5 grid of apples (homework sheet „Practice Numbers 1–20"). The tracing half has the same accuracy meter as Letters — red to green, a bonus football at 95% and a ⭐ on the number. |
| 👀 Jack's Sight Words | [`sight-words/`](sight-words/) | The twenty most common English words (DfE „first 100 high frequency words", rank 1–20) on twenty big cards. Tap one and it is read out in the same neural voice; the card gets a ✓ and counts as read. „Read all" walks the whole list, „Mix" reshuffles the cards so the position is not what he memorises, and a ten-round quiz reads a word out and he taps it. |
| ♟️ Jackies Schach | [`chess/`](chess/) | Chess with a coach, XP, and streaks (German UI). |

## Start page

`index.html` is the launcher: the games are laid out as a football line-up on a pitch, with a **bench** of empty slots for games we add later. Each card carries a 🔊 badge that reads its name out loud (Jack can't read the labels yet) and a progress badge fed from the game's own `localStorage` score.

**Filter tabs** sit above the line-up: **⚽ All · 📚 Homework · 🎓 Practice · 🎲 Fun**. Each tab has its own 🔊. The choice is remembered in `localStorage` (`jackFilter`), and a URL hash beats the remembered one, so <https://jackbenn.ing/#homework> opens straight on this week's school work. An empty filter shows a "Nothing here yet" slot in the bench style.

**What's new** is the ✨ NEW strip between the header and the tabs: up to three chips for the newest things, newest first, each one tappable and speakable, with "more ▸" for the rest. It is fed by the `WHATS_NEW` array at the top of the script in `index.html`; entries older than 21 days drop out by themselves and the strip disappears when nothing is left. A card whose `data-new` date is less than 14 days old also wears a small yellow **NEW** ribbon.

Adding a game: drop a self-contained `new-game/index.html` into the repo and replace one `.slot` in `index.html` with a `.card` (icon, name, one-word description, `data-say`) — plus the two attributes the start page filters on:

- `data-group="homework" | "practice" | "fun"` — which tab the card belongs to (homework cards are `homework`, chess is `fun`, everything else is `practice`).
- `data-new="YYYY-MM-DD"` — the day it was added, so it gets the NEW ribbon for two weeks.

…and a `WHATS_NEW` entry (`date`, `icon`, `text`, `href`, `say`) so it shows up in the NEW strip.

Order rule: homework games first, chess is always the last card.

## Each game also has its own repo

Every game is mirrored into its own public repo under **[github.com/jacks-games](https://github.com/jacks-games)**,
with its own README, screenshot and GitHub Pages URL. This repo stays the source of truth —
edit a game here, then run `./tools/sync-game-repos.sh` to push the copies.

| Game | Repo | Own page |
|------|------|----------|
| 📖 Jack's Words | [jacks-games/words](https://github.com/jacks-games/words) | [play](https://jacks-games.github.io/words/) |
| 🥅 Jack's Match | [jacks-games/match](https://github.com/jacks-games/match) | [play](https://jacks-games.github.io/match/) |
| ✏️ Jack's Letters | [jacks-games/letters](https://github.com/jacks-games/letters) | [play](https://jacks-games.github.io/letters/) |
| 🔢 Jack's Numbers | [jacks-games/numbers](https://github.com/jacks-games/numbers) | [play](https://jacks-games.github.io/numbers/) |
| 💯 Jack's Big Numbers | [jacks-games/big-numbers](https://github.com/jacks-games/big-numbers) | [play](https://jacks-games.github.io/big-numbers/) |
| 🍎 Jack's Apples | [jacks-games/apples](https://github.com/jacks-games/apples) | [play](https://jacks-games.github.io/apples/) |
| 👀 Jack's Sight Words | [jacks-games/sight-words](https://github.com/jacks-games/sight-words) | [play](https://jacks-games.github.io/sight-words/) |
| ♟️ Jackies Schach | [jacks-games/chess](https://github.com/jacks-games/chess) | [play](https://jacks-games.github.io/chess/) |

## Where it runs

- <https://jackbenn.ing> — custom domain (INWX DNS -> GitHub Pages)
- <https://google814.github.io/Jack/> — the Pages default URL

On an iPad: open <https://jackbenn.ing>, then Share -> "Add to Home Screen". It opens full screen with the football icon.

## Voice

Jack found the browser's own voice too robotic on an iPhone, so **every line the
games say is pre-rendered** as a small MP3 with Microsoft's neural
`en-GB-SoniaNeural` voice (rate `-5%`) and played back through Web Audio. The
Web Speech API is only the fallback for a line that has no clip.

```bash
# once: python3 -m venv tts-venv && tts-venv/bin/pip install edge-tts
tts-venv/bin/python tools/build-audio.py --game all      # render what is missing
tts-venv/bin/python tools/build-audio.py --check all     # every phrase has a clip?
```

- `tools/phrases/<game>.txt` — every line a game can say, one per line, already
  split into the segments the games play one after another. Add a new line to a
  game, add it here, re-run the build.
- `audio/<game>/<sha1>.mp3` plus `audio/<game>/manifest.json` (`text -> file`).
  The games fetch that manifest at load and look each segment up in it; anything
  missing falls back to `speechSynthesis`, so nothing ever goes silent.
- The `AudioContext` is created inside the ▶ tap — iOS refuses to start audio
  any other way.

## Run locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/> in a desktop browser (Chrome recommended for the best text-to-speech voices).

## Homework games (automatic)

Every Friday at 07:00 `~/second-brain/scripts/jack_homework.py` reads Jack's Seesaw class (Y1, Frau Tigges), mails the homework to Robert and Maria, and turns each new task into a small self-contained game `hw-YYYYMMDD-<topic>/index.html`. Those cards are inserted at the **top** of the line-up (orange, 📚). **Chess is always the last card, full width at the bottom**, so Jack meets the homework games first. Score key per game: `jackHw_<slug>` in `localStorage`.
