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
    print()

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

def cross_player_cancellation(players):
    """Apply cross-player cancellation rules between all players."""
    rune_counts = {player: Counter([rune for rune, _ in roll]) for player, roll in players.items()}
    
    # Check for orcs across all players
    orc_players = [player for player, runes in rune_counts.items() if 'orc' in runes]
    if len(orc_players) > 0:
        if len(orc_players) == len(players):
            print("All players rolled an orc! All runes are canceled for all players.")
            return {player: Counter() for player in players}
        else:
            for player in orc_players:
                print(f"{player}'s orc cancels all their runes!")
                rune_counts[player] = Counter({'orc': 1})

    # Apply cross-player cancellations iteratively
    while True:
        made_cancellation = False
        
        for p1 in players:
            for p2 in players:
                if p1 != p2:
                    if rune_counts[p1]['ghost'] > 0 and rune_counts[p2]['princess'] > 0:
                        print(f"{p1}'s ghost cancels out {p2}'s princess!")
                        rune_counts[p1]['ghost'] -= 1
                        rune_counts[p2]['princess'] -= 1
                        made_cancellation = True
                        
                    if rune_counts[p1]['knight'] > 0 and rune_counts[p2]['dragon'] > 0:
                        print(f"{p1}'s knight cancels out {p2}'s dragon!")
                        rune_counts[p1]['knight'] -= 1
                        rune_counts[p2]['dragon'] -= 1
                        made_cancellation = True
        
        if not made_cancellation:
            break
    
    # Remove canceled runes
    rune_counts = {player: +runes for player, runes in rune_counts.items()}
    
    return rune_counts

def calculate_score(rune_counts):
    """Calculate the total score based on remaining runes."""
    score = sum(rune_values[rune] * count for rune, count in rune_counts.items())
    return score

def determine_winner(scores):
    """Determine the winner based on the scores."""
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    
    if len(winners) == 1:
        return winners[0], max_score
    else:
        return None, max_score

def play_game():
    """Main game loop."""
    display_face_values()  # Display face values at the beginning of the game
    
    # Get number of players
    num_players = int(input("Enter the number of players: "))
    players = {}

    # Get player names
    for i in range(1, num_players + 1):
        name = input(f"Enter the name of Player {i}: ")
        players[name] = None

    # Play rounds until players decide to stop
    while True:
        # Each player rolls the knuckles
        for player in players:
            players[player] = roll_knuckles()

        # Display the rolls
        for player, roll in players.items():
            display_roll(player, roll)

        # Apply cross-player cancellation
        final_runes = cross_player_cancellation(players)

        # Calculate scores and determine the winner
        scores = {player: calculate_score(runes) for player, runes in final_runes.items()}
        
        # Display results after cancellation
        for player, score in scores.items():
            print(f"After cancellation, {player} has a score of {score}")
        
        winner, max_score = determine_winner(scores)
        
        if winner:
            print(f"{winner} wins the round with a score of {max_score}!\n")
        else:
            print("There is no clear winner this round, save your bets for the next!\n")

        # Ask if players want to play another round
        play_again = input("Do you want to play another round? (yes/no): ").lower()
        if play_again not in ['yes', 'y', 'YES', 'Y', 'yeah', 'yup', 'ye', 'yep']:
            break

    print("Thanks for playing OrcKnuckle!")

# Start the game
if __name__ == "__main__":
    play_game()
