# =============================================================================
# Block Builder - Week 5: Day Cycle - Gather Resources
# =============================================================================
# Module topic: for loops, range(), break, continue, nested loops
# NEW Python this week: for, range(), break, continue, a loop inside a loop
# From before: print, variables, input, arithmetic, if/elif/else, random
# NOT yet: while loops, functions, lists
#
# WHAT YOU'LL BUILD
#   Your day stops being one event and becomes a DAY. A for loop gives the
#   player several actions before night falls, and each action is a menu: chop,
#   mine, gather, collect, or explore. Your Week 3 exploration event does not
#   get rewritten -- it gets INDENTED, so it can happen more than once.
#
#   Then two words that control a loop from the inside: break ends the day
#   early when you are too weak to act, and continue throws away one action
#   when you are starving. Last, a loop inside a loop draws your shelter.
#
# HOW TO WORK THIS WEEK
#   Open YOUR game.py -- the one you have been building since Week 2 -- and
#   add the sections below. Do not start a new file, and do not copy this one
#   over the top of yours: your colors, your numbers and your story stay.
#
#   The one thing you MOVE is your Week 3 exploration event. It belongs inside
#   the new for loop now. Select it, press Tab to indent it, and leave it
#   otherwise alone.
#
# WHAT'S TESTED (20 points)
#   5 pts  The day runs several actions from a for loop
#   5 pts  range() decides how many actions, and difficulty sets the number
#   5 pts  break and continue are both used inside the loop
#   5 pts  A nested loop draws the shelter
#
# TIPS
#   - `for action in range(1, actions_per_day + 1):` counts 1, 2, 3 ... and
#     stops BEFORE the stop value, which is why it needs the + 1.
#   - Everything that happens during an action must be INDENTED under the for.
#     Indentation is the only thing that says what is inside the loop.
#   - break leaves the loop completely. continue skips the rest of THIS pass
#     and starts the next one. Neither needs an else.
#   - print("[]", end="") stays on the line; a bare print() ends the row. That
#     is what makes a nested loop draw a shape instead of a column.
#   - Run it often. A loop that does the wrong thing five times is easier to
#     spot than one that does it once.
# =============================================================================

# -----------------------------------------------------------------------------
# STEP 1: give each difficulty an actions_per_day
# -----------------------------------------------------------------------------
# Find the if/elif/else that sets up your world in game.py. Each branch already
# sets wood, stone, food, water and health. Add ONE more variable to each.
#
# Harder difficulty means fewer actions in a day. Keep your own numbers if you
# would rather -- 6/5/4 is only a suggestion.
#
# TODO 1: in the Peaceful branch, set actions_per_day = 6
# TODO 2: in the Normal branch, set actions_per_day = 5
# TODO 3: in the Hardcore branch, set actions_per_day = 4


# -----------------------------------------------------------------------------
# STEP 2: announce the day
# -----------------------------------------------------------------------------
# Paste this in after your starting status block. It is given to you -- change
# the wording or the colors if you like.

print()
print("[bold green]Day " + str(day) + " begins. You have "
      + str(actions_per_day) + " actions before night falls.[/bold green]")
print()
print("-" * 50)
print("[bold]Day " + str(day) + " - " + str(actions_per_day)
      + " actions available[/bold]")
print("-" * 50)


# -----------------------------------------------------------------------------
# STEP 3: the day cycle
# -----------------------------------------------------------------------------
# This is the week. One for loop, and everything an action does lives inside it.
#
# TODO 4: write the for loop that counts this day's actions. It runs
#         actions_per_day times and the loop variable should be called
#         `action`, because the menu below prints it.
#
#            for action in range(1, actions_per_day + 1):
#
#         Everything from TODO 5 down to the end of STEP 3 is INDENTED inside
#         it.

    # TODO 5: break -- if health is 0 or less, print something final and
    #         break out. There is no point taking an action while dead.

    # TODO 6: continue -- if food is 0 or less AND water is 0 or less, take 5
    #         health off, say the player is starving and cannot act, then
    #         continue. That throws away the rest of this action only.

    # --- The action menu (given to you) ---
    # Indent all of this inside your for loop.

    print()
    print("[bold]Action " + str(action) + " of " + str(actions_per_day)
          + "[/bold]")
    print("  1 - Chop wood")
    print("  2 - Mine stone")
    print("  3 - Gather food")
    print("  4 - Collect water")
    print("  5 - Explore (risky)")
    choice = input("  What do you do? ")

    # TODO 7: choices 1 to 4 each add a random amount to one resource and say
    #         so. One elif per choice, the same shape as this first one:
    #
    #            if choice == "1":
    #                gained = random.randint(2, 5)
    #                wood = wood + gained
    #                print("[green]  +" + str(gained) + " wood[/green]")
    #
    #         2 is stone, 3 is food, 4 is water. Pick your own ranges.

    # TODO 8: choice "5" is where your WEEK 3 EXPLORATION EVENT goes. Do not
    #         retype it -- move it. Select the whole `event = random.randint(...)`
    #         block and everything under it, cut it from where it is now, paste
    #         it here, and indent it so it sits inside this elif.
    #
    #         It worked last week and it still works. The only difference is
    #         that it can now happen several times in one day.

    # TODO 9: an else for anything that is not 1 to 5 -- a wasted action.


# -----------------------------------------------------------------------------
# STEP 4: the rest of the day (you already have this)
# -----------------------------------------------------------------------------
# Your crafting, eating and night-check blocks from Week 4 go here, OUTSIDE the
# for loop -- back at the left margin. They happen once per day, not once per
# action, and the indentation is what says so.


# -----------------------------------------------------------------------------
# STEP 5: draw the shelter with a nested loop
# -----------------------------------------------------------------------------
# A loop inside a loop. The outer one picks the row; the inner one draws the
# blocks across that row.
#
# shelter_level is how many blocks wide the shelter is -- one per 5 wood, four
# at most.

shelter_level = wood // 5
if shelter_level > 4:
    shelter_level = 4

print()
print("Shelter: ", end="")

# TODO 10: write two loops, one inside the other. The outer loop runs twice --
#          `for row in range(2):` -- once for the roof and once for the walls.
#          Inside it, a second loop runs shelter_level times and prints one
#          block with end="" so they line up across the row:
#
#             row 0 (the roof)   print("/\\", end="")
#             row 1 (the walls)  print("[]", end="")
#
#          After each inner loop finishes, a bare print() ends the row. An
#          if/else on `row` picks which block to draw.
#
#          Shelter level 3 should look like this:
#
#             Shelter: /\/\/\
#                      [][][]
