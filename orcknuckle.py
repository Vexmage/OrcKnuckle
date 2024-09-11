import random
from collections import Counter

# Dice class responsible for rolling
class Dice:
    def __init__(self):
        self.knuckle_faces = ['beholder', 'ghost', 'princess', 'knight', 'dragon']
        self.thumb_faces = self.knuckle_faces + ['orc']

    def roll(self):
        """Simulate rolling the four knuckles."""
        rolls = [(random.choice(self.knuckle_faces), 'knuckle') for _ in range(3)]
        rolls.append((random.choice(self.thumb_faces), 'thumb knuckle'))
        return rolls


# Player class
class Player:
    rune_values = {
        'ghost': 0,
        'beholder': 1,
        'princess': 2,
        'knight': 2,
        'dragon': 3,
        'orc': 0  # Orc cancels everything by default
    }

    def __init__(self, name):
        self.name = name
        self.rolls = []
        self.score = 0
        self.is_wild_orc = False

    def roll_knuckles(self, dice):
        """Each player rolls their dice."""
        self.rolls = dice.roll()
        self.calculate_score()

    def calculate_score(self):
        """Calculate the player's score based on the roll."""
        self.score = sum(Player.rune_values[rune] for rune, knuckle_type in self.rolls if knuckle_type == 'knuckle')

        thumb_rune = self.rolls[-1][0]
        if thumb_rune == 'orc':
            if self.is_wild_orc:
                self.handle_wild_orc()
            else:
                print(f"{self.name}'s thumb knuckle shows an Orc, which cancels all other runes!")
                self.score = 0
        else:
            print(f"{self.name}'s thumb knuckle shows a {thumb_rune.capitalize()}, adding {Player.rune_values[thumb_rune]} points.")
            self.score += Player.rune_values[thumb_rune]

    def handle_wild_orc(self):
        """Handles the Wild Orc variant logic for human players."""
        raise NotImplementedError("This method should be overridden in the HumanPlayer class.")

    def display_roll(self):
        """Display the player's roll with points for each face."""
        print(f"{self.name} rolled:")
        for rune, knuckle_type in self.rolls:
            print(f"  - {knuckle_type.capitalize()} shows a {rune.capitalize()} ({Player.rune_values[rune]} points)")
        print(f"{self.name} scored {self.score} points.\n")


# Human player subclass
class HumanPlayer(Player):
    def __init__(self, name, is_wild_orc):
        super().__init__(name)
        self.is_wild_orc = is_wild_orc

    def roll_knuckles(self, dice):
        """Human player must press a key to roll."""
        input(f"{self.name}, press any key to roll the knuckles...")
        super().roll_knuckles(dice)

    def handle_wild_orc(self):
        """Handle the Wild Orc variant for human players."""
        print(f"{self.name}, you rolled an Orc! Choose what it will represent:")
        print("1. Ghost")
        print("2. Beholder")
        print("3. Princess")
        print("4. Knight")
        print("5. Dragon")
        choice = int(input("Enter the number corresponding to your choice: "))
        choices = ['ghost', 'beholder', 'princess', 'knight', 'dragon']
        chosen_rune = choices[choice - 1]
        print(f"{self.name} has declared their Orc as a {chosen_rune.capitalize()}!")
        self.score += Player.rune_values[chosen_rune]

    def choose_cancellation_target(self, candidates, target_rune):
        """Prompt the human player to choose which opponent to cancel."""
        print(f"{self.name}, you have multiple opponents' {target_rune}s to cancel. Choose a target:")
        for i, candidate in enumerate(candidates):
            print(f"{i + 1}. {candidate}")
        choice = int(input(f"Enter the number of the target you want to cancel: ")) - 1
        return candidates[choice]


# Computer player subclass
class ComputerPlayer(Player):
    def __init__(self, name, is_wild_orc):
        super().__init__(name)
        self.is_wild_orc = is_wild_orc

    def roll_knuckles(self, dice):
        """Computer players roll without a prompt."""
        print(f"{self.name} is rolling the knuckles...")
        super().roll_knuckles(dice)

    def handle_wild_orc(self):
        """Handle the Wild Orc variant for computer players."""
        new_rune = random.choice(['ghost', 'beholder', 'princess', 'knight', 'dragon'])
        print(f"{self.name}'s Orc is randomly declared as a {new_rune.capitalize()}!")
        self.score += Player.rune_values[new_rune]


# Game class that runs the main game loop
class Game:
    def __init__(self):
        self.players = []
        self.dice = Dice()
        self.is_wild_orc_variant = False

    def add_player(self):
        """Add players to the game (human or computer)."""
        num_players = int(input("Enter the number of players: "))

        for i in range(1, num_players + 1):
            name = input(f"Enter the name of Player {i}: ")
            player_type = input(f"Is {name} a human or computer player? (human/computer): ").lower()
            if player_type == "human":
                self.players.append(HumanPlayer(name, self.is_wild_orc_variant))
            else:
                self.players.append(ComputerPlayer(name, self.is_wild_orc_variant))

    def play_round(self):
        """Play one round of the game where each player rolls."""
        for player in self.players:
            player.roll_knuckles(self.dice)
            player.display_roll()

        # Apply cancellations
        self.apply_cancellations()

    def apply_cancellations(self):
        """Apply cancellations across all players."""
        rune_counts = {player.name: Counter([rune for rune, _ in player.rolls]) for player in self.players}

        for player in self.players:
            player_name = player.name
            for opponent in self.players:
                if player_name != opponent.name:  # Ensure players can't cancel their own runes
                    # Handle Ghost vs. Princess cancellation
                    if rune_counts[player_name]['ghost'] > 0 and rune_counts[opponent.name]['princess'] > 0:
                        candidates = [op.name for op in self.players if rune_counts[op.name]['princess'] > 0 and op.name != player_name]
                        if isinstance(player, HumanPlayer):
                            target = player.choose_cancellation_target(candidates, 'princess')
                        else:
                            target = candidates[0]  # Auto select for computer
                        print(f"{player_name}'s ghost cancels {target}'s princess!")
                        rune_counts[player_name]['ghost'] -= 1
                        rune_counts[target]['princess'] -= 1

                    # Handle Knight vs. Dragon cancellation
                    if rune_counts[player_name]['knight'] > 0 and rune_counts[opponent.name]['dragon'] > 0:
                        candidates = [op.name for op in self.players if rune_counts[op.name]['dragon'] > 0 and op.name != player_name]
                        if isinstance(player, HumanPlayer):
                            target = player.choose_cancellation_target(candidates, 'dragon')
                        else:
                            target = candidates[0]  # Auto select for computer
                        print(f"{player_name}'s knight cancels {target}'s dragon!")
                        rune_counts[player_name]['knight'] -= 1
                        rune_counts[target]['dragon'] -= 1

        # Update player scores after cancellations
        for player in self.players:
            player.score = sum(Player.rune_values[rune] * count for rune, count in rune_counts[player.name].items())
            print(f"{player.name}'s score after cancellation: {player.score}")

    def determine_winner(self):
        """Determine the winner of the round based on scores."""
        highest_score = max(player.score for player in self.players)
        winners = [player.name for player in self.players if player.score == highest_score]

        if len(winners) == 1:
            print(f"{winners[0]} wins the round with {highest_score} points!\n")
        else:
            print(f"It's a tie between {', '.join(winners)} with {highest_score} points each!\n")

    def start(self):
        """Start the game, set up players, and manage rounds."""
        variant = input("Do you want to play the Wild Orc variant? (yes/no): ").lower()
        self.is_wild_orc_variant = variant in ['yes', 'y']

        self.add_player()  # Allow player setup

        while True:
            # Play a round
            self.play_round()

            # Determine the winner
            self.determine_winner()

            play_again = input("Do you want to play another round? (yes/no): ").lower()
            if play_again not in ['yes', 'y']:
                break

        print("Thanks for playing OrcKnuckle!")


# Example game setup and start
if __name__ == "__main__":
    game = Game()
    game.start()
