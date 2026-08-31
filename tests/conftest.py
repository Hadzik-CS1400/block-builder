"""Prints the point scorecard after the week's tests run.

Plain pytest ends with "4 passed", which is a count, not a grade -- and Block
Builder is submitted as a screenshot of the score, so the run has to end in
something worth photographing. Same scorecard the Code-Togethers print, so a
student sees one consistent format across the whole course.

**Nothing here needs editing when a new week ships.** Points are derived, not
declared: every Block Builder week is worth 20, so each test in the file is
worth 20 divided by however many tests that week has. The standing convention
is four tests at five points; a week with five tests gives four points each and
still totals 20. Row labels come from the test function names, so a new
`test_night_phase_runs` becomes "Night phase runs" on its own.

That means a week is published by dropping in `tests/test_weekNN.py` and
nothing else -- which is the point, because anything that needs remembering
gets forgotten in week 9.
"""

import datetime
import os
import textwrap
import re
import subprocess
import sys

WEEK_POINTS = 20
WIDTH = 62

GREEN, RED, RESET = "\033[32m", "\033[31m", "\033[0m"


def _enable_windows_vt():
    """Turn on ANSI handling in a Windows console."""
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))
    except Exception:
        return False


def _use_color():
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    if os.name == "nt":
        return _enable_windows_vt()
    return True


def _git(*args):
    try:
        out = subprocess.run(("git",) + args, capture_output=True, text=True,
                             timeout=5)
    except (OSError, ValueError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def _identity():
    """Whose repo this is, so the screenshot is visibly theirs."""
    remote = _git("remote", "get-url", "origin")
    repo = ""
    if remote:
        repo = remote.rstrip("/").rsplit("/", 1)[-1]
        if repo.endswith(".git"):
            repo = repo[:-4]
    owner = ""
    if remote and "/" in remote:
        parts = remote.rstrip("/").replace(":", "/").split("/")
        if len(parts) >= 2:
            owner = parts[-2]
    return {
        "user": owner or "(unknown)",
        "repo": repo or "(no git remote -- did you clone your own copy?)",
        "who": (" ".join(x for x in (_git("config", "--get", "user.name"),
                                     _git("config", "--get", "user.email"))
                         if x)
                or "(git identity not set -- see Lab 00, step 5)"),
    }


def _label(nodeid):
    """'tests/test_week02.py::test_asks_for_name' -> 'Asks for name'."""
    name = nodeid.rsplit("::", 1)[-1]
    name = re.sub(r"^test_", "", name).replace("_", " ").strip()
    return name[:1].upper() + name[1:] if name else nodeid


def _week(nodeid):
    m = re.search(r"test_week(\d+)", nodeid)
    return m.group(1) if m else ""


GAME_NEEDS = ("rich",)


def _missing_for_game():
    """Modules game.py imports that its own interpreter cannot find.

    Probed by running `sys.executable -c "import rich"` rather than importing
    here, and the distinction matters: pytest may be running on a different
    Python from the one that launches game.py. That is the single most
    confusing way a machine fails -- pip installed rich for one interpreter,
    the game runs on the other, and the student is told a library they just
    installed is missing.

    Without this, a missing rich shows up as four unrelated test failures
    about title screens and resources, and the actual cause never appears.
    """
    missing = []
    for module in GAME_NEEDS:
        try:
            probe = subprocess.run([sys.executable, "-c", "import " + module],
                                   capture_output=True, timeout=15)
        except (OSError, subprocess.SubprocessError):
            continue
        if probe.returncode:
            missing.append(module)
    return missing


def pytest_configure(config):
    config._scorecard = {}


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    config = getattr(report, "config", None)
    store = getattr(config, "_scorecard", None) if config else None
    if store is None:
        store = globals().setdefault("_fallback", {})
    # The explanation the test author wrote, not pytest's traceback around it.
    # reprcrash.message is that string directly -- parsing str(longrepr)
    # instead means filtering file paths, and "tests/..." vs "tests\..." makes
    # that filter platform-dependent, which is how the path leaked into the
    # scorecard on Windows the first time.
    detail = ""
    if not report.passed:
        crash = getattr(report.longrepr, "reprcrash", None)
        if crash is not None:
            detail = re.sub(r"^\w*Error:?\s*", "", crash.message.strip())
        elif report.longrepr:
            detail = str(report.longrepr).strip().splitlines()[-1]
    store[report.nodeid] = (report.nodeid, report.passed, detail)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    rows = getattr(config, "_scorecard", None) or globals().get("_fallback", {})
    if not rows:
        return

    color = _use_color()

    def write(line, ok=None):
        if color and ok is not None:
            terminalreporter.write_line((GREEN if ok else RED) + line + RESET)
        else:
            terminalreporter.write_line(line)

    values = list(rows.values())
    # Derived, so a week with a different number of tests still totals 20.
    per_test = WEEK_POINTS / len(values)
    week = next((_week(n) for n, _, _ in values if _week(n)), "")

    who = _identity()
    write("")
    write("=" * WIDTH)
    write(("WEEK %s SCORE" % week if week else "YOUR SCORE").center(WIDTH))
    write("=" * WIDTH)
    write("  %-13s %s" % ("GitHub user", who["user"]))
    write("  %-13s %s" % ("Repository", who["repo"]))
    write("  %-13s %s" % ("Submitted by", who["who"]))
    write("  %-13s %s" % ("Run at",
                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    write("-" * WIDTH)

    earned = 0.0
    for nodeid, passed, detail in values:
        label = _label(nodeid)
        got = per_test if passed else 0.0
        earned += got
        dots = "." * max(2, WIDTH - len(label) - 18)
        write("  %s %s %2d/%-2d  %s"
              % (label, dots, round(got), round(per_test),
                 "PASS" if passed else "FAIL"), ok=passed)
        if not passed and detail:
            # Wrapped, not truncated. These messages are the whole point of a
            # failing row -- "game.py not found in the top folder of your" cut
            # off mid-sentence tells a student less than nothing.
            for line in textwrap.wrap(" ".join(detail.split()),
                                      WIDTH - 10)[:3]:
                write("        %s" % line, ok=False)

    write("-" * WIDTH)
    write("  TOTAL".ljust(WIDTH - 12)
          + "%3d / %-3d" % (round(earned), WEEK_POINTS),
          ok=(round(earned) == WEEK_POINTS))
    write("=" * WIDTH)
    if round(earned) == WEEK_POINTS:
        write("  All tests pass. Screenshot this and submit it in Canvas.",
              ok=True)
        write("")
        return

    # Only worth probing when something failed, and only worth saying when it
    # explains the failures rather than adding noise beside them.
    missing = _missing_for_game()
    if missing:
        write("  THIS IS THE REAL PROBLEM, not your code:", ok=False)
        write("")
        write("  Python cannot find: %s" % ", ".join(missing))
        write("  Your game cannot start without it, so every test above")
        write("  failed for that one reason.")
        write("")
        write("  Install it into the SAME Python that runs your game:")
        write("")
        write("      python -m pip install -r requirements.txt")
        write("")
        write("  Use `python -m pip`, not plain `pip`. On a machine with more")
        write("  than one Python, plain `pip` can install into a different one")
        write("  -- which is why a library you just installed still shows as")
        write("  missing. On a Mac, use python3 instead of python.")
        write("")
        write("  Still stuck? See Common Problems on the Canvas assignment.")
        write("")
        return

    write("  Fix the FAIL lines above, then run the tests again.", ok=False)
    write("")
