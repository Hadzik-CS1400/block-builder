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
    if not (result.returncode == 0):
        fail(
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


def fail(message):
    """Fail with exactly this message and nothing else.

    `assert some_list, "..."` makes pytest append its own explanation, and the
    scorecard in conftest.py prints reprcrash.message verbatim -- so the row a
    student reads ended with "assert []". Raising skips that.
    """
    raise AssertionError(message)


def for_loops(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.For)]


def test_day_runs_several_actions():
    """The day runs several actions from a for loop (5 pts)."""
    tree = get_tree()
    if not (for_loops(tree)):
        fail(
            "No for loop anywhere in game.py. The day cycle is "
            "`for action in range(1, actions_per_day + 1):` with the action menu "
            "indented inside it."
        )
    output = get_game_output()
    # Three is enough to prove a loop ran rather than one pasted block. Even
    # Hardcore gives four actions, and break only fires once health hits 0.
    seen = sum(("Action " + str(n)) in output for n in (1, 2, 3))
    if not (seen >= 3):
        fail(
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
    if not (ranged):
        fail(
            "No for loop over range() found. range() is what counts the actions."
        )
    source = get_source_code()
    if not ("actions_per_day" in source):
        fail(
            "No actions_per_day variable. Each difficulty branch sets its own, so "
            "Peaceful gets more actions in a day than Hardcore."
        )
    # Set in the difficulty branches, not just once at the top -- that is what
    # ties the loop to the choice the player made.
    assignments = [n for n in ast.walk(tree)
                   if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "actions_per_day"
                           for t in n.targets)]
    if not (len(assignments) >= 2):
        fail(
            "actions_per_day is only set once. Give it a value in each difficulty "
            "branch -- Peaceful 6, Normal 5, Hardcore 4 -- so the difficulty "
            "changes the length of the day. Found %d assignment(s)."
            % len(assignments)
        )
    if not any(isinstance(n, ast.Name) and n.id == "actions_per_day"
               for f in ranged for n in ast.walk(f.iter)):
        fail(
            "The for loop's range() does not use actions_per_day, so the "
            "difficulty makes no difference to how long the day is."
        )


def test_break_and_continue_used():
    """break and continue are both used inside the loop (5 pts)."""
    tree = get_tree()
    loops = for_loops(tree)
    if not loops:
        fail("No for loop in game.py yet, so neither word has a loop "
             "to control.")
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
    if not (not missing):
        fail(
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
    if not (nested):
        fail(
            "No loop found inside another loop. The shelter needs two: the outer "
            "one picks the row, the inner one draws the blocks across it."
        )
    output = get_game_output()
    if not ("Shelter" in output):
        fail(
            "Nothing in the output mentions the shelter. Print "
            "`print(\"Shelter: \", end=\"\")` before the loops."
        )
    # Checked in the source, not the output. shelter_level is wood // 5, and
    # whether a run ends with 5 wood depends on the dice and on what the player
    # spent -- a correct shelter legitimately draws nothing at level 0. What
    # must be true is that the inner loop prints ACROSS the row.
    inner_prints_inline = False
    for outer in nested:
        for inner in ast.walk(outer):
            if not isinstance(inner, ast.For) or inner is outer:
                continue
            for node in ast.walk(inner):
                if (isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Name)
                        and node.func.id == "print"
                        and any(kw.arg == "end" for kw in node.keywords)):
                    inner_prints_inline = True
    if not (inner_prints_inline):
        fail(
            "The inner loop never prints with end=\"\", so each block would start "
            "a new line and the shelter would come out as a column.\n"
            "Inside the inner loop: print(\"[]\", end=\"\") for the wall row and "
            "print(\"/\\\\\", end=\"\") for the roof. A bare print() after the "
            "inner loop ends the row."
        )
