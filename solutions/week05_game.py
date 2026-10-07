# =============================================================================
# Block Builder — Week 5: Day Cycle — Gather Resources
# =============================================================================
# NEW this week: for loops, range(), break, continue, nested loops
# From before: print, variables, input, arithmetic, if/elif/else, random
# NOT yet: while loops, functions
#
# HOW TO USE THIS FILE: start from your Week 4 game.py. The big change is that
# your exploration event stops happening once and starts happening several
# times a day — you INDENT it inside a for loop rather than rewriting it.
# Everything above the loop is untouched.
# =============================================================================

import random
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

# Week 4: input validation
if difficulty != "1" and difficulty != "2" and difficulty != "3":
    print("[red]That is not 1, 2, or 3. Defaulting to Normal.[/red]")
    difficulty = "2"

# Week 3: if/elif/else sets up the world.
# NEW Week 5: each branch also sets actions_per_day — the number of times the
# for loop below will run. Harder difficulty means fewer actions per day.
if difficulty == "1":
    mode = "Peaceful"
    wood = 10
    stone = 5
    food = 15
    water = 15
    health = 100
    actions_per_day = 6
elif difficulty == "2":
    mode = "Normal"
    wood = 5
    stone = 3
    food = 10
    water = 10
    health = 100
    actions_per_day = 5
else:
    mode = "Hardcore"
    wood = 2
    stone = 1
    food = 5
    water = 5
    health = 80
    actions_per_day = 4

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

# Week 3: a relational operator lets the program tell the truth
if wood_shortage > 0:
    print("[yellow]You still need " + str(wood_shortage) + " more wood.[/yellow]")
else:
    print("[green]You already have enough wood to build![/green]")

print()
print("[bold green]Day " + str(day) + " begins. You have " + str(actions_per_day)
      + " actions before night falls.[/bold green]")

# =============================================================================
# NEW Week 5: The day cycle — a for loop over this day's actions
# =============================================================================
# Week 3 gave you ONE exploration event. Week 4 planned a loop in pseudocode.
# This is that plan, built: range() counts the actions, and the body is the
# menu plus your Week 3 event code, moved inside.

print()
print("-" * 50)
print("[bold]Day " + str(day) + " — " + str(actions_per_day) + " actions available[/bold]")
print("-" * 50)

for action in range(1, actions_per_day + 1):

    # NEW Week 5: break — stop the loop early, no point acting while dead
    if health <= 0:
        print("[bold red]Too weak to continue...[/bold red]")
        break

    # NEW Week 5: continue — skip the rest of THIS action, go to the next one
    if food <= 0 and water <= 0:
        health = health - 5
        print("[red]Action " + str(action) + ": Starving! -5 health. Cannot act.[/red]")
        continue

    print()
    print("[bold]Action " + str(action) + " of " + str(actions_per_day) + "[/bold]")
    print("  1 - Chop wood")
    print("  2 - Mine stone")
    print("  3 - Gather food")
    print("  4 - Collect water")
    print("  5 - Explore (risky)")
    choice = input("  What do you do? ")

    if choice == "1":
        gained = random.randint(2, 5)
        wood = wood + gained
        print("[green]  +" + str(gained) + " wood (total: " + str(wood) + ")[/green]")

    elif choice == "2":
        gained = random.randint(1, 4)
        stone = stone + gained
        if random.randint(1, 10) > 7:
            iron_found = random.randint(1, 2)
            iron = iron + iron_found
            print("[cyan]  +" + str(gained) + " stone AND " + str(iron_found)
                  + " iron![/cyan]")
        else:
            print("[green]  +" + str(gained) + " stone (total: " + str(stone) + ")[/green]")

    elif choice == "3":
        gained = random.randint(2, 6)
        food = food + gained
        print("[green]  +" + str(gained) + " food (total: " + str(food) + ")[/green]")

    elif choice == "4":
        gained = random.randint(3, 7)
        water = water + gained
        print("[blue]  +" + str(gained) + " water (total: " + str(water) + ")[/blue]")

    elif choice == "5":
        # --- Your Week 3 exploration event, now living inside the loop ---
        event = random.randint(1, 6)

        if event == 1:
            # Found a cave
            print("[cyan]  You discover a dark cave entrance![/cyan]")
            print("    1 - Enter the cave (risky but might find iron)")
            print("    2 - Stay outside (safe, gather wood)")
            cave_choice = input("  Choose 1 or 2: ")

            if cave_choice == "1":
                luck = random.randint(1, 10)
                if luck > 5:
                    iron_found = random.randint(2, 6)
                    iron = iron + iron_found
                    print("[green]  You found " + str(iron_found) + " iron ore![/green]")
                else:
                    damage = random.randint(5, 15)
                    health = health - damage
                    print("[red]  A bat attacked you! Health -" + str(damage) + "[/red]")
            else:
                wood = wood + 3
                print("[green]  Gathered 3 wood safely outside.[/green]")

        elif event == 2:
            # Animal encounter
            print("[yellow]  A wolf appears from the bushes![/yellow]")
            if health > 70 and wood >= 3:
                print("  You have a stick to defend yourself.")
                print("    1 - Fight (use a wood stick)")
                print("    2 - Run")
                wolf_choice = input("  Choose 1 or 2: ")
                if wolf_choice == "1":
                    if random.randint(1, 10) > 4:
                        food = food + random.randint(3, 8)
                        wood = wood - 1
                        print("[green]  You defeated the wolf and got meat![/green]")
                    else:
                        health = health - 20
                        print("[red]  The wolf bit you! Health -20[/red]")
                else:
                    print("  You ran away safely.")
            else:
                health = health - 10
                print("[red]  Too weak to fight. The wolf scratched you! -10 health[/red]")

        elif event == 3:
            # Bad weather
            print("[blue]  Dark clouds roll in...[/blue]")
            severity = random.randint(1, 10)
            if severity > 7:
                health = health - 10
                water = water + 5
                print("[yellow]  Heavy rain! Health -10, but collected 5 water.[/yellow]")
            elif severity > 3:
                water = water + 3
                print("[green]  Light rain. Collected 3 water.[/green]")
            else:
                print("[green]  The clouds pass. Nothing happens.[/green]")

        elif event == 4:
            # Found berry bush
            print("[magenta]  You find a bush full of berries![/magenta]")
            food_gain = random.randint(3, 8)
            food = food + food_gain
            print("[green]  Gathered " + str(food_gain) + " food![/green]")

        elif event == 5:
            # River crossing
            print("[blue]  You reach a wide river.[/blue]")
            print("    1 - Wade across (might lose resources)")
            print("    2 - Follow the bank (find a bridge)")
            river_choice = input("  Choose 1 or 2: ")
            if river_choice == "1":
                if random.randint(1, 10) > 5:
                    print("[green]  Crossed safely![/green]")
                    stone = stone + 2
                    print("[green]  Found smooth stones on the far side. +2 stone[/green]")
                else:
                    lost = random.randint(2, 5)
                    food = food - lost
                    print("[red]  Slipped! Lost " + str(lost) + " food in the current.[/red]")
            else:
                wood = wood + 2
                print("[green]  Found a fallen tree by the bank. +2 wood[/green]")

        else:
            # Peaceful gathering
            wood = wood + random.randint(2, 5)
            stone = stone + random.randint(1, 3)
            print("[green]  A quiet day. Gathered some wood and stone.[/green]")

    else:
        print("[dim]  (wasted action)[/dim]")

# =============================================================================
# Week 4: Craft a wooden pickaxe
# =============================================================================

print()
print("-" * 50)
print("[bold]Crafting[/bold]")

# A recipe needs EVERY ingredient, so the check uses "and", not "or"
pickaxe_wood = 3
pickaxe_stone = 2

if wood >= pickaxe_wood and stone >= pickaxe_stone:
    wood = wood - pickaxe_wood
    stone = stone - pickaxe_stone
    has_pickaxe = True
    print("[green]Crafted a wooden pickaxe! (-3 wood, -2 stone)[/green]")
else:
    has_pickaxe = False
    print("[yellow]Not enough materials for a pickaxe (need 3 wood, 2 stone).[/yellow]")

# =============================================================================
# Week 4: Eat and drink
# =============================================================================

print()
food_cost = 2
water_cost = 2
food = food - food_cost
water = water - water_cost

if food < 0:
    food = 0
if water < 0:
    water = 0

print("You consume " + str(food_cost) + " food and " + str(water_cost) + " water.")

# =============================================================================
# Week 3: Night check (compound booleans)
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
# NEW Week 5: Draw the shelter with a nested for loop
# =============================================================================
# A loop inside a loop: the outer one picks the row, the inner one draws the
# blocks across that row. end="" stops print from starting a new line.

shelter_level = wood // 5
if shelter_level > 4:
    shelter_level = 4

print()
print("Shelter: ", end="")
for row in range(2):
    if row == 0:
        for col in range(shelter_level):
            print("/\\", end="")
        print()
        print("         ", end="")
    else:
        for col in range(shelter_level):
            print("[]", end="")
        print()

# =============================================================================
# Week 3: End of day status
# =============================================================================

print()
print("-" * 50)
print("[bold]End of Day " + str(day) + "[/bold]")
print("Health: " + str(health))
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
