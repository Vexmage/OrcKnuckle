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
        'orc': 0  # Orc cancels everything
    }

    def __init__(self, name):
        self.name = name
        self.rolls = []
        self.score = 0

    def roll_knuckles(self, dice):
        """Each player rolls their dice."""
        self.rolls = dice.roll()
        self.calculate_score()

    def calculate_score(self):
        """Calculate the player's score based on the roll."""
        # Calculate score based on the first three knuckles
        self.score = sum(Player.rune_values[rune] for rune, knuckle_type in self.rolls if knuckle_type == 'knuckle')

        # Handle thumb knuckle
        thumb_rune = self.rolls[-1][0]
        if thumb_rune == 'orc':
            print(f"{self.name}'s thumb knuckle shows an Orc, which cancels all other runes!")
            self.score = 0
        else:
            print(f"{self.name}'s thumb knuckle shows a {thumb_rune.capitalize()}, adding {Player.rune_values[thumb_rune]} points.")
            self.score += Player.rune_values[thumb_rune]

    def display_roll(self):
        """Display the player's roll with points for each face."""
        print(f"{self.name} rolled:")
        for rune, knuckle_type in self.rolls:
            print(f"  - {knuckle_type.capitalize()} shows a {rune.capitalize()} ({Player.rune_values[rune]} points)")
        print(f"{self.name} scored {self.score} points.\n")


# Human player subclass
class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def roll_knuckles(self, dice):
        """Human player must press a key to roll."""
        input(f"{self.name}, press any key to roll the knuckles...")
        super().roll_knuckles(dice)


# Computer player subclass
class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def roll_knuckles(self, dice):
        """Computer players roll without a prompt."""
        print(f"{self.name} is rolling the knuckles...")
        super().roll_knuckles(dice)


# Game class that runs the main game loop
class Game:
    def __init__(self):
        self.players = []
        self.dice = Dice()

    def add_player(self):
        """Add players to the game (human or computer)."""
        num_players = int(input("Enter the number of players: "))

        for i in range(1, num_players + 1):
            name = input(f"Enter the name of Player {i}: ")
            player_type = input(f"Is {name} a human or computer player? (human/computer): ").lower()
            if player_type == "human":
                self.players.append(HumanPlayer(name))
            else:
                self.players.append(ComputerPlayer(name))

    def play_round(self):
        """Play one round of the game where each player rolls."""
        for player in self.players:
            player.roll_knuckles(self.dice)
            player.display_roll()

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
        self.add_player()  # Allow player setup

        while True:
            # Play a round
            self.play_round()

            # Determine the winner
            self.determine_winner()

            # Ask if players want to play another round
            play_again = input("Do you want to play another round? (yes/no): ").lower()
            if play_again not in ['yes', 'y']:
                break

        print("Thanks for playing OrcKnuckle!")


# Example game setup and start
if __name__ == "__main__":
    game = Game()
    game.start()
