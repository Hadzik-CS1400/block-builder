# =============================================================================
# Block Builder — Week 7: Refactor into Functions
# =============================================================================
# NEW this week: def, parameters, return, default parameters, scope, import math
# From before: everything through while loops
# NOT yet: string methods (f-strings OK), lists, dicts, files, classes
#
# HOW TO USE THIS FILE: you are not writing new game features this week. You
# are REORGANIZING the game you already have. Take each block of your Week 6
# game.py, put `def name(...):` above it, indent it, and hand back what the
# rest of the program needs with `return`. The game plays exactly the same
# afterwards — that is how you know a refactor worked.
#
# WHY BOTHER: your Week 6 file is one 380-line wall. Finding the night-time
# damage rule means reading all of it. After this week it is nine lines inside
# night_phase(), and nothing else can touch it.
# =============================================================================

import random
import math  # NEW Week 7: importing a module you did not write
from rich import print


# =============================================================================
# NEW Week 7: SCOPE — the rule that trips everyone up
# =============================================================================
# A variable made INSIDE a function is local: it exists while the function
# runs and then it is gone. The `gained` inside gather() is not the `gained`
# anywhere else, and assigning to `wood` inside a function does NOT change the
# `wood` in the main program. That is why these functions `return` things —
# returning is how a function hands a value back out.
# =============================================================================


def title_screen():
    """Display the game title. No parameters, no return — it just prints."""
    print("=" * 50)
    print("[bold green]        BLOCK BUILDER[/bold green]")
    print("     A Survival Craft Adventure")
    print("=" * 50)
    print()


def get_player_info():
    """Ask for name and difficulty (Weeks 2, 3 and 6).

    NEW Week 7: a function can return MORE THAN ONE value. The main program
    unpacks them in the same order they are listed here.
    """
    name = input("What is your name, crafter? ")
    print()

    print("Choose your difficulty:")
    print("  1 - Peaceful  (extra resources, no monsters)")
    print("  2 - Normal    (balanced start)")
    print("  3 - Hardcore  (minimal resources, tough nights)")

    # Week 6: keep asking until the answer is valid
    difficulty = ""
    while difficulty != "1" and difficulty != "2" and difficulty != "3":
        difficulty = input("Enter 1, 2, or 3: ")
        if difficulty != "1" and difficulty != "2" and difficulty != "3":
            print("[red]That is not 1, 2, or 3. Try again.[/red]")

    # Week 3: if/elif/else sets up the world. Week 5 added actions_per_day.
    if difficulty == "1":
        return name, "Peaceful", 100, 6, 10, 5, 15, 15
    elif difficulty == "2":
        return name, "Normal", 100, 5, 5, 3, 10, 10
    else:
        return name, "Hardcore", 80, 4, 2, 1, 5, 5


def show_starting_status(name, day, health, wood, stone, iron, food, water):
    """The Week 2 starting status block, unchanged — just wrapped in a def."""
    total_resources = wood + stone + food + water + iron

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

    # NEW Week 7: math.ceil rounds UP. 9 food is 5 days of eating, not 4 —
    # integer division ( // ) was quietly rounding the last half-day away.
    if food > 0:
        print("Food will last ~" + str(math.ceil(food / 2)) + " days (2 food/day)")


def shelter_plan(wood, walls_needed=4, wood_per_wall=5):
    """Week 2 shelter maths.

    NEW Week 7: DEFAULT PARAMETERS. Call shelter_plan(wood) and you get the
    standard 4-wall hut. Call shelter_plan(wood, 6, 5) for a bigger one. The
    defaults mean the common case stays a one-argument call.
    """
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


def gather(resource_name, min_amt=1, max_amt=5):
    """Gather one resource and return how much was found.

    This one function replaces the four near-identical Week 5 branches for
    wood, stone, food and water. Same code, called with different arguments —
    that is the whole point of a parameter.
    """
    gained = random.randint(min_amt, max_amt)
    print("[green]  +" + str(gained) + " " + resource_name + "[/green]")
    return gained


def explore(health, wood, stone, iron, food, water):
    """The Week 3 exploration event, all six outcomes, moved into a function.

    Note how long this parameter list is: an event can change ANY resource, so
    every resource has to be passed in and handed back. That is annoying, and
    it is meant to be — Week 11 replaces all six with a single dictionary.
    """
    event = random.randint(1, 6)

    if event == 1:
        # Found a cave
        print("[cyan]  You discover a dark cave entrance![/cyan]")
        print("    1 - Enter the cave (risky but might find iron)")
        print("    2 - Stay outside (safe, gather wood)")
        cave_choice = input("  Choose 1 or 2: ")

        if cave_choice == "1":
            if random.randint(1, 10) > 5:
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
        food = food + random.randint(3, 8)
        print("[green]  Gathered berries![/green]")

    elif event == 5:
        # River crossing
        print("[blue]  You reach a wide river.[/blue]")
        print("    1 - Wade across (might lose resources)")
        print("    2 - Follow the bank (find a bridge)")
        river_choice = input("  Choose 1 or 2: ")
        if river_choice == "1":
            if random.randint(1, 10) > 5:
                stone = stone + 2
                print("[green]  Crossed safely! Found smooth stones. +2 stone[/green]")
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

    return health, wood, stone, iron, food, water


def try_craft(item_name, wood, stone, iron, wood_cost, stone_cost, iron_cost=0):
    """Spend resources on one item if they are all available.

    NEW Week 7: iron_cost defaults to 0, because most recipes do not use iron.
    Week 4 taught that a recipe needs EVERY ingredient — hence `and`, not `or`.
    Returns the resources plus a True/False saying whether it worked.
    """
    if wood >= wood_cost and stone >= stone_cost and iron >= iron_cost:
        wood = wood - wood_cost
        stone = stone - stone_cost
        iron = iron - iron_cost
        print("[bold green]    Crafted " + item_name + "![/bold green]")
        return wood, stone, iron, True

    print("[red]    Not enough resources for " + item_name + ".[/red]")
    print("[red]    Need " + str(wood_cost) + " wood, " + str(stone_cost)
          + " stone, " + str(iron_cost) + " iron.[/red]")
    return wood, stone, iron, False


def craft_menu(wood, stone, iron, has_pickaxe, has_shelter, has_bench):
    """The Week 6 crafting menu. The three recipes now share try_craft()."""
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
        wood, stone, iron, ok = try_craft("a wooden pickaxe", wood, stone, iron, 3, 2)
        if ok:
            has_pickaxe = True
    elif craft == "b":
        wood, stone, iron, ok = try_craft("a shelter", wood, stone, iron, 20, 10)
        if ok:
            has_shelter = True
    elif craft == "c":
        wood, stone, iron, ok = try_craft("a crafting bench", wood, stone, iron, 10, 5, 2)
        if ok:
            has_bench = True

    return wood, stone, iron, has_pickaxe, has_shelter, has_bench


def eat_and_drink(food, water, health, food_cost=2, water_cost=2):
    """Week 4 eating, with the daily costs as default parameters."""
    print()
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
    return food, water, health


def night_phase(day, health, has_shelter, wood):
    """Week 3 night check. Returns the health left after the night."""
    print()
    print("-" * 50)
    print("[bold]Night " + str(day) + " falls...[/bold]")

    if has_shelter:
        print("[green]Safe inside the shelter you built.[/green]")
    elif wood >= 5:
        damage = random.randint(5, 10)
        health = health - damage
        print("[yellow]Makeshift shelter. Cold night. Health -" + str(damage) + "[/yellow]")
    else:
        damage = random.randint(10, 25)
        health = health - damage
        print("[red]No shelter! Exposed to cold and creatures. Health -"
              + str(damage) + "[/red]")

    return health


def draw_shelter(wood, max_level=4):
    """Week 5 nested-loop shelter art, with the cap as a default parameter."""
    shelter_level = wood // 5
    if shelter_level > max_level:
        shelter_level = max_level

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


def draw_progress(day, max_days, width=20):
    """Week 6 progress bar. width defaults to 20 but is now adjustable."""
    progress = day * width // max_days
    bar = ""
    for i in range(width):
        if i < progress:
            bar = bar + "#"
        else:
            bar = bar + "-"
    print("Survival: [" + bar + "] Day " + str(day) + "/" + str(max_days))


def show_day_status(day, health, wood, stone, iron, food, water):
    """Week 3 end-of-day report."""
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


def check_game_over(name, health, day, max_days, has_shelter, has_bench):
    """Week 6 win/lose check. Returns True when the while loop should stop."""
    if health <= 0:
        print()
        print("[bold red]" + name + " didn't survive...[/bold red]")
        print("Made it to day " + str(day) + " of " + str(max_days) + ".")
        return True

    if day >= max_days:
        print()
        print("[bold green]" + name + " survived " + str(max_days) + " days![/bold green]")
        if has_shelter and has_bench:
            print("[bold green]With a shelter AND a crafting bench — master crafter![/bold green]")
        elif has_shelter:
            print("[green]Built a shelter. Well done![/green]")
        else:
            print("[yellow]Survived, but never built shelter. Barely made it![/yellow]")
        return True

    return False


# =============================================================================
# MAIN PROGRAM — the same game as Week 6, now readable in one screen
# =============================================================================
# Compare this with your Week 6 file. Every rule is still in the program, but
# the main loop no longer contains any of them: it says WHAT happens, and each
# function says HOW.

title_screen()

name, mode, health, actions_per_day, wood, stone, food, water = get_player_info()

iron = 0
day = 1
max_days = 30
game_over = False
has_shelter = False
has_bench = False
has_pickaxe = False

print()
print("You chose " + mode + " mode.")
show_starting_status(name, day, health, wood, stone, iron, food, water)
shelter_plan(wood)

print()
print("[bold green]" + name + " enters the world. Survive " + str(max_days)
      + " days to win.[/bold green]")

while not game_over:

    print()
    print("=" * 50)
    print("[bold]Day " + str(day) + " of " + str(max_days) + "[/bold]")
    print("Health: " + str(health) + "  Food: " + str(food) + "  Water: " + str(water))
    print("Wood: " + str(wood) + "  Stone: " + str(stone) + "  Iron: " + str(iron))
    print("=" * 50)

    for action in range(1, actions_per_day + 1):

        # Week 5: break out early, no point acting while dead
        if health <= 0:
            print("[bold red]Too weak to continue...[/bold red]")
            break

        # Week 5: skip this action entirely
        if food <= 0 and water <= 0:
            health = health - 5
            print("[red]Action " + str(action) + ": Starving! -5 health. Cannot act.[/red]")
            continue

        print()
        print("[bold]Action " + str(action) + " of " + str(actions_per_day) + "[/bold]")
        print("  1 - Chop wood      4 - Collect water")
        print("  2 - Mine stone     5 - Explore (risky)")
        print("  3 - Gather food    6 - Craft")

        # Week 6: validate the choice
        choice = ""
        while choice != "1" and choice != "2" and choice != "3" and \
                choice != "4" and choice != "5" and choice != "6":
            choice = input("  What do you do? (1-6) ")
            if choice != "1" and choice != "2" and choice != "3" and \
                    choice != "4" and choice != "5" and choice != "6":
                print("[red]  Enter a number from 1 to 6.[/red]")

        # One gather() call replaces four blocks of Week 5 code
        if choice == "1":
            wood = wood + gather("wood", 2, 5)
        elif choice == "2":
            stone = stone + gather("stone", 1, 4)
            if random.randint(1, 10) > 7:
                iron = iron + random.randint(1, 2)
                print("[cyan]  You struck an iron vein![/cyan]")
        elif choice == "3":
            food = food + gather("food", 2, 6)
        elif choice == "4":
            water = water + gather("water", 3, 7)
        elif choice == "5":
            health, wood, stone, iron, food, water = explore(
                health, wood, stone, iron, food, water)
        elif choice == "6":
            wood, stone, iron, has_pickaxe, has_shelter, has_bench = craft_menu(
                wood, stone, iron, has_pickaxe, has_shelter, has_bench)

    food, water, health = eat_and_drink(food, water, health)
    health = night_phase(day, health, has_shelter, wood)
    draw_shelter(wood)
    draw_progress(day, max_days)
    show_day_status(day, health, wood, stone, iron, food, water)

    game_over = check_game_over(name, health, day, max_days, has_shelter, has_bench)
    day = day + 1
