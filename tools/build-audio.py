#!/usr/bin/env python3
"""Render the spoken lines of Jack's games to MP3 clips with a neural voice.

The browser's own speech synthesis sounds like a computer on an iPhone, so
every line the games say is pre-rendered here with Microsoft's neural
en-GB voice and shipped as small MP3 files. Web Speech stays in the games
as a fallback for anything that has no clip.

Usage (needs the edge-tts virtualenv):

    tts-venv/bin/python tools/build-audio.py --game all
    tts-venv/bin/python tools/build-audio.py --game reading-game --force
    tts-venv/bin/python tools/build-audio.py --check all

The venv used while building lives outside the repo:
  /tmp/claude-1000/-home-rbenning/369a4608-4217-4b29-8785-67a151a4d3a0/scratchpad/tts-venv
Any Python 3.9+ with `pip install edge-tts` works just as well.

Input : tools/phrases/<game>.txt  — one utterance per line, '#' comments.
Output: audio/<game>/<sha1(text)[:12]>.mp3 and audio/<game>/manifest.json.
"""

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHRASE_DIR = os.path.join(ROOT, 'tools', 'phrases')
AUDIO_DIR = os.path.join(ROOT, 'audio')

DEFAULT_VOICE = 'en-GB-SoniaNeural'
DEFAULT_RATE = '-5%'
CONCURRENCY = 8
RETRIES = 3

WS = re.compile(r'\s+')


def norm(text):
    """The exact key shape used by the manifest and by the games at runtime."""
    return WS.sub(' ', text).strip()


def clip_name(text):
    return hashlib.sha1(norm(text).encode('utf-8')).hexdigest()[:12] + '.mp3'


def games():
    if not os.path.isdir(PHRASE_DIR):
        return []
    return sorted(f[:-4] for f in os.listdir(PHRASE_DIR) if f.endswith('.txt'))


def read_phrases(game):
    path = os.path.join(PHRASE_DIR, game + '.txt')
    if not os.path.isfile(path):
        raise SystemExit('no phrase list: ' + path)
    out, seen = [], set()
    with open(path, encoding='utf-8') as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            line = norm(line)
            if line and line not in seen:
                seen.add(line)
                out.append(line)
    return out


async def render_one(sem, text, path, voice, rate):
    import edge_tts
    async with sem:
        last = None
        for attempt in range(RETRIES):
            try:
                tmp = path + '.part'
                comm = edge_tts.Communicate(text, voice, rate=rate)
                await comm.save(tmp)
                if os.path.getsize(tmp) < 512:
                    raise RuntimeError('suspiciously small clip')
                os.replace(tmp, path)
                return None
            except Exception as exc:  # network hiccups are common, retry
                last = exc
                try:
                    os.remove(path + '.part')
                except OSError:
                    pass
                await asyncio.sleep(1.5 * (attempt + 1))
        return '%s  ->  %s' % (text, last)


async def build_game(game, voice, rate, force):
    phrases = read_phrases(game)
    out_dir = os.path.join(AUDIO_DIR, game)
    os.makedirs(out_dir, exist_ok=True)

    clips = {}
    todo = []
    for text in phrases:
        name = clip_name(text)
        clips[text] = name
        path = os.path.join(out_dir, name)
        if force or not os.path.isfile(path) or os.path.getsize(path) < 512:
            todo.append((text, path))

    sem = asyncio.Semaphore(CONCURRENCY)
    results = await asyncio.gather(*[render_one(sem, t, p, voice, rate) for t, p in todo])
    failed = [r for r in results if r]

    with open(os.path.join(out_dir, 'manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump({'voice': voice, 'rate': rate, 'clips': clips}, fh,
                  ensure_ascii=False, indent=0, sort_keys=True)
        fh.write('\n')

    # drop clips that no phrase points at any more, so the folder stays clean
    keep = set(clips.values()) | {'manifest.json'}
    stale = [f for f in os.listdir(out_dir) if f not in keep]
    for f in stale:
        os.remove(os.path.join(out_dir, f))

    size = sum(os.path.getsize(os.path.join(out_dir, f)) for f in os.listdir(out_dir))
    print('%-42s %4d phrases  %4d new  %4d kept  %3d stale removed  %5.1f KB%s'
          % (game, len(phrases), len(todo) - len(failed), len(phrases) - len(todo),
             len(stale), size / 1024.0, '  %d FAILED' % len(failed) if failed else ''))
    for f in failed:
        print('   FAILED: ' + f, file=sys.stderr)
    return len(failed)


def check_game(game):
    phrases = read_phrases(game)
    out_dir = os.path.join(AUDIO_DIR, game)
    man_path = os.path.join(out_dir, 'manifest.json')
    problems = []
    if not os.path.isfile(man_path):
        problems.append('missing manifest.json')
        manifest = {'clips': {}}
    else:
        with open(man_path, encoding='utf-8') as fh:
            manifest = json.load(fh)
    clips = manifest.get('clips', {})
    for text in phrases:
        name = clips.get(text)
        if not name:
            problems.append('no manifest entry: ' + text)
            continue
        path = os.path.join(out_dir, name)
        if not os.path.isfile(path):
            problems.append('missing file for: ' + text)
        elif os.path.getsize(path) < 512:
            problems.append('tiny file for: ' + text)
    extra = [t for t in clips if t not in set(phrases)]
    for t in extra:
        problems.append('manifest entry with no phrase: ' + t)
    print('%-42s %4d phrases  %s' % (game, len(phrases),
                                     'OK' if not problems else '%d PROBLEMS' % len(problems)))
    for p in problems:
        print('   ' + p, file=sys.stderr)
    return len(problems)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--game', default='all', help='game folder name, or "all"')
    ap.add_argument('--voice', default=DEFAULT_VOICE)
    ap.add_argument('--rate', default=DEFAULT_RATE)
    ap.add_argument('--force', action='store_true', help='re-render clips that already exist')
    ap.add_argument('--check', metavar='GAME', help='verify clips exist for every phrase')
    args = ap.parse_args()

    if args.check:
        names = games() if args.check == 'all' else [args.check]
        bad = sum(check_game(g) for g in names)
        raise SystemExit(1 if bad else 0)

    names = games() if args.game == 'all' else [args.game]
    bad = 0
    for g in names:
        bad += asyncio.run(build_game(g, args.voice, args.rate, args.force))
    raise SystemExit(1 if bad else 0)


if __name__ == '__main__':
    main()
