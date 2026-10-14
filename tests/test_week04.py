"""
Block Builder - Week 4 Tests
Debug & Plan the Game (20 points)

This week the tests check week04_debug.py, NOT game.py.
"""
import re
import subprocess
import sys
from pathlib import Path

# Top level, NOT weeks/. sync.py treats weeks/ as instructor-owned and
# resolves conflicts there with `checkout --theirs` -- so a student who
# fixed all eight bugs would have the work silently thrown away on their
# next sync. At the top level it is student-owned: their edits survive,
# and a later revision from me stops for a human instead of clobbering.
DEBUG_FILE = Path(__file__).parent.parent / "week04_debug.py"

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

    subtracts = [ln for ln in lines if re.search(r"wood\s*=\s*wood\s*-\s*3\b", ln)]
    assert not subtracts, (
        "Gathering wood still SUBTRACTS it. Picking wood up should leave you "
        "with more, not less. Look for `wood = wood - 3` inside an event."
    )
    assert any(re.search(r"wood\s*=\s*wood\s*\+\s*3\b", ln) for ln in lines), (
        "Expected gathered wood to be ADDED: `wood = wood + 3`."
    )

    food_cost = [ln for ln in lines if re.search(r"food_cost\s*=\s*(\d+)", ln)]
    assert food_cost, "Could not find where food_cost is set."
    value = int(re.search(r"food_cost\s*=\s*(\d+)", food_cost[0]).group(1))
    assert value == 2, (
        "food_cost is %d. A crafter eats 2 food per day -- with %d they starve "
        "on day one. Read the comment above the line." % (value, value)
    )


def test_conditional_logic_fixed():
    """The if-conditions are right (5 pts). Fixes BUG 4, BUG 5 and BUG 7."""
    lines = code_lines()

    # The recipe check compares against named costs, not bare numbers, so the
    # test matches the variables rather than the values they happen to hold.
    craft = [ln for ln in lines
             if "pickaxe_wood" in ln and "pickaxe_stone" in ln and ln.strip().startswith("if")]
    assert craft, "Could not find the crafting condition."
    assert " and " in craft[0], (
        "A wooden pickaxe needs the wood AND the stone. With `or` you can "
        "craft one while holding neither of the two things it is made from."
    )

    luck = [ln for ln in lines if re.search(r"luck\s*>\s*(\d+)", ln)]
    assert luck, "Could not find the luck check."
    threshold = int(re.search(r"luck\s*>\s*(\d+)", luck[0]).group(1))
    assert threshold < 10, (
        "luck is rolled with random.randint(1, 10) but the code tests "
        "`luck > %d` -- that can never be true, so the cave always goes badly. "
        "What threshold gives roughly a 50/50 chance?" % threshold
    )

    assert not any("heatlh" in ln for ln in lines), (
        "There is a misspelled variable name in the night phase. Python "
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
