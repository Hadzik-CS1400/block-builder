# =============================================================================
# Block Builder - Week 7B: Finish the Refactor
# =============================================================================
# Module topic: functions (Module 6), applied to the rest of the file
#
# This is a SEPARATE assignment worth its own 20 points. Week 7 asked for four
# functions and you have already been scored on them. Nothing here takes that
# away -- this is the other ten.
#
# Your Week 7 file, weeks/week07_todo.py, is untouched. Leave it alone; you
# will want STEP 1 to STEP 7 beside you as a reminder of the move.
#
# Score this one with the 7b on the end:
#
#     python tests/check_week.py 7b
#
# STUCK ON WHAT "MOVE IT INTO A FUNCTION" ACTUALLY MEANS?
#   Open docs/week07_refactor.html in a browser -- double-click it. It shows
#   ten blocks of THIS game before and after, side by side, with the block lit
#   in both places: where it used to be, and the one line left behind where it
#   was. Each one also names what had to go IN as a parameter and what had to
#   come OUT as a return. Nothing in it runs; it is about the shape of your
#   file.
# =============================================================================


# =============================================================================
# This is a second assignment worth its own twenty, for carrying the refactor
# through the rest of the file. The worked answer has FOURTEEN functions, not
# four -- these are the other ten, and they are the same move repeated.
# Repeating it is how it stops feeling clever and starts feeling obvious.
#
# WHAT'S TESTED (20 points)
#   5 pts  The refactor reaches the whole file   -- ten or more functions
#   5 pts  Several functions only print          -- three or more
#   5 pts  A function hands back several values  -- two or more, and kept
#   5 pts  The game still plays                  -- same behaviour as before
#
# Score it with the 7b on the end:
#
#     python tests/check_week.py 7b
#
# STUCK ON WHAT "MOVE IT INTO A FUNCTION" ACTUALLY MEANS?
#   Open docs/week07_refactor.html in a browser -- double-click it. It shows
#   six blocks of THIS game before and after, side by side, with the block
#   lit in both places: where it used to be, and the one line left behind
#   where it was. It also names, for each one, what had to go IN and what had
#   to come OUT, and why. Nothing in it runs; it is about the shape of your
#   file.
#
# Nothing checks your function NAMES. The tests look at the shape.
#
# EVERY ONE OF THESE TEN GETS A DOCSTRING, same as the four in Part A.
# One line, in triple quotes, directly under the def, saying what the
# function DOES -- not how it works:
#
#     def draw_progress(day, max_days):
#         """Print the survival bar for the current day."""
#
# With ten more functions in the file, the docstrings are how you find the
# one you want without reading its body. Say what it hands back, too, if it
# hands anything back -- that is the thing you will forget first:
#
#     def explore(health, wood, stone, iron, food, water):
#         """Run one random exploration event; return all six resources."""
#
# A # comment explains a line. A docstring explains the function.
#
# Take them in any order. Run the game after each one. If a change makes the
# game behave differently, undo it -- a refactor that changes behaviour is
# just a bug with good intentions.


# -----------------------------------------------------------------------------
# STEP 8: the blocks that only print
# -----------------------------------------------------------------------------
# The easiest ones to move, because they read values and print them and do
# nothing else. Nothing has to be handed back.
#
# TODO 8: wrap each of these in a function that takes what it
#         prints. Suggested names, but call them whatever you like:
#
#             def title_screen():
#             def show_starting_status(name, day, health, wood, stone, ...):
#             def draw_shelter(wood):
#             def draw_progress(day, max_days):
#
#         Docstring on each one. These are the easy ones to write:
#         """Print the title screen.""" and you are done.
#
#         title_screen() takes no parameters at all, which is allowed and
#         normal: it needs nothing from the rest of the program.


# -----------------------------------------------------------------------------
# STEP 9: two more defaults
# -----------------------------------------------------------------------------
# STEP 3 gave gather() defaults. These two want them for the same reason --
# the numbers are nearly always the same, and spelling them out at every
# call is noise.
#
# TODO 9: give these defaulted parameters:
#
#             def shelter_plan(wood, walls_needed=4, wood_per_wall=5):
#             def eat_and_drink(food, water, health, food_cost=2, water_cost=2):
#
#         Then call each one BOTH ways -- once plainly, and once overriding a
#         default -- and watch the same function do two jobs.
#
#         Docstring each one, and name the default in it:
#             """Report the wood the shelter needs; 4 walls unless told otherwise."""


# -----------------------------------------------------------------------------
# STEP 10: the event blocks
# -----------------------------------------------------------------------------
# These are the hard ones, and they are hard for a reason worth meeting: they
# change several values at once. A function cannot change your wood from the
# inside, so it has to hand everything back.
#
# TODO 10: move the exploring and the night into functions:
#
#             def explore(health, wood, stone, iron, food, water):
#                 ...
#                 return health, wood, stone, iron, food, water
#
#         and at the call site, take them all back in one line:
#
#             health, wood, stone, iron, food, water = explore(
#                 health, wood, stone, iron, food, water)
#
#         That is a lot of names on both sides. Notice it, and remember it --
#         Week 10 replaces every one of them with a single list, and this is
#         the mess it is fixing.
#
#         Docstring each one, and SAY WHAT COMES BACK -- these are the
#         functions whose returns you will forget: """...; return all six
#         resources."""


# -----------------------------------------------------------------------------
# STEP 11: the menus
# -----------------------------------------------------------------------------
# TODO 11: move the crafting menu and the opening questions into
#          functions of their own:
#
#             def craft_menu(wood, stone, iron, has_pickaxe, has_shelter, ...):
#             def get_player_info():
#
#          get_player_info() is the interesting one: it asks for a name and a
#          difficulty and hands back SEVERAL values at once, exactly the way
#          explore() does. One function, one job, several answers.
#
#         Docstring each one. If you cannot write the sentence, the function
#         is probably doing two things and wants splitting in half.


# ---- COMMIT -----------------------------------------------------------------
#   git add game.py
#   git commit -m "refactor: carry the function split through the rest of the file"
#   git push
