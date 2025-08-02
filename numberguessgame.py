"""
Enhanced Number Guessing Game

A feature-rich number guessing game with multiple difficulty levels,
statistics tracking, hints, and improved gameplay mechanics.
"""

import random
import time
import sys
from typing import Dict, List, Tuple
from enum import Enum


class Difficulty(Enum):
    """Game difficulty levels."""
    EASY = ("Easy", 1, 50, 10)
    MEDIUM = ("Medium", 1, 100, 8)
    HARD = ("Hard", 1, 200, 6)
    EXPERT = ("Expert", 1, 500, 5)
    
    def __init__(self, name: str, min_val: int, max_val: int, max_attempts: int):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.max_attempts = max_attempts


class NumberGuessingGame:
    """Enhanced number guessing game with multiple features."""
    
    def __init__(self):
        self.stats = {
            'games_played': 0,
            'games_won': 0,
            'games_lost': 0,
            'total_attempts': 0,
            'best_score': float('inf'),
            'average_attempts': 0.0
        }
        self.current_game = {
            'number': 0,
            'attempts': 0,
            'max_attempts': 0,
            'min_val': 0,
            'max_val': 0,
            'difficulty': None,
            'start_time': 0,
            'hints_used': 0
        }
        
    def print_welcome(self):
        """Display welcome message and game rules."""
        print("🎯 WELCOME TO THE NUMBER GUESSING GAME! 🎯")
        print("=" * 50)
        print("Rules:")
        print("• Guess the secret number within the given range")
        print("• You'll get hints after each guess")
        print("• Use 'hint' for extra help (costs 1 attempt)")
        print("• Use 'quit' to exit the game")
        print("• Try to guess in as few attempts as possible!")
        print("=" * 50)
        time.sleep(2)
    
    def select_difficulty(self) -> Difficulty:
        """Let player select difficulty level."""
        print("\n📊 Select Difficulty Level:")
        for i, difficulty in enumerate(Difficulty, 1):
            print(f"{i}. {difficulty.name} ({difficulty.min_val}-{difficulty.max_val}, "
                  f"{difficulty.max_attempts} attempts)")
        
        while True:
            try:
                choice = input("\nEnter difficulty (1-4): ").strip()
                if choice.lower() == 'quit':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(Difficulty):
                    return list(Difficulty)[choice_num - 1]
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                sys.exit(0)
    
    def get_hint(self, guess: int) -> str:
        """Provide a hint based on the current guess."""
        number = self.current_game['number']
        min_val = self.current_game['min_val']
        max_val = self.current_game['max_val']
        
        if guess < number:
            # Guess is too low
            if number - guess <= 5:
                return "Very close! You're just a bit low."
            elif number - guess <= 15:
                return "Getting warmer! Try a higher number."
            else:
                return "Too low! Try a much higher number."
        else:
            # Guess is too high
            if guess - number <= 5:
                return "Very close! You're just a bit high."
            elif guess - number <= 15:
                return "Getting warmer! Try a lower number."
            else:
                return "Too high! Try a much lower number."
    
    def get_range_hint(self) -> str:
        """Provide a range-based hint."""
        number = self.current_game['number']
        min_val = self.current_game['min_val']
        max_val = self.current_game['max_val']
        
        # Divide range into quarters
        quarter = (max_val - min_val) // 4
        q1 = min_val + quarter
        q2 = min_val + 2 * quarter
        q3 = min_val + 3 * quarter
        
        if number <= q1:
            return f"The number is in the first quarter ({min_val}-{q1})"
        elif number <= q2:
            return f"The number is in the second quarter ({q1+1}-{q2})"
        elif number <= q3:
            return f"The number is in the third quarter ({q2+1}-{q3})"
        else:
            return f"The number is in the fourth quarter ({q3+1}-{max_val})"
    
    def start_new_game(self, difficulty: Difficulty):
        """Start a new game with the specified difficulty."""
        self.current_game['difficulty'] = difficulty
        self.current_game['number'] = random.randint(difficulty.min_val, difficulty.max_val)
        self.current_game['attempts'] = 0
        self.current_game['max_attempts'] = difficulty.max_attempts
        self.current_game['min_val'] = difficulty.min_val
        self.current_game['max_val'] = difficulty.max_val
        self.current_game['start_time'] = time.time()
        self.current_game['hints_used'] = 0
        
        print(f"\n🎮 New Game - {difficulty.name} Difficulty")
        print(f"Range: {difficulty.min_val} to {difficulty.max_val}")
        print(f"Max attempts: {difficulty.max_attempts}")
        print("-" * 40)
    
    def get_guess(self) -> str:
        """Get and validate player's guess."""
        while True:
            try:
                guess = input(f"Enter your guess (or 'hint'/'quit'): ").strip().lower()
                
                if guess == 'quit':
                    return 'quit'
                elif guess == 'hint':
                    if self.current_game['attempts'] < self.current_game['max_attempts'] - 1:
                        self.current_game['hints_used'] += 1
                        print(f"\n💡 {self.get_range_hint()}")
                        self.current_game['attempts'] += 1
                        print(f"Attempts remaining: {self.current_game['max_attempts'] - self.current_game['attempts']}")
                        continue
                    else:
                        print("❌ No hints left! You're on your last attempt!")
                        continue
                elif not guess.isdigit():
                    print("❌ Please enter a valid number.")
                    continue
                else:
                    return guess
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                sys.exit(0)
    
    def play_round(self) -> bool:
        """Play a single round of the game."""
        # Select difficulty
        difficulty = self.select_difficulty()
        if difficulty is None:
            return False
        
        # Start new game
        self.start_new_game(difficulty)
        
        # Main game loop
        while self.current_game['attempts'] < self.current_game['max_attempts']:
            print(f"\nAttempt {self.current_game['attempts'] + 1}/{self.current_game['max_attempts']}")
            
            guess = self.get_guess()
            if guess == 'quit':
                return False
            
            try:
                guess_num = int(guess)
                self.current_game['attempts'] += 1
                
                if guess_num == self.current_game['number']:
                    self.display_win()
                    return True
                else:
                    hint = self.get_hint(guess_num)
                    print(f"❌ {hint}")
                    
                    if self.current_game['attempts'] >= self.current_game['max_attempts']:
                        self.display_lose()
                        return False
                        
            except ValueError:
                print("❌ Please enter a valid number.")
                continue
        
        return False
    
    def display_win(self):
        """Display win message and statistics."""
        end_time = time.time()
        game_time = end_time - self.current_game['start_time']
        
        print("\n🎉 CONGRATULATIONS! 🎉")
        print(f"You guessed the number: {self.current_game['number']}")
        print(f"Attempts used: {self.current_game['attempts']}")
        print(f"Time taken: {game_time:.2f} seconds")
        print(f"Hints used: {self.current_game['hints_used']}")
        
        # Calculate score (lower is better)
        score = self.current_game['attempts'] + self.current_game['hints_used']
        print(f"Score: {score} points")
        
        if score < self.stats['best_score']:
            self.stats['best_score'] = score
            print("🏆 NEW BEST SCORE! 🏆")
    
    def display_lose(self):
        """Display lose message."""
        print("\n💀 GAME OVER! 💀")
        print(f"The number was: {self.current_game['number']}")
        print("Better luck next time!")
    
    def update_stats(self, won: bool):
        """Update game statistics."""
        self.stats['games_played'] += 1
        self.stats['total_attempts'] += self.current_game['attempts']
        
        if won:
            self.stats['games_won'] += 1
        else:
            self.stats['games_lost'] += 1
        
        # Update average attempts
        if self.stats['games_played'] > 0:
            self.stats['average_attempts'] = self.stats['total_attempts'] / self.stats['games_played']
    
    def display_stats(self):
        """Display game statistics."""
        print("\n📊 GAME STATISTICS")
        print("=" * 30)
        print(f"Games played: {self.stats['games_played']}")
        print(f"Games won: {self.stats['games_won']}")
        print(f"Games lost: {self.stats['games_lost']}")
        
        if self.stats['games_played'] > 0:
            win_rate = (self.stats['games_won'] / self.stats['games_played']) * 100
            print(f"Win rate: {win_rate:.1f}%")
            print(f"Average attempts: {self.stats['average_attempts']:.1f}")
        
        if self.stats['best_score'] != float('inf'):
            print(f"Best score: {self.stats['best_score']} points")
        else:
            print("Best score: None")
        
        print("=" * 30)
    
    def play(self):
        """Main game loop."""
        self.print_welcome()
        
        while True:
            won = self.play_round()
            self.update_stats(won)
            
            # Ask to play again
            while True:
                try:
                    play_again = input("\nPlay again? (y/n): ").strip().lower()
                    if play_again in ['y', 'yes']:
                        break
                    elif play_again in ['n', 'no']:
                        self.display_stats()
                        print("\nThanks for playing! 👋")
                        return
                    else:
                        print("Please enter 'y' or 'n'.")
                except KeyboardInterrupt:
                    print("\n\nThanks for playing! 👋")
                    return


def main():
    """Main function to start the game."""
    try:
        game = NumberGuessingGame()
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try running the game again.")


if __name__ == "__main__":
    main()