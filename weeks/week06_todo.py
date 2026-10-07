# =============================================================================
# Block Builder - Week 6: Main Game Loop & Menus
# =============================================================================
# Module topic: while loops, input validation, menu-driven programs
# NEW Python this week: while, validating input by asking again, menus
# From before: print, variables, input, arithmetic, if/elif/else, for, random
# NOT yet: functions, string methods, lists, dicts, files, classes
#
# WHAT YOU'LL BUILD
#   Week 5 played exactly one day. This week your game plays until it is over:
#   thirty days, or death, whichever comes first. The whole day goes INSIDE a
#   while loop, so your for loop over the actions is now a loop inside a loop.
#
#   You also stop accepting nonsense. Week 4 took one bad answer and shrugged
#   -- "that is not 1, 2 or 3, defaulting to Normal". A while loop can just
#   keep asking until the answer is usable, which is what every real program
#   does.
#
#   Last, the crafting bench becomes a MENU: print the options, read a
#   validated choice, act on it with if/elif. You already know all three
#   pieces; a menu is just the three of them together.
#
# HOW TO WORK THIS WEEK
#   Open YOUR game.py and change it. Do not start a new file. Your colors,
#   your numbers and your story stay.
#
#   STEP 3 is the big one and it is mostly indenting. Select your whole day --
#   the status block, the for loop over the actions, crafting, eating, night,
#   the end-of-day status -- and press Tab once. That is the week.
#
# WHAT'S TESTED (20 points)
#   5 pts  The main loop plays more than one day
#   5 pts  Bad input is rejected instead of defaulted
#   5 pts  The crafting menu offers choices and a way out
#   5 pts  The game ends, and says how it ended
#
# TIPS
#   - A while loop needs three things, same as the countdown in CT07: a
#     variable set BEFORE it, a condition, and something INSIDE that changes
#     the condition. Miss the third and it runs forever.
#   - `while not game_over:` reads as "keep going while the game is not over".
#     game_over starts False, and the end-of-day check is what sets it True.
#   - Ctrl+C stops a runaway program. If your game replays day 1 forever, you
#     forgot `day = day + 1` at the bottom of the loop.
#   - The validation pattern is always the same shape: set the variable to ""
#     first, then `while it is not one of the things I accept:` ask again.
#   - Indentation is the whole of STEP 3. If Python complains about an
#     unexpected indent, one line inside the day did not move with the rest.
# =============================================================================

# -----------------------------------------------------------------------------
# STEP 1: stop accepting bad difficulties
# -----------------------------------------------------------------------------
# Find your Week 4 validation -- the bit that prints "defaulting to Normal" --
# and REPLACE it. Instead of giving up after one bad answer, keep asking.
#
# The shape, which you will use twice more this week:
#
#     difficulty = ""                       # start with something invalid
#     while difficulty != "1" and difficulty != "2" and difficulty != "3":
#         difficulty = input("Enter 1, 2, or 3: ")
#         if difficulty != "1" and ... :    # still bad? say so
#             print("[red]That is not 1, 2, or 3. Try again.[/red]")
#
# TODO 1: replace the Week 4 default-to-Normal block with a while loop that
#         asks until the answer is "1", "2" or "3".


# -----------------------------------------------------------------------------
# STEP 2: the state the loop needs
# -----------------------------------------------------------------------------
# A while loop needs an off switch, and the game needs to remember what you
# built. Add these next to your `day = 1`.
#
# TODO 2: add these five variables:
#
#         max_days = 30             # the win condition
#         game_over = False         # the loop's off switch
#         has_shelter = False       # remembered between days now
#         has_crafting_bench = False
#         has_pickaxe = False


# -----------------------------------------------------------------------------
# STEP 3: wrap the day in the main game loop
# -----------------------------------------------------------------------------
# This is the week, and it is mostly a Tab key.
#
# TODO 3: write `while not game_over:` just above your day, then INDENT your
#         entire Week 5 day inside it -- the status display, the for loop over
#         the actions and everything in it, crafting, eating, the night check,
#         the shelter drawing, the end-of-day status. All of it moves one
#         level right.
#
#         Nothing inside needs rewriting. Your for loop over the actions is
#         now a loop inside a loop, which is the only thing that changed.
#
# A day header is worth printing at the top of the loop, so you can see the
# days going by. This part is given to you -- indent it inside the while:

    print()
    print("=" * 50)
    print("[bold]Day " + str(day) + " of " + str(max_days) + "[/bold]")
    print("Health: " + str(health) + "  Food: " + str(food)
          + "  Water: " + str(water))
    print("=" * 50)


# -----------------------------------------------------------------------------
# STEP 4: validate the action choice too
# -----------------------------------------------------------------------------
# Your action menu reads a choice with input(). Right now anything that is not
# 1 to 5 falls through to your "wasted action" else. Make it ask again instead,
# and add a sixth option while you are there.
#
# TODO 4: add `6 - Craft` to the action menu you print.
#
# TODO 5: validate the choice with the same while-loop shape as STEP 1 -- keep
#         asking until it is "1" through "6".


# -----------------------------------------------------------------------------
# STEP 5: the crafting menu
# -----------------------------------------------------------------------------
# Choice "6" opens a menu. A menu is three things you already know: a print
# block, a validated input, and an if/elif chain.
#
# TODO 6: under `elif choice == "6":` print the bench:
#
#             a - Wooden pickaxe  (3 wood, 2 stone)
#             b - Shelter         (20 wood, 10 stone)
#             c - Crafting bench  (10 wood, 5 stone, 2 iron)
#             d - Cancel
#
# TODO 7: read the letter with a validation while loop -- keep asking until it
#         is "a", "b", "c" or "d".
#
# TODO 8: act on it with if/elif. Each recipe checks it can afford EVERY
#         ingredient (that is `and`, from Week 3), takes the materials, and
#         sets its has_ flag to True:
#
#             if craft == "a":
#                 if wood >= 3 and stone >= 2:
#                     wood = wood - 3
#                     stone = stone - 2
#                     has_pickaxe = True
#                     print("[green]    Crafted a wooden pickaxe![/green]")
#                 else:
#                     print("[red]    Need 3 wood and 2 stone.[/red]")
#
#         "d" is Cancel, so it does nothing at all -- that is why the player
#         needs it. Pick your own recipes and prices if you like.


# -----------------------------------------------------------------------------
# STEP 6: a progress bar (given to you)
# -----------------------------------------------------------------------------
# A for loop building up a string, one character at a time. Nothing new -- it
# just looks good. Indent it inside the while loop, after the night phase.

    progress = day * 20 // max_days
    bar = ""
    for i in range(20):
        if i < progress:
            bar = bar + "#"
        else:
            bar = bar + "-"
    print("Survival: [" + bar + "] Day " + str(day) + "/" + str(max_days))


# -----------------------------------------------------------------------------
# STEP 7: end the game
# -----------------------------------------------------------------------------
# The loop runs `while not game_over`, so something has to set game_over to
# True or it never stops. Two ways to finish, and they read differently.
#
# TODO 9: at the bottom of the loop, still INSIDE it:
#
#           - if health is 0 or less: set game_over = True and print that they
#             died, and which day they got to.
#           - elif day has reached max_days: set game_over = True and print
#             that they survived. This is the win, so make it sound like one --
#             your has_shelter and has_crafting_bench flags are worth checking
#             here for a better ending.
#
# TODO 10: the very last line inside the loop:
#
#              day = day + 1
#
#          This is the line that makes the condition eventually change. Without
#          it the game replays day 1 forever and you have to Ctrl+C out. It is
#          the single most common bug of the week, and the tests will tell you
#          if you have it.
