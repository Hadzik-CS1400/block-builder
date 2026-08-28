"""
Block Builder - Week 3 Tests
Exploration Events & Choices (20 points)
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


def run_game(difficulty="2"):
    """Run game.py answering the difficulty prompt with the given choice."""
    require_game_file()
    stdin = "TestCrafter\n" + difficulty + "\n" + "1\n" * 50
    return subprocess.run(
        [sys.executable, str(GAME_FILE)],
        input=stdin, capture_output=True, text=True, timeout=5,
    )


def get_source_code():
    require_game_file()
    return GAME_FILE.read_text(encoding="utf-8")


def strip_comments(source):
    return "\n".join(
        line for line in source.split("\n") if not line.strip().startswith("#")
    )


def test_difficulty_actually_changes_the_game():
    """Difficulty drives an if/elif/else and all three run (5 pts)."""
    source = strip_comments(get_source_code())

    branches = re.findall(r"^\s*(?:if|elif)\s+.*difficulty.*:", source,
                          re.MULTILINE)
    assert len(branches) >= 2, (
        f"Found {len(branches)} conditions testing `difficulty`, expected at "
        f"least 2 (an `if` and an `elif`). Difficulty should decide your "
        f"starting resources, not just get printed back out."
    )
    assert re.search(r"^\s*else\s*:", source, re.MULTILINE), (
        "Expected an `else` so difficulty 3 (Hardcore) is handled too."
    )

    # Every branch has to actually work, not just exist
    for choice, label in (("1", "Peaceful"), ("2", "Normal"), ("3", "Hardcore")):
        result = run_game(choice)
        assert result.returncode == 0, (
            f"game.py crashed on difficulty {choice} ({label}). Error was:\n"
            + result.stderr
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
