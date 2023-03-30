"""
This code implements a command-line game of Rock-Paper-Scissors between the user and the computer. The user is prompted to input their choice of 
rock, paper, or scissors, and the computer randomly selects its choice. 
The game then determines the winner of each round based on the classic Rock-Paper-Scissors rules, and keeps a running tally of the user's wins and 
the computer's wins. The game continues until the user enters "q" to quit. Finally, the game prints out the total number of wins for each player 
and exits.
"""
# Import the random module
import random

class RockPaperScissors:
    def __init__(self):
        # Initialize user and computer wins to 0
        self.user_wins = 0
        self.computer_wins = 0

        # List of available options
        self.options = ["rock", "paper", "scissors"]

        # Dictionary mapping each option to the option it beats
        self.winning_conditions = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }

    def play(self):
        # Main game loop
        while True:
            # Get user input
            user_input = input(
                "Type Rock/Paper/Scissors or Q to quit: ").lower()
            if user_input == "q":
                # Quit if user enters "q"
                break

            if user_input not in self.options:
                # If user enters an invalid input, prompt them again
                continue

            # Generate computer's pick
            random_number = random.randint(0, 2)
            computer_pick = self.options[random_number]
            print(f"Computer picked {computer_pick}.")

            # Determine the winner of the round
            winner = self.determine_winner(user_input, computer_pick)
            if winner == "user":
                print("You won!")
                self.user_wins += 1
            elif winner == "computer":
                print("You lost!")
                self.computer_wins += 1
            else:
                print("Tie!")

        # Print the final scores and exit the game
        print(f"You won {self.user_wins} times.")
        print(f"The computer won {self.computer_wins} times.")
        print("Goodbye!")

    def determine_winner(self, user_input, computer_pick):
        # Determine the winner of a single round
        if user_input == computer_pick:
            # If the choices are the same, it's a tie
            return "tie"
        if self.winning_conditions[user_input] == computer_pick:
            # If the user's pick beats the computer's pick, the user wins
            return "user"
        return "computer"

# Create a new game and play it
game = RockPaperScissors()
game.play()