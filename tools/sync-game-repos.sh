#!/usr/bin/env bash
# Push each game from this repo out to its own public repo under github.com/jacks-games.
#
# This repo stays the source of truth — jackbenn.ing is built from it. The
# per-game repos are copies, so every game also has its own page and its own
# link. Edit a game here, run this, and the copy follows.
#
#   ./tools/sync-game-repos.sh            # copy + commit + push
#   ./tools/sync-game-repos.sh --dry-run  # just show what would change
#   ./tools/sync-game-repos.sh --reorder  # push every mirror once more, in GAMES order
#
# GitHub lists the org's repos by last push. A sync only pushes the games that
# changed, so after editing an old game it jumps to the top of that list. Run
# --reorder afterwards: it pushes what is still unpushed and gives every other
# mirror an empty commit, oldest game first, so the list reads newest first again.
set -euo pipefail

ORG=jacks-games
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${JACK_GAMES_DIR:-$HOME/jack-games}"
DRY=""
REORDER=""
[ "${1:-}" = "--dry-run" ] && DRY=1
[ "${1:-}" = "--reorder" ] && REORDER=1

# folder in this repo  ->  repo name in the org
# In push order: GitHub lists the org's repos by last push, so the oldest game
# goes first and the newest last — the list then reads newest first. Chess
# goes first of all so it stays at the bottom. A new game goes on the end.
GAMES="chess:chess reading-game:words math-game:numbers letters-game:letters match-game:match apples-game:apples sight-words:sight-words big-numbers:big-numbers clock-game:clock ten-frames:ten-frames"

for pair in $GAMES; do
  from="${pair%%:*}"
  name="${pair##*:}"
  dest="$WORK/$name"

  [ -d "$dest" ] || { echo "skip $name (no clone at $dest)"; continue; }

  if [ -n "$REORDER" ]; then
    ( cd "$dest"
      git fetch -q origin
      if [ -z "$(git rev-list origin/main..HEAD)" ]; then
        git commit -q --allow-empty -m "Keep the org's repo list newest first"
      fi
      git push -q origin main
      echo "$name: pushed"
    )
    sleep 2   # one push per timestamp, so the order is unambiguous
    continue
  fi

  cp "$SRC/$from/index.html" "$dest/index.html"
  mkdir -p "$dest/icons"
  cp "$SRC"/icons/*.png "$dest/icons/"

  # the pre-rendered voice clips travel with the game
  if [ -d "$SRC/audio/$from" ]; then
    rm -rf "$dest/audio"
    mkdir -p "$dest/audio"
    cp "$SRC/audio/$from"/* "$dest/audio/"
  fi

  # standalone copies sit at the root of their own site, and the home button
  # goes to the family start page instead of a parent folder
  sed -i 's#"\.\./icons/#"icons/#g; s#href="\.\./"#href="https://jackbenn.ing"#g' "$dest/index.html"
  # ../audio/<game>/ only exists in the source repo; here the clips sit in audio/
  sed -i "s#'\.\./audio/$from/'#'audio/'#g" "$dest/index.html"

  if [ -n "$DRY" ]; then
    ( cd "$dest" && git --no-pager diff --stat || true )
    continue
  fi

  ( cd "$dest"
    git add -A
    if git diff --cached --quiet; then
      echo "$name: unchanged"
    else
      git commit -qm "Sync $name from the jackbenn.ing repo"
      git push -q origin main
      echo "$name: pushed"
    fi
  )
done
