# =============================================================================
# Block Builder - Week 10: Lists & Dictionaries
# =============================================================================
# Module topic: lists (Module 8) and dictionaries (Module 9)
# NEW Python this week: [] lists, .append(), slicing, `in`, {} dictionaries,
#   .items(), .get(), dict comprehensions
# From before: print, variables, input, arithmetic, if/elif/else, for, while,
#   def/return/defaults, random, math, f-strings, string methods
# NOT yet: files, classes
#
# TWO MODULES IN ONE WEEK, and only this once. The game normally runs a module
# behind the lectures and this week it catches up, so lists and dictionaries
# arrive together. Next semester they get a week each.
#
# It is less work than it sounds, because the second half DELETES the first
# half's problems rather than adding to them. Watch for that -- the week is
# easier at the end than in the middle.
#
# WHAT YOU'LL BUILD
#   Nothing new happens in the game. Every rule stays exactly as it is. What
#   changes is how the game HOLDS what it knows, and almost every line you
#   write this week removes two.
#
#     - a journal that is a real list, not one long string with newlines in it
#     - one list of everything you have built
#     - ONE dictionary holding all six resources
#     - a recipe book that is data instead of code
#
# HOW TO WORK THIS WEEK
#   Open YOUR game.py and change it. Do not start a new file.
#
#   Do PART A and run the game. Then do PART B and run it again. Do not try to
#   do both before running anything -- you will not know which half broke it.
#
# WHAT'S TESTED (20 points)
#   4 pts  The journal is a list
#   4 pts  Resources and recipes are dictionaries
#   4 pts  A comprehension picks out what is low
#   4 pts  The resource rows are printed in one place
#   4 pts  The game still plays
#
#   Nothing checks your function NAMES or your wording.
#
# THE IDEA THAT RUNS THROUGH BOTH HALVES
#   A list and a dictionary are MUTABLE: a function can change the one that
#   everybody is sharing. A string and a number are not -- a function can only
#   hand you back a new one.
#
#   That single difference is why this week deletes so much code. Last week
#   every function that touched a resource had to be handed all six and hand
#   all six back. This week they are handed one dictionary and hand back
#   nothing at all.
#
# TIPS
#   - `journal.append(x)` changes the list and returns None. So it is
#         journal.append(entry)          <- right
#         journal = journal.append(x)    <- throws your journal away
#     The same trap as `.sort()`. If something becomes None for no reason,
#     this is why.
#   - `player["wood"]` is a KeyError if "wood" was never put in.
#     `player.get("wood", 0)` hands back 0 instead. Use .get() when you are
#     not sure, [ ] when you are.
#   - `.items()` gives you the key AND the value each time round:
#         for name, amount in player.items():
#   - A dict comprehension builds pairs, not single values:
#         low = {k: v for k, v in player.items() if v < 5}
#     Note the k: v. Leave the colon out and you have built a set.
#   - Dictionaries keep the order you put things in. Printing one will not
#     shuffle your status panel.
#
# CANNOT PICTURE WHAT "CHANGE THE SHAPE" MEANS?
#   Open docs/week10_data.html in a browser -- double-click it. It has ONE
#   STEP PER TODO BELOW, in this order, and arrow keys walk it. Each step puts
#   THIS game's real lines side by side -- your Week 9 code on the left, the
#   same place after that one TODO on the right -- and then names the shape it
#   was, the shape it becomes, and the one thing the old shape could not do.
#   That last part is the only reason any of these changes are worth making.
#
#   So when you are stuck on, say, TODO 6b, open it and press along to 6b.
#   Nothing in it runs; it is about the shape of your data, the way
#   week07_refactor.html was about the shape of your file.
# =============================================================================


# =============================================================================
# PART A - LISTS
# =============================================================================

# -----------------------------------------------------------------------------
# STEP 1: the journal becomes a list
# -----------------------------------------------------------------------------
# Last week you built the journal out of ONE string with "|" between entries,
# because a list is exactly the tool for "many things" and you did not have one
# yet. Now you do.
#
# TODO 1a: start it as an empty list instead of an empty string:
#
#              journal = []
#
# TODO 1b: rewrite add_journal to append, and DELETE its return:
#
#              def add_journal(journal, day, event):
#                  journal.append(f"Day {day}: {event}")
#
#          Read that twice, because it is the point of the whole week. There
#          is no `return`, and there does not need to be. A list is mutable,
#          so .append() changes the one list everybody is sharing.
#
# TODO 1c: so every call site loses its assignment:
#
#              journal = add_journal(journal, day, "Mob attack!")   <- before
#              add_journal(journal, day, "Mob attack!")             <- now
#
#          If you leave the `journal =` on the front, journal becomes None,
#          because append returns nothing. The game will run for a while and
#          then fail somewhere else entirely. This is the single most common
#          way to lose an hour this week.


# -----------------------------------------------------------------------------
# STEP 2: show it back, and show only the end of it
# -----------------------------------------------------------------------------
# TODO 2a: there is nothing left to split. Just walk the list:
#
#              def show_journal(journal):
#                  if not journal:
#                      return
#                  print()
#                  print("[bold]Trail Journal[/bold]")
#                  for entry in journal:
#                      print("  " + entry)
#
#          `if not journal:` is how you ask a list whether it is empty.
#
# TODO 2b: in your end-of-day display, show just the last three entries:
#
#              if journal:
#                  print("  [dim]Lately: " + "; ".join(journal[-3:]) + "[/dim]")
#
#          [-3:] is a SLICE: "from three before the end, to the end". It is
#          safe on a list of one -- it hands back the one, not an error. Try
#          it on day 1 and see.


# -----------------------------------------------------------------------------
# STEP 3: one list for everything you have built
# -----------------------------------------------------------------------------
# You have has_shelter, has_bench and has_pickaxe. Three variables, three
# places to update, and no way to ask "what have I built?" without naming all
# three.
#
# TODO 3a: replace all three with one list:
#
#              crafted = []
#
# TODO 3b: near the top of your file, name the three recipes once:
#
#              PICKAXE = "pickaxe"
#              SHELTER = "shelter"
#              BENCH = "bench"
#
#          Do this BEFORE you start using the names, because you are about
#          to type each one in several places and that is the problem.
#
#          A bare "shelter" typed wrong is not an error. Python is perfectly
#          happy with
#
#              if "sheltr" in crafted:
#
#          -- "sheltr" is simply never in the list, so the test is always
#          False, your shelter silently never works, and nothing points at
#          the line that caused it. You would go looking at night_phase.
#
#          Write SHELTER instead and a typo is a NameError the first time
#          you run it, naming the line. CAPITALS are the convention for a
#          value that never changes; you already have one in this game.
#
# TODO 3c: when a recipe succeeds, append its name:
#
#              crafted.append(SHELTER)
#
# TODO 3d: everywhere you tested a flag, ask the list instead:
#
#              if has_shelter:          <- before
#              if SHELTER in crafted:   <- now
#
#          `in` asks a list whether it holds something. Add a fourth recipe
#          next month and you add no new variable at all.


# =============================================================================
# PART B - DICTIONARIES
# =============================================================================

# -----------------------------------------------------------------------------
# STEP 4: six variables become one dictionary
# -----------------------------------------------------------------------------
# A list is the right tool for "many things in order". It is the WRONG tool
# for "a wood count, a stone count and a health" -- those are not in an order,
# they have NAMES. That is a dictionary.
#
# TODO 4: where your game sets up, replace the loose variables with one dict:
#
#              player = {
#                  "health": health,
#                  "wood": wood,
#                  "stone": stone,
#                  "iron": 0,
#                  "food": food,
#                  "water": water,
#              }
#
#         Then every read and write changes shape:
#
#              wood = wood + 3                              <- before
#              player["wood"] = player["wood"] + 3          <- now
#
#         Do it ONE function at a time and run the game after each. Doing all
#         of them and then running is how you end up with nine errors and no
#         idea which came first.


# -----------------------------------------------------------------------------
# STEP 5: the functions stop juggling
# -----------------------------------------------------------------------------
# This is the payoff, and it is worth stopping to look at. Here is explore()
# as you wrote it in Week 7B:
#
#     def explore(health, wood, stone, iron, food, water):
#         ...
#         return health, wood, stone, iron, food, water
#
#     health, wood, stone, iron, food, water = explore(
#         health, wood, stone, iron, food, water)
#
# Six in, six out, and a call that does not fit on a line. The comment in that
# function has said "it is meant to be annoying" since the day you wrote it.
#
# TODO 5: give the dictionary to each function instead, and delete the returns:
#
#              def explore(player):
#                  ...
#                  player["health"] = player["health"] - damage
#                  # no return at all
#
#              explore(player)
#
#         The function changes nothing it was not given, and yet the change
#         sticks. That is mutability again -- the same rule as .append() in
#         STEP 1, and the reason the journal stopped being passed around.
#
#         Do the same to eat_and_drink, night_phase, shelter_plan, draw_shelter
#         and your status functions. Count the parameters you delete.


# -----------------------------------------------------------------------------
# STEP 6: a recipe book that is data, not code
# -----------------------------------------------------------------------------
# Your crafting menu has a branch per recipe, and each branch repeats the same
# five steps with different numbers. The numbers are the only thing that
# differs, so the numbers should be the only thing written down.
#
# TODO 6a: near the top of your file, write the recipes as a dict of dicts:
#
#              RECIPES = {
#                  PICKAXE: {"wood": 3, "stone": 2},
#                  SHELTER: {"wood": 20, "stone": 10},
#                  BENCH:   {"wood": 10, "stone": 5, "iron": 2},
#              }
#
#          The keys are the constants from TODO 3b, so the recipe book and
#          the `in crafted` checks can never disagree about a name.
#
#          The value of each key is itself a dictionary. That is allowed, and
#          it is how most real data is shaped.
#
# TODO 6b: make try_craft look the costs up instead of taking them as
#          parameters, and check them with a loop:
#
#              def try_craft(player, crafted, item_name):
#                  costs = RECIPES[item_name]
#                  for resource, needed in costs.items():
#                      if player.get(resource, 0) < needed:
#                          print("[red]    Not enough resources for "
#                                + item_name + ".[/red]")
#                          print("[red]    Need " + str(needed) + " "
#                                + resource + ", have "
#                                + str(player.get(resource, 0)) + ".[/red]")
#                          return False
#                  for resource, needed in costs.items():
#                      player[resource] = player[resource] - needed
#                  crafted.append(item_name)
#                  print("[bold green]    Crafted " + item_name
#                        + "![/bold green]")
#                  return True
#
#          Two loops, not one: check EVERYTHING first, then spend. Spend as
#          you go and a recipe you cannot afford still takes your wood.
#
#          Keep both of your old messages -- the green "Crafted" line and the
#          red refusal. You are moving them, not deleting them: they used to
#          sit in each of the three branches, and now one copy serves all
#          three. The second red line is new, and it is the one that makes the
#          loop worth having: it can say WHICH resource ran short, because
#          `resource` is the name the loop is holding when it gives up.
#
#          .get(resource, 0) matters here. The pickaxe recipe never mentions
#          iron, and a player who has never held iron has no "iron" key --
#          player["iron"] would raise KeyError and end the game.
#
# TODO 6c: now the menu branches shrink to one line each:
#
#              if craft == "a":
#                  try_craft(player, crafted, PICKAXE)


# -----------------------------------------------------------------------------
# STEP 7: what is running low
# -----------------------------------------------------------------------------
# TODO 7: build a small dictionary of just the resources running out:
#
#             low = {name: amount for name, amount in player.items()
#                    if name != "health" and amount < 5}
#             if low:
#                 print("  [yellow]Running low: " + ", ".join(low) + "[/yellow]")
#
#         Same shape as the list comprehension from Module 8, except it builds
#         `name: amount` pairs, so what comes out is another dictionary.
#
#         ", ".join(low) joins the KEYS. Looping a dictionary gives you its
#         keys unless you ask for .items() or .values() -- worth knowing, and
#         worth being caught by once.


# =============================================================================
# PART C
# =============================================================================

# -----------------------------------------------------------------------------
# STEP 8: one place that prints the resources
# -----------------------------------------------------------------------------
# Open your two status displays side by side. Both print wood, stone, iron,
# food and water.
#
# You already paid for that. Week 9 asked you to put a width on every status
# row, and you did it TWICE, once in each function. Change your mind about the
# widths and you change them twice -- and the day you change one and forget the
# other, two panels that should match stop matching for no visible reason.
#
# That is the real argument for a function, and a better one than "it is
# tidier": two copies of a thing drift apart. One cannot.
#
# TODO 8a: write the rows ONCE, as a loop over the dictionary:
#
#              def show_inventory(player):
#                  for name, amount in player.items():
#                      if name == "health":
#                          continue
#                      print(f"  {name.title() + ':':<12} {amount:>5}")
#
#          Look at what .items() just bought you: add a resource to the dict
#          and a row appears here, with no change to this function at all. Six
#          separate variables could never do that.
#
# TODO 8b: delete the resource rows from BOTH status functions and call
#          show_inventory(player) where they used to be.
#
#          Move ONLY the resource rows. The header, the health line, the
#          end-of-day banner and the warnings stay where they are -- those are
#          genuinely different between the two displays. Duplication is only a
#          problem when it is the SAME thing twice.


# -----------------------------------------------------------------------------
# STEP 9: play it, then let something else play it
# -----------------------------------------------------------------------------
# TODO 9a: run `python game.py` and play a full game. Every rule should behave
#          exactly as it did last week. You changed how the game REMEMBERS
#          things, not what it does.
#
# TODO 9b: now hand it to something that has no habits:
#
#              python playtest.py mixed
#
#          That plays twenty games for you, answering from plays/mixed.txt,
#          and reports anything that crashed -- the error, the file, the line.
#
#          TWENTY and not one, because the game uses random numbers: the same
#          answers do not give the same game twice. A bug that only appears
#          when you are low on wood might turn up in one game out of five.
#          Playing once and seeing nothing proves very little.
#
#          MIXED and not your own playing, because you have habits. If you
#          always chop wood then you have only ever tested chopping wood, and
#          a bug in the crafting menu can sit there for a month looking like
#          nothing is wrong. Watch the answer change:
#
#              python playtest.py explore
#              python playtest.py craft
#              python playtest.py chop
#
#          plays/ is a folder of ordinary text files, one answer per line.
#          Open plays/explore.txt -- it is a single character. Write your own:
#          save plays/myplan.txt and run `python playtest.py myplan`.
#
# TODO 9c: then score it:
#
#              python tests/check_week.py 10
#
#          Type the 10. With no number the scorecard grades the newest week it
#          can find, which may not be the one you just did.


# ---- COMMIT -----------------------------------------------------------------
#   git add game.py
#   git commit -m "feat: a list journal and a player dictionary"
#   git push
