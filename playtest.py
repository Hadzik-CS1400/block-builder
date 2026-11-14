"""
playtest.py - play your program for you, many times, and report what broke.

===========================================================================
EVERY COMMAND
===========================================================================

    python playtest.py
        List the scripts you have, and suggest one to start with. Does not
        run anything.

    python playtest.py all
        Run EVERY script, 6 runs each. This is the one to run before you
        hand anything in. Ends with the coverage table for the whole suite.

    python playtest.py all 20
        Every script, but 20 runs each instead of 6.

    python playtest.py all --show
        Every script, played in full with every question and answer printed.
        Long on purpose: it is how you prove to somebody (or to yourself)
        that your program really is being driven.

    python playtest.py normal
        One script - plays/normal.txt - 20 runs.

    python playtest.py normal 50
        That script, 50 runs.

    python playtest.py normal --show
        ONE run of that script, printed line by line with the answers shown
        where they were typed. The one to use when something is going wrong
        and you want to see it happen.

    python playtest.py normal --sweep
        Every value every random draw in the program can produce, forced one
        at a time. Running many times SAMPLES the random numbers; this covers
        them. Slower -- one game per value -- and it answers a different
        question: not "did anything break this time" but "which values break
        it, and are there any others".

    -s        is the short form of --show.
    EXIT CODE is 0 when everything passed and 1 when anything crashed,
              stalled or jammed, so this can gate a commit or a hand-in.

===========================================================================
WHAT YOU SEE WHILE IT RUNS
===========================================================================

    .   the run finished              x   it crashed - you get the error,
    !   it never got going                the file and the line number
    ?   it ran out of time (30s)

Every run ends with a table of the questions your program asked and the
answers your scripts gave. A question that only ever heard ONE answer has
not been tested - it has been visited.

===========================================================================
WHY THIS EXISTS
===========================================================================

Clicking through your own program to find a bug is slow, and it is worse
than slow: you tend to press the same keys every time. If you always pick
option 1, you only ever test option 1. A bug in option 4 will sit there for
weeks looking like nothing is wrong.

This runs the program for you with the answers read from a file, so you can
say "try every menu option" and watch what happens.

It also runs it MANY times, which matters more than it sounds. If your
program uses random numbers, the same answers do not give the same run. A
bug that needs an unlucky draw might appear once in five. Running once and
seeing nothing proves very little.

===========================================================================
THE SCRIPTS - what you actually write
===========================================================================

plays/normal.txt and the rest are lists of answers, one per line. Open one;
there is nothing clever in it.

    - Everything up to a "#" is typed at your program exactly as written.
      Anything after the "#" is a note for you and is never typed:

          5     # action menu - explore
          1     # explore's "1 or 2" - take the risky option

      --show prints your note beside the answer, so a file that explains
      itself stays readable next month.
    - Blank lines are skipped.
    - The file REPEATS. If your program asks more questions than the file
      has answers, it starts again from the top. That is why a one-line file
      is legal and useful - and why a file that never reaches your quit
      option never ends.
    - A file whose name starts with "_" is settings, not a script, and is
      left out of the listing. plays/_player.txt is the only one.

Write your own: make plays/myplan.txt, put the answers in it, and run
    python playtest.py myplan

===========================================================================
plays/_player.txt - answers given BEFORE your script starts
===========================================================================

Some programs open by asking something every run has to answer the same way
- Block Builder asks for a name and a difficulty. Those live here instead of
at the top of every script, so the scripts stay readable.

    line 1       the name
    lines 2+     one difficulty per line, rotated across runs

An EMPTY file means "this program asks nothing before the script starts",
which is the normal case for a final project. A MISSING file falls back to
built-in Block Builder defaults, which is wrong for anything else - so if
your program does not open with fixed questions, create the file and leave
it empty.

===========================================================================
READING THIS FILE
===========================================================================

You do not have to. Nothing here is on any test, and you should not edit it
- a change here affects every script you run.

But it is commented line by line in case you want to, because it is a real
program doing a real job with the things you have been learning: lists,
dictionaries, sets, file reading, string methods, try/except, and functions
that hand things back to each other. If you ever wondered what your own code
could grow into, this is roughly that size.

The journey, start to finish:

    your plays file
        -> a list of answers            build_answers()
        -> one long string of them      build_answers()
        -> typed at your program        play_once() + RUNNER
        -> a record of every Q and A    RUNNER, written to stderr
        -> pulled apart from crashes    split_records()
        -> one dictionary of answers    run_all()
        -> the table you read           coverage()
"""
# All six ship with Python. Nothing to install.
import ast                        # read code as a structure, without running it
import re                         # find the file and line inside a crash message
import subprocess                 # run game.py separately, and catch its output
import sys                        # this Python: executable, argv, stderr, exit
from collections import Counter   # count repeats: spots a question asked 1000x
from pathlib import Path          # paths that work on Windows and on a Mac

r""" WHAT "HERE" IS DOING - it is the folder THIS FILE is sitting in

    Say your repo lives in C:\CS1400\block-builder, and from C:\CS1400 you
    typed:   python block-builder\playtest.py

      __file__    the path Python was handed, just as you typed it:
                                  block-builder\playtest.py
      .resolve()  fills in front: C:\CS1400\block-builder\playtest.py
      .parent     drops the file: C:\CS1400\block-builder      <-- HERE

    so PLAYS, which is HERE / "plays", comes out as
                                  C:\CS1400\block-builder\plays
    and your game.py sits next to it, at
                                  C:\CS1400\block-builder\game.py

    Paste either into File Explorer and it opens. HERE is never the folder
    you were standing in when you typed the command, which is exactly why
    this works from anywhere.
"""
HERE = Path(__file__).resolve().parent  # EX: C:\CS1400\block-builder
PLAYS = HERE / "plays"                  # EX: C:\CS1400\block-builder\plays


def find_program():
    """Work out which .py file we are supposed to be testing.

    Takes:
        nothing

    Hands back:
        a Path to the program, or None when it cannot tell

    Prefers game.py if there is one. Otherwise, if there is exactly one
    other .py file beside this one, that must be it. Two or more and it
    gives up rather than guess, and main() prints what it found instead.

    Hardcoding game.py meant the first step of reusing this on any other
    project was editing it -- and students are told not to edit it.
    """
    if (HERE / "game.py").exists():
        return HERE / "game.py"
    # glob("*.py") finds every Python file in this folder. We drop
    # playtest.py itself -- Path(__file__) is "the file I am written in".
    others = [p for p in sorted(HERE.glob("*.py")) if p.name != Path(__file__).name]
    return others[0] if len(others) == 1 else None


GAME = find_program()  # EX: C:\CS1400\block-builder\game.py

# "game" is wrong on a final project and "program" reads oddly in Block
# Builder, so the noun follows the file being tested. Cosmetic only -- nothing
# below branches on it except the words it prints.
IS_GAME = GAME is not None and GAME.name == "game.py"
THING = "game" if IS_GAME else "program"
THINGS = "games" if IS_GAME else "runs"
TITLE = "Block Builder - playtest" if IS_GAME else "playtest"

# Terminal colour codes. "\033[" starts a display instruction, the number
# picks it, "m" ends it. Swap a number: 91 red, 92 green, 93 yellow, 94 blue,
# 95 magenta, 96 cyan. Nothing below cares what you choose.
GREEN  = "\033[92m"   # it worked - a game that ran, a script that came back
YELLOW = "\033[93m"   # worth a look - a warning, or a draw never reached
RED    = "\033[91m"   # it broke - the crash, and the line that caused it
DIM    = "\033[2m"    # grey - asides, quoted source, the small print
BOLD   = "\033[1m"    # headings and totals: the line to read first
OFF    = "\033[0m"    # back to normal. Every colour above MUST end with this

DEFAULT_RUNS = 20
ALL_RUNS = 6         # per script when running them all
OURS = {}            # prompts answered from plays/_player.txt
SETUP_COUNT = [2]    # how many of those there are, set at run time
MAX_ANSWERS = 4000          # a game that wants more than this is stuck
TIMEOUT = 30                # seconds for one game

# --show runs the game through this instead of running it directly, so every
# answer appears where it was read. input() writes its prompt without a
# newline and a piped answer is never echoed, which is why a normal run shows
# questions with nothing after them.
#
# Echoing beats trying to work the answers out from the output afterwards. An
# earlier version did that by looking for lines that ended in a space, and
# found 3 of roughly 150 -- because the game usually prints the RESULT of an
# action onto the end of the prompt's own line.
#
# MARK is a character the game will never print, so the echo can be told from
# whatever the prompt said and coloured separately.
MARK = "\x01"

# Every run goes through this. It replaces input() inside the game, so it sees
# the prompt STRING -- which is what makes the coverage report possible without
# knowing anything about this particular game's menus.
#
# The record goes to stderr so stdout stays exactly what the game printed.
# The echo (MARK) is only added for --show.
RECORD = "\x02"
RUNNER = (
    "import builtins, runpy, sys\n"
    "echo = len(sys.argv) > 2\n"
    "_read = builtins.input\n"
    "def _ask(prompt=''):\n"
    "    value = _read(prompt)\n"
    "    sys.stderr.write('\\x02' + str(prompt).strip() + '\\x02' + value + '\\n')\n"
    "    if echo:\n"
    "        print('\\x01' + value)\n"
    "    return value\n"
    "builtins.input = _ask\n"
    "runpy.run_path(sys.argv[1], run_name='__main__')\n"
)


def split_records(stderr_text):
    """Separate our own bookkeeping from whatever else landed on stderr.

    Takes:
        stderr_text  str -- everything the run wrote to stderr

    Hands back:
        a tuple of (asked, leftover)
          asked     a list of (prompt, answer) pairs, in the order asked
          leftover  str -- every other line, joined back together

    The leftover is not rubbish: it is where a traceback lives. Throwing it
    away would mean reporting a clean run on a program that died.
    """
    # Two empty lists, filled as we walk the lines: one for our own
    # records, one for everything else.
    asked, leftover = [], []
    for line in stderr_text.splitlines():
        # RECORD is a character no program prints, so a line that starts
        # with it can only be one we wrote ourselves.
        if line.startswith(RECORD):
            parts = line.split(RECORD)
            # "\x02Choose:\x021" splits into ["", "Choose:", "1"] -- three
            # pieces. Fewer means the line was cut short, so we leave it alone.
            if len(parts) >= 3:
                asked.append((parts[1], parts[2]))
                continue
        leftover.append(line)
    return asked, "\n".join(leftover)


# --sweep needs a different wrapper from the one above. It still answers
# input() from the script, but it also seeds the program and can FORCE one
# random draw to one value.
#
# Why the seed: while one call is forced, every other call must be pinned, or
# an unlucky draw somewhere else gets blamed on the value being forced. The
# demo version of this reported a harmless roll as a bug before the seed was
# added, with a real traceback behind it.
#
# target of -1 forces nothing, which is how the call sites are discovered.
RAND = chr(4)
RAND_RUNNER = (
    "import builtins, random, runpy, sys, inspect\n"
    "target, forced = int(sys.argv[2]), int(sys.argv[3])\n"
    "random.seed(0)\n"
    "_real_rand = random.randint\n"
    "def swept(low, high):\n"
    "    caller = inspect.currentframe().f_back\n"
    "    if caller.f_lineno == target and low <= forced <= high:\n"
    "        value = forced\n"
    "    else:\n"
    "        value = _real_rand(low, high)\n"
    "    sys.stderr.write(chr(4) + '%d|%d|%d' % (caller.f_lineno, low, high)"
    " + chr(10))\n"
    "    return value\n"
    "random.randint = swept\n"
    "runpy.run_path(sys.argv[1], run_name='__main__')\n"
)

# A range wider than this is not worth trying one value at a time.
SWEEPABLE = 60


def say(msg="", color=""):
    """Print one line, optionally wrapped in a colour code.

    Takes:
        msg    str -- the text. Default "", which prints a blank line
        color  str -- an ANSI colour constant, or "" for no colour

    Hands back:
        None -- it prints

    The OFF code is always added when a colour was used, so a colour can
    never leak onto the lines that follow.
    """
    print(f"{color}{msg}{OFF}" if color else msg)


def rule():
    """Print a dim horizontal line, to separate sections of the report.

    Takes:
        nothing

    Hands back:
        None -- it prints
    """
    say("-" * 62, DIM)


def die(*lines):
    """Print an error the student can act on, then stop the program.

    Takes:
        *lines  any number of strings. The FIRST is the headline and is
                printed in red; the rest are printed under it as advice

    Hands back:
        nothing -- it never returns, because it calls sys.exit(1)

    Every exit from this script goes through here, so an error always looks
    the same and always says what to do next.
    """
    say()
    rule()
    say(f"  {lines[0]}", RED + BOLD)
    rule()
    for line in lines[1:]:
        say(f"  {line}")
    say()
    sys.exit(1)


def available():
    """List the play scripts the student has written.

    Takes:
        nothing

    Hands back:
        a sorted list of names WITHOUT the .txt, e.g. ["badinput", "normal"]

    A leading underscore means "not a script". That is how _player.txt stays
    out of the listing while living in the same folder.
    """
    if not PLAYS.is_dir():
        return []
    # .stem is the filename without its extension, so normal.txt
    # becomes "normal" -- which is what a student types.
    return sorted(p.stem for p in PLAYS.glob("*.txt")
                  if not p.name.startswith("_"))


def read_player():
    """Read the answers that come before the script starts.

    Takes:
        nothing

    Hands back:
        a tuple of (player, levels)
          player  str -- the name to answer first, or "" for none
          levels  a list of difficulties to rotate through, one per run

    An EMPTY plays/_player.txt is an answer, not an absence: it means this
    program asks nothing before the script. Only a MISSING file falls back
    to the built-in defaults.
    """
    setup = PLAYS / "_player.txt"
    if setup.exists():
        with open(setup, encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        # An EMPTY file is an answer, not an absence: it means this program
        # asks nothing before the script starts. Falling back to a name here
        # fed "PlayTester" to a budget tracker's main menu, which rejected it
        # forever. Only a MISSING file takes the defaults.
        return (lines[0] if lines else ""), (lines[1:] or [""])
    return "PlayTester", ["1", "2", "3"]


def read_script(path):
    """Read a plays file into (answer, note) pairs.

    Everything from a # to the end of the line is a note for the reader and
    is never typed at the program. That is what lets a plays file explain
    itself:

        9     # action menu - not a valid choice, so it asks again
        1     # action menu - chop wood

    Notes are not decoration. --show prints them instead of "line 4 of the
    file", so the person watching sees what each answer was FOR rather than
    where it lived.

    One reader for every caller. There were four separate readers before this,
    which is four chances for one of them to forget that # is a comment.
    """
    pairs = []
    with open(path, encoding="utf-8") as answers_file:
        for line in answers_file:
            answer, _, note = line.partition("#")
            answer, note = answer.strip(), note.strip()
            if answer:
                pairs.append((answer, note))
    return pairs


def build_answers(script, player, difficulty):
    """Turn one plays file into the keystrokes a single run will type.

    Takes:
        script      a Path to the plays/<name>.txt file to read
        player      str -- the name answered first, or "" for none
        difficulty  str -- the difficulty answered next, or "" for none

    Hands back:
        str -- every answer joined with newlines, ending with one

    The file is repeated until there are MAX_ANSWERS of them. That is what
    lets a one-line script be a real script, and it means a run can never
    end early for the boring reason of running out of answers.
    """
    # Module 10 teaches exactly these three lines: `with` closes the file
    # whatever happens, `for line in answers_file` reads it one line at a
    # time, and .strip() takes off the "\n" that every line arrives with.
    # The file-io concept page points back at this function.
    choices = [answer for answer, _ in read_script(script)]
    if not choices:
        die(f"{script.name} is empty.",
            "Put one answer per line in it - the numbers you would type.")
    # Keep only the ones that are not empty. For a final project both
    # usually are, so this list stays empty and the script starts at
    # the student's very first answer.
    answers = [a for a in (player, difficulty) if a]
    # Keep adding whole copies of the file until there are plenty.
    # This is the "the file repeats" rule, and it is exactly this
    # loop -- nothing cleverer is going on.
    while len(answers) < MAX_ANSWERS:
        # .extend() adds every item of choices. .append() would have
        # added the list itself as one item, which is the classic slip.
        answers.extend(choices)
    return "\n".join(answers[:MAX_ANSWERS]) + "\n"


def explain(message):
    """A sentence about what this kind of error usually means here, or ''.

    Tied to the mistakes this course actually produces. A generic error name
    tells a first-year student nothing; "a function forgot to return" tells
    them where to look.
    """
    hints = [
        ("cannot unpack non-iterable NoneType",
         "A function that should hand back several values returned nothing. "
         "Find the function called on that line and check it ends with a "
         "`return`."),
        ("not associated with a value",
         "A function is changing something it was never given. It needs that "
         "value as a parameter, and needs to `return` it."),
        ("object is not subscriptable",
         "Something you indexed with [ ] is None -- usually a function that "
         "forgot to return."),
        ("KeyError",
         "A dictionary was asked for a key it does not have. `.get(key, 0)` "
         "hands back a default instead of stopping the program."),
        ("IndexError",
         "A list was asked for a position it does not have. Check the list is "
         "as long as you think -- print len() of it."),
        ("TypeError: can only concatenate str",
         "A number is being added to a string. str() the number, or use an "
         "f-string."),
        ("ZeroDivisionError",
         "Something divided by a value that reached zero. Guard it with an "
         "`if` before the division."),
    ]
    for needle, hint in hints:
        if needle in message:
            return hint
    return ""


def first_real_error(text):
    """Find the error a student should act on, if there is one.

    Takes:
        text  str -- the run's output and leftover stderr, joined

    Hands back:
        a tuple of (message, where, source_line, hint) when the program
        crashed, or None when it did not. `where` is written as
        `game.py:601, in craft_menu` -- VS Code turns file:line into a
        ctrl-clickable link, which is the whole reason for that shape.

    EOFError is deliberately ignored. It means the answers ran out while the
    program was still asking -- this script hitting its own limit, not a bug
    in the program. Reporting it would send a student hunting for a problem
    that is not theirs, which is worse than reporting nothing.
    """
    if "Traceback" not in text:
        return None
    lines = text.splitlines()
    last = next((ln.strip() for ln in reversed(lines)
                 if ln.strip() and ln.lstrip()[:1].isupper() and "Error" in ln), "")
    # The answers ran out while the program was still asking. That is
    # our answer limit, not the student's bug, so we say nothing.
    if last.startswith("EOFError"):
        return None

    # The LAST frame in the student's own file -- not the deepest frame, which
    # may be inside Python's own library and is never where they should look.
    where, source = "", ""
    pattern = re.compile(r'File "([^"]+)", line (\d+)(?:, in (.+))?')
    for line in reversed(lines):
        m = pattern.search(line)
        if not m:
            continue
        path, number, func = m.group(1), int(m.group(2)), (m.group(3) or "").strip()
        if Path(path).name != GAME.name:
            continue
        shown = Path(path).name          # relative: clickable from the repo root
        where = f"{shown}:{number}" + (f", in {func}" if func else "")
        try:
            with open(path, encoding="utf-8") as f:
                source = f.read().splitlines()[number - 1].strip()
        except (OSError, IndexError):
            source = ""
        break
    return (last, where, source, explain(last))


def report_crash(err, indent="     "):
    """Print a crash the same way everywhere: what, where, which line, why."""
    message, where, source, hint = err
    say(f"{indent}This run crashed:", RED + BOLD)
    say(f"{indent}  {message}", RED)
    if where:
        # file:line -- ctrl+click it in the VS Code terminal to jump there
        say(f"{indent}  {where}", BOLD)
    if source:
        say(f"{indent}    {source[:64]}", DIM)
    if hint:
        say(f"{indent}  {hint}", DIM)
    if where:
        say(f"{indent}  {DIM}Ctrl+click the file:line above to open it.{OFF}")


def show_one(name, answers, choices, player, difficulty, notes=None):
    """Play one run with every question and answer printed as it happens.

    Takes:
        name        str -- the script's name, for the heading
        answers     str -- the keystrokes, from build_answers()
        choices     a list of the script's lines, for the explanation above
        player      str -- the name answered first, or ""
        difficulty  str -- the difficulty answered next, or ""

    Hands back:
        True if the run finished cleanly, False if it crashed or stalled

    This is the --show path, and it exists to be believed: a student
    watching their own prompts scroll past with the answers beside them can
    see that the program really is being driven, which a row of dots cannot
    show.
    """
    given = answers.splitlines()
    say()
    say("  1. The file", BOLD)
    say(f"     plays/{name}.txt holds "
        + ("1 line: " if len(choices) == 1 else f"{len(choices)} lines: ")
        + ", ".join(choices))
    say()
    say("  2. What it becomes", BOLD)
    say("     Those lines are keystrokes, typed in order, starting again at")
    say(f"     the top when the {THING} asks for more.")
    say()
    if SETUP_COUNT[0]:
        say(f"     The first {SETUP_COUNT[0]} answer(s) come from "
            f"plays/_player.txt, not from this")
        say("     script -- every run opens with the same ones, so they live in")
        say("     one place instead of at the top of every play script.")
        say()
    setup = SETUP_COUNT[0]
    for i, answer in enumerate(given[:14]):
        # Which answers are setup is a count, not the constant 2. A program
        # that opens with no questions has none, and labelling its first two
        # real answers as ours was wrong in both directions.
        if i < setup:
            note = (f"{YELLOW}plays/_player.txt{OFF}{DIM} - "
                    + ("the name" if i == 0 else
                       f"difficulty {answer}; the runs rotate through them"))
        else:
            spot = (i - setup) % len(choices)
            written = (notes or [""] * len(choices))[spot]
            note = written or ("line %d of the file" % (spot + 1))
        say(f"       {i + 1:>3}. {answer:<14}{DIM}{note}{OFF}")
    say(f"       ... {len(given) - 14} more, cycling the same lines", DIM)
    say()

    say("  3. The program running, with those answers typed in", BOLD)
    say(f"     The {THING} is run normally. The only difference is that each", DIM)
    say("     answer is echoed where it was read, the way it would appear", DIM)
    say("     if somebody were sitting there typing it.", DIM)
    say()
    done = subprocess.run([sys.executable, "-c", RUNNER, str(GAME), "echo"],
                          input=answers, capture_output=True, text=True,
                          timeout=TIMEOUT)

    # One cycle means one day, so Day 2's banner is where to stop.
    day_one, seen_any = [], False
    for line in done.stdout.splitlines():
        if not line.strip():
            continue
        if seen_any and re.search(r"\bday 2\b", line, re.I):
            break
        day_one.append(line)
        seen_any = True

    # A whole day is too tall for a projector, and most of it is the status
    # panel. Long runs of ordinary output are collapsed so that every answer
    # stays on screen -- the answers are the entire point of this section.
    run = []

    def flush():
        if not run:
            return
        if len(run) <= 5:
            for text in run:
                say(f"     {DIM}{text[:66]}{OFF}")
        else:
            say(f"     {DIM}{run[0][:66]}{OFF}")
            say(f"     {DIM}... {len(run) - 2} lines of the {THING}'s own "
                f"output ...{OFF}")
            say(f"     {DIM}{run[-1][:66]}{OFF}")
        run.clear()

    answered = 0
    for line in day_one:
        if MARK in line:
            flush()
            before, _, typed = line.partition(MARK)
            # The first two came from playtest.py, not the file. Labelling
            # them "from the file" was wrong, and it was the first thing a
            # reader challenged -- those two answers appear nowhere in it.
            source = ("playtest.py" if answered < 2
                      else "line %d of the file"
                           % ((answered - 2) % len(choices) + 1))
            say(f"     {DIM}{before[:52]}{OFF}{GREEN}{BOLD}{typed}{OFF}"
                f"{DIM}   <- {source}{OFF}")
            answered += 1
        else:
            run.append(line)
    flush()
    say(f"     ... then day 2 starts, and it carries on the same way{OFF}", DIM)
    say()

    records, errors = split_records(done.stderr)
    err = first_real_error(done.stdout + errors)
    if not err:
        say("     This run finished without crashing.", GREEN)
        say()
    else:
        # Day one is the wrong window when the run died on day nine. Show the
        # end instead, and name the answer it was holding when it stopped --
        # that is the thing a reader wants and could not get from "it crashed
        # somewhere after the part we showed you".
        say("  4. Where it actually stopped", BOLD)
        say("     The crash came later than the day above, so here is the end", DIM)
        say("     of the run instead:", DIM)
        say()
        tail = [ln for ln in done.stdout.splitlines() if ln.strip()][-9:]
        last_mark = max((i for i, ln in enumerate(tail) if MARK in ln), default=-1)
        for i, line in enumerate(tail):
            if MARK not in line:
                say(f"     {DIM}{line[:66]}{OFF}")
                continue
            before, _, typed = line.partition(MARK)
            if i == last_mark:
                say(f"     {DIM}{before[:46]}{OFF}{RED}{BOLD}{typed}{OFF}"
                    f"{RED}   <- reading this when it crashed{OFF}")
            else:
                say(f"     {DIM}{before[:52]}{OFF}{GREEN}{typed}{OFF}")
        say()
        if records:
            prompt, answer = records[-1]
            setup = SETUP_COUNT[0]
            if len(records) <= setup:
                source = "plays/_player.txt"
            else:
                spot = (len(records) - 1 - setup) % len(choices)
                written = (notes or [""] * len(choices))[spot]
                source = "line %d of plays/%s.txt" % (spot + 1, name)
                if written:
                    source += f" -- {written}"
            say(f"     It had just answered {BOLD}{prompt.strip()[:40]}{OFF}"
                f" with {RED}{BOLD}{answer}{OFF},")
            say(f"     which is {source}.")
            say()
        report_crash(err)
        say()


def jam_line(text):
    """Spot a program stuck re-asking one question, and name the question.

    Takes:
        text  str -- everything the run printed

    Hands back:
        a tuple of (line, times) when one line repeats 50 or more times,
        or None otherwise

    This is NOT a crash, and the report says so. It means the program kept
    rejecting every answer it was given, which usually means the script is
    wrong rather than the program. A validating menu plus a file of nothing
    but junk produces exactly this.
    """
    # BOTH conditions, and the first one is what makes it sound. A thirty-day
    # game prints the action menu about a hundred and fifty times, so
    # repetition alone marks every healthy long game as jammed -- which it
    # duly did, calling three good scripts broken. A jam is repetition that
    # ran until the answers RAN OUT; a real game ends by winning or dying.
    if "EOFError" not in text:
        return None
    # Counter counts how many times each line appeared. A program
    # stuck on one prompt prints the same line thousands of times.
    counts = Counter(line.strip() for line in text.splitlines() if line.strip())
    if not counts:
        return None
    # most_common(1) hands back a list with one (line, count) pair in
    # it, so [0] pulls that pair out and we unpack it into two names.
    line, seen = counts.most_common(1)[0]
    return (line, seen) if seen >= 50 else None


def coverage(asked, runs):
    """Print the table of every question asked and every answer it heard.

    Takes:
        asked  a dict of {prompt: set of answers}, built across every run
        runs   int -- how many runs went into it, for the wording

    Hands back:
        None -- it prints

    It needs to know nothing about this program's menus, because the keys
    ARE the prompts, captured from the program's own input() calls. Sorted
    most-answers-first, so the thin ones fall to the bottom where a reader
    will actually look.
    """
    if not asked:
        return
    say(f"  What the {THING} asked, and what your script answered:", BOLD)
    say()
    # Sorting a dict walks its KEYS. The minus makes it descending,
    # so the most-answered questions come first and the thin ones
    # fall to the bottom, where a reader will actually look.
    for prompt in sorted(asked, key=lambda k: -len(asked[k])):
        # asked[prompt] is a SET, so the same answer given fifty times is
        # in it once. That is what makes the next line meaningful.
        answers = sorted(asked[prompt])
        shown = " ".join(answers[:8]) + (" ..." if len(answers) > 8 else "")
        thin = len(answers) == 1
        colour = YELLOW if thin else GREEN
        note = f"{YELLOW}  <- only ever this one{OFF}" if thin else ""
        say(f"    {DIM}{prompt[:34]:<34}{OFF}{colour}{shown}{OFF}{note}")
    for prompt in sorted(OURS):
        if prompt in asked:
            continue
        shown = " ".join(sorted(OURS[prompt]))
        say(f"    {DIM}{prompt[:34]:<34}{shown}   <- plays/_player.txt{OFF}")
    say()
    lonely = [p for p in asked if len(asked[p]) == 1]
    if lonely:
        say("  A question that only ever heard one answer has not been", DIM)
        say("  tested -- it has been visited. Add the other options to the", DIM)
        say("  script, or write a second script that gives them.", DIM)
        say()


def run_all(runs, player, levels):
    """Run every script several times and report on the suite as a whole.

    Takes:
        runs    int -- how many runs of each script
        player  str -- the name answered first, or ""
        levels  a list of difficulties to rotate through

    Hands back:
        nothing -- it exits 0 if everything passed and 1 if anything did not

    ONE coverage dictionary is kept across every script. Each script is
    deliberately narrow, so no single one covers the program and no single
    report should claim to. What matters is whether the whole suite leaves a
    question untried, and that is only visible added up.
    """
    # ONE dictionary for the whole suite. Every run below adds into
    # this same one, which is why the table at the end covers
    # everything rather than just the last script.
    asked, rows, trouble = {}, [], 0
    for script in available():
        tally = {"crashed": 0, "stuck": 0, "jammed": 0, "ok": 0}
        detail = None
        sys.stdout.write(f"  {DIM}{script:<10}{OFF}")
        # The same script, several times. The answers are identical; if
        # the program uses random numbers the runs are not.
        for i in range(runs):
            stdin = build_answers(PLAYS / f"{script}.txt", player,
                                  levels[i % len(levels)])
            state, err = play_once(stdin, asked)
            # state is one of the four keys in tally, so this adds one to
            # whichever outcome this run had.
            tally[state] += 1
            if state in ("crashed", "jammed") and detail is None:
                detail = (state, err)
            sys.stdout.write({"ok": GREEN + "." + OFF,
                              "crashed": RED + "x" + OFF,
                              "stuck": YELLOW + "?" + OFF,
                              "jammed": YELLOW + "!" + OFF}[state])
            sys.stdout.flush()
        bad = tally["crashed"] + tally["stuck"] + tally["jammed"]
        trouble += bad
        say(f"   {RED + 'needs a look' + OFF if bad else GREEN + 'ok' + OFF}")
        rows.append((script, tally, detail))

    say()
    rule()
    for script, tally, detail in rows:
        if not detail:
            continue
        state, err = detail
        if state == "crashed":
            say(f"  {script}:", RED + BOLD)
            report_crash(err, indent="    ")
        else:
            say(f"  {script}: never got going -- the {THING} kept asking "
                f"{err[0][:36]!r}", YELLOW)
    if trouble:
        say()
    say(f"  {len(rows)} scripts, {len(rows) * runs} {THINGS}.",
        (RED if trouble else GREEN) + BOLD)
    say()
    coverage(asked, len(rows) * runs)
    say("  This is what the WHOLE suite covers. A menu listed with only one", DIM)
    say("  answer is untried by every script you have, not just by one.", DIM)
    say()
    sys.exit(1 if trouble else 0)


def play_once(stdin, asked_so_far):
    """Run the program once, with the answers piped in, and say how it went.

    Takes:
        stdin         str -- the keystrokes, from build_answers()
        asked_so_far  the shared coverage dict. This function ADDS to it

    Hands back:
        a tuple of (state, detail)
          state   "ok", "crashed", "stuck" or "jammed"
          detail  the error for a crash, the repeated line for a jam,
                  None for everything else

    A separate process per run, so a crash in the program cannot take this
    script down with it, and a timeout turns an endless loop into a result
    instead of a hang.

    Note that the second argument is CHANGED rather than returned. A dict
    handed to a function is the same dict, so adding to it here adds to the
    caller's -- which is how one table ends up covering every run.
    """
    try:
        # Start a SEPARATE Python and hand it the RUNNER as a one-line
        # program, with the real program as its argument. Separate, so a
        # crash in the program cannot take this script down with it.
        done = subprocess.run(
            [sys.executable, "-c", RUNNER, str(GAME)], input=stdin,
            capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "stuck", None
    asked, errors = split_records(done.stderr)
    for i, (prompt, answer) in enumerate(asked):
        # The first two answers of every game come from plays/_player.txt,
        # not from the play script. Counting them against the script means
        # scolding it for two questions it never had a say in.
        # The first answers of each run come from _player.txt, not from
        # the script. Counting them against the script would scold it for
        # questions it never had a say in.
        bucket = OURS if i < SETUP_COUNT[0] else asked_so_far
        # setdefault: "give me the set for this prompt, making an empty
        # one first if this is a prompt we have not seen". Then .add()
        # puts the answer in it. Two lines of work in one.
        bucket.setdefault(prompt, set()).add(answer)
    blob = done.stdout + errors
    err = first_real_error(blob)
    if err:
        return "crashed", err
    jam = jam_line(blob)
    if jam:
        return "jammed", jam
    return "ok", None


def roll_once(stdin, target, forced):
    """Play one game with one random draw forced. Hands back (crash, sites)."""
    try:
        done = subprocess.run(
            [sys.executable, "-c", RAND_RUNNER, str(GAME), str(target), str(forced)],
            input=stdin, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "", {}
    sites, leftover = {}, []
    for line in done.stderr.splitlines():
        if line.startswith(RAND):
            where, low, high = line[1:].split("|")
            sites[int(where)] = (int(low), int(high))
        else:
            leftover.append(line)
    return first_real_error(done.stdout + "\n".join(leftover)), sites


def sweep(name, player, level):
    """Try every value every random draw in the game can produce.

    A seed replays a sample; this covers the range. The question it answers is
    not "did anything break this time" but "which values break it, and are
    there any others".
    """
    stdin = build_answers(PLAYS / f"{name}.txt", player, level)
    say(f"  Finding the random draws first, using plays/{name}.txt ...", DIM)
    _crash, sites = roll_once(stdin, -1, 0)
    if not sites:
        say("  This game made no random.randint calls.", GREEN)
        say()
        return 0

    # Discovery runs the game ONCE, so a draw inside a branch that run did
    # not take is never seen. Counting what the source actually contains is
    # the only way to say so -- otherwise the report reads as full coverage
    # when it may be a little over half.
    written = 0
    try:
        tree = ast.parse(GAME.read_text(encoding="utf-8"))
        written = sum(1 for n in ast.walk(tree)
                      if isinstance(n, ast.Call)
                      and isinstance(n.func, ast.Attribute)
                      and n.func.attr == "randint")
    except (OSError, SyntaxError):
        pass

    plan = {w: (lo, hi) for w, (lo, hi) in sites.items() if hi - lo + 1 <= SWEEPABLE}
    skipped = {w: v for w, v in sites.items() if w not in plan}
    total = sum(hi - lo + 1 for lo, hi in plan.values())
    say(f"  {len(sites)} draw(s) found. Trying every value of {len(plan)} of "
        f"them &mdash; {total} games.".replace("&mdash;", "--"), BOLD)
    say()

    found = []
    for where in sorted(plan):
        low, high = plan[where]
        hits = []
        for value in range(low, high + 1):
            crash, _ = roll_once(stdin, where, value)
            if crash:
                hits.append((value, crash))
                found.append((where, value, crash))
            sys.stdout.write((RED + "x" + OFF) if crash else (GREEN + "." + OFF))
            sys.stdout.flush()
        say()
        say(f"    {GAME.name}:{where:<5} {low} to {high:<4} "
            + (f"{RED}{len(hits)} value(s) crash{OFF}" if hits
               else f"{GREEN}all fine{OFF}"))
        for value, crash in hits:
            say(f"      when it draws {value}  ->  {crash[0][:52]}", RED)
    say()
    for where, (low, high) in skipped.items():
        say(f"    {GAME.name}:{where:<5} {low} to {high} skipped -- "
            f"{high - low + 1} values is too many to try one at a time", DIM)
    if skipped:
        say()

    rule()
    if found:
        # One bug reached by six different values is one bug. Listing it six
        # times reads as six problems and buries the thing worth fixing.
        by_line = {}
        for where, value, crash in found:
            by_line.setdefault((where, crash[0]), []).append(value)
        say(f"  {len(by_line)} problem(s), reached by {len(found)} value(s).",
            RED + BOLD)
        say()
        for (where, message), values in by_line.items():
            run = (f"{min(values)} to {max(values)}"
                   if len(values) > 2 and
                   values == list(range(min(values), max(values) + 1))
                   else ", ".join(map(str, values)))
            say(f"    {GAME.name} line {where}, when it draws {run}", BOLD)
            say(f"      {message[:62]}", RED)
        say()
        say("  Not a seed and not a sample -- those are the values, and for", DIM)
        say("  the draws that were swept there are no others.", DIM)
    else:
        say(f"  {total} games, nothing broke.", GREEN + BOLD)
        say()
        say("  Every value those draws can produce has been tried.", DIM)

    missed = written - len(sites) if written else 0
    if missed > 0:
        say()
        say(f"  {missed} of the {written} random draws in {GAME.name} were "
            f"never reached,", YELLOW)
        say(f"  so nothing was swept for them. They sit in code this script "
            f"did not", YELLOW)
        say(f"  run -- try another plays file.", YELLOW)
    say()
    return 1 if found else 0


def main():
    """Read the command line and do what it asks.

    Takes:
        nothing -- it reads sys.argv

    Hands back:
        nothing -- every path ends in a print, or in sys.exit

    The full list of commands is at the top of this file.
    """
    say()
    say(f"  {TITLE}", BOLD)
    rule()

    if GAME is None or not GAME.exists():
        here = [p.name for p in sorted(HERE.glob("*.py"))
                if p.name != Path(__file__).name]
        die("I cannot tell which program to test.",
            "Looked for game.py and did not find it."
            + (f" Found instead: {', '.join(here)}." if here else ""),
            "",
            "Run this from the folder your program is in. If there is more",
            "than one .py file, name the one to test game.py.")
    say(f"  {DIM}Testing {GAME.name}{OFF}")

    names = available()
    if not names:
        die("No scripts found in plays/.",
            "Run  python sync.py  to get them.")

    if len(sys.argv) < 2:
        say("  Scripts you can run:")
        for n in names:
            first = [a for a, _ in read_script(PLAYS / f"{n}.txt")]
            say(f"    {n:<12} {DIM}answers: {' '.join(first[:8])}{OFF}")
        say()
        # Suggest the script most likely to find something. Alphabetical order
        # puts "chop" first, and chop is the one that tries a single choice
        # over and over -- the least likely of the lot to turn anything up.
        pick = "mixed" if "mixed" in names else names[0]
        say(f"  Run them all:  python playtest.py all", BOLD)
        say(f"  {DIM}Or just one:   python playtest.py {pick}{OFF}")
        say()
        return

    name = sys.argv[1]
    if name not in names and name != "all":
        die(f"There is no plays/{name}.txt",
            "Scripts you have: " + ", ".join(names),
            "",
            "Or run every one of them:  python playtest.py all")

    # Flags and the run count are separated, so `mixed --show` is not read as
    # a request for "--show" games. That exact message was the first thing a
    # reader hit when they went looking for what this does.
    # Split what the student typed into flags and numbers, so that
    # `playtest.py mixed --show` is not read as a request for
    # "--show" runs. That exact message confused the first reader.
    flags = [a for a in sys.argv[2:] if a.startswith("-")]
    numbers = [a for a in sys.argv[2:] if not a.startswith("-")]
    unknown = [f for f in flags if f not in ("--show", "-s", "--sweep")]
    if unknown:
        die(f"'{unknown[0]}' is not an option.",
            "There are two: --show plays ONE game and walks through what the",
            "file is and what the game did, and --sweep tries every value",
            "every random draw in the game can produce.",
            "",
            f"Try:  python playtest.py {name} --show")
    if numbers and not numbers[0].isdigit():
        die(f"'{numbers[0]}' is not a number.",
            f"Try:  python playtest.py {name} 50",
            f"  or: python playtest.py {name} --show")

    player, levels = read_player()
    SETUP_COUNT[0] = len([a for a in (player, levels[0]) if a])
    if name == "all":
        if "--show" in flags or "-s" in flags:
            # Every script, in full. It is long on purpose -- the point of
            # --show is proving to somebody that the work is really being
            # done, and a summary proves nothing. Each script gets the next
            # difficulty in the rotation, so that is visible too.
            for number, script in enumerate(names):
                say()
                rule()
                say(f"  SCRIPT {number + 1} OF {len(names)}:  {script}", BOLD)
                rule()
                pairs = read_script(PLAYS / f"{script}.txt")
                choices = [a for a, _ in pairs]
                level = levels[number % len(levels)]
                show_one(script,
                         build_answers(PLAYS / f"{script}.txt", player, level),
                         choices, player, level, [n for _, n in pairs])
            rule()
            say(f"  That was all {len(names)} scripts, each played for real.",
                GREEN + BOLD)
            say(f"  {DIM}To score them instead of watching them: "
                f"python playtest.py all{OFF}")
            say()
            return
        runs = max(1, int(numbers[0])) if numbers else ALL_RUNS
        who = (f" as {player}" if player else "")
        how = (f", difficulty {', '.join(levels)}" if levels[0] else "")
        say(f"  Every script, {runs} {THINGS} each{who}{how}.")
        say()
        run_all(runs, player, levels)
        return
    if "--sweep" in flags:
        sys.exit(sweep(name, player, levels[0]))

    if "--show" in flags or "-s" in flags:
        pairs = read_script(PLAYS / f"{name}.txt")
        choices = [a for a, _ in pairs]
        show_one(name, build_answers(PLAYS / f"{name}.txt", player, levels[0]),
                 choices, player, levels[0], [n for _, n in pairs])
        return

    runs = max(1, int(numbers[0])) if numbers else DEFAULT_RUNS
    say(f"  Playing {runs} {THINGS}, answering from plays/{name}.txt ...")
    if player or levels[0]:
        where = ("from plays/_player.txt" if (PLAYS / "_player.txt").exists()
                 else "built-in defaults -- make plays/_player.txt to change them")
        say(f"  {DIM}Playing as {player}, rotating difficulty "
            f"{', '.join(levels)} -- {where}{OFF}")
    say(f"  {DIM}Same answers every run -- but the dice are different, so the"
        f"{OFF}")
    say(f"  {DIM}{THINGS} are not. That is why it is {runs} and not one.{OFF}")
    say()
    say(f"  {DIM}. = finished   x = crashed   ! = never got going{OFF}")
    say()

    crashes, stuck, jams, seen = [], 0, [], {}
    asked = {}
    for i in range(runs):
        stdin = build_answers(PLAYS / f"{name}.txt", player,
                              levels[i % len(levels)])
        state, err = play_once(stdin, asked)
        if state == "crashed":
            crashes.append(err)
            seen[err[0]] = seen.get(err[0], 0) + 1
            sys.stdout.write(RED + "x" + OFF)
        elif state == "stuck":
            stuck += 1
            sys.stdout.write(YELLOW + "?" + OFF)
        elif state == "jammed":
            jams.append(err)
            sys.stdout.write(YELLOW + "!" + OFF)
        else:
            sys.stdout.write(GREEN + "." + OFF)
        sys.stdout.flush()
    say()
    say()
    rule()

    if not crashes and not stuck and not jams:
        say(f"  {runs} games, none of them broke.", GREEN + BOLD)
        say()
        coverage(asked, runs)
        say("  That is a real result for THESE answers. A different script", DIM)
        say("  may still find something - try another one.", DIM)
        say()
        return
    # Everything below is a failure path, and every one of them ends by
    # printing coverage too. It used to print only when nothing broke, which
    # is exactly backwards -- a run that crashed is when you most want to know
    # which menus the script had actually reached before it died.

    if crashes:
        say(f"  {len(crashes)} of {runs} games crashed.", RED + BOLD)
        say()
        for message, _ in sorted(seen.items(), key=lambda x: -x[1]):
            err = next((e for e in crashes if e[0] == message), None)
            if err:
                report_crash(err, indent="  ")
            say(f"    happened in {seen[message]} of {runs} games", DIM)
            say()

    if jams:
        line, seen_count = jams[0]
        say(f"  {len(jams)} of {runs} games never got going.", YELLOW + BOLD)
        say()
        say(f"  The game asked this {seen_count} times in a single game:", YELLOW)
        say(f"    {line[:62]}", BOLD)
        say()
        say("  That is not a crash. The game rejected the answer and asked")
        say(f"  again, and plays/{name}.txt kept giving the same one until the")
        say("  answers ran out -- so the game never got past the first day.")
        say()
        say("  Fix the script: it needs an answer this question will accept.")
        say()

    if stuck:
        say(f"  {stuck} of {runs} games never finished.", YELLOW + BOLD)
        say("  Something is waiting for an answer it never accepts - look for")
        say("  a while loop around an input() that rejects what it is given.")
        say()
    coverage(asked, runs)
    sys.exit(1)


if __name__ == "__main__":
    main()
