"""
Block Builder - Week 2 Tests
Character Creation & Starting Resources (20 points)
"""
import re
import subprocess
import sys
from pathlib import Path

GAME_FILE = Path(__file__).parent.parent / "game.py"

MISSING = (
    "game.py not found in the top folder of your repo. In Week 2, open "
    "weeks/week02_todo.py and use File > Save As to save it as game.py "
    "next to README.md (NOT inside weeks/)."
)


def require_game_file():
    if not GAME_FILE.exists():
        raise AssertionError(MISSING)


# Answers for every prompt the game might ask, plus padding so a game that
# asks more questions than we expect can never hang waiting on stdin.
FAKE_INPUT = "TestCrafter\n2\n" + "\n" * 100


def run_game(stdin=FAKE_INPUT):
    """Run game.py with fake keyboard input and capture what it prints."""
    require_game_file()
    return subprocess.run(
        [sys.executable, str(GAME_FILE)],
        input=stdin, capture_output=True, text=True, timeout=5,
    )


def get_game_output():
    return run_game().stdout


def get_source_code():
    require_game_file()
    return GAME_FILE.read_text(encoding="utf-8")


def test_title_screen():
    """Title screen shows the game name (5 pts)."""
    result = run_game()
    assert result.returncode == 0, (
        "game.py crashed before it finished. Error was:\n" + result.stderr
    )
    assert "BLOCK BUILDER" in result.stdout.upper(), (
        "Expected 'BLOCK BUILDER' somewhere in the output"
    )


def test_asks_for_name_and_uses_it():
    """The player's name is stored and printed back (5 pts)."""
    output = get_game_output()
    assert "TestCrafter" in output, (
        "Typed the name 'TestCrafter' but never saw it in the output. "
        "Ask for it with input() and print the variable back out."
    )


def test_all_five_resources_reported():
    """The status display lists all five resources (5 pts)."""
    output = get_game_output().lower()
    missing = [r for r in ("wood", "stone", "iron", "food", "water")
               if r not in output]
    assert not missing, (
        f"These resources are never mentioned in the output: {missing}"
    )


def test_arithmetic_is_used():
    """Values are calculated, not just typed in (5 pts)."""
    source = get_source_code()
    # An assignment whose right-hand side does arithmetic on something,
    # e.g.  total_resources = wood + stone + food
    pattern = r"^\s*\w+\s*=\s*[^=\n]*[-+*/%][^=\n]*$"
    calculations = [
        line for line in source.split("\n")
        if re.match(pattern, line) and not line.strip().startswith("#")
    ]
    assert len(calculations) >= 3, (
        f"Expected at least 3 calculated values (a total, days of food, "
        f"shelter cost...), found {len(calculations)}. Use arithmetic to "
        f"work values out instead of typing the answer in."
    )
    assert "total" in get_game_output().lower(), (
        "Expected the output to show a total. Print your total_resources."
    )
