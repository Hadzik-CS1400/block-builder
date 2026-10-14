# =============================================================================
# Block Builder - Week 2 Solution
# =============================================================================
# NEW this week: variables, input(), int/float/str, arithmetic
# From before: print(), comments
#
# This is one correct answer, not the only one. Your starting numbers, colours
# and wording can all differ and still score full marks.
# =============================================================================

from rich import print

# --- Title screen ---

print("=" * 50)
print("[bold green]        BLOCK BUILDER[/bold green]")
print("     A Survival Craft Adventure")
print("=" * 50)
print()

# --- Character creation (NEW: variables, input) ---

# TODO 1 - ask for the player's name
name = input("What is your name, crafter? ")

print()

print("Choose your difficulty:")
print("  1 - Peaceful  (extra resources, no monsters)")
print("  2 - Normal    (balanced start)")
print("  3 - Hardcore  (minimal resources, tough nights)")

# TODO 2 - ask for the difficulty
# input() gives back a STRING, so difficulty is "2", not 2.
difficulty = input("Enter 1, 2, or 3: ")

# --- Starting resources (NEW: variables) ---

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

# TODO 3 - add up every resource
total_resources = wood + stone + food + water + iron

# TODO 4 - integer division: 2 food per day, whole days only
days_of_food = food // 2

walls_needed = 4
wood_per_wall = 5

# TODO 5 - multiplication
total_wood_needed = walls_needed * wood_per_wall

# TODO 6 - subtraction
wood_shortage = total_wood_needed - wood

# --- Status display ---

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

# TODO 7 - str() turns the number into text so + can join it on
print("Total resources: " + str(total_resources))

# TODO 8
print("Food will last ~" + str(days_of_food) + " days (2 food/day)")

# TODO 9
print()
print("[yellow]To build basic shelter you need "
      + str(total_wood_needed) + " wood.[/yellow]")
print("[yellow]You still need " + str(wood_shortage) + " more wood.[/yellow]")

print()
print("[bold green]Day " + str(day)
      + " begins. The sun is high. Start gathering![/bold green]")
