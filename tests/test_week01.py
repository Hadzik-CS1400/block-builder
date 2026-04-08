"""
Block Builder — Week 1 Tests
Title Screen & World Intro (20 points)
"""
import subprocess
import sys
from pathlib import Path

GAME_FILE = Path(__file__).parent.parent / "game.py"


def get_game_output():
    """Run game.py and capture output."""
    result = subprocess.run(
        [sys.executable, str(GAME_FILE)],
        capture_output=True, text=True, timeout=5
    )
    return result.stdout


def get_source_code():
    """Read game.py source code."""
    return GAME_FILE.read_text()


def test_title_contains_game_name():
    """Title screen contains 'BLOCK BUILDER' (5 pts)."""
    output = get_game_output()
    assert "BLOCK BUILDER" in output.upper(), (
        "Expected 'BLOCK BUILDER' somewhere in the output"
    )


def test_biome_section_exists():
    """A biome description is printed (5 pts)."""
    output = get_game_output().lower()
    # Check for biome-related keywords
    biome_words = ["biome", "forest", "desert", "tundra", "cave", "mountain",
                   "river", "plains", "swamp", "ocean"]
    found = any(word in output for word in biome_words)
    assert found, (
        "Expected a biome description (forest, desert, etc.) in the output"
    )


def test_enough_print_statements():
    """At least 10 print statements in source code (5 pts)."""
    source = get_source_code()
    count = source.count("print(")
    assert count >= 10, (
        f"Expected at least 10 print() calls, found {count}"
    )


def test_enough_comments():
    """At least 5 student-written comments (5 pts)."""
    source = get_source_code()
    lines = source.split("\n")
    comment_lines = [line.strip() for line in lines
                     if line.strip().startswith("#")]
    # Exclude the file header block (first 6 lines are boilerplate)
    student_comments = [c for c in comment_lines
                        if "===" not in c
                        and "Block Builder" not in c
                        and "Week 1" not in c
                        and "Concepts used" not in c]
    assert len(student_comments) >= 5, (
        f"Expected at least 5 comments, found {len(student_comments)}"
    )
