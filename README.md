# Jack's Games

Browser games for Jack. No build tools needed — every game is a single HTML file with no build step. Two reach out for one thing: chess loads its rules engine (chess.js) from jsDelivr, and Sight Words its font from Google Fonts.

## Games

| Game | Path | What it is |
|------|------|------------|
| 🔟 Jack's Ten Frames | [`ten-frames/`](ten-frames/) | Adding with ten frames, the way Year 1 does it at school (homework, October 2026). Red and yellow counters, like the double-sided ones in class. Forty sums in five steps: a quick look at a frame that is then covered (see five-and-two, don't count), how many more to make ten, adding inside one frame by tapping yellow counters in from a tray, going past ten by filling the first frame and letting the rest spill into the second, and two frames where he taps yellow counters across until the first one is a full ten. A full frame glows and wears a 10. The wrong tiles are the real mistakes: one out, the empty spaces read instead of the counters, the number just counted instead of the total, the full ten forgotten. |
| ⏰ Jack's Clock | [`clock-game/`](clock-game/) | Learning to tell the time on a real clock face. Forty clocks in six steps: read o'clock, set o'clock, read half past, set half past, read quarter past / quarter to, set them all. Reading: the clock shows a time and he picks one of three tiles; the wrong tiles are the real mistakes (half past read one hour on, past and to swapped, the long hand read as the hour). Setting: he drags the hands, which are geared like a real clock (the long hand going round twelve carries the short hand on), stop on the quarters and say the time when he lets go; ✓ Check gives a spoken hint about the hand that is wrong, and after three tries the clock shows him. In the quarter steps the right half of the face is green "past", the left half orange "to". |
| ⚽💯 Jack's Big Numbers | [`big-numbers/`](big-numbers/) | The harder sequel to Jack's Numbers: two-digit maths to 100 in six steps — reading tens and ones off nets of ten footballs, adding ones without bridging, a whole ten more or less, bridging over the ten, whole tens, and counting on in twos, fives and tens. Sixty sums in a fixed order; the wrong tiles are the mistakes a six-year-old really makes (one out, ten out, digits swapped). |
| 👀 Jack's Sight Words | [`sight-words/`](sight-words/) | The twenty most common English words (DfE „first 100 high frequency words", rank 1–20) on twenty big cards. Tap one and it is read out in the same neural voice; the card gets a ✓ and counts as read. „Read all" walks the whole list, „Mix" reshuffles the cards so the position is not what he memorises, and a ten-round quiz reads a word out and he taps it. |
| 🍎 Jack's Apples | [`apples-game/`](apples-game/) | Trace the numbers 1–20 with a finger, then fill the missing numbers into a 4×5 grid of apples (homework sheet „Practice Numbers 1–20"). The tracing half has the same accuracy meter as Letters — red to green, a bonus football at 95% and a ⭐ on the number. |
| 🥅✍️ Jack's Match | [`match-game/`](match-game/) | Two halves. First half is the phonics screening check idea: a word appears and he decides GOAL (real word) or ALIEN (made-up but decodable — `zat`, `shob`). Nothing is read out first, so he has to sound it out. Second half he hears a word and writes it on an ABC keyboard with no letters given. |
| ✏️ Jack's Letters | [`letters-game/`](letters-game/) | Trace lowercase letters with a finger. Each letter is SVG stroke paths; the checker samples points along each stroke with `getPointAtLength()` and requires them to be hit in order, so the letter has to be formed the way it is written. Taught in movement families (`c a d g o q`, `i l t u`, …), not a–z. An accuracy meter under the board scores how closely the finger hugged the line, red to green; 95% or more pays a bonus football and leaves a ⭐ on that letter. |
| ⚽🔢 Jack's Numbers | [`math-game/`](math-game/) | English maths game for Year 1: counting, adding, and taking away up to 10. Every sum is shown with clickable footballs that count out loud; the answer is picked from number tiles and celebrated with a rainbow result and a football ⚽. |
| ⚽📖 Jack's Words | [`reading-game/`](reading-game/) | English reading game for Year 1: hear a word, click letters to hear them, build the word from scrambled tiles, then see it rainbow-highlighted in a simple sentence. Every finished word earns a football ⚽. Spoken with a pre-rendered neural English voice (see “Voice” below). |
| ♟️ Jackies Schach | [`chess/`](chess/) | Chess with a spoken German coach (piece + from → to, gold arrow on the board), big status line, captured pieces, XP and streaks. |

## Start page

`index.html` is the launcher: the games are laid out as a football line-up on a pitch, with a **bench** of empty slots for games we add later. Each card carries a 🔊 badge that reads its name out loud (Jack can't read the labels yet) and a progress badge fed from the game's own `localStorage` score.

**Subject sections and tabs.** The cards are written once in the `.lineup` of `index.html`; when the page loads, the script sorts them into one section per subject, each with a heading (icon + English word in the display font + its own 🔊): **📚 New homework** (see below) → **📖 Reading** → **✏️ Writing** → **🔢 Maths** → **🇩🇪 Deutsch** (this heading is read out in German) → **♟️ Chess**. Empty sections are hidden. Above them sit the tabs **⚽ All · 📚 Homework · 📖 Reading · ✏️ Writing · 🔢 Maths · 🇩🇪 Deutsch · ♟️ Chess**, each with its own 🔊 (they wrap instead of scrolling; on a phone the icon is big and the word small). **All** shows every section; **Homework** shows all homework cards in one section; a subject tab shows just that subject. The choice is remembered in `localStorage` (`jackFilter`; unknown or old values such as `practice` and `fun` fall back to All), and a URL hash beats the remembered one, so <https://jackbenn.ing/#homework> opens straight on the school work. An empty tab shows a "Nothing here yet" slot in the bench style.

**New homework** is the top section of the All view: the homework cards (`data-group="homework"`) whose `data-new` is less than 14 days old, shown there as **copies**. The originals also stay in their subject section, so a subject never looks empty because its newest game is homework. The copies have no `id` and still show the score badge (it is set from `data-hw`).

**What's new** is the ✨ NEW strip between the header and the tabs: up to three chips for the newest things, newest first, each one tappable and speakable, with "more ▸" for the rest. It is fed by the `WHATS_NEW` array at the top of the script in `index.html`; entries older than 21 days drop out by themselves and the strip disappears when nothing is left. A card whose `data-new` date is less than 14 days old also wears a small yellow **NEW** ribbon.

Adding a game: drop a self-contained `new-game/index.html` into the repo and add a `.card` to the `.lineup` in `index.html` (icon, name, one-word description, `data-say`) — plus the two attributes the start page filters and sorts on:

- `data-group="homework" | "practice" | "fun"` — homework cards are `homework`, chess is `fun`, everything else is `practice`. Only `homework` matters for the page now: it feeds the Homework tab and New homework.
- `data-subject="reading" | "writing" | "maths" | "deutsch" | "chess"` — **required**: the section the card sits in. A card without it still shows up (🔢 icon → maths, everything else → reading), but fix it.
- `data-new="YYYY-MM-DD"` — the day it was added (the day its folder first landed in this repo), so it gets the NEW ribbon for two weeks, sorts into place and (for homework) counts as New homework for 14 days.

…and a `WHATS_NEW` entry (`date`, `icon`, `text`, `href`, `say`) so it shows up in the NEW strip.

Order rule: **newest first.** In every section the cards are sorted by `data-new` (newest first; on the same day the order in `index.html` decides), and chess is always the last card, full width. The start page sorts itself when it loads, so a new card can go anywhere at the top of the line-up — but keep `index.html` in the same order so the source reads like the page.

## Each game also has its own repo

Every game except the homework games is mirrored into its own public repo under
**[github.com/jacks-games](https://github.com/jacks-games)**, with its own README, screenshot and
GitHub Pages URL. This repo stays the source of truth — edit a game here, then run
`./tools/sync-game-repos.sh` to push the copies.

A new game needs, once: `gh repo create jacks-games/<name> --public` with a description and the
Pages URL as homepage, topics, Pages switched on with `build_type=workflow` **before** the first push
(otherwise `configure-pages` fails), `.github/workflows/deploy-pages.yml` copied from `letters`, a
README in the same shape as the others and a `screenshot.png`, a pair in `GAMES` in the sync script,
and a row in the "🎈 The other games" table of **every** mirror README and in the org profile
(`jacks-games/.github`, `profile/README.md` + `profile/img/<name>.png`). A cloud session cannot
create org repos — that step has to happen on the machine with `gh`.

Everything is listed **newest first**, chess last. GitHub's org repo list sorts by last push, so
the sync script pushes the oldest game first and the newest last. It only pushes the games that
changed, though — after editing one older game, run `./tools/sync-game-repos.sh --reorder` to put
the list back in order.

| Game | Repo | Own page |
|------|------|----------|
| 🔟 Jack's Ten Frames | [jacks-games/ten-frames](https://github.com/jacks-games/ten-frames) | [play](https://jacks-games.github.io/ten-frames/) |
| ⏰ Jack's Clock | [jacks-games/clock](https://github.com/jacks-games/clock) | [play](https://jacks-games.github.io/clock/) |
| 💯 Jack's Big Numbers | [jacks-games/big-numbers](https://github.com/jacks-games/big-numbers) | [play](https://jacks-games.github.io/big-numbers/) |
| 👀 Jack's Sight Words | [jacks-games/sight-words](https://github.com/jacks-games/sight-words) | [play](https://jacks-games.github.io/sight-words/) |
| 🍎 Jack's Apples | [jacks-games/apples](https://github.com/jacks-games/apples) | [play](https://jacks-games.github.io/apples/) |
| 🥅 Jack's Match | [jacks-games/match](https://github.com/jacks-games/match) | [play](https://jacks-games.github.io/match/) |
| ✏️ Jack's Letters | [jacks-games/letters](https://github.com/jacks-games/letters) | [play](https://jacks-games.github.io/letters/) |
| 🔢 Jack's Numbers | [jacks-games/numbers](https://github.com/jacks-games/numbers) | [play](https://jacks-games.github.io/numbers/) |
| 📖 Jack's Words | [jacks-games/words](https://github.com/jacks-games/words) | [play](https://jacks-games.github.io/words/) |
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

**Which voice a game gets.** A header line `# voice: de-DE-KatjaNeural` at the top
of a phrases file sets that game's voice; `--voice` on the command line overrides
it; without either it is `en-GB-SoniaNeural`. `--check` reports a manifest whose
voice differs from the one its phrases file asks for. German games:
chess, Lama Alma (`hw-20261007-lama-alma`) and the German pieces of Ma Mi Mo
(`hw-20261002-gfil-y1-silben-und-erste-2-de`; its English lines are the game
without `-de`, spoken by Sonia). Render **one game at a time**
(`--game <name>`), never `--game all`: it would re-render every game.

```bash
# once: python3 -m venv tts-venv && tts-venv/bin/pip install edge-tts
tts-venv/bin/python tools/build-audio.py --game reading-game   # render what is missing, one game
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

Every day at 07:00 and 17:00 `~/second-brain/scripts/jack_homework.py` reads Jack's Seesaw classes and the school mails and mails new homework to Robert and Maria. On the first Friday of the month at 17:00 (`--games`) it also turns each new task into a small self-contained game `hw-YYYYMMDD-<topic>/index.html`. Its card (orange, 📚) gets `data-group="homework"`, `data-subject` (guessed from the Seesaw text: GFiL / Leseübung / Silben / Wörter / deutsch → `deutsch`, the maths words → `maths`, write / capital / handwriting / trace → `writing`, otherwise `reading`), `data-new` and a `WHATS_NEW` entry, and takes its name from the game's `<title>`. The game is built with **pre-rendered voice clips** like every other game: the build prompt makes it copy the TEXT-CORE block and clip player from a reference game (English: `hw-20261002-mathematics-homework-wee-3`, German: `hw-20261007-lama-alma`, one voice only), then the script runs `node tools/gen-phrases.js <slug> --voice …`, renders with `~/second-brain/venv-tts` (`tools/build-audio.py --game <slug>`) and gates on `--check`. Clips and phrases file go into the same commit as the game. If a step fails the game still ships (the browser voice is the per-segment fallback) and Robert gets one ⚠️ mail. It appears under **New homework** at the top for 14 days and, for good, in its subject section. **Chess is always the last card, full width at the bottom.** Score key per game: `jackHw_<slug>` in `localStorage`.
