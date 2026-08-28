# =============================================================================
# Block Builder - Week 4: Debug & Plan the Game
# =============================================================================
# Module topic: the VS Code debugger, breakpoints, tracebacks, pseudocode
# NEW Python this week: none. No new syntax.
#
# THIS WEEK IS DIFFERENT: you do NOT touch game.py.
# You fix THIS file, right here, and commit it.
#
#   Run it:   python weeks/week04_debug.py
#   Test it:  pytest tests/test_week04.py -v
#
# WHAT YOU'LL DO
#   There are EIGHT bugs below. Each is marked with a "# BUG n" comment on the
#   line above it - but the comment does NOT tell you what's wrong. That's your
#   job. Some crash immediately. Some run fine and quietly produce nonsense,
#   which is the harder and more important kind to find.
#
#   Then fill in the PSEUDOCODE block at the bottom. That plan is what you'll
#   actually build in Weeks 5 and 6.
#
# WHAT'S TESTED (20 points)
#   5 pts  The program runs start to finish without crashing
#   5 pts  Gathering and eating change resources correctly
#   5 pts  The if-conditions are right
#   5 pts  At least 5 pseudocode steps are written
#
# TIPS
#   - Fix the crash FIRST. Python won't run any of the file until the syntax
#     error is gone. The traceback names the line.
#   - Read a traceback from the BOTTOM UP. The last line says what went wrong;
#     the line above says where.
#   - Set a breakpoint (click left of the line number) and press F5. Step with
#     F10 and watch the Variables panel. A number moving the wrong way is your
#     bug.
#   - A misspelled variable name doesn't crash. Python just makes a NEW
#     variable. That's why the damage disappears.
#   - Pseudocode is plain English, one step per line. No Python.
# =============================================================================

import random
from rich import print

print("=" * 50)
print("[bold green]        BLOCK BUILDER[/bold green]")
print("=" * 50)
print()

# --- Character setup ---

name = input("What is your name? ")
print()
print("Difficulty: 1-Peaceful  2-Normal  3-Hardcore")
choice = input("Choose (1/2/3): ")

if choice == "1":
    mode = "Peaceful"
    wood = 10
    food = 15
# BUG 1
elif choice == "2"
    mode = "Normal"
    wood = 5
    food = 10
else:
    mode = "Hardcore"
    wood = 2
    food = 5

stone = 3
iron = 0
health = 100
water = 10
day = 1

print("[bold]" + name + " spawns in " + mode + " mode![/bold]")

# --- Gather resources ---

print()
print("[bold]Gathering resources...[/bold]")

gathered_wood = random.randint(2, 6)

# BUG 2
wood = wood - gathered_wood
print("Gathered " + str(gathered_wood) + " wood. Total: " + str(wood))

gathered_stone = random.randint(1, 4)
stone = stone + gathered_stone
print("Gathered " + str(gathered_stone) + " stone. Total: " + str(stone))

# --- Eat food ---

print()
print("[bold]Eating...[/bold]")

# BUG 3
food_cost = 20
food = food - food_cost
print("Ate " + str(food_cost) + " food. Remaining: " + str(food))

# --- Craft a wooden pickaxe ---
# A wooden pickaxe needs 3 wood AND 2 stone.

print()
print("[bold]Crafting...[/bold]")

# BUG 4
if wood >= 3 or stone >= 2:
    wood = wood - 3
    stone = stone - 2
    print("[green]Crafted a wooden pickaxe![/green]")
else:
    print("[red]Not enough resources to craft.[/red]")

# --- Exploration event ---

print()
event = random.randint(1, 3)

if event == 1:
    print("[cyan]Found a cave![/cyan]")
    cave_choice = input("Enter? (1=yes, 2=no): ")
    if cave_choice == "1":
        luck = random.randint(1, 10)
        # BUG 5
        if luck > 50:
            iron = iron + 3
            print("[green]+3 iron ore![/green]")
        else:
            health = health - 10
            print("[red]Cave spider! -10 health[/red]")
    else:
        print("Stayed outside safely.")

elif event == 2:
    # BUG 6
    damage = random.randint(5, 15)
    health = health - damage

else:
    food = food + random.randint(2, 5)
    print("[green]Found berries![/green]")

# --- Night phase ---

print()
print("-" * 40)
print("[bold]Night falls...[/bold]")

if wood >= 10:
    print("[green]Shelter holds! Safe night.[/green]")
elif wood >= 5:
    health = health - 5
    print("[yellow]Cold night. -5 health[/yellow]")
else:
    # BUG 7
    heatlh = health - 15
    print("[red]No shelter! -15 health[/red]")

# --- End of day ---

print()
print("-" * 40)

# BUG 8
print("Health: " + health)
print("Wood: " + str(wood) + "  Stone: " + str(stone) + "  Iron: " + str(iron))
print("Food: " + str(food) + "  Water: " + str(water))

if health <= 0:
    print("[bold red]You didn't survive...[/bold red]")
else:
    print("[green]You survived day " + str(day) + "![/green]")


# =============================================================================
# PSEUDOCODE: Plan the survival game loop (you'll build this in Weeks 5 and 6)
# =============================================================================
# Pseudocode is plain English, one step per line. No Python syntax.
# Write AT LEAST 5 numbered steps describing what happens over and over
# each day until the game ends.
#
# Think about:
#   - What repeats every day? (gather, craft, eat, night)
#   - What ends the game? (health reaches 0, or you survive 30 days)
#   - What choices does the player make each turn?
#   - How does the day/night cycle work?
#
# TODO: Replace each "..." with one step of your plan.
#
# 1. ...
# 2. ...
# 3. ...
# 4. ...
# 5. ...
# =============================================================================
