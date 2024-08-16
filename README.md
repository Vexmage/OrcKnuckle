# OrcKnuckle Game

OrcKnuckle is a text-based dice game implemented in Python, inspired by a popular gambling game from the Crossfire RPG. 
This project simulates a fantasy gambling game where players roll custom dice (knuckles) and score based on the faces showing. 
OrcKnuckle is released under the GNU General Public License (GPL), ensuring that it remains free and open source.

## Game Overview
OrcKnuckle is a simple yet engaging game where players roll four knuckles—three 5-sided dice and one special 6-sided die 
(the thumb knuckle). The faces of the dice are carved with runes representing different characters and creatures:

    - Knuckle Faces: Beholder, Ghost, Princess, Knight, Dragon
    - Thumb Knuckle Faces: Beholder, Ghost, Princess, Knight, Dragon, Orc

## Scoring Rules

    - Beholder: 1 point
    - Princess & Knight: 2 points each
    - Dragon: 3 points
    - Ghost: Cancels out a Princess (no points)
    - Knight: Cancels out a Dragon (no points)
    - Orc: Cancels everything (0 points)

The player with the highest score after rolling wins the round. If there is a tie, the bets carry over to the next round.

## Getting Started

To run the game, you'll need Python installed on your machine. Simply clone this repository and run the Python script:

- git clone https://github.com/Vexmage/OrcKnuckle.git
- cd OrcKnuckle
- python orcknuckle.py

## License

This project is licensed under the GNU General Public License (GPL) version 2 or later. 
You can freely modify and redistribute the code under the terms of this license.

OrcKnuckle Game
Copyright (C) 2024 Joel Southall

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

## Acknowledgments

This project is inspired by the game rules from the Crossfire RPG, an open-source, cooperative multiplayer graphical RPG 
and adventure game. The official Crossfire site can be found at https://crossfire.real-time.com.

