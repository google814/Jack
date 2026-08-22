#!/usr/bin/env bash
# Push each game from this repo out to its own public repo under github.com/jacks-games.
#
# This repo stays the source of truth — jackbenn.ing is built from it. The
# per-game repos are copies, so every game also has its own page and its own
# link. Edit a game here, run this, and the copy follows.
#
#   ./tools/sync-game-repos.sh            # copy + commit + push
#   ./tools/sync-game-repos.sh --dry-run  # just show what would change
set -euo pipefail

ORG=jacks-games
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${JACK_GAMES_DIR:-$HOME/jack-games}"
DRY=""
[ "${1:-}" = "--dry-run" ] && DRY=1

# folder in this repo  ->  repo name in the org
GAMES="reading-game:words math-game:numbers match-game:match letters-game:letters chess:chess"

for pair in $GAMES; do
  from="${pair%%:*}"
  name="${pair##*:}"
  dest="$WORK/$name"

  [ -d "$dest" ] || { echo "skip $name (no clone at $dest)"; continue; }

  cp "$SRC/$from/index.html" "$dest/index.html"
  mkdir -p "$dest/icons"
  cp "$SRC"/icons/*.png "$dest/icons/"

  # standalone copies sit at the root of their own site, and the home button
  # goes to the family start page instead of a parent folder
  sed -i 's#"\.\./icons/#"icons/#g; s#href="\.\./"#href="https://jackbenn.ing"#g' "$dest/index.html"

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
