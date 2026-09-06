# Jack's Games

Browser games for Jack. No build tools needed — every game is a single self-contained HTML file.

## Games

| Game | Path | What it is |
|------|------|------------|
| ⚽📖 Jack's Words | [`reading-game/`](reading-game/) | English reading game for Year 1: hear a word, click letters to hear them, build the word from scrambled tiles, then see it rainbow-highlighted in a simple sentence. Every finished word earns a football ⚽. Spoken with a female English voice (Web Speech API). |
| ⚽🔢 Jack's Numbers | [`math-game/`](math-game/) | English maths game for Year 1: counting, adding, and taking away up to 10. Every sum is shown with clickable footballs that count out loud; the answer is picked from number tiles and celebrated with a rainbow result and a football ⚽. |
| 🥅✍️ Jack's Match | [`match-game/`](match-game/) | Two halves. First half is the phonics screening check idea: a word appears and he decides GOAL (real word) or ALIEN (made-up but decodable — `zat`, `shob`). Nothing is read out first, so he has to sound it out. Second half he hears a word and writes it on an ABC keyboard with no letters given. |
| ✏️ Jack's Letters | [`letters-game/`](letters-game/) | Trace lowercase letters with a finger. Each letter is SVG stroke paths; the checker samples points along each stroke with `getPointAtLength()` and requires them to be hit in order, so the letter has to be formed the way it is written. Taught in movement families (`c a d g o q`, `i l t u`, …), not a–z. |
| 🍎 Jack's Apples | [`apples-game/`](apples-game/) | Trace the numbers 1–20 with a finger, then fill the missing numbers into a 4×5 grid of apples (homework sheet „Practice Numbers 1–20"). |
| ♟️ Jackies Schach | [`chess/`](chess/) | Chess with a coach, XP, and streaks (German UI). |

## Start page

`index.html` is the launcher: the games are laid out as a football line-up on a pitch, with a **bench** of empty slots for games we add later. Each card carries a 🔊 badge that reads its name out loud (Jack can't read the labels yet) and a progress badge fed from the game's own `localStorage` score.

Adding a game: drop a self-contained `new-game/index.html` into the repo and replace one `.slot` in `index.html` with a `.card` (icon, name, one-word description, `data-say`).

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
| 🍎 Jack's Apples | [jacks-games/apples](https://github.com/jacks-games/apples) | [play](https://jacks-games.github.io/apples/) |
| ♟️ Jackies Schach | [jacks-games/chess](https://github.com/jacks-games/chess) | [play](https://jacks-games.github.io/chess/) |

## Where it runs

- <https://jackbenn.ing> — custom domain (INWX DNS -> GitHub Pages)
- <https://google814.github.io/Jack/> — the Pages default URL

On an iPad: open <https://jackbenn.ing>, then Share -> "Add to Home Screen". It opens full screen with the football icon.

## Run locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/> in a desktop browser (Chrome recommended for the best text-to-speech voices).

## Homework games (automatic)

Every Friday at 07:00 `~/second-brain/scripts/jack_homework.py` reads Jack's Seesaw class (Y1, Frau Tigges), mails the homework to Robert and Maria, and turns each new task into a small self-contained game `hw-YYYYMMDD-<topic>/index.html`. Those cards are inserted at the **top** of the line-up (orange, 📚). **Chess is always the last card, full width at the bottom**, so Jack meets the homework games first. Score key per game: `jackHw_<slug>` in `localStorage`.
