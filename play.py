"""Run your game when `rich` will not install:  python play.py

Normally you just run `python game.py`. That needs the `rich` library, which
is what makes the colors work, and installing it is one command.

Some machines will not let you. A Chromebook is the usual one: its Linux side
is Debian, whose python3 arrives with no pip at all, so the install command
everyone tells you to run cannot run. Fixing that properly is a system-admin
job, not a Python one, and it should not stand between you and your own game.

So this runs game.py with a colorless stand-in for rich (in
tests/_fallback/). Your game plays exactly the same -- same text, same
choices, same numbers -- just without the colors. The tests score you the
same too.

When you do get rich installed, go back to `python game.py`; this file will
then use the real one anyway.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tests"))

import _norich                                             # noqa: E402

GAME = os.path.join(HERE, "game.py")

if not os.path.exists(GAME):
    raise SystemExit(
        "No game.py here yet. Open weeks/week02_todo.py and use File > Save As\n"
        "to save it as game.py next to README.md (NOT inside weeks/)."
    )

if not _norich.rich_installed():
    print("(running without rich -- no colors, everything else the same)\n")

sys.exit(subprocess.run([sys.executable, GAME], env=_norich.env_for_game()).returncode)
