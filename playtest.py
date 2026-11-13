"""
Block Builder - play the game for you, many times, and report what broke

    python playtest.py              list the scripts you can run
    python playtest.py all          EVERY script -- the one to run before you
                                    hand anything in
    python playtest.py explore      play 20 games, exploring every turn
    python playtest.py mixed 50     play 50 games, trying every choice
    python playtest.py mixed --show play ONE game and explain what happened

    Every run ends with a list of the questions the game asked and the
    answers your script gave it. A question that only ever heard one answer
    has not been tested -- it has been visited.

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
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAYS = HERE / "plays"


def find_program():
    """The program to test: game.py, or the only other .py beside this one.

    Hardcoding game.py meant the first step of reusing this on any other
    project was editing it -- and students are told not to. Auto-detecting
    costs nothing when there is one obvious answer and says so when there
    is not.
    """
    if (HERE / "game.py").exists():
        return HERE / "game.py"
    others = [p for p in sorted(HERE.glob("*.py")) if p.name != Path(__file__).name]
    return others[0] if len(others) == 1 else None


GAME = find_program()

GREEN, YELLOW, RED, DIM, BOLD, OFF = (
    "\033[92m", "\033[93m", "\033[91m", "\033[2m", "\033[1m", "\033[0m"
)

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
    """Pull the prompt->answer records out, and hand back the rest.

    The rest matters: it is where a traceback lives, and mixing the records
    into it would have jam_line() counting our own bookkeeping as repetition.
    """
    asked, leftover = [], []
    for line in stderr_text.splitlines():
        if line.startswith(RECORD):
            parts = line.split(RECORD)
            if len(parts) >= 3:
                asked.append((parts[1], parts[2]))
                continue
        leftover.append(line)
    return asked, "\n".join(leftover)


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
    """The play scripts. A leading _ means "not a script" -- see _player.txt."""
    if not PLAYS.is_dir():
        return []
    return sorted(p.stem for p in PLAYS.glob("*.txt")
                  if not p.name.startswith("_"))


def read_player():
    """Who plays, and on which difficulties, from plays/_player.txt.

    First line is the name. Every line after it is a difficulty, and the runs
    rotate through them -- so twenty games cover all three rather than
    hammering one. Both used to be written into this file, which meant
    changing either one meant editing a program students are told not to
    touch.

    Missing or half-filled, it falls back to something that works. A testing
    tool that refuses to start because its settings file is absent has picked
    the wrong thing to be strict about.
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


def build_answers(script, player, difficulty):
    """name, difficulty, then the script's choices repeated until we run out.

    The name and the difficulty are supplied HERE rather than in the plays
    file. Every game opens by asking for both, so every file would otherwise
    begin with the same two lines, and a reader comparing explore.txt against
    what actually gets typed would find two answers they could not account
    for. --show now says where they come from, because that is exactly the
    question the first reader asked.

    Repeating the rest is what lets plays/explore.txt be one line long instead
    of two thousand. It also means a script can never "run out" partway
    through a game for a boring reason.
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
    answers = [a for a in (player, difficulty) if a]
    while len(answers) < MAX_ANSWERS:
        answers.extend(choices)
    return "\n".join(answers[:MAX_ANSWERS]) + "\n"


def first_real_error(text):
    """The error a student should act on, or None.

    EOFError is filtered out on purpose. It means the answers ran out while
    the game was still asking - that is this script hitting its own limit,
    not a bug in the game. Reporting it would send students hunting for a
    problem that is not theirs, which is worse than reporting nothing.

    That silence had a cost, though, and jam_line() now pays it back: a
    script that answers a menu with something it rejects loops until the
    answers run out, dies of EOFError, and was reported as a clean game.
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


def show_one(name, answers, choices, player, difficulty):
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
    say("     Those lines are keystrokes, typed in order, starting again at")
    say("     the top when the game asks for more.")
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
            note = "line %d of the file" % ((i - setup) % len(choices) + 1)
        say(f"       {i + 1:>3}. {answer:<14}{DIM}{note}{OFF}")
    say(f"       ... {len(given) - 14} more, cycling the same lines", DIM)
    say()

    say("  3. The program running, with those answers typed in", BOLD)
    say("     The game is run normally. The only difference is that each", DIM)
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
            say(f"     {DIM}... {len(run) - 2} lines of the game's own "
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


def jam_line(text):
    """The question a run got stuck re-asking, if there is one.

    A script that answers a menu with something the menu rejects does not
    crash -- the game's own validation loop asks again, forever, until the
    answers run out. The run then dies of EOFError, which is swallowed as
    harmless, and the game is reported as fine while never having got past
    day one.

    Three of the five shipped scripts did exactly that and all showed green.
    A question asked fifty times in one game is not a game being played.
    """
    # BOTH conditions, and the first one is what makes it sound. A thirty-day
    # game prints the action menu about a hundred and fifty times, so
    # repetition alone marks every healthy long game as jammed -- which it
    # duly did, calling three good scripts broken. A jam is repetition that
    # ran until the answers RAN OUT; a real game ends by winning or dying.
    if "EOFError" not in text:
        return None
    counts = Counter(line.strip() for line in text.splitlines() if line.strip())
    if not counts:
        return None
    line, seen = counts.most_common(1)[0]
    return (line, seen) if seen >= 50 else None


def coverage(asked, runs):
    """Every question the game asked, and the answers it received.

    Needs no knowledge of this game's menus: the prompt strings come from
    input() itself. That matters twice over -- it works on a student's own
    game whatever they called things, and it answers "did my script test
    everything?" with a list rather than a guess.

    A menu that only ever heard ONE answer is the thing to look at. That is
    how all-5s went a whole term without entering the cave.
    """
    if not asked:
        return
    say("  What the game asked, and what your script answered:", BOLD)
    say()
    for prompt in sorted(asked, key=lambda k: -len(asked[k])):
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
    """Every script in turn, with ONE combined coverage report at the end.

    Combined on purpose. Each script is deliberately narrow -- chop only
    chops, craft only crafts -- so no single one covers the game and no
    single report should claim to. What matters is whether the SUITE leaves
    a menu untried, and that is only visible added up.
    """
    asked, rows, trouble = {}, [], 0
    for script in available():
        tally = {"crashed": 0, "stuck": 0, "jammed": 0, "ok": 0}
        detail = None
        sys.stdout.write(f"  {DIM}{script:<10}{OFF}")
        for i in range(runs):
            stdin = build_answers(PLAYS / f"{script}.txt", player,
                                  levels[i % len(levels)])
            state, err = play_once(stdin, asked)
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
            say(f"  {script}: {err[0]}", RED)
            if err[1]:
                say(f"    {err[1]}", DIM)
        else:
            say(f"  {script}: never got going -- the game kept asking "
                f"{err[0][:36]!r}", YELLOW)
    if trouble:
        say()
    say(f"  {len(rows)} scripts, {len(rows) * runs} games.",
        (RED if trouble else GREEN) + BOLD)
    say()
    coverage(asked, len(rows) * runs)
    say("  This is what the WHOLE suite covers. A menu listed with only one", DIM)
    say("  answer is untried by every script you have, not just by one.", DIM)
    say()
    sys.exit(1 if trouble else 0)


def play_once(stdin, asked_so_far):
    try:
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
        bucket = OURS if i < SETUP_COUNT[0] else asked_so_far
        bucket.setdefault(prompt, set()).add(answer)
    blob = done.stdout + errors
    err = first_real_error(blob)
    if err:
        return "crashed", err
    jam = jam_line(blob)
    if jam:
        return "jammed", jam
    return "ok", None


def main():
    say()
    say("  Block Builder - playtest", BOLD)
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
            first = (PLAYS / f"{n}.txt").read_text(encoding="utf-8").split()
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
                with open(PLAYS / f"{script}.txt", encoding="utf-8") as f:
                    choices = [ln.strip() for ln in f if ln.strip()]
                level = levels[number % len(levels)]
                show_one(script,
                         build_answers(PLAYS / f"{script}.txt", player, level),
                         choices, player, level)
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
        say(f"  Every script, {runs} games each{who}{how}.")
        say()
        run_all(runs, player, levels)
        return
    if "--show" in flags or "-s" in flags:
        with open(PLAYS / f"{name}.txt", encoding="utf-8") as answers_file:
            choices = [ln.strip() for ln in answers_file if ln.strip()]
        show_one(name, build_answers(PLAYS / f"{name}.txt", player, levels[0]),
                 choices, player, levels[0])
        return

    runs = max(1, int(numbers[0])) if numbers else DEFAULT_RUNS
    say(f"  Playing {runs} games, answering from plays/{name}.txt ...")
    if player or levels[0]:
        where = ("from plays/_player.txt" if (PLAYS / "_player.txt").exists()
                 else "built-in defaults -- make plays/_player.txt to change them")
        say(f"  {DIM}Playing as {player}, rotating difficulty "
            f"{', '.join(levels)} -- {where}{OFF}")
    say(f"  {DIM}Same answers every game -- but the dice are different, so the"
        f"{OFF}")
    say(f"  {DIM}games are not. That is why it is {runs} and not one.{OFF}")
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
    sys.exit(1)


if __name__ == "__main__":
    main()
