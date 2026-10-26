# =============================================================================
# Block Builder — Week 6: Main Game Loop & Menus
# =============================================================================
# NEW this week: while loops, input validation, menu-driven programs
# From before: print, variables, input, arithmetic, if/elif/else, for, random
# NOT yet: functions, string methods, lists, dicts, files, classes
#
# HOW TO USE THIS FILE: start from your Week 5 game.py. Week 5 played exactly
# one day. This week you INDENT that whole day inside a while loop so it
# repeats until the player dies or survives to day 30. Your for loop is still
# in there, now nested inside the while — a loop inside a loop.
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

# NEW Week 6: real input validation. Week 4 gave up and defaulted to Normal
# after one bad answer. A while loop can simply keep asking.
difficulty = ""
while difficulty != "1" and difficulty != "2" and difficulty != "3":
    difficulty = input("Enter 1, 2, or 3: ")
    if difficulty != "1" and difficulty != "2" and difficulty != "3":
        print("[red]That is not 1, 2, or 3. Try again.[/red]")

# Week 3: if/elif/else sets up the world. Week 5 added actions_per_day.
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

# NEW Week 6: state the while loop needs. game_over is the loop's off switch;
# max_days is the win condition; the two "has_" flags remember what you built.
max_days = 30
game_over = False
has_shelter = False
has_crafting_bench = False
has_pickaxe = False

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
print("[bold green]" + name + " enters the world. Survive " + str(max_days)
      + " days to win.[/bold green]")

# =============================================================================
# NEW Week 6: THE MAIN GAME LOOP
# =============================================================================
# Everything from here to the bottom is your Week 5 day, indented one level.
# The while loop repeats it. Nothing inside had to be rewritten.

while not game_over:

    print()
    print("=" * 50)
    print("[bold]Day " + str(day) + " of " + str(max_days) + "[/bold]")
    print("Health: " + str(health) + "  Food: " + str(food) + "  Water: " + str(water))
    print("Wood: " + str(wood) + "  Stone: " + str(stone) + "  Iron: " + str(iron))
    print("=" * 50)

    # ------------------------------------------------------------------
    # Week 5: the day cycle — a for loop, now NESTED inside the while
    # ------------------------------------------------------------------
    for action in range(1, actions_per_day + 1):

        # Week 5: break — stop the loop early, no point acting while dead
        if health <= 0:
            print("[bold red]Too weak to continue...[/bold red]")
            break

        # Week 5: continue — skip the rest of THIS action, go to the next one
        if food <= 0 and water <= 0:
            health = health - 5
            print("[red]Action " + str(action) + ": Starving! -5 health. Cannot act.[/red]")
            continue

        print()
        print("[bold]Action " + str(action) + " of " + str(actions_per_day) + "[/bold]")
        print("  1 - Chop wood      4 - Collect water")
        print("  2 - Mine stone     5 - Explore (risky)")
        print("  3 - Gather food    6 - Craft")

        # NEW Week 6: validate the action choice the same way
        choice = ""
        while choice != "1" and choice != "2" and choice != "3" and \
                choice != "4" and choice != "5" and choice != "6":
            choice = input("  What do you do? (1-6) ")
            if choice != "1" and choice != "2" and choice != "3" and \
                    choice != "4" and choice != "5" and choice != "6":
                print("[red]  Enter a number from 1 to 6.[/red]")

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
            # --- Your Week 3 exploration event, inside the loop since Week 5 ---
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

        elif choice == "6":
            # ----------------------------------------------------------
            # NEW Week 6: a crafting MENU. Week 4 crafted one pickaxe with
            # no choice. A menu is just a print block, a validated input,
            # and an if/elif chain -- all things you already know.
            # ----------------------------------------------------------
            print()
            print("  [bold]Crafting bench:[/bold]")
            print("    a - Wooden pickaxe  (3 wood, 2 stone)")
            print("    b - Shelter         (20 wood, 10 stone)")
            print("    c - Crafting bench  (10 wood, 5 stone, 2 iron)")
            print("    d - Cancel")

            craft = ""
            while craft != "a" and craft != "b" and craft != "c" and craft != "d":
                craft = input("    Craft what? ")
                if craft != "a" and craft != "b" and craft != "c" and craft != "d":
                    print("[red]    Enter a, b, c, or d.[/red]")

            if craft == "a":
                # Week 4: a recipe needs EVERY ingredient, so this is "and"
                if wood >= 3 and stone >= 2:
                    wood = wood - 3
                    stone = stone - 2
                    has_pickaxe = True
                    print("[green]    Crafted a wooden pickaxe![/green]")
                else:
                    print("[red]    Need 3 wood and 2 stone.[/red]")
            elif craft == "b":
                if wood >= 20 and stone >= 10:
                    wood = wood - 20
                    stone = stone - 10
                    has_shelter = True
                    print("[bold green]    Built a shelter![/bold green]")
                else:
                    print("[red]    Need 20 wood and 10 stone.[/red]")
            elif craft == "c":
                if wood >= 10 and stone >= 5 and iron >= 2:
                    wood = wood - 10
                    stone = stone - 5
                    iron = iron - 2
                    has_crafting_bench = True
                    print("[bold green]    Built a crafting bench![/bold green]")
                else:
                    print("[red]    Need 10 wood, 5 stone and 2 iron.[/red]")

    # ------------------------------------------------------------------
    # Week 4: Eat and drink
    # ------------------------------------------------------------------
    print()
    food_cost = 2
    water_cost = 2
    food = food - food_cost
    water = water - water_cost

    if food < 0:
        food = 0
        health = health - 5
        print("[red]Starving! -5 health[/red]")
    if water < 0:
        water = 0
        health = health - 5
        print("[red]Dehydrated! -5 health[/red]")

    print("You consume " + str(food_cost) + " food and " + str(water_cost) + " water.")

    # ------------------------------------------------------------------
    # Week 3: Night check — now aware of the shelter you actually built
    # ------------------------------------------------------------------
    print()
    print("-" * 50)
    print("[bold]Night " + str(day) + " falls...[/bold]")

    has_some_shelter = wood >= 5

    if has_shelter:
        print("[green]Safe inside the shelter you built.[/green]")
    elif has_some_shelter:
        damage = random.randint(5, 10)
        health = health - damage
        print("[yellow]Makeshift shelter. Cold night. Health -" + str(damage) + "[/yellow]")
    else:
        damage = random.randint(10, 25)
        health = health - damage
        print("[red]No shelter! Exposed to cold and creatures. Health -" + str(damage) + "[/red]")

    # ------------------------------------------------------------------
    # Week 5: Draw the shelter with a nested for loop
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # NEW Week 6: a progress bar, built by a for loop over 20 slots
    # ------------------------------------------------------------------
    progress = day * 20 // max_days
    bar = ""
    for i in range(20):
        if i < progress:
            bar = bar + "#"
        else:
            bar = bar + "-"
    print("Survival: [" + bar + "] Day " + str(day) + "/" + str(max_days))

    # ------------------------------------------------------------------
    # Week 3: End of day status
    # ------------------------------------------------------------------
    print()
    print("-" * 50)
    print("[bold]End of Day " + str(day) + "[/bold]")
    print("Health: " + str(health))
    print("Wood: " + str(wood) + "  Stone: " + str(stone) + "  Iron: " + str(iron))
    print("Food: " + str(food) + "  Water: " + str(water))

    if health < 30 and food < 5:
        print("[bold red]CRITICAL: Low health AND low food![/bold red]")
    elif health < 30 or food < 5:
        print("[yellow]Warning: Watch your health and food.[/yellow]")
    else:
        print("[green]You survived day " + str(day) + "![/green]")

    # ------------------------------------------------------------------
    # NEW Week 6: decide whether the loop keeps going
    # ------------------------------------------------------------------
    if health <= 0:
        game_over = True
        print()
        print("[bold red]" + name + " didn't survive...[/bold red]")
        print("Made it to day " + str(day) + " of " + str(max_days) + ".")

    elif day >= max_days:
        game_over = True
        print()
        print("[bold green]" + name + " survived " + str(max_days) + " days![/bold green]")
        if has_shelter and has_crafting_bench:
            print("[bold green]With a shelter AND a crafting bench — master crafter![/bold green]")
        elif has_shelter:
            print("[green]Built a shelter. Well done![/green]")
        else:
            print("[yellow]Survived, but never built shelter. Barely made it![/yellow]")

    # NEW Week 6: the counter that keeps the while loop from running forever.
    # Forget this line and the game replays day 1 until you kill the program.
    day = day + 1
