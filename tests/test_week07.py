"""
Block Builder - Week 7 Tests
Refactor into Functions (20 points)

Four tests, five points each. The names below become the scorecard rows, so
they match the grading table in weeks/week07_todo.py word for word.

A refactor is the hardest week to grade, because a correct answer looks
exactly like last week from the outside: same prompts, same numbers, same
ending. The whole change is structural, so three of these four read the
source rather than the output, and the fourth only checks that moving the
code did not break the game.

Nothing here checks function NAMES. A student who calls it `collect()`
instead of `gather()` has done the week; a test that insisted on a spelling
would be grading obedience. What is checked is that repeated blocks became
functions, that at least one hands a value back and the caller keeps it, and
that a default parameter is both declared and relied on.

The "caller keeps it" half of test two is the week's defining mistake. A
function can announce "You found 4 wood" perfectly and still leave `wood`
untouched, because printing is not returning. Checking only for a `return`
statement would pass a program whose resources never move.
"""
import ast
import subprocess
import sys
from pathlib import Path

# pytest imports this file as `tests.test_weekNN`, which does NOT put tests/ on
# the path, so `import _norich` needs the folder naming itself first.
sys.path.insert(0, str(Path(__file__).parent))
import _norich  # noqa: E402

GAME_FILE = Path(__file__).parent.parent / "game.py"

MISSING = (
    "game.py not found in the top folder of your repo. It should be next to "
    "README.md, not inside weeks/. If you are starting fresh this week, run "
    "python sync.py first."
)

# Difficulty 2, then "1" (chop wood) for every action for thirty days.
FAKE_INPUT = "TestCrafter\n2\n" + "1\n" * 600

TIMED_OUT = "TIMED_OUT"


def fail(message):
    """Fail with exactly this message and nothing else.

    `assert some_list, "..."` makes pytest append its own explanation, and the
    scorecard in conftest.py prints reprcrash.message verbatim -- so the row a
    student reads would end with "assert []". Raising skips that.
    """
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
            "Python cannot read the file, so nothing can be checked. This "
            "week the usual cause is a `def` line: it needs a colon at the "
            "end, and everything belonging to the function has to be indented "
            "underneath it."
            % (exc.lineno, exc.msg)
        )


def run_game(stdin=FAKE_INPUT):
    """Run game.py and return its stdout, or TIMED_OUT if it never finished."""
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


def functions(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def calls_of(tree, names):
    """Every call to one of `names`, as {name: [arg counts]}."""
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in names:
            out.setdefault(node.func.id, []).append(
                len(node.args) + len(node.keywords))
    return out


def returns_a_value(fn):
    """A `return expr` -- not a bare `return`, and not `return None`.

    Nested functions are not walked into: a return inside a function defined
    inside this one belongs to that one.
    """
    for node in ast.walk(fn):
        if isinstance(node, ast.Return) and node.value is not None:
            if isinstance(node.value, ast.Constant) and node.value.value is None:
                continue
            return True
    return False


def keeps_a_return_value(tree, names):
    """Is any call's result stored, or used in an expression that is stored?

    `wood = wood + gather("wood")` and `found = gather("wood")` both count.
    A bare `gather("wood")` on its own line does not -- that is the week's
    classic mistake, and the point of the check.
    """
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AugAssign)):
            continue
        for inner in ast.walk(node.value):
            if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name) \
                    and inner.func.id in names:
                return inner.func.id
    return None


def calls_from_module_level(tree, names):
    """Calls to `names` that are NOT inside a function body.

    This is what tells a refactor from a pile of unused defs: the day loop has
    to be the thing doing the calling.
    """
    inner = set()
    for fn in functions(tree):
        for node in ast.walk(fn):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                inner.add(id(node))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)                 and node.func.id in names and id(node) not in inner:
            out.append(node.func.id)
    return out


def test_the_repeated_blocks_are_functions():
    """Gathering, crafting and the status display are each a def (5 pts)."""
    tree = get_tree()
    defined = functions(tree)
    if len(defined) < 4:
        fail(
            "Found %d function definition(s); expected at least four.\n"
            "This week turns the blocks you wrote three times each into one "
            "function apiece -- gathering, the craft check, eating, and the "
            "status display are the four that repeat most.\n"
            "    def gather(resource_name):\n"
            "        ...\n"
            "Nothing checks the names. Call them what you like."
            % len(defined)
        )
    names = {fn.name for fn in defined}
    called = calls_of(tree, names)
    uncalled = sorted(names - set(called))
    if len(uncalled) > len(names) - 4:
        fail(
            "%d function(s) are defined but never called: %s.\n"
            "A refactor MOVES code -- the block comes out of the day and a "
            "call goes in where it used to be. If the old code is still "
            "sitting in the day loop as well, the function is dead weight and "
            "the game is running the copy.\n"
            "Each function needs a call: `wood = wood + gather(\"wood\")`"
            % (len(uncalled), ", ".join(uncalled[:6]))
        )


def test_functions_hand_values_back():
    """At least one function returns a value and the caller keeps it (5 pts)."""
    tree = get_tree()
    defined = functions(tree)
    if not defined:
        fail("No functions yet -- start with the first test's row.")
    returning = [fn for fn in defined if returns_a_value(fn)]
    if not returning:
        fail(
            "No function returns a value. Every one of them prints and hands "
            "nothing back.\n"
            "A function that prints is not a function that returns:\n"
            "    def gather(resource_name):\n"
            "        amount = random.randint(1, 5)\n"
            "        print(\"You found\", amount, resource_name)\n"
            "        return amount          <-- this line\n"
            "Without the return, the caller gets None and your resources "
            "never change."
        )
    kept = keeps_a_return_value(tree, {fn.name for fn in returning})
    if not kept:
        fail(
            "A function returns a value, but no caller keeps it. The result "
            "is thrown away the moment it comes back.\n"
            "    gather(\"wood\")                 <-- the number vanishes\n"
            "    wood = wood + gather(\"wood\")   <-- the number is kept\n"
            "Run your game and watch the wood count: if it never moves, this "
            "is why."
        )


def test_a_default_parameter_is_used():
    """A def supplies a default, and a call leaves it out (5 pts)."""
    tree = get_tree()
    defined = functions(tree)
    with_defaults = [fn for fn in defined if fn.args.defaults]
    if not with_defaults:
        fail(
            "No function has a default parameter. A default is a value the "
            "caller may leave out:\n"
            "    def gather(resource_name, min_amt=1, max_amt=5):\n"
            "Defaults go LAST in the parameter list -- every parameter after "
            "the first default needs one too, or Python refuses the file."
        )
    # Relying on a default is the lesson: the call is shorter than the
    # signature. Insisting a default also be OVERRIDDEN somewhere would be
    # brittle -- the reference game only overrides one of its six.
    names = {fn.name for fn in with_defaults}
    counts = calls_of(tree, names)
    for fn in with_defaults:
        required = len(fn.args.args) - len(fn.args.defaults)
        for n in counts.get(fn.name, []):
            if required <= n < len(fn.args.args):
                return
    fail(
        "A default parameter is declared but every call passes every "
        "argument anyway, so the default never does anything.\n"
        "The point of a default is the shorter call:\n"
        "    def gather(resource_name, min_amt=1, max_amt=5): ...\n"
        "    gather(\"wood\")              <-- uses both defaults\n"
        "    gather(\"iron\", 1, 2)        <-- overrides them\n"
        "Call it at least once WITHOUT the defaulted arguments."
    )


def test_the_game_still_plays():
    """A full day runs, resources change, and the ending triggers (5 pts)."""
    tree = get_tree()
    # The row means "you did not break it WHILE refactoring". Scored on its
    # own it paid 5/20 for changing nothing at all, because last week's game
    # plays perfectly -- and Weeks 5 and 6 both score 0/20 on the previous
    # week's file, so that was this week being the odd one out.
    defined = {fn.name for fn in functions(tree)}
    called = set(calls_from_module_level(tree, defined))
    if len(defined) < 2 or len(called) < 1:
        fail(
            "Nothing has been refactored yet, so there is nothing to check "
            "for breakage. Your game still plays because it is still last "
            "week's game.\n"
            "Start with the first row: move one repeated block into a `def` "
            "and call it from the day loop. Then this row checks you did it "
            "without changing how the game behaves."
        )
    source = get_source_code()
    output = run_game()
    if output == TIMED_OUT:
        fail(
            "The game never ended -- it was still running after 25 seconds.\n"
            "It worked last week, so the refactor broke the loop. The usual "
            "cause is that `day = day + 1` moved INSIDE a function: a name "
            "changed in a function is local, so the day outside never goes "
            "up and `while not game_over:` replays day 1 forever.\n"
            "Keep the day counter in the main loop, or return the new day and "
            "assign it: `day = next_day(day)`."
        )
    seen = [n for n in (1, 2, 3) if ("Day " + str(n)) in output]
    if len(seen) < 3:
        fail(
            "Expected the game to play at least three days (Day 1, Day 2, "
            "Day 3 ...). Days found: %s.\n"
            "The refactor should not have changed how the game plays. If the "
            "day loop is now calling functions that print nothing, check each "
            "one actually got its body moved into it."
            % (seen or "none")
        )
    if "max_days" not in source:
        fail(
            "No max_days variable. The survival target is what the "
            "end-of-day check compares the day against: `elif day >= "
            "max_days:` -- it should have survived the refactor untouched."
        )
