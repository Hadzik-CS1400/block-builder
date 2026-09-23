# =============================================================================
# Block Builder — Week 4: Debug & Plan the Game
# =============================================================================
# This week: fix 8 bugs using the VS Code debugger, then plan the game loop
# NO new Python syntax — this is practice at debugging and planning
# From before: print, variables, input, arithmetic, if/elif/else, random
# NOT yet: loops, functions
#
# INSTRUCTIONS: this file has 8 bugs in it. Each one is marked with a
# "# BUG N:" comment describing the symptom, not the fix. Find and repair
# all 8. TWO of them raise an error; the other SIX run fine and quietly
# produce nonsense, which is the harder kind. Fix them in order — bug 1
# stops the file from running at all.
# =============================================================================

import random  # NEW Week 3: random events need this
from rich import print

# --- Title screen (from Week 1) ---
print("=" * 50)
print("[bold green]        BLOCK BUILDER[/bold green]")
print("     A Survival Craft Adventure")
print("=" * 50)
print()

# --- Character creation (Week 2: variables, input) ---

name = input("What is your name, crafter? ")
print()

# Difficulty determines starting resources
print("Choose your difficulty:")
print("  1 - Peaceful  (extra resources, no monsters)")
print("  2 - Normal    (balanced start)")
print("  3 - Hardcore  (minimal resources, tough nights)")
difficulty = input("Enter 1, 2, or 3: ")

# NEW Week 4: input validation. Without this, typing "banana" silently drops
# you into Hardcore via the else branch — a bug that never raises an error.
if difficulty != "1" and difficulty != "2" and difficulty != "3":
    print("[red]That is not 1, 2, or 3. Defaulting to Normal.[/red]")
    difficulty = "2"

# NEW Week 3: if/elif/else replaces the hardcoded numbers from Week 2.
# Week 2 handed you the same starting pile no matter what you typed. Now the
# difficulty you chose actually changes the game.
if difficulty == "1":
    mode = "Peaceful"
    wood = 10
    stone = 5
    food = 15
    water = 15
    health = 100
# BUG 1: the file will not run at all. The traceback names the line.
elif difficulty == "2"
    mode = "Normal"
    wood = 5
    stone = 3
    food = 10
    water = 10
    health = 100
else:
    mode = "Hardcore"
    wood = 2
    stone = 1
    food = 5
    water = 5
    health = 80

iron = 0
day = 1

print()
print("You chose difficulty: " + difficulty + " (" + mode + ")")
print("Your name is: " + name)

# Calculate total starting resources (Week 2: arithmetic)
total_resources = wood + stone + food + water + iron

# Display starting status
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
print("Total resources: " + str(total_resources))

# Calculate how many days of food you have (Week 2: division)
days_of_food = food // 2
print("Food will last ~" + str(days_of_food) + " days (2 food/day)")

# Calculate shelter building cost (Week 2: multiplication)
walls_needed = 4
wood_per_wall = 5
total_wood_needed = walls_needed * wood_per_wall
wood_shortage = total_wood_needed - wood
print()
print("[yellow]To build basic shelter you need " + str(total_wood_needed)
      + " wood.[/yellow]")

# NEW Week 3: Week 2 always claimed you were short on wood, even when you
# were not. A relational operator lets the program tell the truth instead.
if wood_shortage > 0:
    print("[yellow]You still need " + str(wood_shortage) + " more wood.[/yellow]")
else:
    print("[green]You already have enough wood to build![/green]")

print()
print("[bold green]Day " + str(day) + " begins. The sun is high. Start gathering![/bold green]")

# =============================================================================
# NEW Week 3: Exploration event (if/elif/else driven by random)
# =============================================================================

print()
print("-" * 50)
print("[bold]Day " + str(day) + " — Exploring the forest...[/bold]")
print("-" * 50)
print()

event = random.randint(1, 6)

if event == 1:
    # Found a cave
    print("[cyan]You discover a dark cave entrance![/cyan]")
    print("  1 - Enter the cave (risky but might find iron)")
    print("  2 - Stay outside (safe, gather wood)")
    choice = input("Choose 1 or 2: ")

    if choice == "1":
        luck = random.randint(1, 10)
        # BUG 5: the cave never pays out. It is a spider every single time.
        if luck > 50:
            iron_found = random.randint(2, 6)
            iron = iron + iron_found
            print("[green]You found " + str(iron_found) + " iron ore![/green]")
        else:
            damage = random.randint(5, 15)
            health = health - damage
            print("[red]A bat attacked you! Health -" + str(damage) + "[/red]")
    else:
        # BUG 2: gathering wood leaves you with less wood than you started with.
        wood = wood - 3
        print("[green]Gathered 3 wood safely outside.[/green]")

elif event == 2:
    # Animal encounter
    # BUG 6: something takes your health here and never says what it was.
    # NEW Week 3: compound boolean — BOTH sides must be true
    if health > 70 and wood >= 3:
        print("You have a stick to defend yourself.")
        print("  1 - Fight (use a wood stick)")
        print("  2 - Run")
        choice = input("Choose 1 or 2: ")
        if choice == "1":
            if random.randint(1, 10) > 4:
                food = food + random.randint(3, 8)
                wood = wood - 1
                print("[green]You defeated the wolf and got meat![/green]")
            else:
                # BUG 7: the wolf bites, the message prints, and your health does not move.
                heatlh = health - 20
                print("[red]The wolf bit you! Health -20[/red]")
        else:
            print("You ran away safely.")
    else:
        health = health - 10
        print("[red]Too weak to fight. The wolf scratched you! -10 health[/red]")

elif event == 3:
    # Bad weather
    print("[blue]Dark clouds roll in...[/blue]")
    severity = random.randint(1, 10)
    if severity > 7:
        health = health - 10
        water = water + 5
        print("[yellow]Heavy rain! Health -10, but collected 5 water.[/yellow]")
    elif severity > 3:
        water = water + 3
        print("[green]Light rain. Collected 3 water.[/green]")
    else:
        print("[green]The clouds pass. Nothing happens.[/green]")

elif event == 4:
    # Found berry bush
    print("[magenta]You find a bush full of berries![/magenta]")
    food_gain = random.randint(3, 8)
    food = food + food_gain
    print("[green]Gathered " + str(food_gain) + " food![/green]")

elif event == 5:
    # River crossing
    print("[blue]You reach a wide river.[/blue]")
    print("  1 - Wade across (might lose resources)")
    print("  2 - Follow the bank (find a bridge)")
    choice = input("Choose 1 or 2: ")
    if choice == "1":
        if random.randint(1, 10) > 5:
            print("[green]Crossed safely![/green]")
            stone = stone + 2
            print("[green]Found smooth stones on the other side. +2 stone[/green]")
        else:
            lost = random.randint(2, 5)
            food = food - lost
            print("[red]Slipped! Lost " + str(lost) + " food in the current.[/red]")
    else:
        wood = wood + 2
        print("[green]Found a fallen tree by the bank. +2 wood[/green]")

else:
    # Peaceful gathering
    wood = wood + random.randint(2, 5)
    stone = stone + random.randint(1, 3)
    print("[green]A quiet day. Gathered some wood and stone.[/green]")

# =============================================================================
# NEW Week 4: Craft a wooden pickaxe
# =============================================================================

print()
print("-" * 50)
print("[bold]Crafting[/bold]")

# A recipe needs EVERY ingredient, so the check uses "and", not "or"
pickaxe_wood = 3
pickaxe_stone = 2

# BUG 4: the pickaxe gets crafted with only one of the two materials.
if wood >= pickaxe_wood or stone >= pickaxe_stone:
    wood = wood - pickaxe_wood
    stone = stone - pickaxe_stone
    has_pickaxe = True
    print("[green]Crafted a wooden pickaxe! (-3 wood, -2 stone)[/green]")
else:
    has_pickaxe = False
    print("[yellow]Not enough materials for a pickaxe (need 3 wood, 2 stone).[/yellow]")

# =============================================================================
# NEW Week 4: Eat and drink
# =============================================================================

print()
# BUG 3: one meal wipes out the entire food supply.
food_cost = 20
water_cost = 2
food = food - food_cost
water = water - water_cost

if food < 0:
    food = 0
if water < 0:
    water = 0

print("You consume " + str(food_cost) + " food and " + str(water_cost) + " water.")

# =============================================================================
# NEW Week 3: Night check (compound booleans)
# =============================================================================

print()
print("-" * 50)
print("[bold]Night falls...[/bold]")

# A boolean variable holds the ANSWER to a comparison, not the comparison
has_enough_wood = wood >= 10
has_some_shelter = wood >= 5

if has_enough_wood:
    print("[green]You built a solid shelter! Safe through the night.[/green]")
elif has_some_shelter:
    damage = random.randint(5, 10)
    health = health - damage
    print("[yellow]Makeshift shelter. Cold night. Health -" + str(damage) + "[/yellow]")
else:
    damage = random.randint(10, 25)
    health = health - damage
    print("[red]No shelter! Exposed to cold and creatures. Health -" + str(damage) + "[/red]")

# =============================================================================
# NEW Week 3: End of day status
# =============================================================================

print()
print("-" * 50)
print("[bold]End of Day " + str(day) + "[/bold]")
# BUG 8: it crashes right at the end, after everything else worked.
print("Health: " + health)
print("Wood: " + str(wood) + "  Stone: " + str(stone) + "  Iron: " + str(iron))
print("Food: " + str(food) + "  Water: " + str(water))

# "and" needs both sides true; "or" needs only one
if health < 30 and food < 5:
    print("[bold red]CRITICAL: Low health AND low food![/bold red]")
elif health < 30 or food < 5:
    print("[yellow]Warning: Watch your health and food.[/yellow]")
else:
    print("[green]You survived day " + str(day) + "![/green]")

if health <= 0:
    print("[bold red]You didn't survive the night...[/bold red]")

# =============================================================================
# NEW Week 4: PSEUDOCODE — plan the survival loop you build in Weeks 5-6
# =============================================================================
# Pseudocode is the plan you write BEFORE the code. It is plain English with
# the shape of a program. Writing it first is what stops you from discovering
# in week 6 that the whole thing needed restructuring.
#
# Write AT LEAST 5 steps. Keep the numbering: the test counts lines that
# start with "# 1.", "# 2." and so on, so an unnumbered plan scores zero.
#
# 1. ...
# 2. ...
# 3. ...
# 4. ...
# 5. ...
#
# Questions your plan should answer:
#   - What repeats every day?
#   - What ends the game, the good way and the bad?
#   - Which choices does the player make more than once?
#   - Which values have to survive from one day to the next?
# =============================================================================
