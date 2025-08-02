"""
Enhanced Hangman Game

A feature-rich implementation of the classic Hangman game with multiple categories,
statistics tracking, better UI, and improved gameplay mechanics.
"""

import random
import time
import sys
from typing import List, Set, Dict


class HangmanGame:
    """Main game class for the Hangman game."""
    
    # Game categories with words
    CATEGORIES = {
        'fruits': [
            'apple', 'banana', 'mango', 'strawberry', 'orange', 'grape', 'pineapple',
            'apricot', 'lemon', 'coconut', 'watermelon', 'cherry', 'papaya', 'berry',
            'peach', 'lychee', 'muskmelon', 'kiwi', 'plum', 'fig', 'date'
        ],
        'animals': [
            'elephant', 'giraffe', 'penguin', 'kangaroo', 'dolphin', 'tiger', 'lion',
            'zebra', 'panda', 'koala', 'rhinoceros', 'hippopotamus', 'crocodile',
            'flamingo', 'ostrich', 'gorilla', 'chimpanzee', 'orangutan', 'sloth'
        ],
        'countries': [
            'australia', 'brazil', 'canada', 'denmark', 'egypt', 'france', 'germany',
            'india', 'japan', 'kenya', 'mexico', 'norway', 'portugal', 'russia',
            'spain', 'thailand', 'ukraine', 'vietnam', 'zimbabwe', 'argentina'
        ],
        'colors': [
            'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown',
            'black', 'white', 'gray', 'cyan', 'magenta', 'violet', 'indigo',
            'turquoise', 'maroon', 'navy', 'olive', 'teal'
        ]
    }
    
    # ASCII art for hangman stages
    HANGMAN_STAGES = [
        """
           +---+
               |
               |
               |
              ===
        """,
        """
           +---+
           O   |
               |
               |
              ===
        """,
        """
           +---+
           O   |
           |   |
               |
              ===
        """,
        """
           +---+
           O   |
          /|   |
               |
              ===
        """,
        """
           +---+
           O   |
          /|\\  |
               |
              ===
        """,
        """
           +---+
           O   |
          /|\\  |
          /    |
              ===
        """,
        """
           +---+
           O   |
          /|\\  |
          / \\  |
              ===
        """
    ]
    
    def __init__(self):
        self.stats = {
            'games_played': 0,
            'games_won': 0,
            'games_lost': 0,
            'total_guesses': 0,
            'best_score': 0
        }
        self.current_word = ""
        self.guessed_letters: Set[str] = set()
        self.correct_letters: Set[str] = set()
        self.incorrect_guesses = 0
        self.max_attempts = 6
        self.category = ""
        
    def clear_screen(self):
        """Clear the console screen."""
        print("\n" * 50)
        
    def print_welcome(self):
        """Display welcome message and game rules."""
        self.clear_screen()
        print("🎯 WELCOME TO HANGMAN! 🎯")
        print("=" * 40)
        print("Rules:")
        print("• Guess the word one letter at a time")
        print("• You have 6 incorrect guesses allowed")
        print("• Type 'quit' to exit the game")
        print("• Type 'hint' for a hint (costs 1 attempt)")
        print("=" * 40)
        time.sleep(2)
        
    def select_category(self) -> str:
        """Let player select a word category."""
        print("\n📚 Choose a category:")
        for i, category in enumerate(self.CATEGORIES.keys(), 1):
            print(f"{i}. {category.title()}")
        
        while True:
            try:
                choice = input("\nEnter category number (1-4): ").strip()
                if choice.lower() == 'quit':
                    return 'quit'
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.CATEGORIES):
                    category = list(self.CATEGORIES.keys())[choice_num - 1]
                    return category
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                sys.exit(0)
    
    def get_hint(self) -> str:
        """Provide a hint for the current word."""
        if len(self.correct_letters) < len(set(self.current_word)) - 1:
            # Find a letter that hasn't been guessed yet
            unguessed = set(self.current_word) - self.correct_letters
            if unguessed:
                return f"Hint: The word contains the letter '{random.choice(list(unguessed))}'"
        return "Hint: You're doing great! Keep guessing!"
    
    def display_word(self) -> str:
        """Display the word with underscores for unguessed letters."""
        display = []
        for letter in self.current_word:
            if letter in self.correct_letters:
                display.append(letter.upper())
            else:
                display.append('_')
        return ' '.join(display)
    
    def display_game_state(self):
        """Display current game state."""
        self.clear_screen()
        print(f"🎯 HANGMAN - Category: {self.category.title()}")
        print("=" * 40)
        
        # Display hangman
        print(self.HANGMAN_STAGES[self.incorrect_guesses])
        
        # Display word
        print(f"\nWord: {self.display_word()}")
        print(f"Length: {len(self.current_word)} letters")
        
        # Display game info
        print(f"\nIncorrect guesses: {self.incorrect_guesses}/{self.max_attempts}")
        print(f"Guessed letters: {', '.join(sorted(self.guessed_letters)) if self.guessed_letters else 'None'}")
        
        # Display remaining letters
        remaining = set('abcdefghijklmnopqrstuvwxyz') - self.guessed_letters
        print(f"Remaining letters: {', '.join(sorted(remaining))}")
        
        print("-" * 40)
    
    def get_guess(self) -> str:
        """Get and validate player's guess."""
        while True:
            try:
                guess = input("Enter a letter (or 'hint'/'quit'): ").strip().lower()
                
                if guess == 'quit':
                    return 'quit'
                elif guess == 'hint':
                    if self.incorrect_guesses < self.max_attempts - 1:
                        print(f"\n💡 {self.get_hint()}")
                        self.incorrect_guesses += 1
                        input("Press Enter to continue...")
                        return 'hint'
                    else:
                        print("❌ No hints left! You're on your last attempt!")
                        continue
                elif len(guess) != 1:
                    print("❌ Please enter exactly one letter.")
                    continue
                elif not guess.isalpha():
                    print("❌ Please enter a letter (a-z).")
                    continue
                elif guess in self.guessed_letters:
                    print("❌ You already guessed that letter!")
                    continue
                else:
                    return guess
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                sys.exit(0)
    
    def process_guess(self, guess: str) -> bool:
        """Process the player's guess and return True if correct."""
        self.guessed_letters.add(guess)
        
        if guess in self.current_word:
            self.correct_letters.add(guess)
            print(f"✅ Correct! '{guess}' is in the word!")
            return True
        else:
            self.incorrect_guesses += 1
            print(f"❌ Wrong! '{guess}' is not in the word.")
            return False
    
    def check_win(self) -> bool:
        """Check if the player has won."""
        return self.correct_letters == set(self.current_word)
    
    def check_lose(self) -> bool:
        """Check if the player has lost."""
        return self.incorrect_guesses >= self.max_attempts
    
    def play_round(self) -> bool:
        """Play a single round of hangman."""
        # Select category
        self.category = self.select_category()
        if self.category == 'quit':
            return False
        
        # Initialize round
        self.current_word = random.choice(self.CATEGORIES[self.category])
        self.guessed_letters.clear()
        self.correct_letters.clear()
        self.incorrect_guesses = 0
        
        print(f"\n🎮 Starting new game in category: {self.category.title()}")
        time.sleep(1)
        
        # Main game loop
        while True:
            self.display_game_state()
            
            if self.check_win():
                self.display_win()
                return True
            elif self.check_lose():
                self.display_lose()
                return False
            
            guess = self.get_guess()
            if guess == 'quit':
                return False
            elif guess == 'hint':
                continue
            
            self.process_guess(guess)
            time.sleep(1)
    
    def display_win(self):
        """Display win message."""
        self.display_game_state()
        print("\n🎉 CONGRATULATIONS! 🎉")
        print(f"You guessed the word: {self.current_word.upper()}")
        print(f"Attempts used: {len(self.guessed_letters)}")
        print(f"Incorrect guesses: {self.incorrect_guesses}")
        
        # Calculate score
        score = max(0, 100 - (self.incorrect_guesses * 15))
        print(f"Score: {score} points!")
        
        if score > self.stats['best_score']:
            self.stats['best_score'] = score
            print("🏆 NEW HIGH SCORE! 🏆")
    
    def display_lose(self):
        """Display lose message."""
        self.display_game_state()
        print("\n💀 GAME OVER! 💀")
        print(f"The word was: {self.current_word.upper()}")
        print("Better luck next time!")
    
    def update_stats(self, won: bool):
        """Update game statistics."""
        self.stats['games_played'] += 1
        self.stats['total_guesses'] += len(self.guessed_letters)
        
        if won:
            self.stats['games_won'] += 1
        else:
            self.stats['games_lost'] += 1
    
    def display_stats(self):
        """Display game statistics."""
        print("\n📊 GAME STATISTICS")
        print("=" * 30)
        print(f"Games played: {self.stats['games_played']}")
        print(f"Games won: {self.stats['games_won']}")
        print(f"Games lost: {self.stats['games_lost']}")
        
        if self.stats['games_played'] > 0:
            win_rate = (self.stats['games_won'] / self.stats['games_played']) * 100
            avg_guesses = self.stats['total_guesses'] / self.stats['games_played']
            print(f"Win rate: {win_rate:.1f}%")
            print(f"Average guesses per game: {avg_guesses:.1f}")
        
        print(f"Best score: {self.stats['best_score']} points")
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
                        print("\nThanks for playing Hangman! 👋")
                        return
                    else:
                        print("Please enter 'y' or 'n'.")
                except KeyboardInterrupt:
                    print("\n\nThanks for playing Hangman! 👋")
                    return


def main():
    """Main function to start the game."""
    try:
        game = HangmanGame()
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try running the game again.")


if __name__ == "__main__":
    main()