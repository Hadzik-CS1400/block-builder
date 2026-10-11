"""A stand-in for `rich`, used ONLY when the real rich is not installed.

The week tests run your game.py in a separate Python process. Your game starts
with `from rich import print`, so on a machine without rich that process dies
at line 1 and every test reports "game.py crashed" -- which tells you nothing
about your code.

ChromeOS's Linux container is the case that matters: it is Debian, whose
python3 ships with no pip and with ensurepip switched off, so the usual
`python3 -m pip install rich` does not work and the real fix is an apt command.
A student should not need that before their own tests will speak to them.

So the tests add this folder to the path of the game process, and only when
importing rich has actually failed. If you have rich installed you get the real
one, colors and all -- this file is never reached. What you lose without it is
color, nothing else: the markup tags are stripped out and the text prints.
"""
import builtins
import re

# Deliberately a closed list rather than "anything in square brackets". A game
# that prints a list would otherwise lose it: `[1, 2, 3]` is not a style.
_STYLE = (r"(?:bold|dim|italic|underline|strike|reverse|blink|not|on|default"
          r"|black|red|green|yellow|blue|magenta|cyan|white"
          r"|bright_(?:black|red|green|yellow|blue|magenta|cyan|white))")
_TAG = re.compile(r"\[/?" + _STYLE + r"(?:\s+" + _STYLE + r")*\]|\[/\]")


def _plain(obj):
    return _TAG.sub("", obj) if isinstance(obj, str) else obj


def print(*objects, sep=" ", end="\n", file=None, flush=False, **_rich_only):
    """`rich.print` minus the color. Extra rich keywords are accepted and
    ignored, so a call that works with rich still works here."""
    builtins.print(*[_plain(o) for o in objects],
                   sep=sep, end=end, file=file, flush=flush)
