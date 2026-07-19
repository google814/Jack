# Jack's Games

Browser games for Jack. No build tools needed — every game is a single self-contained HTML file.

## Games

| Game | Path | What it is |
|------|------|------------|
| ⚽📖 Jack's Words | [`reading-game/`](reading-game/) | English reading game for Year 1: hear a word, click letters to hear them, build the word from scrambled tiles, then see it rainbow-highlighted in a simple sentence. Every finished word earns a football ⚽. Spoken with a female English voice (Web Speech API). |
| ♟️ Jackies Schach | [`chess/`](chess/) | Chess with a coach, XP, and streaks (German UI). |

The start page (`index.html`) links to both games.

## Run locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/> in a desktop browser (Chrome recommended for the best text-to-speech voices).
