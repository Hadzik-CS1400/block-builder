"""
Block Builder - Week 6 Tests
Main Game Loop & Menus (20 points)

Four tests, five points each. The names below become the scorecard rows, so
they match the grading table in weeks/week06_todo.py word for word.

A while loop can fail in a way no earlier week could: it can never stop. So
every run here has a timeout, and a timeout is reported as the bug it almost
always is -- a missing `day = day + 1` -- rather than as a crash. That is the
most common mistake of the week and it deserves its own sentence.

Validation is read from the source. Whether a program asked twice cannot be
seen in its output: input() prints the prompt the student wrote, so there is no
fixed string to count, and a program that silently defaults to Normal reaches
Day 1 looking exactly like one that asked again. What distinguishes them is
structural -- a while loop with an input() inside it -- so that is what is
checked.
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

# Difficulty 2, then "1" (chop wood) for every action for thirty days. 30 days
# x 6 actions is 180 answers, so this is well clear -- and a game stuck on day
# 1 forever runs out of input and dies instead of filling the disk.
FAKE_INPUT = "TestCrafter\n2\n" + "1\n" * 600

# Junk first, then a usable answer. A validating program keeps asking and ends
# up on Normal; a program that defaults takes the junk and moves on.
JUNK_INPUT = "TestCrafter\nx\nnope\n9\n2\n" + "1\n" * 600


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


TIMED_OUT = "TIMED_OUT"


def run_game(stdin=FAKE_INPUT):
    """Run game.py and return its stdout, or TIMED_OUT if it never finished."""
    require_game_file()
    try:
        result = subprocess.run(
            [sys.executable, str(GAME_FILE)],
            input=stdin, capture_output=True, text=True, timeout=25,
        )
    except subprocess.TimeoutExpired:
        return TIMED_OUT
    if result.returncode != 0:
        fail("game.py crashed before it finished. Python said:\n"
             + result.stderr.strip()[-600:])
    return result.stdout


def forever_message():
    """The same explanation wherever a run fails to end."""
    return (
        "The game never ended -- it was still running after 25 seconds.\n"
        "Almost always this is the last line of the loop: `day = day + 1`.\n"
        "Without it, day stays 1, `day >= max_days` is never true, game_over "
        "is never set, and `while not game_over:` replays day 1 forever.\n"
        "Run it yourself and press Ctrl+C to stop it."
    )


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
            "week the usual cause is STEP 3: one line of the day did not get "
            "indented with the rest when it moved inside the while loop."
            % (exc.lineno, exc.msg)
        )


def while_loops(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.While)]


def calls_input(node):
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == "input" for n in ast.walk(node))


def assigns_true(tree, name):
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Constant)
                and node.value.value is True
                and any(isinstance(t, ast.Name) and t.id == name
                        for t in node.targets)):
            return True
    return False


def string_constants(tree):
    return {n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)}


def test_main_loop_plays_several_days():
    """The main loop plays more than one day (5 pts)."""
    tree = get_tree()
    if not while_loops(tree):
        fail("No while loop anywhere in game.py. The main game loop is "
             "`while not game_over:` with your whole day indented inside it.")
    output = run_game()
    if output == TIMED_OUT:
        fail(forever_message())
    seen = [n for n in (1, 2, 3) if ("Day " + str(n)) in output]
    if len(seen) < 3:
        fail(
            "Expected the game to play at least three days (Day 1, Day 2, "
            "Day 3 ...). Days found: %s.\n"
            "Is the whole day inside the while loop, and does `day = day + 1` "
            "run at the bottom of it?" % (seen or "none")
        )


def test_bad_input_is_rejected():
    """Bad input is rejected instead of defaulted (5 pts)."""
    tree = get_tree()
    validators = [w for w in while_loops(tree) if calls_input(w)]
    if len(validators) < 2:
        hint = ""
        if "default" in get_source_code().lower():
            hint = ("\nYour file still has the Week 4 \"defaulting to "
                    "Normal\" block. That is the one to replace: this week "
                    "the program asks again instead of giving up.")
        fail(
            "Found %d while loop with an input() inside it; expected at least "
            "two -- the main game loop, plus a validation loop that keeps "
            "asking until the answer is usable.\n"
            "The shape is:\n"
            "    difficulty = \"\"\n"
            "    while difficulty != \"1\" and difficulty != \"2\" and "
            "difficulty != \"3\":\n"
            "        difficulty = input(\"Enter 1, 2, or 3: \")%s"
            % (len(validators), hint)
        )
    output = run_game(JUNK_INPUT)
    if output == TIMED_OUT:
        fail(
            "The game never ended when it was given bad input first.\n"
            "A validation loop has to keep READING inside the loop. If the "
            "input() call sits above the while instead of inside it, the "
            "answer never changes and the loop spins forever."
        )
    if "Day 1" not in output:
        fail(
            "After three bad answers and then a good one, the game never "
            "reached Day 1.\n"
            "The loop should ask again for each bad answer and carry on once "
            "it gets \"1\", \"2\" or \"3\"."
        )


def test_crafting_menu_has_choices_and_a_way_out():
    """The crafting menu offers choices and a way out (5 pts)."""
    tree = get_tree()
    letters = {s.strip().lower() for s in string_constants(tree)
               if len(s.strip()) == 1}
    menu = {"a", "b", "c", "d"} & letters
    if len(menu) < 4:
        fail(
            "The crafting menu's options were not all found. Expected the "
            "letters \"a\", \"b\", \"c\" and \"d\" in the file -- found %s.\n"
            "\"d\" is Cancel, and it matters: a menu with no way out traps a "
            "player who opened it by accident."
            % (sorted(menu) if menu else "none")
        )
    if not any(assigns_true(tree, flag)
               for flag in ("has_shelter", "has_crafting_bench")):
        fail(
            "No recipe sets has_shelter or has_crafting_bench to True.\n"
            "Each recipe checks it can afford every ingredient (`and`), takes "
            "the materials off, and sets its flag so the game remembers what "
            "you built."
        )
    validators = [w for w in while_loops(tree) if calls_input(w)]
    if len(validators) < 3:
        fail(
            "Only %d while loop reads input(). By now there should be three: "
            "the main game loop, the difficulty check, the action choice, and "
            "the crafting letter -- the menu's answer gets validated the same "
            "way as the others." % len(validators)
        )


def test_game_ends_and_says_how():
    """The game ends, and says how it ended (5 pts)."""
    tree = get_tree()
    if not assigns_true(tree, "game_over"):
        fail(
            "Nothing ever sets game_over to True, so `while not game_over:` "
            "can never finish.\n"
            "At the bottom of the loop: if health has run out, or day has "
            "reached max_days, set game_over = True and tell the player which "
            "of the two happened."
        )
    source = get_source_code()
    if ("day = day + 1" not in source.replace("  ", " ")
            and "day += 1" not in source):
        fail(
            "No `day = day + 1` (or `day += 1`) found.\n"
            "This is the line that lets the loop finish: without it day stays "
            "1, max_days is never reached, and the game replays day 1 until "
            "you kill it."
        )
    output = run_game()
    if output == TIMED_OUT:
        fail(forever_message())
    if "max_days" not in source:
        fail(
            "No max_days variable. The survival target is what the end-of-day "
            "check compares the day against: `elif day >= max_days:`"
        )
