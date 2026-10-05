"""
Block Builder - Week 5 Tests
Day Cycle - Gather Resources (20 points)

Four tests, five points each. The names below become the scorecard rows, so
they match the grading table in weeks/week05_todo.py word for word.

Source and output are both read, for the reason Week 3's tests give: the game
is random, and a run that rolls the quiet day prints almost nothing. Where this
week differs is that the loop itself is checkable in the source -- a for over a
range, a break and a continue inside it, and one loop nested in another are all
structural, so they are read from the syntax tree rather than guessed at from
what got printed.
"""
import ast
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
# asks more questions than we expect can never hang waiting on stdin. "5" picks
# Explore from the action menu, which is the branch worth exercising.
FAKE_INPUT = "TestCrafter\n2\n" + "5\n1\n" * 100


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


def get_game_output():
    return run_game().stdout


def get_source_code():
    require_game_file()
    return GAME_FILE.read_text(encoding="utf-8")


def get_tree():
    """The parsed source, or a clear failure if it will not parse."""
    try:
        return ast.parse(get_source_code())
    except SyntaxError as exc:
        raise AssertionError(
            "game.py has a syntax error on line %s: %s\n"
            "Python cannot read the file, so nothing can be checked. A for "
            "loop whose body is not indented is the usual cause this week."
            % (exc.lineno, exc.msg)
        )


def for_loops(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.For)]


def test_day_runs_several_actions():
    """The day runs several actions from a for loop (5 pts)."""
    tree = get_tree()
    assert for_loops(tree), (
        "No for loop anywhere in game.py. The day cycle is "
        "`for action in range(1, actions_per_day + 1):` with the action menu "
        "indented inside it."
    )
    output = get_game_output()
    # Three is enough to prove a loop ran rather than one pasted block. Even
    # Hardcore gives four actions, and break only fires once health hits 0.
    seen = sum(("Action " + str(n)) in output for n in (1, 2, 3))
    assert seen >= 3, (
        "Expected the day to print at least three actions (Action 1, "
        "Action 2, Action 3 ...). Only %d of the first three appeared.\n"
        "Is the menu inside the for loop? Everything that happens during an "
        "action has to be indented under it." % seen
    )


def test_range_sets_the_action_count():
    """range() decides how many actions, from the difficulty (5 pts)."""
    tree = get_tree()
    ranged = [f for f in for_loops(tree)
              if isinstance(f.iter, ast.Call)
              and isinstance(f.iter.func, ast.Name)
              and f.iter.func.id == "range"]
    assert ranged, (
        "No for loop over range() found. range() is what counts the actions."
    )
    source = get_source_code()
    assert "actions_per_day" in source, (
        "No actions_per_day variable. Each difficulty branch sets its own, so "
        "Peaceful gets more actions in a day than Hardcore."
    )
    # Set in the difficulty branches, not just once at the top -- that is what
    # ties the loop to the choice the player made.
    assignments = [n for n in ast.walk(tree)
                   if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "actions_per_day"
                           for t in n.targets)]
    assert len(assignments) >= 2, (
        "actions_per_day is only set once. Give it a value in each difficulty "
        "branch -- Peaceful 6, Normal 5, Hardcore 4 -- so the difficulty "
        "changes the length of the day. Found %d assignment(s)."
        % len(assignments)
    )
    assert any(isinstance(n, ast.Name) and n.id == "actions_per_day"
               for f in ranged for n in ast.walk(f.iter)), (
        "The for loop's range() does not use actions_per_day, so the "
        "difficulty makes no difference to how long the day is."
    )


def test_break_and_continue_used():
    """break and continue are both used inside the loop (5 pts)."""
    tree = get_tree()
    loops = for_loops(tree)
    assert loops, "No for loop in game.py yet, so neither word has a loop to control."
    has_break = any(isinstance(n, ast.Break) for f in loops for n in ast.walk(f))
    has_continue = any(isinstance(n, ast.Continue)
                       for f in loops for n in ast.walk(f))
    missing = []
    if not has_break:
        missing.append(
            "break -- end the day early when health drops to 0 or below"
        )
    if not has_continue:
        missing.append(
            "continue -- skip the rest of one action when food and water are "
            "both gone"
        )
    assert not missing, (
        "Missing inside the day loop:\n  " + "\n  ".join(missing)
        + "\nBoth have to be INSIDE the for loop. Outside one, Python raises "
          "a SyntaxError."
    )


def test_nested_loop_draws_shelter():
    """A nested loop draws the shelter (5 pts)."""
    tree = get_tree()
    nested = [outer for outer in for_loops(tree)
              if any(isinstance(inner, ast.For) and inner is not outer
                     for inner in ast.walk(outer))]
    assert nested, (
        "No loop found inside another loop. The shelter needs two: the outer "
        "one picks the row, the inner one draws the blocks across it."
    )
    output = get_game_output()
    assert "Shelter" in output, (
        "Nothing in the output mentions the shelter. Print "
        "`print(\"Shelter: \", end=\"\")` before the loops."
    )
    assert ("/\\" in output) or ("[]" in output), (
        "The shelter never draws any blocks. The inner loop should print one "
        "block at a time with end=\"\" -- \"/\\\\\" for the roof row and "
        "\"[]\" for the wall row -- and a bare print() ends each row.\n"
        "If the shelter is empty, check shelter_level: with under 5 wood it "
        "is 0, so there is nothing to draw."
    )
