import random
from collections import Counter

# Define the faces of the dice (knuckles)
knuckle_faces = ['beholder', 'ghost', 'princess', 'knight', 'dragon']
thumb_faces = ['beholder', 'ghost', 'princess', 'knight', 'dragon', 'orc']

# Define the value of each rune
rune_values = {
    'ghost': 0,
    'beholder': 1,
    'princess': 2,
    'knight': 2,
    'dragon': 3,
    'orc': 0  # Orc cancels everything, so it's worth 0
}

def display_face_values():
    """Display the worth of each face."""
    print("Welcome to OrcKnuckle!")
    print("Here’s what each face is worth:")
    for rune, value in rune_values.items():
        print(f"  - {rune.capitalize()}: {value} point{'s' if value != 1 else ''}")

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

def cross_player_cancellation(rolls):
    """Apply cross-player cancellation rules between two players."""
    # Extract the runes from each player's rolls
    player1_runes = Counter([rune for rune, _ in rolls['Player 1']])
    player2_runes = Counter([rune for rune, _ in rolls['Player 2']])
    
    # Handle cross-player orc cancellation
    if 'orc' in player1_runes and 'orc' in player2_runes:
        print("Both players rolled an orc! All runes are canceled for both players.")
        return {'Player 1': Counter(), 'Player 2': Counter()}

    # Handle individual orc cancellation
    if 'orc' in player1_runes:
        print("Player 1's orc cancels all their runes!")
        player1_runes = Counter({'orc': 1})
    if 'orc' in player2_runes:
        print("Player 2's orc cancels all their runes!")
        player2_runes = Counter({'orc': 1})

    # Apply cross-player cancellations iteratively
    while True:
        made_cancellation = False
        
        if player1_runes['ghost'] > 0 and player2_runes['princess'] > 0:
            print("Player 1's ghost cancels out Player 2's princess!")
            player1_runes['ghost'] -= 1
            player2_runes['princess'] -= 1
            made_cancellation = True
            
        if player2_runes['ghost'] > 0 and player1_runes['princess'] > 0:
            print("Player 2's ghost cancels out Player 1's princess!")
            player2_runes['ghost'] -= 1
            player1_runes['princess'] -= 1
            made_cancellation = True
            
        if player1_runes['knight'] > 0 and player2_runes['dragon'] > 0:
            print("Player 1's knight cancels out Player 2's dragon!")
            player1_runes['knight'] -= 1
            player2_runes['dragon'] -= 1
            made_cancellation = True
            
        if player2_runes['knight'] > 0 and player1_runes['dragon'] > 0:
            print("Player 2's knight cancels out Player 1's dragon!")
            player2_runes['knight'] -= 1
            player1_runes['dragon'] -= 1
            made_cancellation = True
        
        if not made_cancellation:
            break
    
    # Remove canceled runes
    player1_runes = +player1_runes
    player2_runes = +player2_runes
    
    return {'Player 1': player1_runes, 'Player 2': player2_runes}

def calculate_score(rune_counts):
    """Calculate the total score based on remaining runes."""
    score = sum(rune_values[rune] * count for rune, count in rune_counts.items())
    return score

# Main game execution
if __name__ == "__main__":
    display_face_values()  # Display face values at the beginning of the game
    
    players = {
        "Player 1": roll_knuckles(),
        "Player 2": roll_knuckles()
    }

    for player, roll in players.items():
        display_roll(player, roll)

    # Apply cross-player cancellation
    final_runes = cross_player_cancellation(players)

    # Display results after cancellation and calculate scores
    for player, runes in final_runes.items():
        score = calculate_score(runes)
        print(f"After cancellation, {player} has: {runes}, with a score of {score}\n")
