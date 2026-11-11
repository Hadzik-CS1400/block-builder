# =============================================================================
# Block Builder - Week 9: Formatted Displays & Journal
# =============================================================================
# Module topic: f-strings, string formatting, string methods
# NEW Python this week: format specifiers (width, alignment, fill, %),
#   .upper(), .strip(), .split()
# From before: print, variables, input, arithmetic, if/elif/else, for, while,
#   def/return/defaults, random, math
# NOT yet: lists, dicts, files, classes
#
# There is no Week 8. Week 8 of the course is midterm week and carries no
# game session, so we go Week 7 -> Week 9.
#
# WHAT YOU'LL BUILD
#   Your game works and it is ugly. The status lines wander, the numbers do
#   not line up, and nothing records what happened.
#
#   This week is entirely about the OUTPUT. The rules do not change, no new
#   mechanic appears, and the game plays exactly as it did last week. What
#   changes is that somebody can read it.
#
#     - a status panel whose numbers form a column
#     - a header that shouts, centered, with a rule running out to both edges
#     - a survival bar drawn out of repeated characters
#     - a journal that records what happened on which day
#
# HOW TO WORK THIS WEEK
#   Open YOUR game.py and change it. Do not start a new file.
#
#   This is the easiest week to check as you go: run the game after every
#   TODO and LOOK at it. A column that does not line up is visible.
#
# THE JOURNAL, WITHOUT LISTS
#   A list is the obvious tool for "many things" and you meet it in class
#   this week -- but the game is a module behind, so you do it the way
#   people did before lists: ONE string, with a character between entries.
#
#       journal = "Day 1: Found iron|Day 3: Mob attack"
#
#   Building it is concatenation. Reading it back is .split("|"). That is
#   the whole trick, and it is worth seeing once, because it is why lists
#   feel like such a relief next week.
#
# WHAT'S TESTED (20 points)
#   5 pts  The status panel lines up
#   5 pts  A header is shouted and centered
#   5 pts  The journal records the day
#   5 pts  The game still plays
#
#   Nothing checks your wording. Call the panel what you like.
#
# TIPS
#   - A format specifier goes after a colon INSIDE the braces:
#         f"{health:>5}"      right-aligned in five characters
#         f"{'Health:':<12}"  left-aligned in twelve
#     Text left, numbers right. That is what puts the digits in a column.
#   - A character before < > or ^ fills the space instead of blanks:
#         f"{header:=^50}"    centered in fifty, padded with =
#   - .upper() does not change the string it is called on -- it hands back a
#     new one. `name.upper()` on its own line does nothing at all. This is
#     the string rule from Module 7, and it is the opposite of the list rule
#     you are learning in class right now. Keep them apart.
#   - :.0% formats a fraction as a whole percentage: 0.4 becomes 40%.
#   - Run it and look. This is the one week where the tests and your eyes
#     agree completely.
# =============================================================================


# -----------------------------------------------------------------------------
# STEP 1: line the status numbers up
# -----------------------------------------------------------------------------
# Find where your game prints the player's resources. It is probably a run of
# prints like this, and the numbers land wherever they land:
#
#       print("Health:", health)
#       print("Wood:", wood)
#
# TODO 1: rewrite each status line as an f-string with a width on the LABEL
#         and a width on the NUMBER:
#
#             print(f"  {'Health:':<12} {health:>5}")
#             print(f"  {'Wood:':<12} {wood:>5}")
#
#         Do all of them -- health, food, water, wood, stone, iron. Run the
#         game and look at the right-hand edge: the digits should form a
#         straight line whether the number is 7 or 100.


# -----------------------------------------------------------------------------
# STEP 2: a header that shouts
# -----------------------------------------------------------------------------
# TODO 2a: build a header string out of the player's name and the day, and
#          put it in capitals with .upper():
#
#              header = f" {name}'s World - Day {day} ".upper()
#
#          Keep the spaces at the ends. They become the gap between the text
#          and the fill characters in a moment.
#
# TODO 2b: print it centered in fifty characters, filled with =
#
#              print(f"{header:=^50}")
#
#          ^ centers. The = before it is the fill character. Try - and * and
#          pick the one you like.


# -----------------------------------------------------------------------------
# STEP 3: rewrite the survival bar
# -----------------------------------------------------------------------------
# YOU ARE NOT WRITING A NEW FUNCTION HERE. You already have one -- you wrote
# draw_progress() back in Week 6 and gave it a width parameter in Week 7. Find
# it in your game.py. It looks like this:
#
#     def draw_progress(day, max_days, width=20):
#         progress = day * width // max_days
#         bar = ""
#         for i in range(width):
#             if i < progress:
#                 bar = bar + "#"
#             else:
#                 bar = bar + "-"
#         print("Survival: [" + bar + "] Day " + str(day) + "/" + str(max_days))
#
# It works. It is also eight lines doing what two can do, now that you have
# f-strings and string repetition.
#
# TODO 3: replace the BODY of your draw_progress with this:
#
#     def draw_progress(day, max_days, width=30):
#         pct = day / max_days
#         if pct > 1:
#             pct = 1
#         filled = int(width * pct)
#         print(f"  Survival: [{'#' * filled}{'-' * (width - filled)}] {pct:.0%}")
#
#         Four things changed, and each is worth knowing:
#
#         1. THE LOOP IS GONE. The old one grew the bar a character at a
#            time, going round thirty times to build thirty characters.
#            '#' * filled builds the whole run in one go. Same output --
#            check it against your old version if you want to be sure.
#
#         2. THE DEFAULT WIDTH IS NOW 30. At 20 the bar line came out at 38
#            characters under a 50-wide panel and looked stranded. Note it is
#            `width` doing the work in both places, not a hardcoded 30 --
#            thirty is the bar's WIDTH and has nothing to do with max_days
#            being thirty. They are equal by coincidence. Change max_days to
#            45 and the bar should still be thirty wide.
#
#         3. IT SHOWS A PERCENTAGE, not "Day 8/30" -- the day is already in
#            the header you built in STEP 2, so printing it twice is noise.
#            :.0% turns 0.27 into 27% and does the x100 for you.
#
#         4. THE `if` IS NEW, and it is the one to understand -- because it
#            is the price of the shorter code, not a bug you had.
#
#            The old loop could NEVER draw the wrong number of characters.
#            `for i in range(width)` runs exactly width times whatever the
#            day is, so even on day 40 of 30 it drew a full bar of 20. The
#            loop was its own guard.
#
#            Repetition has no such guard. Past day 30 pct goes over 1, so
#            filled goes over width, and then
#
#                '-' * (30 - 31)
#
#            is NOT an error. Python hands back an empty string for a
#            negative count, quite happily. The bar grows a character, the
#            empty half disappears, and every line under it stops lining up
#            -- with nothing to tell you why.
#
#            So: you traded eight lines for two, and bought one `if` with the
#            change. That is a trade worth making, and worth noticing you
#            made. Shorter code is not automatically safer code.
#
#         int() still matters for the same reason it always did: you cannot
#         repeat a string a fractional number of times.


# -----------------------------------------------------------------------------
# STEP 4: start a journal
# -----------------------------------------------------------------------------
# TODO 4a: ABOVE your main loop, write a function that adds one entry to a
#          journal string and hands the new journal back:
#
#              def add_journal(journal, day, event):
#                  entry = f"Day {day}: {event}"
#                  if journal == "":
#                      return entry
#                  return journal + "|" + entry
#
#          The if is there so the journal does not begin with a stray |.
#
# TODO 4b: before the loop starts, make an empty journal:
#
#              journal = ""
#
# TODO 4c: call it when something worth recording happens -- a mob attack,
#          finding iron, surviving a night. KEEP what it hands back:
#
#              journal = add_journal(journal, day, "Mob attack! -10 hp")
#
#          Not just `add_journal(...)` on its own line. It returns the new
#          journal; throwing it away leaves the old one.


# -----------------------------------------------------------------------------
# STEP 5: read the journal back
# -----------------------------------------------------------------------------
# TODO 5: write a function that prints the journal one entry per line, and
#         call it when the game ends:
#
#             def show_journal(journal):
#                 print("=" * 50)
#                 for entry in journal.split("|"):
#                     print(entry)
#
#         .split("|") takes the one long string apart at every | and hands
#         back the pieces, which the for loop walks. You joined them with a
#         character; you split them on the same character.


# -----------------------------------------------------------------------------
# STEP 6: tidy the input
# -----------------------------------------------------------------------------
# TODO 6: when you read the player's name, .strip() the spaces off:
#
#             name = input("Name: ").strip()
#
#         A name typed with a trailing space breaks every width you set in
#         STEP 1, and the player will never work out why.


# -----------------------------------------------------------------------------
# STEP 7: play it and score it
# -----------------------------------------------------------------------------
# TODO 7: run `python game.py` and play a full game. The rules should behave
#         exactly as they did last week -- only the display has changed.
#
#         Then score it:
#
#             python tests/check_week.py 9
#
#         Type the 9. sync.py brings later weeks' files down too, and with no
#         number the scorecard grades the NEWEST week it can find.


# ---- COMMIT -----------------------------------------------------------------
#   git add game.py
#   git commit -m "feat: format the status panel and keep a journal"
#   git push
