import random

# Define the faces of the dice (knuckles)
knuckle_faces = ['beholder', 'ghost', 'princess', 'knight', 'dragon']
thumb_faces = ['beholder', 'ghost', 'princess', 'knight', 'dragon', 'orc']

def roll_knuckles():
    """Simulate rolling the four knuckles."""
    rolls = [(random.choice(knuckle_faces), 'knuckle') for _ in range(3)]  # Roll the first three knuckles
    rolls.append((random.choice(thumb_faces), 'thumb knuckle'))  # Roll the thumb (fourth knuckle)
    return rolls

def display_roll(player, roll):
    """Display the roll with details."""
    print(f"{player} rolled:")
    for rune, knuckle_type in roll:
        print(f"  - {knuckle_type.capitalize()} shows a {rune.capitalize()}")

# Preliminary testing
players = {
    "Player 1": roll_knuckles(),
    "Player 2": roll_knuckles()
}

for player, roll in players.items():
    display_roll(player, roll)

