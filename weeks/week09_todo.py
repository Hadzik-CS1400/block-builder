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
# STEP 3: a survival bar
# -----------------------------------------------------------------------------
# A progress bar is two repeated strings next to each other: the filled part
# and the empty part.
#
# TODO 3: work out how far through the thirty days the player is, and draw it:
#
#             pct = day / max_days
#             filled = int(20 * pct)
#             print(f"  Survival: [{'#' * filled}{'-' * (20 - filled)}] {pct:.0%}")
#
#         :.0% turns 0.4 into 40%. The int() matters -- you cannot repeat a
#         string a fractional number of times.


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
