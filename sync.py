"""
Block Builder - weekly sync

Run this at the start of every Block Builder session to get the new week's
files:

    python sync.py

It is safe to run any time, and safe to run twice. It will tell you exactly
what to do if something needs your attention.

You do not need to understand this file. Do not edit it.
"""
import subprocess
import sys
from pathlib import Path

UPSTREAM_URL = "https://github.com/Hadzik-CS1400/block-builder.git"
REPO = Path(__file__).resolve().parent

GREEN, YELLOW, RED, DIM, BOLD, OFF = (
    "\033[92m", "\033[93m", "\033[91m", "\033[2m", "\033[1m", "\033[0m"
)


def say(msg="", color=""):
    print(f"{color}{msg}{OFF}" if color else msg)


def rule():
    say("-" * 62, DIM)


def git(*args, check=False):
    """Run a git command inside the repo and hand back the result."""
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, check=check
    )


def die(title, *lines):
    say()
    rule()
    say(f"  {title}", RED + BOLD)
    rule()
    for line in lines:
        say(f"  {line}")
    say()
    sys.exit(1)


# Paths the instructor owns. Everything here is fetched, never authored by a
# student, so upstream's version is correct by definition and a conflict in one
# can be resolved without asking. Anything NOT matching this is the student's,
# and is never touched automatically.
#
# game.py is the important omission: it does not exist in the class repo at
# all, so it can never conflict -- but if that ever changes, it falls through
# to the "your own work" branch and stops for a human.
INSTRUCTOR_PATHS = ("weeks/", "tests/", "solutions/", "images/")
INSTRUCTOR_FILES = ("README.md", "sync.py", "requirements.txt", ".gitignore")


def owned_by_student(path):
    path = path.replace("\\", "/")
    if path in INSTRUCTOR_FILES:
        return False
    return not path.startswith(INSTRUCTOR_PATHS)


def main():
    say()
    say("  Block Builder - weekly sync", BOLD)
    rule()

    # --- 0. Is git even here, and are we in the repo? ---------------------
    if git("rev-parse", "--git-dir").returncode != 0:
        die("This folder isn't a git repository.",
            "Make sure you're running this from inside your block-builder",
            "folder - the one with README.md in it.")

    # --- 1. Unsaved work blocks a pull -----------------------------------
    dirty = git("status", "--porcelain").stdout.strip()
    if dirty:
        say()
        rule()
        say("  Commit your work first", YELLOW + BOLD)
        rule()
        say("  You have changes that aren't committed yet. Save them before")
        say("  pulling, so nothing can get lost:")
        say()
        say('    git add -A', BOLD)
        say('    git commit -m "my work so far"', BOLD)
        say()
        say("  Then run  python sync.py  again.")
        say()
        say("  Not committed yet:", DIM)
        for line in dirty.splitlines()[:10]:
            say(f"    {line}", DIM)
        say()
        sys.exit(1)

    # --- 2. Make sure the class repo is connected ------------------------
    remotes = git("remote").stdout.split()
    if "upstream" not in remotes:
        say("  Connecting to the class repo for the first time...")
        if git("remote", "add", "upstream", UPSTREAM_URL).returncode != 0:
            die("Couldn't connect to the class repo.",
                "Ask your instructor for help.")
        say("  Connected.", GREEN)

    # --- 3. Fetch --------------------------------------------------------
    say("  Checking for new files...")
    fetched = git("fetch", "upstream")
    if fetched.returncode != 0:
        die("Couldn't reach GitHub.",
            "Check your internet connection and try again.",
            "",
            "If you're on campus wifi and it still fails, tell your",
            "instructor - it may be a GitHub sign-in problem.")

    before = set(git("ls-files").stdout.split())
    before_tree = git("rev-parse", "HEAD^{tree}").stdout.strip()

    # --- 4. Already up to date? ------------------------------------------
    local = git("rev-parse", "HEAD").stdout.strip()
    remote = git("rev-parse", "upstream/main").stdout.strip()
    if git("merge-base", "--is-ancestor", remote, local).returncode == 0:
        say()
        say("  You already have everything. Nothing new this week yet.", GREEN)
        check_game_file()
        return

    # --- 5. Pull ---------------------------------------------------------
    # A repo made with "Use this template" starts its own history, so the very
    # first pull has no common ancestor and git needs to be told that's fine.
    args = ["pull", "upstream", "main", "--no-rebase"]
    if git("merge-base", "HEAD", "upstream/main").returncode != 0:
        args.append("--allow-unrelated-histories")

    pulled = git(*args)
    if pulled.returncode != 0:
        conflicts = git("diff", "--name-only", "--diff-filter=U").stdout.split()

        # Conflicts in files the student does not own are not a student
        # problem, and on the first sync they are close to guaranteed.
        #
        # A repo made from the template starts its own history, so there is no
        # common ancestor for git to compare against. It cannot tell that the
        # student's copy of README.md is simply the older one -- both sides
        # look like "added this file", and every instructor file that changed
        # since the repo was created comes back as an add/add conflict. Adding
        # new files stays clean; editing existing ones is what collides.
        #
        # The ownership rule already answers it: these files are mine, the
        # student never edits them, so upstream is correct by definition. Take
        # it and carry on rather than stopping them on their first run.
        mine = [c for c in conflicts if not owned_by_student(c)]
        theirs = [c for c in conflicts if owned_by_student(c)]

        if conflicts and not theirs:
            for path in mine:
                git("checkout", "--theirs", "--", path)
                git("add", "--", path)
            committed = git("commit", "--no-edit")
            if committed.returncode == 0:
                say()
                say("  Updated my files to the current version.", DIM)
                for path in mine:
                    say(f"    {path}", DIM)
                say("  Your game.py was not touched.", DIM)
            else:
                die("Sync failed.",
                    "Show your instructor this message:",
                    "",
                    *committed.stderr.strip().splitlines()[:6])
        elif conflicts:
            die("Sync hit a conflict in your own work.",
                "These are files you own, so I will not overwrite them:",
                "",
                *[f"  - {c}" for c in theirs],
                "",
                "Nothing is lost. Do not run any more git commands until",
                "you've asked - it's a two-minute fix.")
        else:
            die("Sync failed.",
                "Show your instructor this message:",
                "",
                *pulled.stderr.strip().splitlines()[:6])

    # --- 6. Report what arrived ------------------------------------------
    after = set(git("ls-files").stdout.split())
    new = sorted(after - before)

    say()
    if new:
        todo = [f for f in new if f.startswith("weeks/")]
        test = [f for f in new if f.startswith("tests/")]
        sols = [f for f in new if f.startswith("solutions/")
                and f.endswith(".py")]

        say("  New this week:", GREEN + BOLD)
        for f in new:
            say(f"    {f}", GREEN)
        say()
        if todo:
            say(f"  Start here:  {todo[0]}", BOLD)
        if test:
            say(f"  Score it:    pytest {test[0]} -v")
        if sols:
            say()
            say("  Last week's solution is now available:", YELLOW + BOLD)
            for f in sols:
                say(f"    {f}", YELLOW)
            say("  Behind, or missed last week? Open it beside your game.py", DIM)
            say("  and copy across what you're missing. Don't fall further.", DIM)
    elif git("rev-parse", "HEAD^{tree}").stdout.strip() != before_tree:
        say("  Updated. No new week files - your instructor fixed", GREEN)
        say("  something in the existing ones.", GREEN)
    else:
        say("  You're up to date. Nothing new this week yet.", GREEN)

    check_game_file()


def check_game_file():
    """Week 2 is the only week that creates game.py; nudge if it's missing."""
    if (REPO / "game.py").exists():
        return
    week2 = REPO / "weeks" / "week02_todo.py"
    if not week2.exists():
        return
    say()
    rule()
    say("  You don't have a game.py yet", YELLOW + BOLD)
    rule()
    say("  Open  weeks/week02_todo.py  and use File > Save As to save it as")
    say(f"  {BOLD}game.py{OFF} in this folder (next to README.md, NOT inside weeks/).")
    say()
    say("  That file becomes your game for the rest of the semester.")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        say()
        say("  git isn't installed, or isn't on your PATH.", RED + BOLD)
        say("  Reinstall Git for Windows and reopen VS Code.")
        sys.exit(1)
    say()
