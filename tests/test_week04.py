"""
Block Builder - Week 4 Tests
Debug & Plan the Game (20 points)

This week the tests check weeks/week04_debug.py, NOT game.py.
"""
import re
import subprocess
import sys
from pathlib import Path

DEBUG_FILE = Path(__file__).parent.parent / "weeks" / "week04_debug.py"

FAKE_INPUT = "TestCrafter\n2\n" + "1\n" * 50


def run_debug_file():
    return subprocess.run(
        [sys.executable, str(DEBUG_FILE)],
        input=FAKE_INPUT, capture_output=True, text=True, timeout=5,
    )


def get_source_code():
    return DEBUG_FILE.read_text(encoding="utf-8")


def code_lines():
    """Source with comments and blank lines removed."""
    return [
        line for line in get_source_code().split("\n")
        if line.strip() and not line.strip().startswith("#")
    ]


def test_program_runs_without_crashing():
    """The program runs start to finish (5 pts). Fixes BUG 1 and BUG 8."""
    result = run_debug_file()
    assert result.returncode == 0, (
        "week04_debug.py still crashes. Read the traceback - it names the "
        "file and line number:\n" + result.stderr
    )


def test_gathering_and_eating_math():
    """Resources move the right direction (5 pts). Fixes BUG 2 and BUG 3."""
    lines = code_lines()
    subtracts_gathered = [
        ln for ln in lines if re.search(r"wood\s*=\s*wood\s*-\s*gathered_wood", ln)
    ]
    assert not subtracts_gathered, (
        "Gathering wood still SUBTRACTS it. Picking wood up should make you "
        "have more, not less."
    )
    assert any(re.search(r"wood\s*=\s*wood\s*\+\s*gathered_wood", ln) for ln in lines), (
        "Expected the gathered wood to be added to your wood total."
    )

    food_cost = [ln for ln in lines if re.search(r"food_cost\s*=\s*(\d+)", ln)]
    assert food_cost, "Could not find where food_cost is set."
    value = int(re.search(r"food_cost\s*=\s*(\d+)", food_cost[0]).group(1))
    assert value == 2, (
        f"food_cost is {value}. A crafter eats 2 food per day - with {value} "
        f"they'd starve on day one. Check the comment above the line."
    )


def test_conditional_logic_fixed():
    """The if-conditions are right (5 pts). Fixes BUG 4, BUG 5 and BUG 7."""
    lines = code_lines()

    craft = [ln for ln in lines if "wood >= 3" in ln and "stone >= 2" in ln]
    assert craft, "Could not find the crafting condition."
    assert " and " in craft[0], (
        "A wooden pickaxe needs 3 wood AND 2 stone. With `or` you can craft "
        "one out of thin air when you have stone but no wood."
    )

    luck = [ln for ln in lines if re.search(r"luck\s*>\s*(\d+)", ln)]
    assert luck, "Could not find the luck check."
    threshold = int(re.search(r"luck\s*>\s*(\d+)", luck[0]).group(1))
    assert threshold < 10, (
        f"luck is rolled with random.randint(1, 10) but the code tests "
        f"`luck > {threshold}` - that can never be true, so the cave always "
        f"goes badly. What threshold gives roughly a 50/50 chance?"
    )

    assert not any("heatlh" in ln for ln in lines), (
        "There's a misspelled variable name in the night phase. Python "
        "happily makes a NEW variable instead of updating the real one, so "
        "the damage silently vanishes."
    )


def test_pseudocode_written():
    """The game loop is planned in pseudocode (5 pts)."""
    source = get_source_code()
    steps = re.findall(r"^#\s*\d+\.\s*(.+)$", source, re.MULTILINE)
    filled = [s.strip() for s in steps
              if s.strip() and s.strip() not in ("...", ".")]
    assert len(filled) >= 5, (
        f"Found {len(filled)} pseudocode steps, expected at least 5. Fill in "
        f"the numbered lines at the bottom of the file with plain-English "
        f"steps describing the daily game loop."
    )
