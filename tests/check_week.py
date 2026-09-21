"""Print this week's Block Builder scorecard WITHOUT pytest.

    python tests/check_week.py        # the newest week you have
    python tests/check_week.py 3      # a specific week

Every other assignment in this course can be scored with nothing installed --
`python tests/check_main.py` uses only the standard library. Block Builder
could not: its scorecard came out of conftest.py's pytest hooks, so pytest and
therefore pip were mandatory.

That is fine until a student is on a Chromebook. ChromeOS's Linux container is
Debian, which ships python3 with no pip and with ensurepip deliberately
disabled -- so `python3 -m pip install` and `python3 -m ensurepip` both fail,
and the fix is `sudo apt install python3-pip`, which is not a Python lesson.
One student lost an evening to exactly this.

This runs the same test functions and hands the results to the SAME renderer
conftest uses, so the two routes cannot print different scores. A scorecard
that depended on how you ran it would be worse than no scorecard.
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import conftest                                          # noqa: E402


def weeks_available():
    return sorted(int(m.group(1))
                  for f in os.listdir(HERE)
                  for m in [re.match(r"test_week(\d+)\.py$", f)] if m)


def load_week(week):
    path = os.path.join(HERE, "test_week%02d.py" % week)
    if not os.path.exists(path):
        raise SystemExit("No tests/test_week%02d.py. Run `python sync.py` first."
                         % week)
    spec = importlib.util.spec_from_file_location("_week%02d" % week, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(week):
    """(nodeid, passed, detail) per test, in the order they are written."""
    mod = load_week(week)
    src = open(mod.__file__, encoding="utf-8").read()
    # Source order, not alphabetical: the scorecard should read top to bottom
    # the same way the file does.
    names = re.findall(r"^def (test_\w+)", src, re.MULTILINE)
    rows = []
    for name in names:
        nodeid = "tests/test_week%02d.py::%s" % (week, name)
        try:
            getattr(mod, name)()
            rows.append((nodeid, True, ""))
        except AssertionError as exc:
            rows.append((nodeid, False, str(exc).strip()))
        except Exception as exc:
            rows.append((nodeid, False, "%s: %s" % (type(exc).__name__, exc)))
    return rows


def main():
    available = weeks_available()
    if not available:
        raise SystemExit("No week tests found in tests/. Run `python sync.py`.")
    if len(sys.argv) > 1:
        try:
            week = int(sys.argv[1])
        except ValueError:
            raise SystemExit("Usage: python tests/check_week.py [week number]")
    else:
        week = available[-1]

    rows = run(week)
    color = conftest._use_color()

    def write(line, ok=None):
        if color and ok is not None:
            print((conftest.GREEN if ok else conftest.RED) + line + conftest.RESET)
        else:
            print(line)

    conftest._write_week_scorecard(write, "%02d" % week, rows, color)
    return 0 if all(passed for _, passed, _ in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
