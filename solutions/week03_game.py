# =============================================================================
# Block Builder - Week 3 Solution
# =============================================================================
# NEW this week: if/elif/else, relational operators, and/or/not,
#                compound booleans, random
# From before: print(), variables, input(), arithmetic
# NOT yet: loops, functions
#
# This is one correct answer, not the only one.
# =============================================================================

import random
from rich import print

# --- Title screen (from Week 2) ---

print("=" * 50)
print("[bold green]        BLOCK BUILDER[/bold green]")
print("     A Survival Craft Adventure")
print("=" * 50)
print()

# --- Character creation (from Week 2) ---

name = input("What is your name, crafter? ")

print()
print("Choose your difficulty:")
print("  1 - Peaceful  (extra resources, no monsters)")
print("  2 - Normal    (balanced start)")
print("  3 - Hardcore  (minimal resources, tough nights)")
difficulty = input("Enter 1, 2, or 3: ")

# --- STEP 1: difficulty now sets the resources (NEW: if/elif/else) ---

if difficulty == "1":
    mode = "Peaceful"
    wood = 10
    stone = 5
    food = 15
    water = 15
    health = 100

elif difficulty == "2":
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
print("[bold]" + name + " spawns in " + mode + " mode![/bold]")

# --- Status display (from Week 2) ---

total_resources = wood + stone + food + water + iron
days_of_food = food // 2

print()
print("-" * 40)
print("[bold]Starting Status[/bold]")
print("-" * 40)
print("Health:  " + str(health))
print("  Wood:  " + str(wood) + " blocks")
print("  Stone: " + str(stone) + " blocks")
print("  Iron:  " + str(iron) + " ore")
print("  Food:  " + str(food) + " items")
print("  Water: " + str(water) + " units")
print("Total resources: " + str(total_resources))
print("Food will last ~" + str(days_of_food) + " days (2 food/day)")

# --- STEP 2: exploration event (NEW: random + if/elif/else) ---

print()
print("-" * 50)
print("[bold]Day " + str(day) + " - Exploring the forest...[/bold]")
print("-" * 50)
print()

event = random.randint(1, 4)

if event == 1:
    print("[cyan]You discover a dark cave entrance![/cyan]")
    print("  1 - Enter the cave (risky, but there might be iron)")
    print("  2 - Stay outside (safe, gather wood)")
    choice = input("Choose 1 or 2: ")

    if choice == "1":
        luck = random.randint(1, 10)
        if luck > 5:
            iron_found = random.randint(2, 6)
            iron = iron + iron_found
            print("[green]You found " + str(iron_found) + " iron ore![/green]")
        else:
            damage = random.randint(5, 15)
            health = health - damage
            print("[red]A bat attacked you! Health -" + str(damage) + "[/red]")
    else:
        wood = wood + 3
        print("[green]Gathered 3 wood safely outside.[/green]")

elif event == 2:
    print("[yellow]A wolf appears from the bushes![/yellow]")

    # A compound boolean: BOTH conditions have to be true to fight
    if health > 70 and wood >= 3:
        print("You have a stick to defend yourself.")
        print("  1 - Fight (uses a wood stick)")
        print("  2 - Run")
        choice = input("Choose 1 or 2: ")

        if choice == "1":
            if random.randint(1, 10) > 4:
                meat = random.randint(3, 8)
                food = food + meat
                wood = wood - 1
                print("[green]You drove the wolf off and got "
                      + str(meat) + " meat![/green]")
            else:
                health = health - 20
                print("[red]The wolf bit you! Health -20[/red]")
        else:
            print("You ran away safely.")
    else:
        health = health - 10
        print("[red]Too weak to fight. The wolf scratched you! -10 health[/red]")

elif event == 3:
    print("[blue]Dark clouds roll in...[/blue]")
    severity = random.randint(1, 10)

    if severity > 7:
        health = health - 10
        water = water + 5
        print("[yellow]Heavy storm! Health -10, but collected 5 water.[/yellow]")
    elif severity > 3:
        water = water + 3
        print("[green]Light rain. Collected 3 water.[/green]")
    else:
        print("[green]The clouds pass. Nothing happens.[/green]")

else:
    found_wood = random.randint(2, 5)
    found_stone = random.randint(1, 3)
    wood = wood + found_wood
    stone = stone + found_stone
    print("[green]A quiet day. Gathered " + str(found_wood) + " wood and "
          + str(found_stone) + " stone.[/green]")

# --- STEP 3: night phase (NEW: booleans stored in variables) ---

print()
print("-" * 50)
print("[bold]Night falls...[/bold]")

# A comparison IS a value - these hold True or False
has_enough_wood = wood >= 10
has_some_shelter = wood >= 5

if has_enough_wood:
    print("[green]You built a solid shelter! Safe through the night.[/green]")
elif has_some_shelter:
    damage = random.randint(5, 10)
    health = health - damage
    print("[yellow]Makeshift shelter. Cold night. Health -"
          + str(damage) + "[/yellow]")
else:
    damage = random.randint(10, 25)
    health = health - damage
    print("[red]No shelter! Exposed to the cold. Health -"
          + str(damage) + "[/red]")

# --- STEP 4: end of day (NEW: compound booleans) ---

print()
print("-" * 50)
print("[bold]End of Day " + str(day) + "[/bold]")
print("Health: " + str(health))
print("Wood: " + str(wood) + "  Stone: " + str(stone) + "  Iron: " + str(iron))
print("Food: " + str(food) + "  Water: " + str(water))

if health < 30 and food < 5:
    print("[bold red]CRITICAL: low health AND low food![/bold red]")
elif health < 30 or food < 5:
    print("[yellow]Warning: watch your health and food.[/yellow]")
else:
    print("[green]You survived day " + str(day) + "![/green]")

if health <= 0:
    print("[bold red]You didn't survive the night...[/bold red]")
