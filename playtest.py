"""playtest.py - the settings. This is the only file here you might change.

Run it exactly as before:

    python playtest.py              list your scripts
    python playtest.py all          run every script
    python playtest.py normal 50    one script, 50 runs
    python playtest.py normal -s    one run, printed line by line

The answers your program is given live in the plays folder, one file per
plan, and those ARE yours to write - open plays/normal.txt and see.

The machinery lives in playtest_engine.py. You never need to open it. It is
commented line by line if you ever want to, but nothing in it is on a test
and changing it affects every script you run.
"""

# Which file to play. None means "the .py file sitting next to this one",
# which is right for Block Builder and for most final projects. Set it to a
# name, like "budget.py", only if there is more than one and it picks wrong.
PROGRAM = None

# How many times to play one script when you do not give a number yourself.
RUNS = 20

# Seconds a single run is allowed before it counts as stuck. Raise it if
# your program is genuinely slow; leave it if your program is genuinely
# looping, because that is the bug and you want to hear about it.
TIMEOUT = 30

# The heading at the top of the report. None picks one from the file name.
TITLE = None


try:
    from playtest_engine import main
except ImportError:
    raise SystemExit(
        "playtest.py cannot find playtest_engine.py.\n"
        "The two files work as a pair and must sit in the same folder.\n"
        "If you copied this into another project, copy playtest_engine.py\n"
        "and the plays folder across as well."
    )


if __name__ == "__main__":
    main(program=PROGRAM, runs=RUNS, timeout=TIMEOUT, title=TITLE)
