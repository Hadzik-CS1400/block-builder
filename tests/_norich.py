"""Decide what environment to run the student's game.py under.

If `rich` imports, nothing happens -- the game runs exactly as it does when
the student plays it. If it does not, `_fallback/` is put on the game
process's path so the colorless stand-in in `_fallback/rich/` is found
instead, and the tests can go on testing the student's logic.

Kept in its own file because every test_weekNN.py needs it and those files are
meant to be readable start to finish by a first-semester student. One import
is a smaller tax on that than fifteen lines of path juggling.
"""
import os

_FALLBACK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_fallback")


def rich_installed():
    try:
        import rich                                        # noqa: F401
        return True
    except Exception:
        # Not just ImportError: a half-installed rich can raise other things,
        # and the fallback is the right answer for those too.
        return False


def env_for_game():
    """os.environ, plus the fallback on PYTHONPATH when rich is missing."""
    env = dict(os.environ)
    if rich_installed():
        return env
    previous = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = _FALLBACK + (os.pathsep + previous if previous else "")
    return env
