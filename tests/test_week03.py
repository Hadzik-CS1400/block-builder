"""
Block Builder - Week 3 Tests
Exploration Events & Choices (20 points)

Four tests, five points each. The names below become the scorecard rows, so
they match the grading table on the Canvas page word for word.

These read the source as often as the output, deliberately. The game is random
by design this week -- a run that happens to roll the quiet day prints almost
nothing -- so checking only what was printed would fail students for their
dice rather than their code.
"""
import re
import subprocess
import sys
from pathlib import Path

GAME_FILE = Path(__file__).parent.parent / "game.py"

MISSING = (
    "game.py not found in the top folder of your repo. It should be next to "
    "README.md, not inside weeks/. If you are starting fresh this week, run "
    "python sync.py first."
)


def require_game_file():
    if not GAME_FILE.exists():
        raise AssertionError(MISSING)


# Answers for every prompt the game might ask, plus padding so a game that
# asks more questions than we expect can never hang waiting on stdin.
FAKE_INPUT = "TestCrafter\n2\n" + "1\n" * 100


def run_game(stdin=FAKE_INPUT):
    """Run game.py with fake keyboard input and capture what it prints."""
    require_game_file()
    result = subprocess.run(
        [sys.executable, str(GAME_FILE)],
        input=stdin, capture_output=True, text=True, timeout=15,
    )
    assert result.returncode == 0, (
        "game.py crashed before it finished. Python said:\n" + result.stderr
    )
    return result


def source():
    """game.py with comments stripped, so a commented-out line never counts."""
    require_game_file()
    text = GAME_FILE.read_text(encoding="utf-8")
    return "\n".join(
        line for line in text.split("\n") if not line.strip().startswith("#")
    )


def test_four_or_more_events():
    """The if/elif chain has at least four branches (5 pts)."""
    code = source()
    assert "import random" in code, (
        "Expected `import random` at the top of game.py -- the exploration "
        "event needs it to pick a different day each run."
    )
    assert re.search(r"random\.randint\s*\(", code), (
        "Expected random.randint(1, 6) to roll which event happens."
    )
    branches = len(re.findall(r"^\s*elif\s+.*:", code, re.MULTILINE))
    assert branches >= 3, (
        "Found %d elif branches. Week 3 wants at least four events, which is "
        "an if, three or more elifs, and a final else.\n"
        "Remember the else IS the last event, not an error case -- without it "
        "one roll does nothing at all." % branches
    )


def test_choices_change_the_outcome():
    """An input() inside an event is branched on (5 pts)."""
    code = source()
    assert re.search(r"\binput\s*\(", code), (
        "No input() found. At least two events should offer a choice of 1 or 2."
    )
    # The choice has to be compared as TEXT -- input() never returns a number.
    compared = re.search(r"""(?:if|elif)\s+\w+\s*==\s*['"]\s*\d""", code)
    assert compared, (
        "Nothing branches on what the player typed.\n"
        "Compare it as text, with the quotes:  if choice == \"1\":\n"
        "Writing  if choice == 1:  compares a string to a number. That is "
        "always False, so the safe branch would run every single time."
    )


def test_resources_change_during_events():
    """At least one resource is reassigned inside a branch (5 pts)."""
    code = source()
    names = r"(?:wood|stone|food|water|health|iron)"
    # e.g.  wood = wood + 3   /   health = health - damage   /   food += 5
    changed = re.findall(
        r"^\s+(%s)\s*(?:=\s*\1\s*[-+]|[-+]=)" % names, code,
        re.MULTILINE | re.IGNORECASE,
    )
    assert changed, (
        "No resource changes inside an event. An event that prints a message "
        "but leaves wood, food and health untouched has not cost or earned "
        "the player anything.\n"
        "Something like:  wood = wood + 3   or   health = health - damage"
    )


def test_compound_conditions_used():
    """Two or more conditions join tests with and/or (5 pts)."""
    code = source()
    compound = re.findall(
        r"^\s*(?:if|elif)\s+.*\s(?:and|or)\s+.*:", code, re.MULTILINE
    )
    assert len(compound) >= 2, (
        "Found %d compound condition(s); Week 3 wants at least two.\n"
        "One belongs in the night check and one in the end-of-day warning:\n"
        "    if health > 70 and wood >= 3:\n"
        "    if health < 30 or food < 5:" % len(compound)
    )
