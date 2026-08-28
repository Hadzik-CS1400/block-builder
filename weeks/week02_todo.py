# =============================================================================
# Block Builder - Week 2: Character Creation & Starting Resources
# =============================================================================
# Module topic: variables, data types, input(), arithmetic
#
# HOW TO USE THIS FILE
#   This is the ONLY week you do this: use File > Save As to save this file as
#   game.py in the top folder of your repo (next to README.md, NOT inside
#   weeks/). Then fill in the 9 TODOs below.
#
#   From Week 3 on you'll copy new sections INTO that game.py instead.
#
#   Run it:   python game.py
#   Test it:  pytest tests/test_week02.py -v
#
# WHAT YOU'LL BUILD
#   - A title screen for your world
#   - A prompt asking the crafter's name and difficulty
#   - Starting resources: wood, stone, iron, food, water, plus health and day
#   - Calculated values: total resources, how long your food lasts, and how
#     much wood a shelter still needs
#
# WHAT'S TESTED (20 points)
#   5 pts  Title screen shows the game name
#   5 pts  The player's name is stored and printed back
#   5 pts  All five resources appear in the status display
#   5 pts  Values are calculated with arithmetic, and a total is shown
#
# TIPS
#   - input() always gives you a STRING, even when the player types 2.
#   - You can't join a number onto a string. "Day " + 1 is an error.
#     Wrap it: "Day " + str(1)
#   - // is integer division: 10 // 3 is 3, not 3.33. That's what you want
#     for "how many whole days of food".
#   - Run your game after every TODO. Don't write all nine and then run once.
# =============================================================================

from rich import print

# --- Title screen ---
# Written for you. Change the colours or wording if you like!

print("=" * 50)
print("[bold green]        BLOCK BUILDER[/bold green]")
print("     A Survival Craft Adventure")
print("=" * 50)
print()

# --- Character creation (NEW: variables, input) ---

# TODO 1: Ask the player for their name and store it in a variable called `name`
#         Hint: name = input("What is your name, crafter? ")


print()

# Difficulty menu - written for you
print("Choose your difficulty:")
print("  1 - Peaceful  (extra resources, no monsters)")
print("  2 - Normal    (balanced start)")
print("  3 - Hardcore  (minimal resources, tough nights)")

# TODO 2: Ask for the difficulty and store it in a variable called `difficulty`


# --- Starting resources (NEW: variables) ---
# Every resource is a whole number, so these are all ints.
# Pick your own starting numbers if you want - just keep them sensible.

wood = 5
stone = 3
food = 10
water = 10
iron = 0
health = 100
day = 1

print()
print("Your name is: " + name)
print("You chose difficulty: " + difficulty)

# --- Arithmetic (NEW: +, -, *, //) ---

# TODO 3: Add up wood + stone + food + water + iron and store it
#         in a variable called `total_resources`


# TODO 4: Your crafter eats 2 food per day. Using integer division (//),
#         work out how many days the food will last.
#         Store it in a variable called `days_of_food`


# A basic shelter needs 4 walls at 5 wood each - written for you
walls_needed = 4
wood_per_wall = 5

# TODO 5: Multiply walls_needed by wood_per_wall to get `total_wood_needed`


# TODO 6: Subtract the wood you have from total_wood_needed to find out
#         how much more you need. Store it in `wood_shortage`


# --- Status display ---
# Remember: str() turns a number into text so you can join it onto a string.

print()
print("-" * 40)
print("[bold]Starting Status[/bold]")
print("-" * 40)
print("Name:    " + name)
print("Day:     " + str(day))
print("Health:  " + str(health))
print("-" * 40)
print("[bold cyan]Resources:[/bold cyan]")
print("  Wood:  " + str(wood) + " blocks")
print("  Stone: " + str(stone) + " blocks")
print("  Iron:  " + str(iron) + " ore")
print("  Food:  " + str(food) + " items")
print("  Water: " + str(water) + " units")
print("-" * 40)

# TODO 7: Print the total resources, using str() to join the number on.
#         It must include the word "Total" so the tests can find it.
#         Example: print("Total resources: " + str(total_resources))


# TODO 8: Print how many days the food will last, using days_of_food


print()

# TODO 9: Print how much wood a shelter needs and how much more you need,
#         using total_wood_needed and wood_shortage


print()
print("[bold green]Day " + str(day) + " begins. The sun is high. Start gathering![/bold green]")
