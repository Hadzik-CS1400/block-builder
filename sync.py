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


def say(msg="", colour=""):
    print(f"{colour}{msg}{OFF}" if colour else msg)


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
        if conflicts:
            die("Sync hit a conflict.",
                "This usually means a file you weren't meant to edit got",
                "changed. Show your instructor this list:",
                "",
                *[f"  - {c}" for c in conflicts],
                "",
                "Nothing is lost. Do not run any more git commands until",
                "you've asked - it's a two-minute fix.")
        die("Sync failed.",
            "Show your instructor this message:",
            "",
            *pulled.stderr.strip().splitlines()[:6])

    # --- 6. Report what arrived ------------------------------------------
    after = set(git("ls-files").stdout.split())
    new = sorted(after - before)

    say()
    if new:
        say("  New this week:", GREEN + BOLD)
        for f in new:
            say(f"    {f}", GREEN)
        todo = [f for f in new if f.startswith("weeks/")]
        test = [f for f in new if f.startswith("tests/")]
        say()
        if todo:
            say(f"  Start here:  {todo[0]}", BOLD)
        if test:
            say(f"  Score it:    pytest {test[0]} -v")
    else:
        say("  Updated. No new week files - your instructor fixed", GREEN)
        say("  something in the existing ones.", GREEN)

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
