"""
Block Builder - Week 10 tests
Lists & Dictionaries (20 points)

Five tests, four points each. The names below become the scorecard rows, so
they match the grading table in weeks/week10_todo.py word for word.

This is the one week that carries two modules, because the game spent the
term a module behind the lectures and catches up here. Lists and dictionaries
are graded together.

Every row asks two questions where it can: is the construct in the source,
and did the game actually PRINT something that proves it ran. A student can
write a comprehension, never call the function holding it, and have a game
that behaves exactly as it did last week -- the source check alone passes
that.

This week's trap is `journal = journal.append(x)`. .append() changes the list
and hands back None, so that line throws the journal away and raises nothing.
It is checked explicitly, because the symptom turns up somewhere else
entirely.

Nothing checks your function NAMES or your wording.
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

# Difficulty 2, then "1" (chop wood) for every action for thirty days.
FAKE_INPUT = "TestCrafter\n2\n" + "1\n" * 600

TIMED_OUT = "TIMED_OUT"

RESOURCES = ("wood", "stone", "iron", "food", "water")


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
            "week the usual cause is a bracket: every { needs its }, and a "
            "dictionary wants a colon between the name and the value."
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


def output_lines():
    out = run_game()
    if out == TIMED_OUT:
        fail(
            "The game never ended -- it was still running after 25 seconds.\n"
            "It worked last week, so something added this week did not stop. "
            "Check that nothing inside the day loop reads input() without a "
            "way out, and that `day = day + 1` is still running."
        )
    return out.splitlines()


def dict_literals(tree, min_keys=1, values_are_dicts=False, allow_names=False):
    """Dictionary literals, optionally ones whose values are themselves dicts.

    `allow_names` counts a key that is a NAME as well as one that is a string
    literal. STEP 3 has students pull the recipe names out into constants --
    PICKAXE = "pickaxe" -- so that a mistyped name is a NameError instead of
    a silent False. Those constants then key RECIPES, and a check that only
    recognised string literals would have told a student who did exactly what
    was asked that their recipe book "is still code rather than data".
    """
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = [k for k in node.keys
                if (isinstance(k, ast.Constant) and isinstance(k.value, str))
                or (allow_names and isinstance(k, ast.Name))]
        if len(keys) < min_keys:
            continue
        if values_are_dicts:
            inner = [v for v in node.values if isinstance(v, ast.Dict)]
            if len(inner) < 2:
                continue
        found.append(node)
    return found


def aligned_specs(call):
    """Format specifiers in this call that pad to a width: :<12, :>5, :^50."""
    out = []
    for node in ast.walk(call):
        if isinstance(node, ast.FormattedValue) and node.format_spec is not None:
            text = "".join(p.value for p in node.format_spec.values
                           if isinstance(p, ast.Constant))
            if any(c in text for c in "<>^"):
                out.append(text)
    return out


def prints_literal_rows(fn):
    """Types the labels out: print(f"  {'Wood:':<12} {wood:>5}")."""
    labelled = set()
    for call in [c for c in ast.walk(fn)
                 if isinstance(c, ast.Call) and getattr(c.func, "id", "") == "print"]:
        for node in ast.walk(call):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                for r in RESOURCES:
                    if re.search(r"\b%s\s*:" % r, node.value, re.I):
                        labelled.add(r)
    return len(labelled) >= 4


def prints_rows_from_data(fn):
    """Loops a collection and prints one ALIGNED row per entry.

    The alignment is what separates a status row from prose. try_craft() also
    loops `costs.items()` and prints the resource name, but it prints a
    sentence -- no width, no column -- so it is not a second status panel and
    must not be counted as one.
    """
    for loop in [n for n in ast.walk(fn) if isinstance(n, ast.For)]:
        bound = {t.id for t in ast.walk(loop.target) if isinstance(t, ast.Name)}
        for call in [c for c in ast.walk(loop)
                     if isinstance(c, ast.Call) and getattr(c.func, "id", "") == "print"]:
            if not aligned_specs(call):
                continue
            used = {n.id for n in ast.walk(call) if isinstance(n, ast.Name)}
            if used & bound:
                return True
    return False


def status_panels(tree):
    """Functions that print the resource rows, however they spell it.

    No function NAMES are used -- a student who called theirs show_the_stuff()
    is not penalised.
    """
    return [fn.name for fn in ast.walk(tree)
            if isinstance(fn, ast.FunctionDef)
            and (prints_literal_rows(fn) or prints_rows_from_data(fn))]


# ---------------------------------------------------------------------------
# The five scored tests
# ---------------------------------------------------------------------------


def test_the_journal_is_a_list():
    """The journal is a real list, appended to and sliced (4 pts)."""
    tree = get_tree()

    appends = [n for n in ast.walk(tree)
               if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "append"]
    if not appends:
        fail(
            "Nothing calls .append(). The journal stops being one long string "
            "this week and becomes a list:\n"
            "    journal = []\n"
            '    journal.append(f"Day {day}: {event}")\n'
            "That is STEP 1, and the rest of the week leans on it."
        )

    # journal = journal.append(x) is this module's defining mistake: it
    # appends, returns None, and the journal is gone with no error raised.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Attribute) \
                and node.value.func.attr in ("append", "sort", "extend",
                                             "insert", "remove", "reverse"):
            fail(
                "A list method's return value is being stored:\n"
                "    journal = journal.%s(...)\n"
                "Those methods change the list and hand back None, so this "
                "replaces your journal with None -- and nothing raises an "
                "error until something else tries to use it. Call it on a "
                "line of its own:\n"
                "    journal.%s(...)"
                % (node.value.func.attr, node.value.func.attr)
            )

    if not [n for n in ast.walk(tree) if isinstance(n, ast.Slice)]:
        fail(
            "Nothing is sliced. STEP 2 shows only the end of the journal:\n"
            '    "; ".join(journal[-3:])\n'
            "[-3:] means \"from three before the end, to the end\", and it is "
            "safe on a list of one."
        )

    # It has to actually run: a journal built and never shown is invisible.
    out = "\n".join(output_lines())
    if not re.search(r"Day \d+\s*:", out, re.I):
        fail(
            "The game ran, but nothing printed that looks like a journal "
            "entry -- something naming a day, like \"Day 4: Mob attack\".\n"
            "Is add_journal being CALLED, and is the journal shown at the end?"
        )


def test_resources_and_recipes_are_dictionaries():
    """Loose variables become a player dict; recipes become data (4 pts)."""
    tree = get_tree()

    player_like = [d for d in dict_literals(tree, min_keys=4)
                   if sum(1 for k in d.keys
                          if isinstance(k, ast.Constant)
                          and str(k.value).lower() in RESOURCES) >= 3]
    if not player_like:
        fail(
            "No dictionary holds the resources. STEP 4 replaces the separate "
            "variables with one dict, keyed by name:\n"
            '    player = {"health": 100, "wood": 10, "stone": 5,\n'
            '              "iron": 0, "food": 10, "water": 10}\n'
            "Then  wood = wood + 3  becomes\n"
            '    player["wood"] = player["wood"] + 3'
        )

    nested = dict_literals(tree, min_keys=2, values_are_dicts=True,
                           allow_names=True)
    if not nested:
        fail(
            "The recipe book is still code rather than data. STEP 6 writes "
            "the recipes as a dictionary whose values are themselves "
            "dictionaries:\n"
            '    RECIPES = {\n'
            '        PICKAXE: {"wood": 3, "stone": 2},\n'
            '        SHELTER: {"wood": 20, "stone": 10},\n'
            '    }\n'
            "Then try_craft looks the costs up instead of taking one "
            "parameter per ingredient."
        )

    gets = [n for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == "get"]
    if not gets:
        fail(
            "Nothing uses .get(). It matters in try_craft: the pickaxe recipe "
            "never mentions iron, so a player who has never held iron has no "
            '"iron" key, and player["iron"] raises KeyError and ends the '
            "game.\n"
            '    player.get(resource, 0)   hands back 0 instead'
        )

    items = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and n.func.attr == "items"]
    if not items:
        fail(
            "Nothing uses .items(). Looping a dictionary plainly gives you "
            "only its keys; .items() gives you the key AND the value:\n"
            "    for name, amount in player.items():\n"
            "STEP 6 and STEP 8 both need it."
        )


def test_a_comprehension_picks_out_what_is_low():
    """A filtered dict comprehension finds what is running out (4 pts)."""
    tree = get_tree()
    comps = [n for n in ast.walk(tree)
             if isinstance(n, ast.DictComp) and any(g.ifs for g in n.generators)]
    if not comps:
        plain = [n for n in ast.walk(tree) if isinstance(n, ast.DictComp)]
        if plain:
            fail(
                "There is a dict comprehension, but nothing filters it. The "
                "`if` is what makes it pick things out:\n"
                "    low = {name: amount for name, amount in player.items()\n"
                "           if name != \"health\" and amount < 5}"
            )
        fail(
            "No dict comprehension yet. STEP 7 builds a small dictionary of "
            "just the resources running out:\n"
            "    low = {name: amount for name, amount in player.items()\n"
            "           if name != \"health\" and amount < 5}\n"
            "Same shape as the list comprehension from Module 8, but it "
            "builds `name: amount` pairs -- note the colon."
        )


def test_the_resource_rows_are_printed_in_one_place():
    """The status rows are written once and called, not copied (4 pts)."""
    tree = get_tree()
    # "Zero panels" is not "more than one", so without this gate a file that
    # has not started the week collects the row for free -- the week 2 answer
    # key scored 4/20 on week 10 that way, for a game written in September.
    if not dict_literals(tree, min_keys=4) and not [
            n for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == "append"]:
        fail(
            "Nothing from this week is in the file yet, so there is nothing "
            "to check for duplication. Start with STEP 1 and come back to "
            "this row -- STEP 8 is the one it grades."
        )
    panels = status_panels(tree)
    if len(panels) > 1:
        fail(
            "The resource rows are printed in %d separate places: %s.\n"
            "Both of your status displays list the resources, so every change "
            "to a width has to be made twice -- which is how two panels that "
            "should match stop matching.\n"
            "STEP 8 writes them once, as a loop over the dictionary, and has "
            "both displays call it. Keep the header, the health line and the "
            "warnings where they are; only the resource rows move."
            % (len(panels), ", ".join(panels))
        )
    # There is deliberately no "at least one panel must exist" check. Once the
    # rows are printed from the dict the labels come out of the data, so the
    # words "wood" and "food" need not appear in the source at all, and a
    # presence check would fail the very refactor this row asks for.
    # test_the_journal_is_a_list already requires the game to print, and
    # test_the_game_still_plays requires it to finish.


def test_the_game_still_plays():
    """A full game runs, ends, and this week's work is in it (4 pts)."""
    tree = get_tree()
    source = get_source_code()
    # Require this week's work to exist before checking it did not break the
    # game. Scored alone the row pays 4/20 for changing nothing at all, since
    # last week's game plays perfectly.
    if not dict_literals(tree, min_keys=4) and ".append(" not in source:
        fail(
            "Nothing from this week is in the file yet, so there is nothing "
            "to check for breakage. Your game still plays because it is still "
            "last week's game.\n"
            "Start with STEP 1: make the journal a list."
        )
    lines = output_lines()
    low = "\n".join(lines).lower()
    seen = [n for n in (1, 2, 3) if ("day " + str(n)) in low]
    if len(seen) < 3:
        fail(
            "Expected the game to play at least three days (Day 1, Day 2, "
            "Day 3 ...). Days found: %s.\n"
            "Nothing this week changes a rule -- only where the numbers are "
            "kept -- so the game should play exactly as it did." % (seen or "none")
        )
    if "max_days" not in source:
        fail(
            "No max_days variable. The survival target is what the end-of-day "
            "check compares the day against, and it should have survived this "
            "week untouched."
        )
