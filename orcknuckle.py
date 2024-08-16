# OrcKnuckle Game
# Copyright (C) 2024 Joel Southall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# See <https://www.gnu.org/licenses/>.


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

