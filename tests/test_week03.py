"""
Block Builder - Week 3 Tests
Exploration Events & Choices (20 points)
"""
import re
import subprocess
import sys
from pathlib import Path

GAME_FILE = Path(__file__).parent.parent / "game.py"


def run_game(difficulty="2"):
    """Run game.py answering the difficulty prompt with the given choice."""
    stdin = "TestCrafter\n" + difficulty + "\n" + "1\n" * 50
    return subprocess.run(
        [sys.executable, str(GAME_FILE)],
        input=stdin, capture_output=True, text=True, timeout=5,
    )


def get_source_code():
    return GAME_FILE.read_text(encoding="utf-8")


def strip_comments(source):
    return "\n".join(
        line for line in source.split("\n") if not line.strip().startswith("#")
    )


def test_difficulty_actually_changes_the_game():
    """Peaceful and Hardcore produce different starts (5 pts)."""
    peaceful = run_game("1")
    hardcore = run_game("3")
    assert peaceful.returncode == 0, (
        "game.py crashed on Peaceful. Error was:\n" + peaceful.stderr
    )
    assert hardcore.returncode == 0, (
        "game.py crashed on Hardcore. Error was:\n" + hardcore.stderr
    )
    assert peaceful.stdout != hardcore.stdout, (
        "Choosing 1 (Peaceful) and 3 (Hardcore) produced identical output. "
        "Use if/elif/else on `difficulty` to set different starting resources."
    )


def test_random_events_are_used():
    """An exploration event is rolled with random (5 pts)."""
    source = strip_comments(get_source_code())
    assert "import random" in source, (
        "Expected `import random` at the top of game.py"
    )
    assert "random.randint" in source, (
        "Expected random.randint(...) to roll an exploration event"
    )


def test_night_phase_exists():
    """The day ends with a night phase (5 pts)."""
    output = run_game().stdout.lower()
    night_words = ["night", "shelter", "dark", "sleep", "cold"]
    assert any(word in output for word in night_words), (
        "Expected a night phase in the output - something about night, "
        "shelter, or the cold."
    )


def test_compound_boolean_used():
    """A condition combines two tests with and/or (5 pts)."""
    source = strip_comments(get_source_code())
    # e.g.  if health > 70 and wood >= 3:
    compound = re.findall(r"^\s*(?:if|elif)\s+.*\s(?:and|or)\s+.*:", source,
                          re.MULTILINE)
    assert compound, (
        "No compound condition found. Somewhere you need an `if` that joins "
        "two comparisons, like:  if health < 30 and food < 5:"
    )
