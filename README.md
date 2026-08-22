# Jack's Games

Browser games for Jack. No build tools needed — every game is a single self-contained HTML file.

## Games

| Game | Path | What it is |
|------|------|------------|
| ⚽📖 Jack's Words | [`reading-game/`](reading-game/) | English reading game for Year 1: hear a word, click letters to hear them, build the word from scrambled tiles, then see it rainbow-highlighted in a simple sentence. Every finished word earns a football ⚽. Spoken with a female English voice (Web Speech API). |
| ⚽🔢 Jack's Numbers | [`math-game/`](math-game/) | English maths game for Year 1: counting, adding, and taking away up to 10. Every sum is shown with clickable footballs that count out loud; the answer is picked from number tiles and celebrated with a rainbow result and a football ⚽. |
| 🥅✍️ Jack's Match | [`match-game/`](match-game/) | Two halves. First half is the phonics screening check idea: a word appears and he decides GOAL (real word) or ALIEN (made-up but decodable — `zat`, `shob`). Nothing is read out first, so he has to sound it out. Second half he hears a word and writes it on an ABC keyboard with no letters given. |
| ✏️ Jack's Letters | [`letters-game/`](letters-game/) | Trace lowercase letters with a finger. Each letter is SVG stroke paths; the checker samples points along each stroke with `getPointAtLength()` and requires them to be hit in order, so the letter has to be formed the way it is written. Taught in movement families (`c a d g o q`, `i l t u`, …), not a–z. |
| ♟️ Jackies Schach | [`chess/`](chess/) | Chess with a coach, XP, and streaks (German UI). |

## Start page

`index.html` is the launcher: the games are laid out as a football line-up on a pitch, with a **bench** of empty slots for games we add later. Each card carries a 🔊 badge that reads its name out loud (Jack can't read the labels yet) and a progress badge fed from the game's own `localStorage` score.

Adding a game: drop a self-contained `new-game/index.html` into the repo and replace one `.slot` in `index.html` with a `.card` (icon, name, one-word description, `data-say`).

## Where it runs

- <https://jackbenn.ing> — custom domain (INWX DNS -> GitHub Pages)
- <https://google814.github.io/Jack/> — the Pages default URL

On an iPad: open <https://jackbenn.ing>, then Share -> "Add to Home Screen". It opens full screen with the football icon.

## Run locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/> in a desktop browser (Chrome recommended for the best text-to-speech voices).
