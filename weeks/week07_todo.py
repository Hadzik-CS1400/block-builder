# =============================================================================
# Block Builder - Week 7: Refactor into Functions
# =============================================================================
# Module topic: function definitions, parameters, return values, defaults,
#   scope, imports
# NEW Python this week: def, parameters, return, default parameters, scope,
#   docstrings
# From before: print, variables, input, arithmetic, if/elif/else, for, while,
#   random, math
# NOT yet: lists, dicts, files, classes
#
# String methods are this week's CLASS topic, not this week's game topic --
# the game runs a module behind. You do not need a single one here.
#
# WHAT YOU'LL BUILD
#   Nothing. That is the week.
#
#   Your game works, and when you are finished it will work exactly the same:
#   same prompts, same numbers, same ending. What changes is the shape. The
#   eight lines of gathering that appear three times become ONE function
#   called three times. The craft check that appears once per recipe becomes
#   one function. The status block comes out of the day loop.
#
#   This is called refactoring, and it is most of what a working programmer
#   does. You will not see it from the outside, which is exactly why you run
#   the game after every step -- if the behavior changed, you broke it.
#
# HOW TO WORK THIS WEEK
#   Open YOUR game.py and change it. Do not start a new file.
#
#   MOVE code, do not retype it. Cut the block, paste it inside the def, put
#   a call where the block used to be. Retyping is how behavior changes by
#   accident, and you will not notice until the numbers drift.
#
#   One step at a time, and play the game after each one. Six functions
#   written before the first run means six places the bug could be hiding.
#
# WHAT'S TESTED (20 points)
#   5 pts  The repeated blocks are functions
#   5 pts  Functions hand values back
#   5 pts  A default parameter is used
#   5 pts  The game still plays
#
#   Nothing checks your function NAMES. Call it collect() instead of gather()
#   if you like -- the tests look at the shape, not the spelling.
#
# TIPS
#   - A function that PRINTS is not a function that RETURNS. gather() can
#     announce "You found 4 wood" perfectly and still leave your wood
#     untouched. The line that matters is `return amount`, and the call that
#     matters is `wood = wood + gather("wood")`.
#   - A name made inside a function is gone when the function ends. It cannot
#     reach out and change `wood` for you. Pass values IN as parameters,
#     hand them OUT with return.
#   - Defaults go LAST in the parameter list. `def gather(name, min_amt=1)`
#     is fine; `def gather(min_amt=1, name)` is a syntax error, because
#     Python would not know what a single argument meant.
#   - Define every function ABOVE the code that calls it. Python reads the
#     file top to bottom, so a call on line 10 to a def on line 200 is a
#     NameError.
#   - Every function gets a docstring: one line, in triple quotes, saying
#     what it does and what it hands back. It is the Python standard, and
#     VS Code shows it when you hover over a call. Not scored this week --
#     write them anyway.
#   - `solutions/week06_game.py` is your before-picture. If the game plays
#     differently than it did last week, diff against it.
# =============================================================================


# -----------------------------------------------------------------------------
# STEP 1: your first function -- the gathering block
# -----------------------------------------------------------------------------
# Find the block in your day that gathers a resource. It looks something like
# this, and some version of it appears three times -- wood, stone, iron:
#
#     amount = random.randint(1, 5)
#     print("You gathered " + str(amount) + " wood")
#     wood = wood + amount
#
# TODO 1: put the gathering block inside a function, ABOVE your main game
#         loop. Give it a parameter for which resource it is:
#
#         def gather(resource_name):
#             """Gather a random amount of one resource and announce it."""
#             amount = random.randint(1, 5)
#             print("You gathered " + str(amount) + " " + resource_name)
#
#         The line in triple quotes is a DOCSTRING -- the Python standard way
#         to describe a function. It goes on the FIRST line inside the def,
#         indented with the body, and says what the function does in one
#         sentence. A # comment explains a line; a docstring explains the
#         whole function to whoever calls it, and VS Code shows it when you
#         hover over gather( anywhere in your file. Every function you write
#         from here on gets one.
#
#         Leave the `wood = wood + amount` line OUT of the function for now.
#         STEP 2 is about getting that number back out.


# -----------------------------------------------------------------------------
# STEP 2: hand the value back
# -----------------------------------------------------------------------------
# Right now gather() knows the amount and nobody else does. `amount` was made
# inside the function, so it is gone the moment the function ends -- that is
# what scope means, and it is why the function has to hand it over.
#
# TODO 2a: add a return as the LAST line of gather():
#
#              return amount
#
#          Then update the docstring to say so -- it now hands something back:
#
#              """Gather a random amount of one resource and return it."""
#
# TODO 2b: in your day, replace each gathering block with a call that KEEPS
#          what comes back:
#
#              wood = wood + gather("wood")
#              stone = stone + gather("stone")
#
#          Not just `gather("wood")` on its own line. That runs the function,
#          prints the message, and throws the number away -- your wood never
#          moves. Run the game and watch the wood count to be sure.


# -----------------------------------------------------------------------------
# STEP 3: a default parameter
# -----------------------------------------------------------------------------
# Iron should be harder to find than wood. Rather than a second function,
# give gather() the range as parameters WITH defaults, so the calls that do
# not care stay short.
#
# TODO 3a: add two defaulted parameters:
#
#              def gather(resource_name, min_amt=1, max_amt=5):
#                  """Gather min_amt to max_amt of a resource; return it."""
#                  amount = random.randint(min_amt, max_amt)
#
# TODO 3b: leave your wood and stone calls exactly as they are -- they use
#          the defaults. Make iron rarer by overriding them:
#
#              iron = iron + gather("iron", 1, 2)
#
#          Both calls work on the same function. That is the point of a
#          default: the caller supplies a value only when it differs.


# -----------------------------------------------------------------------------
# STEP 4: the craft check
# -----------------------------------------------------------------------------
# Your crafting menu has one block per recipe, and every one of them does the
# same three things: check you can afford it, take the materials off, say
# what happened. One function covers all of them.
#
# TODO 4: write a function that takes what the recipe costs and reports
#         whether it worked:
#
#         def try_craft(item_name, wood, stone, wood_cost, stone_cost):
#             """Return True if the materials cover the cost, else False."""
#             if wood >= wood_cost and stone >= stone_cost:
#                 print("Crafted a " + item_name + "!")
#                 return True
#             print("Not enough materials for a " + item_name)
#             return False
#
#         Call it from each branch of the menu. Note what it CANNOT do: it
#         cannot subtract the materials, because wood and stone inside the
#         function are copies. Do the subtraction at the call site, where the
#         real variables live:
#
#             if try_craft("pickaxe", wood, stone, 3, 2):
#                 wood = wood - 3
#                 stone = stone - 2
#                 has_pickaxe = True


# -----------------------------------------------------------------------------
# STEP 5: the status display
# -----------------------------------------------------------------------------
# The status block is a run of print() calls that uses nothing but the values
# you hand it, which makes it the easiest thing in the file to move.
#
# TODO 5: move the whole status block into a function that takes every value
#         it prints:
#
#         def show_day_status(day, health, wood, stone, food, water):
#             """Print the day's status panel. Returns nothing."""
#             print("-" * 50)
#             print("Day " + str(day) + "  Health: " + str(health))
#             ...
#
#         It returns nothing -- it only prints -- and that is correct. Not
#         every function has to hand something back.
#
#         Then call it where the block used to be:
#
#             show_day_status(day, health, wood, stone, food, water)


# -----------------------------------------------------------------------------
# STEP 6: the ending, as a question
# -----------------------------------------------------------------------------
# Your end-of-day check sets game_over = True in the middle of the loop. It
# reads better as a question the loop asks: "is it over?"
#
# TODO 6a: write a function that ANSWERS instead of assigning:
#
#          def check_game_over(health, day, max_days):
#              """Return True when the game should end, else False."""
#              if health <= 0:
#                  print("You did not survive.")
#                  return True
#              if day >= max_days:
#                  print("You survived all " + str(max_days) + " days!")
#                  return True
#              return False
#
# TODO 6b: at the bottom of your day, keep its answer:
#
#              game_over = check_game_over(health, day, max_days)
#
#          `day = day + 1` stays in the LOOP, not in the function. A day
#          counter incremented inside a function goes back up by nothing at
#          all out here, and the game replays day 1 forever.


# -----------------------------------------------------------------------------
# STEP 7: play it, and compare
# -----------------------------------------------------------------------------
# TODO 7: run `python game.py` and play a full game. It should behave exactly
#         as it did last week -- same prompts, resources moving the same way,
#         the same two endings.
#
#         Then score it:
#
#             python tests/check_week.py 7
#
#         Type the 7. sync.py brings later weeks' files down too, and with no
#         number the scorecard grades the NEWEST week it can find, which is
#         not the one you just did.
#
#         If anything plays differently, you changed something while moving
#         it. `solutions/week06_game.py` is last week's worked answer -- open
#         it beside yours and find the line.


# ---- COMMIT -----------------------------------------------------------------
#   git add game.py
#   git commit -m "refactor: give each part of the day a name"
#   git push
