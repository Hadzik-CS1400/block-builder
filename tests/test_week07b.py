"""
Block Builder - Week 7B tests
Finish the Refactor (20 points)

Four tests, five points each. The names below become the scorecard rows.

Week 7 asked for four functions and required four. This asks for the rest of
the file, and the difference is deliberate: the first time you split a block
out it feels clever, and by the tenth it feels obvious. Obvious is the point.

What this does NOT do is check function NAMES. A student may call it
show_panel or draw_status or whatever they like; the tests look at shape --
how many definitions, how many only print, whether anything hands back more
than one value, and whether the game still behaves as it did.

The last part matters most. A refactor that changes behaviour is a bug with
good intentions, so the final test runs the game and insists it still plays.
"""
import ast
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _norich  # noqa: E402

GAME_FILE = Path(__file__).parent.parent / "game.py"

MISSING = (
    "game.py not found in the top folder of your repo. It should be next to "
    "README.md, not inside weeks/. If you are starting fresh this week, run "
    "python sync.py first."
)

FAKE_INPUT = "TestCrafter\n2\n" + "1\n" * 600
TIMED_OUT = "TIMED_OUT"


def fail(message):
    """Fail with exactly this message and nothing else."""
    raise AssertionError(message)


def require_game_file():
    if not GAME_FILE.exists():
        fail(MISSING)


def get_source_code():
    require_game_file()
    return GAME_FILE.read_text(encoding="utf-8")


def get_tree():
    try:
        return ast.parse(get_source_code())
    except SyntaxError as exc:
        fail(
            "game.py has a syntax error on line %s: %s\n"
            "Python cannot read the file, so nothing can be checked. When a "
            "refactor breaks the parse it is almost always indentation -- a "
            "block that moved inside a def needs every one of its lines to "
            "move with it." % (exc.lineno, exc.msg)
        )


def run_game(stdin=FAKE_INPUT):
    require_game_file()
    try:
        result = subprocess.run(
            [sys.executable, str(GAME_FILE)],
            input=stdin, capture_output=True, text=True, timeout=25,
            env=_norich.env_for_game(),
        )
    except subprocess.TimeoutExpired:
        return TIMED_OUT
    if result.returncode != 0:
        fail("game.py crashed before it finished. Python said:\n"
             + result.stderr.strip()[-600:])
    return result.stdout


def output_lines():
    out = run_game()
    if out == TIMED_OUT:
        fail(
            "The game never ended -- it was still running after 25 seconds.\n"
            "A function that moved is the usual cause: check that `day = day "
            "+ 1` is still in the LOOP and did not travel inside a def, where "
            "it increments a copy and the loop never advances."
        )
    return out.splitlines()


def functions(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def returns_a_value(fn):
    """True if any return hands something back. `return` alone does not."""
    for node in ast.walk(fn):
        if isinstance(node, ast.Return) and node.value is not None:
            return True
    return False


def prints(fn):
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "print":
            return True
    return False


def defaulted(fn):
    """Parameters carrying a default value."""
    return len(fn.args.defaults) + len(
        [d for d in fn.args.kw_defaults or [] if d is not None])


def multi_returns(tree):
    """Functions that hand back several values at once."""
    out = []
    for fn in functions(tree):
        for node in ast.walk(fn):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple) \
                    and len(node.value.elts) >= 3:
                out.append((fn.name, len(node.value.elts)))
                break
    return out


# ---------------------------------------------------------------------------
# The four scored tests
# ---------------------------------------------------------------------------


def test_the_refactor_reaches_the_whole_file():
    """Ten or more functions, not just Week 7's four (5 pts)."""
    tree = get_tree()
    defs = functions(tree)

    if len(defs) < 5:
        fail(
            "Found %d function definition(s). Week 7 already needed four, so "
            "this row is asking for the rest of the file:\n"
            "    STEP 8   the blocks that only print\n"
            "    STEP 9   two more with defaults\n"
            "    STEP 10  the event blocks\n"
            "    STEP 11  the menus\n"
            "Start with STEP 8 -- those are the easiest, because they read "
            "values and print them and do nothing else." % len(defs)
        )
    if len(defs) < 10:
        fail(
            "Found %d function definition(s); Part B finishes at ten or more.\n"
            "Still inline somewhere, most likely: the title screen, the "
            "starting status block, the shelter drawing, the progress bar, "
            "the explore events, the night phase, the crafting menu, or the "
            "opening questions.\n"
            "You have %d to go. They are all the same move you have already "
            "done four times." % (len(defs), 10 - len(defs))
        )


def test_several_functions_only_print():
    """The display blocks moved, and they return nothing (5 pts)."""
    tree = get_tree()
    defs = functions(tree)

    printers = [f for f in defs if prints(f) and not returns_a_value(f)]
    if len(printers) < 3:
        fail(
            "Only %d function(s) print without handing anything back. STEP 8 "
            "moves the display blocks, and those are exactly that shape:\n"
            "    def draw_progress(day, max_days):\n"
            '        print("Day " + str(day) + " of " + str(max_days))\n'
            "A function that returns nothing is still a function -- it does "
            "its work on the screen, not in a value. Three or more."
            % len(printers)
        )

    # A function taking no parameters at all is allowed, and the title screen
    # is the honest example: it needs nothing from the rest of the program.
    # Not required -- flagged only if the student has none AND few printers.
    if len(printers) < 4 and not any(
            not f.args.args and prints(f) for f in defs):
        fail(
            "The display functions all take parameters. At least one of them "
            "needs nothing from the rest of the program -- the title screen "
            "prints the same thing every time:\n"
            "    def title_screen():\n"
            "A function with an empty parameter list is normal, not a "
            "mistake."
        )


def test_a_function_hands_back_several_values():
    """An event block returns everything it changed (5 pts)."""
    tree = get_tree()

    multi = multi_returns(tree)
    # TWO, not one. try_craft() is one of Week 7's four graded functions and
    # it already hands back several values, so `if not multi` would pay this
    # row out for work done last week. Part B adds explore(), night_phase(),
    # craft_menu() and get_player_info() -- any two of those clears it.
    if len(multi) < 2:
        fail(
            "No function hands back several values at once. STEP 10 is the "
            "one that needs it: explore() changes health AND wood AND stone "
            "AND food AND water, and a function cannot reach out and change "
            "them for you.\n"
            "    def explore(health, wood, stone, iron, food, water):\n"
            "        ...\n"
            "        return health, wood, stone, iron, food, water\n"
            "and at the call site, catch them all:\n"
            "    health, wood, stone, iron, food, water = explore(\n"
            "        health, wood, stone, iron, food, water)\n"
            "Notice how long that line is. It is supposed to bother you -- "
            "a list fixes it in a couple of weeks."
        )

    # The caller has to KEEP them, or the function ran and changed nothing.
    source = get_source_code()
    if not re.search(r"^\s*\w+\s*,\s*\w+\s*,[^=\n]*=\s*\w+\s*\(",
                     source, re.M):
        fail(
            "A function hands back several values, but nothing catches them. "
            "Calling it on a line of its own throws the answer away and your "
            "resources never move:\n"
            "    explore(health, wood, ...)                  <-- discarded\n"
            "    health, wood, ... = explore(health, wood, ...)   <-- kept\n"
            "Run the game and watch a resource after exploring: if it never "
            "changes, this is why."
        )


def test_the_game_still_plays():
    """A full game runs and ends, behaving as it did before (5 pts)."""
    tree = get_tree()
    defs = functions(tree)

    # Require Part B's work before checking it did not break anything.
    # Scored alone this row pays 5/20 for changing nothing, since Week 7's
    # game already plays -- the same floor every other week sets.
    if len(defs) < 10:
        fail(
            "Nothing from Part B is in the file yet, so there is nothing to "
            "check for breakage. Your game still plays because it is still "
            "last week's game.\n"
            "Start with STEP 8 and come back to this row."
        )

    lines = output_lines()
    low = "\n".join(lines).lower()

    seen = [n for n in (1, 2, 3) if ("day " + str(n)) in low]
    if len(seen) < 3:
        fail(
            "Expected the game to play at least three days (Day 1, Day 2, "
            "Day 3 ...). Days found: %s.\n"
            "A refactor should change NOTHING about how the game plays. If "
            "it stops early, a block that moved into a function is no longer "
            "running -- check you left a CALL where the code used to be."
            % (seen or "none")
        )

    if re.search(r"^\s*None\s*$", "\n".join(lines), re.M):
        fail(
            "The game printed a bare None. A function that returns nothing "
            "is being printed:\n"
            "    print(show_status(...))     <-- prints the None it returns\n"
            "    show_status(...)            <-- what you meant\n"
            "The display functions do their work on the screen; they have "
            "nothing to hand back."
        )
