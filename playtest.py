"""
Block Builder - play the game for you, many times, and report what broke

    python playtest.py              list the scripts you can run
    python playtest.py explore      play 20 games, exploring every turn
    python playtest.py mixed 50     play 50 games, trying every choice
    python playtest.py mixed --show play ONE game and explain what happened

WHY THIS EXISTS
    Clicking through your own game to find a bug is slow, and it is worse
    than slow: you tend to press the same keys every time. If you always
    chop wood, you only ever test chopping wood. A bug that lives in the
    crafting menu will sit there for weeks and look like nothing is wrong.

    This runs the game for you with the answers read from a file, so you can
    say "explore every single turn" and watch what happens.

    It also runs it MANY times, which matters more than it sounds. The game
    uses random numbers, so the same answers do not give the same game. A bug
    that only shows up when you are low on wood might appear in one game out
    of five. Playing once and seeing nothing proves very little.

THE SCRIPTS
    plays/explore.txt and the rest are just lists of answers, one per line.
    Open one. There is nothing clever in it. If the game asks more questions
    than the file has answers, it starts again from the top of the file.

    Write your own: make plays/myplan.txt, put choices in it, and run
    `python playtest.py myplan`.

You do not need to understand this file. Do not edit it.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GAME = HERE / "game.py"
PLAYS = HERE / "plays"

GREEN, YELLOW, RED, DIM, BOLD, OFF = (
    "\033[92m", "\033[93m", "\033[91m", "\033[2m", "\033[1m", "\033[0m"
)

DEFAULT_RUNS = 20
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
ECHO_RUNNER = (
    "import builtins, runpy, sys\n"
    "_read = builtins.input\n"
    "def _echo(prompt=''):\n"
    "    value = _read(prompt)\n"
    "    print('\\x01' + value)\n"
    "    return value\n"
    "builtins.input = _echo\n"
    "runpy.run_path(sys.argv[1], run_name='__main__')\n"
)


def say(msg="", color=""):
    print(f"{color}{msg}{OFF}" if color else msg)


def rule():
    say("-" * 62, DIM)


def die(*lines):
    say()
    rule()
    say(f"  {lines[0]}", RED + BOLD)
    rule()
    for line in lines[1:]:
        say(f"  {line}")
    say()
    sys.exit(1)


def available():
    if not PLAYS.is_dir():
        return []
    return sorted(p.stem for p in PLAYS.glob("*.txt"))


def build_answers(script):
    """name, difficulty, then the script's choices repeated until we run out.

    Repeating is what lets plays/explore.txt be one line long instead of two
    thousand. It also means a script can never "run out" partway through a
    game for a boring reason.
    """
    # Module 10 teaches exactly these three lines: `with` closes the file
    # whatever happens, `for line in answers_file` reads it one line at a
    # time, and .strip() takes off the "\n" that every line arrives with.
    # The file-io concept page points back at this function.
    with open(script, encoding="utf-8") as answers_file:
        choices = [line.strip() for line in answers_file if line.strip() != ""]
    if not choices:
        die(f"{script.name} is empty.",
            "Put one answer per line in it - the numbers you would type.")
    answers = ["PlayTester", "2"]
    while len(answers) < MAX_ANSWERS:
        answers.extend(choices)
    return "\n".join(answers[:MAX_ANSWERS]) + "\n"


def first_real_error(text):
    """The error a student should act on, or None.

    EOFError is filtered out on purpose. It means the answers ran out while
    the game was still asking - that is this script hitting its own limit,
    not a bug in the game. Reporting it would send students hunting for a
    problem that is not theirs, which is worse than reporting nothing.
    """
    if "Traceback" not in text:
        return None
    lines = text.splitlines()
    last = next((ln.strip() for ln in reversed(lines)
                 if ln.strip() and ln.lstrip()[:1].isupper() and "Error" in ln), "")
    if last.startswith("EOFError"):
        return None
    where = [ln.strip() for ln in lines if ln.strip().startswith('File "')]
    spot = ""
    for w in reversed(where):
        if "game.py" in w:
            spot = w
            break
    return (last, spot)


def show_one(name, answers, choices):
    """Explain one run: the file, the keystrokes it becomes, and the game.

    Part 3 plays a real day with the answers echoed where they were read, so
    the file's lines can be watched going in one at a time.

    The first attempt worked the answers out AFTERWARDS, by looking for
    prompts in the captured output, and was wrong in the worst way -- it
    under-reported and said nothing about it. input() writes its prompt with
    no newline, so when the game prints the RESULT of an action it lands on
    the same line and the prompt stops looking like one. Three questions
    showed up out of roughly a hundred and fifty, which reads as "the game
    only asked three things". Echoing at the source cannot miss one.
    """
    given = answers.splitlines()
    say()
    say("  1. The file", BOLD)
    say(f"     plays/{name}.txt holds "
        + ("1 line: " if len(choices) == 1 else f"{len(choices)} lines: ")
        + ", ".join(choices))
    say()
    say("  2. What it becomes", BOLD)
    say("     Those lines are keystrokes. playtest.py types them for you, in")
    say("     order, and goes back to the top when the game asks for more:")
    say()
    for i, answer in enumerate(given[:14]):
        if i == 0:
            note = "the player's name"
        elif i == 1:
            note = "the difficulty"
        else:
            note = "line %d of the file" % ((i - 2) % len(choices) + 1)
        say(f"       {i + 1:>3}. {answer:<14}{DIM}{note}{OFF}")
    say(f"       ... {len(given) - 14} more, cycling the same lines", DIM)
    say()

    say("  3. One day of the game, with those answers typed in", BOLD)
    say("     The game is run normally. The only difference is that each", DIM)
    say("     answer is echoed where it was read, the way it would appear", DIM)
    say("     if somebody were sitting there typing it.", DIM)
    say()
    done = subprocess.run([sys.executable, "-c", ECHO_RUNNER, str(GAME)],
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
            say(f"     {DIM}... {len(run) - 2} lines of the game's own "
                f"output ...{OFF}")
            say(f"     {DIM}{run[-1][:66]}{OFF}")
        run.clear()

    for line in day_one:
        if MARK in line:
            flush()
            before, _, typed = line.partition(MARK)
            say(f"     {DIM}{before[:52]}{OFF}{GREEN}{BOLD}{typed}{OFF}"
                f"{DIM}   <- from the file{OFF}")
        else:
            run.append(line)
    flush()
    say(f"     ... then day 2 starts, and it carries on the same way{OFF}", DIM)
    say()
    err = first_real_error(done.stdout + done.stderr)
    if err:
        say(f"     This run crashed: {err[0]}", RED)
    else:
        say("     This run finished without crashing.", GREEN)
    say()
    say("  That is the whole trick: the file is a stack of keystrokes, so", DIM)
    say("  nothing depends on a person being there to type them. Run it", DIM)
    say("  twenty times and the answers stay the same while the dice do not.", DIM)
    say()


def play_once(stdin):
    try:
        done = subprocess.run(
            [sys.executable, str(GAME)], input=stdin,
            capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "stuck", None
    blob = done.stdout + done.stderr
    err = first_real_error(blob)
    if err:
        return "crashed", err
    return "ok", None


def main():
    say()
    say("  Block Builder - playtest", BOLD)
    rule()

    if not GAME.exists():
        die("No game.py here.",
            "Run this from inside your block-builder folder, the one with",
            "README.md in it.")

    names = available()
    if not names:
        die("No scripts found in plays/.",
            "Run  python sync.py  to get them.")

    if len(sys.argv) < 2:
        say("  Scripts you can run:")
        for n in names:
            first = (PLAYS / f"{n}.txt").read_text(encoding="utf-8").split()
            say(f"    {n:<12} {DIM}answers: {' '.join(first[:8])}{OFF}")
        say()
        # Suggest the script most likely to find something. Alphabetical order
        # puts "chop" first, and chop is the one that tries a single choice
        # over and over -- the least likely of the lot to turn anything up.
        pick = "mixed" if "mixed" in names else names[0]
        say(f"  Try:  python playtest.py {pick}", BOLD)
        say()
        return

    name = sys.argv[1]
    if name not in names:
        die(f"There is no plays/{name}.txt",
            "Scripts you have: " + ", ".join(names))

    # Flags and the run count are separated, so `mixed --show` is not read as
    # a request for "--show" games. That exact message was the first thing a
    # reader hit when they went looking for what this does.
    flags = [a for a in sys.argv[2:] if a.startswith("-")]
    numbers = [a for a in sys.argv[2:] if not a.startswith("-")]
    unknown = [f for f in flags if f not in ("--show", "-s")]
    if unknown:
        die(f"'{unknown[0]}' is not an option.",
            "The only one is --show, which plays ONE game and walks through",
            "what the file is, what it turns into, and what the game did.",
            "",
            f"Try:  python playtest.py {name} --show")
    if numbers and not numbers[0].isdigit():
        die(f"'{numbers[0]}' is not a number.",
            f"Try:  python playtest.py {name} 50",
            f"  or: python playtest.py {name} --show")

    stdin = build_answers(PLAYS / f"{name}.txt")
    if "--show" in flags or "-s" in flags:
        with open(PLAYS / f"{name}.txt", encoding="utf-8") as answers_file:
            choices = [ln.strip() for ln in answers_file if ln.strip()]
        show_one(name, stdin, choices)
        return

    runs = max(1, int(numbers[0])) if numbers else DEFAULT_RUNS
    say(f"  Playing {runs} games, answering from plays/{name}.txt ...")
    say(f"  {DIM}Same answers every game -- but the dice are different, so the"
        f"{OFF}")
    say(f"  {DIM}games are not. That is why it is {runs} and not one.{OFF}")
    say()
    say(f"  {DIM}. = a game that finished    x = a game that crashed{OFF}")
    say()

    crashes, stuck, seen = [], 0, {}
    for i in range(runs):
        state, err = play_once(stdin)
        if state == "crashed":
            crashes.append(err)
            seen[err[0]] = seen.get(err[0], 0) + 1
            sys.stdout.write(RED + "x" + OFF)
        elif state == "stuck":
            stuck += 1
            sys.stdout.write(YELLOW + "?" + OFF)
        else:
            sys.stdout.write(GREEN + "." + OFF)
        sys.stdout.flush()
    say()
    say()
    rule()

    if not crashes and not stuck:
        say(f"  {runs} games, none of them broke.", GREEN + BOLD)
        say()
        say("  That is a real result for THESE answers. A different script", DIM)
        say("  may still find something - try another one.", DIM)
        say()
        return

    if crashes:
        say(f"  {len(crashes)} of {runs} games crashed.", RED + BOLD)
        say()
        for message, spot in sorted(seen.items(), key=lambda x: -x[1]):
            where = next((s for m, s in crashes if m == message), "")
            say(f"  {message}", RED)
            if where:
                say(f"    {where}", DIM)
            say(f"    happened in {seen[message]} of {runs} games", DIM)
            say()
        say("  Open that line. The number after 'line' is where to look.")
        say()
        say("  If it says a variable is not associated with a value, the", DIM)
        say("  function is changing something it was never given - it needs", DIM)
        say("  that value as a parameter, and needs to return it.", DIM)
        say()

    if stuck:
        say(f"  {stuck} of {runs} games never finished.", YELLOW + BOLD)
        say("  Something is waiting for an answer it never accepts - look for")
        say("  a while loop around an input() that rejects what it is given.")
        say()
    sys.exit(1)


if __name__ == "__main__":
    main()
