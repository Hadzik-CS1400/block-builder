"""
Block Builder - Week 9 Tests
Formatted Displays & Journal (20 points)

Five tests, four points each. The names below become the scorecard rows, so
they match the grading table in weeks/week09_todo.py word for word.

The fifth is STEP 7's `# FOUND:` note. It is the odd one out: the other four
check what the program does, and that one checks that the student wrote down
what they saw when they tried to break it. STEP 7 changes no code, so there
would otherwise be nothing to grade and the step would be marked on trust.

There is no Week 8. Week 8 of the course is midterm week and carries no game
session, so the sequence runs Week 7 -> Week 9. That is deliberate.

This week is the first that can be graded mostly on OUTPUT rather than
source, because formatting is visible: a column that does not line up is a
column that does not line up. So three of these four read what the program
printed, and only the journal test reads the source -- because a journal
that is built correctly and never shown looks identical to no journal at
all from the outside.

Nothing checks your wording. The status panel can say anything it likes; the
tests look at whether the numbers form a column, whether a header was
shouted, and whether days are being recorded.
"""
import ast
import re
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
            "week the usual cause is an f-string: every { needs a matching }, "
            "and a quote inside an f-string has to differ from the quotes "
            "around it."
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


def labelled_numbers(lines):
    """Lines that look like a status row: some label, then a number.

    Returns {column of the number's last digit: [lines]}, which is what
    tells an aligned column from a ragged one.
    """
    found = {}
    for line in lines:
        m = re.match(r"^\s*\S.*?(\d+)\s*$", line.rstrip())
        if m and not line.strip().startswith("Day"):
            found.setdefault(len(line.rstrip()), []).append(line)
    return found


def fstrings(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.JoinedStr)]


def specs(tree):
    """Every format specifier used in an f-string."""
    out = []
    for fs in fstrings(tree):
        for v in fs.values:
            if isinstance(v, ast.FormattedValue) and v.format_spec is not None:
                out.append("".join(
                    p.value for p in v.format_spec.values
                    if isinstance(p, ast.Constant) and isinstance(p.value, str)))
    return out


def test_the_status_panel_lines_up():
    """The status numbers form a column, not a ragged edge (4 pts)."""
    tree = get_tree()
    aligned = [s for s in specs(tree) if any(c in s for c in "<>^")]
    if not aligned:
        fail(
            "No alignment specifiers anywhere. A width and a direction are "
            "what turn a ragged list into a column:\n"
            "    print(f\"  {'Health:':<12} {health:>5}\")\n"
            "Text left, numbers right -- that is what lines the digits up."
        )
    if len(aligned) < 4:
        fail(
            "Found %d aligned field(s). The status panel has a row for each "
            "of health, food, water, wood, stone and iron, and every row "
            "needs a width on the label AND on the number:\n"
            "    print(f\"  {'Food:':<12} {food:>5}\")"
            % len(aligned)
        )
    # Now look at what it actually printed: aligned rows end in the same column.
    columns = labelled_numbers(output_lines())
    if not columns:
        fail(
            "The game ran, but nothing printed that looks like a status row "
            "-- a label followed by a number. Is show_status being CALLED "
            "inside the day loop, and not just defined?"
        )
    best = max(len(v) for v in columns.values())
    if best < 4:
        fail(
            "The status rows do not line up. The longest run of rows ending "
            "in the same column is %d, and the panel has at least six rows.\n"
            "A width on the number is what does it: {health:>5} reserves five "
            "characters whatever the number, so 7 and 100 end in the same "
            "place." % best
        )


def test_a_header_is_shouted_and_centered():
    """A header uses .upper() and is centered in the panel (4 pts)."""
    tree = get_tree()
    source = get_source_code()
    if ".upper()" not in source:
        fail(
            "Nothing calls .upper(). Part of this week is making the panel "
            "header stand out without retyping it in capitals:\n"
            "    header = f' {name}'s World - Day {day} '.upper()\n"
            "Typing the capitals yourself does not count -- the point is that "
            "the method does it to whatever the player named themselves."
        )
    centered = [s for s in specs(tree) if "^" in s]
    if not centered:
        fail(
            "Nothing is centered. ^ centers a value in a width, and a "
            "character before it fills the space:\n"
            '    print(f"{header:=^50}")\n'
            "That draws the header with = running out to both edges."
        )
    out = "\n".join(output_lines())
    if not re.search(r"[A-Z]{4,}", out):
        fail(
            ".upper() and a centered field are both in the file, but nothing "
            "in the output is actually in capitals. Is the shouted header "
            "being printed?"
        )


def test_the_journal_records_the_day():
    """Events are recorded against a day number and can be shown (4 pts)."""
    tree = get_tree()
    source = get_source_code()
    if "journal" not in source.lower():
        fail(
            "No journal yet. This week the game keeps a record of what "
            "happened, built up as a string:\n"
            '    entry = f"Day {day}: {event}"\n'
            '    journal = journal + "|" + entry\n'
            "A list would be the obvious tool and you do not have it yet -- "
            "a delimiter character does the same job."
        )
    # The entry has to carry the day, or it is a list of events with no when.
    day_in_entry = False
    for fs in fstrings(tree):
        names = {n.id for n in ast.walk(fs) if isinstance(n, ast.Name)}
        text = "".join(p.value for p in fs.values
                       if isinstance(p, ast.Constant) and isinstance(p.value, str))
        if "day" in names and ("Day" in text or "day" in text):
            day_in_entry = True
    if not day_in_entry:
        fail(
            "Nothing builds an entry that names the day. A journal line has "
            "to say WHEN:\n"
            '    entry = f"Day {day}: {event}"\n'
            "Without the day it is a pile of events in no order."
        )
    if ".split(" not in source:
        fail(
            "The journal is being built but never taken apart. Showing it "
            "back means splitting on the delimiter you joined with:\n"
            '    for entry in journal.split("|"):\n'
            "        print(entry)"
        )


def test_the_game_still_plays():
    """A full game runs and ends, with the new display in it (4 pts)."""
    source = get_source_code()
    # Require this week's work to exist before checking it did not break the
    # game. Scored alone the row paid 5/20 for changing nothing at all, since
    # last week's game plays perfectly -- and Weeks 5, 6 and 7 all score 0/20
    # against the previous week's file.
    tree = get_tree()
    if not [x for x in specs(tree) if any(c in x for c in "<>^")]             and "journal" not in source.lower():
        fail(
            "Nothing from this week is in the file yet, so there is nothing "
            "to check for breakage. Your game still plays because it is "
            "still last week's game.\n"
            "Start with the status panel: give each row a width on the label "
            "and on the number, then come back to this row."
        )
    lines = output_lines()
    out = "\n".join(lines)
    # Case-insensitive on purpose: this week's own header is shouted with
    # .upper(), so the day marker prints as "DAY 2". Searching for "Day 2"
    # made a correct answer look like a game that never reached day two.
    low = out.lower()
    seen = [n for n in (1, 2, 3) if ("day " + str(n)) in low]
    if len(seen) < 3:
        fail(
            "Expected the game to play at least three days (Day 1, Day 2, "
            "Day 3 ...). Days found: %s.\n"
            "The formatting work this week should not have changed how the "
            "game plays." % (seen or "none")
        )
    if "max_days" not in source:
        fail(
            "No max_days variable. The survival target is what the end-of-day "
            "check compares the day against, and it should have survived this "
            "week untouched."
        )
    # Repetition is how the panel's rules and bars get drawn.
    if not re.search(r"[\"'][^\"']+[\"']\s*\*\s*\d+|\d+\s*\*\s*[\"'][^\"']+[\"']",
                     source):
        fail(
            "Nothing repeats a string. The panel's rules and the survival bar "
            "are both built that way:\n"
            '    print("=" * 50)\n'
            "    print(f\"[{'=' * filled}{'-' * (30 - filled)}]\")"
        )
    # The bar has to SHOW, and that is not the same question as whether the
    # code that builds it is there. It is drawn inside square brackets, and
    # rich reads [#...] as a hex colour -- so a bar filled with "#" is
    # swallowed whole, printing "Survival:  23%" with no bar and no error.
    # No other row here would notice: the bar line ends in "%", so the
    # column check in the first test skips it. This is the only row that looks
    # at the bar, which is how a "#" bar stayed invisible through a release.
    if not [ln for ln in lines if re.search(r"\[[-=*+#o ]{6,}\]", ln)]:
        # The scorecard shows only the first three wrapped lines of this, so
        # the fix has to come first and the reason second -- not the other way
        # round, which is how it read until a student would have lost it.
        fail(
            "The survival bar never shows. Change its fill from '#' to '=': "
            "rich reads [#...] as a colour and swallows the whole bar.\n"
            "    [{'#' * filled}...]   <- vanishes\n"
            "    [{'=' * filled}...]   <- prints\n"
            "Your game prints through rich, which reads [...] as a style tag "
            "and [#ff0000] as a hex colour. A bar starting [### looks like a "
            "colour to it, so it prints nothing at all and reports no error. "
            "* and + work too; a block character crashes on Windows."
        )


def test_you_tried_to_break_it():
    """STEP 7's note: one line recording what the layout did (4 pts).

    STEP 7 is five deliberate inputs aimed at the formatting -- spaces round
    the name, a 40-character name, a number crossing 9 to 10, max_days set to
    3, an empty journal. None of them change the code, so nothing in game.py
    would show they ever happened.

    So the step asks for a sentence, and this looks for it. It cannot prove a
    student ran anything, and does not pretend to: the same is true of CT08's
    `# WHY:` note, which this copies. Writing down what you saw is most of the
    value, and the alternative is marking the step on trust.
    """
    source = get_source_code()
    for raw in source.split("\n"):
        line = raw.strip()
        if not line.startswith("#"):
            continue
        body = line.lstrip("#").strip()
        if body.upper().startswith("FOUND:") and body.split(":", 1)[1].strip():
            return
    fail(
        "No `# FOUND:` note. STEP 7 asks you to try five things that attack "
        "the layout, then write ONE line in game.py saying what you found:\n"
        "    # FOUND: a 40-character name runs the header past 50 and\n"
        "    #        stops it centering\n"
        "Anything after the colon counts. An empty `# FOUND:` does not -- "
        "the sentence is the point, the same as the `# WHY:` note in CT08."
    )
