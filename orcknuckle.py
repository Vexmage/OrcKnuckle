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
    def __init__(self, name):
        self.name = name
        self.rolls = []

    def roll_knuckles(self, dice):
        """Each player rolls their dice."""
        self.rolls = dice.roll()

    def display_roll(self):
        print(f"{self.name} rolled:")
        for rune, knuckle_type in self.rolls:
            print(f"  - {knuckle_type.capitalize()} shows a {rune.capitalize()}")


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

    def add_player(self, name, player_type):
        """Add players to the game (human or computer)."""
        if player_type == "human":
            self.players.append(HumanPlayer(name))
        else:
            self.players.append(ComputerPlayer(name))

    def play_round(self):
        """Play one round of the game where each player rolls."""
        for player in self.players:
            player.roll_knuckles(self.dice)
            player.display_roll()

    def start(self):
        """Start the game, set up players, and manage rounds."""
        # Example: Add players
        self.add_player("Sam", "human")
        self.add_player("Rex", "computer")
        self.add_player("Hal", "computer")

        # Play a single round for now
        self.play_round()


# Example game setup and start
if __name__ == "__main__":
    game = Game()
    game.start()
