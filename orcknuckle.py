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
    'orc': 0  # Orc cancels everything, so it's worth 0 in the regular game
}

def display_orc_warrior():
    """Display an ASCII art of an orc warrior holding a raised club."""
    orc_warrior = r"""
        __,='`````'=/__
       '//  (o) \(o) \ `'         _,-,
       //|     ,_)   (`\      ,-'`_,-\
     ,-~~~\  `'==='  /-,      \==```` \__
    /        `----'     `\     \       \/
 /`,-'                 ,   `\_,,')       \ \
/` /`              ,  , \   / \   \   \   \ \
/  /    ,        ,    \ \ /  `\   \  \    \ \

"""
    print(orc_warrior)

def display_face_values(wild_orc_variant):
    """Display the worth of each face."""
    print("************************************")
    print("Welcome to OrcKnuckle!")
    print("************************************")
    display_orc_warrior() 
    print("Here’s what each face is worth:")
    print("  - Ghost: 0 points")
    print("  - Beholder: 1 point")
    print("  - Princess: 2 points")
    print("  - Knight: 2 points")
    print("  - Dragon: 3 points")
    if wild_orc_variant:
        print("  - Orc: Wild (can be any face!)")
    else:
        print("  - Orc: 0 points (cancels all runes)")
    print()

def choose_orc_value(player_name):
    """Prompt the player to choose what their Orc will represent."""
    print(f"{player_name}, you rolled an Orc! Choose what it will represent:")
    print("1. Ghost")
    print("2. Beholder")
    print("3. Princess")
    print("4. Knight")
    print("5. Dragon")
    choice = int(input("Enter the number corresponding to your choice: "))
    choices = ['ghost', 'beholder', 'princess', 'knight', 'dragon']
    return choices[choice - 1]

def roll_knuckles():
    """Simulate rolling the four knuckles."""
    rolls = [(random.choice(knuckle_faces), 'knuckle') for _ in range(3)]  # Roll the first three knuckles
    rolls.append((random.choice(thumb_faces), 'thumb knuckle'))  # Roll the thumb (fourth knuckle)
    return rolls

def apply_wild_orc(players):
    """Allow human players to choose what their Orc represents, and assign a random face for computer players."""
    for player in players:
        roll = player['roll']
        for i, (rune, knuckle_type) in enumerate(roll):
            if rune == 'orc':
                if player['type'] == 'human':
                    new_rune = choose_orc_value(player['name'])
                else:
                    # Randomly assign a face for computer players
                    new_rune = random.choice(['ghost', 'beholder', 'princess', 'knight', 'dragon'])
                    print(f"{player['name']}'s Orc is randomly declared as a {new_rune.capitalize()}!")
                roll[i] = (new_rune, knuckle_type)
                print(f"{player['name']} has declared their Orc as a {new_rune.capitalize()}!")


def display_roll(player, roll):
    """Display the roll with details."""
    print(f"{player} rolled:")
    for rune, knuckle_type in roll:
        print(f"  - {knuckle_type.capitalize()} shows a {rune.capitalize()}")

def choose_cancellation_target(human_player, candidates):
    """Prompt the human player to choose which opponent's face to cancel."""
    print(f"{human_player}, you have multiple targets to cancel. Choose a target:")
    for i, candidate in enumerate(candidates):
        print(f"{i + 1}. {candidate}")
    choice = int(input(f"Enter the number of the target you want to cancel: ")) - 1
    return candidates[choice]

def cross_player_cancellation(players):
    """Apply cross-player cancellation rules between all players."""
    rune_counts = {player['name']: Counter([rune for rune, _ in player['roll']]) for player in players}

    # Check for orcs across all players
    orc_players = [player['name'] for player in players if 'orc' in rune_counts[player['name']]]
    if len(orc_players) > 0:
        if len(orc_players) == len(players):
            print("All players rolled an orc! All runes are canceled for all players.")
            return {player['name']: Counter() for player in players}
        else:
            for player_name in orc_players:
                print(f"{player_name}'s orc cancels all their runes!")
                rune_counts[player_name] = Counter({'orc': 1})

    # Apply cross-player cancellations iteratively
    while True:
        made_cancellation = False

        for player in players:
            player_name = player['name']
            for opponent in players:
                opponent_name = opponent['name']
                if player_name != opponent_name:
                    # Handle Ghost vs. Princess
                    if rune_counts[player_name]['ghost'] > 0 and rune_counts[opponent_name]['princess'] > 0:
                        if player['type'] == 'human':
                            candidates = [op['name'] for op in players if op['name'] != player_name and rune_counts[op['name']]['princess'] > 0]
                            if len(candidates) > 1:
                                target = choose_cancellation_target(player_name, candidates)
                            else:
                                target = candidates[0]  # Only one target available
                        else:
                            target = opponent_name  # Simple AI chooses the first match
                        print(f"{player_name}'s ghost cancels out {target}'s princess!")
                        rune_counts[player_name]['ghost'] -= 1
                        rune_counts[target]['princess'] -= 1
                        made_cancellation = True

                    # Handle Knight vs. Dragon
                    if rune_counts[player_name]['knight'] > 0 and rune_counts[opponent_name]['dragon'] > 0:
                        if player['type'] == 'human':
                            candidates = [op['name'] for op in players if op['name'] != player_name and rune_counts[op['name']]['dragon'] > 0]
                            if len(candidates) > 1:
                                target = choose_cancellation_target(player_name, candidates)
                            else:
                                target = candidates[0]  # Only one target available
                        else:
                            target = opponent_name  # Simple AI chooses the first match
                        print(f"{player_name}'s knight cancels out {target}'s dragon!")
                        rune_counts[player_name]['knight'] -= 1
                        rune_counts[target]['dragon'] -= 1
                        made_cancellation = True

                        # Prevent double cancellation by breaking out after one knight cancels one dragon
                        break

        if not made_cancellation:
            break

    # Remove canceled runes
    rune_counts = {player_name: +runes for player_name, runes in rune_counts.items()}

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
    variant = input("Do you want to play the Wild Orc variant? (yes/no): ").lower()
    wild_orc_variant = variant in ['yes', 'y']

    display_face_values(wild_orc_variant)  # Pass the variant flag to display face values correctly

    # Get number of players
    num_players = int(input("Enter the number of players: "))
    players = []

    # Get player names and types
    for i in range(1, num_players + 1):
        name = input(f"Enter the name of Player {i}: ")
        player_type = input(f"Is {name} a human or computer player? (human/computer): ").lower()
        players.append({'name': name, 'type': player_type})

    # Play rounds until players decide to stop
    while True:
        # Each player rolls the knuckles
        for player in players:
            player['roll'] = roll_knuckles()

        # Display the rolls
        for player in players:
            display_roll(player['name'], player['roll'])

        # Apply Wild Orc variant if selected
        if wild_orc_variant:
            apply_wild_orc(players)

        # Apply cross-player cancellation
        final_runes = cross_player_cancellation(players)

        # Calculate scores and determine the winner
        scores = {player['name']: calculate_score(runes) for player, runes in zip(players, final_runes.values())}

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
        if play_again not in ['yes', 'y']:
            break

    print("Thanks for playing OrcKnuckle!")

# Start the game
if __name__ == "__main__":
    play_game()
