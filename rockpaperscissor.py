"""
Enhanced Rock Paper Scissors Game

A feature-rich implementation with AI difficulty levels,
statistics tracking, and improved gameplay mechanics.
"""

import random
import time
import sys
from typing import Dict, List, Tuple
from enum import Enum


class Move(Enum):
    """Available moves in the game."""
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class Difficulty(Enum):
    """AI difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class RockPaperScissors:
    """Enhanced Rock Paper Scissors game."""
    
    def __init__(self):
        self.stats = {
            'games_played': 0,
            'player_wins': 0,
            'computer_wins': 0,
            'ties': 0,
            'current_streak': 0,
            'best_streak': 0,
            'move_history': []
        }
        self.difficulty = Difficulty.MEDIUM
        self.computer_memory = []  # For learning AI
        
    def print_welcome(self):
        """Display welcome message and game rules."""
        print("✂️  ENHANCED ROCK PAPER SCISSORS! ✂️")
        print("=" * 40)
        print("Rules:")
        print("• Rock beats Scissors")
        print("• Scissors beats Paper")
        print("• Paper beats Rock")
        print("• Type 'rock', 'paper', or 'scissors'")
        print("• Type 'stats' to see your statistics")
        print("• Type 'difficulty' to change AI level")
        print("• Type 'quit' to exit the game")
        print("=" * 40)
        time.sleep(2)
    
    def get_valid_move(self, input_text: str) -> Move:
        """Convert user input to valid move."""
        input_lower = input_text.lower().strip()
        
        if input_lower in ['r', 'rock']:
            return Move.ROCK
        elif input_lower in ['p', 'paper']:
            return Move.PAPER
        elif input_lower in ['s', 'scissors']:
            return Move.SCISSORS
        else:
            raise ValueError("Invalid move")
    
    def get_computer_move_easy(self) -> Move:
        """Get computer move for easy difficulty (random)."""
        return random.choice(list(Move))
    
    def get_computer_move_medium(self) -> Move:
        """Get computer move for medium difficulty (some strategy)."""
        # 70% random, 30% counter to player's most common move
        if random.random() < 0.7:
            return random.choice(list(Move))
        else:
            # Counter the player's most common move
            if self.stats['move_history']:
                player_moves = [move[0] for move in self.stats['move_history']]
                most_common = max(set(player_moves), key=player_moves.count)
                return self.get_counter_move(most_common)
            else:
                return random.choice(list(Move))
    
    def get_computer_move_hard(self) -> Move:
        """Get computer move for hard difficulty (advanced strategy)."""
        if len(self.stats['move_history']) < 3:
            return random.choice(list(Move))
        
        # Analyze recent patterns
        recent_moves = self.stats['move_history'][-3:]
        player_moves = [move[0] for move in recent_moves]
        
        # Look for patterns
        if len(player_moves) >= 2:
            # Check if player tends to repeat moves
            if player_moves[-1] == player_moves[-2]:
                # Player might repeat again, counter the expected move
                expected_move = player_moves[-1]
                return self.get_counter_move(expected_move)
            
            # Check if player cycles through moves
            if len(player_moves) >= 3:
                if (player_moves[-3] == Move.ROCK and 
                    player_moves[-2] == Move.PAPER and 
                    player_moves[-1] == Move.SCISSORS):
                    # Player is cycling R->P->S, expect Rock next
                    return self.get_counter_move(Move.ROCK)
                elif (player_moves[-3] == Move.SCISSORS and 
                      player_moves[-2] == Move.PAPER and 
                      player_moves[-1] == Move.ROCK):
                    # Player is cycling S->P->R, expect Scissors next
                    return self.get_counter_move(Move.SCISSORS)
        
        # Fall back to medium difficulty strategy
        return self.get_computer_move_medium()
    
    def get_counter_move(self, move: Move) -> Move:
        """Get the move that beats the given move."""
        if move == Move.ROCK:
            return Move.PAPER
        elif move == Move.PAPER:
            return Move.SCISSORS
        else:  # SCISSORS
            return Move.ROCK
    
    def get_computer_move(self) -> Move:
        """Get computer move based on current difficulty."""
        if self.difficulty == Difficulty.EASY:
            return self.get_computer_move_easy()
        elif self.difficulty == Difficulty.MEDIUM:
            return self.get_computer_move_medium()
        else:  # HARD
            return self.get_computer_move_hard()
    
    def determine_winner(self, player_move: Move, computer_move: Move) -> str:
        """Determine the winner of a round."""
        if player_move == computer_move:
            return "tie"
        
        # Check if player wins
        if ((player_move == Move.ROCK and computer_move == Move.SCISSORS) or
            (player_move == Move.PAPER and computer_move == Move.ROCK) or
            (player_move == Move.SCISSORS and computer_move == Move.PAPER)):
            return "player"
        else:
            return "computer"
    
    def update_stats(self, player_move: Move, computer_move: Move, result: str):
        """Update game statistics."""
        self.stats['games_played'] += 1
        self.stats['move_history'].append((player_move, computer_move, result))
        
        # Keep only last 50 moves for memory
        if len(self.stats['move_history']) > 50:
            self.stats['move_history'] = self.stats['move_history'][-50:]
        
        if result == "player":
            self.stats['player_wins'] += 1
            self.stats['current_streak'] += 1
            self.stats['best_streak'] = max(self.stats['best_streak'], self.stats['current_streak'])
        elif result == "computer":
            self.stats['computer_wins'] += 1
            self.stats['current_streak'] = 0
        else:  # tie
            self.stats['ties'] += 1
            self.stats['current_streak'] = 0
    
    def display_stats(self):
        """Display game statistics."""
        if self.stats['games_played'] == 0:
            print("📊 No games played yet!")
            return
        
        print("\n📊 GAME STATISTICS")
        print("=" * 30)
        print(f"Games played: {self.stats['games_played']}")
        print(f"Player wins: {self.stats['player_wins']}")
        print(f"Computer wins: {self.stats['computer_wins']}")
        print(f"Ties: {self.stats['ties']}")
        
        win_rate = (self.stats['player_wins'] / self.stats['games_played']) * 100
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Current streak: {self.stats['current_streak']}")
        print(f"Best streak: {self.stats['best_streak']}")
        print(f"Difficulty: {self.difficulty.value.title()}")
        
        # Show move distribution
        if self.stats['move_history']:
            player_moves = [move[0] for move in self.stats['move_history']]
            rock_count = player_moves.count(Move.ROCK)
            paper_count = player_moves.count(Move.PAPER)
            scissors_count = player_moves.count(Move.SCISSORS)
            
            print(f"\nMove distribution:")
            print(f"Rock: {rock_count} ({rock_count/len(player_moves)*100:.1f}%)")
            print(f"Paper: {paper_count} ({paper_count/len(player_moves)*100:.1f}%)")
            print(f"Scissors: {scissors_count} ({scissors_count/len(player_moves)*100:.1f}%)")
        
        print("=" * 30)
    
    def change_difficulty(self):
        """Change AI difficulty level."""
        print(f"\n🎯 DIFFICULTY SETTINGS")
        print("=" * 25)
        print("1. Easy - Random moves")
        print("2. Medium - Some strategy")
        print("3. Hard - Advanced AI")
        
        while True:
            try:
                choice = input(f"\nSelect difficulty (1-3, current: {self.difficulty.value.title()}): ").strip()
                if choice == '1':
                    self.difficulty = Difficulty.EASY
                    print("✅ Difficulty set to Easy")
                    break
                elif choice == '2':
                    self.difficulty = Difficulty.MEDIUM
                    print("✅ Difficulty set to Medium")
                    break
                elif choice == '3':
                    self.difficulty = Difficulty.HARD
                    print("✅ Difficulty set to Hard")
                    break
                else:
                    print("❌ Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                sys.exit(0)
    
    def play_round(self) -> bool:
        """Play a single round of the game."""
        print(f"\n🎮 Round {self.stats['games_played'] + 1}")
        print("-" * 20)
        
        # Get player move
        while True:
            try:
                player_input = input("Your move (rock/paper/scissors, or 'help'/'quit'): ").strip().lower()
                
                if player_input == 'quit':
                    return False
                elif player_input == 'help':
                    self.show_help()
                    continue
                elif player_input == 'stats':
                    self.display_stats()
                    continue
                elif player_input == 'difficulty':
                    self.change_difficulty()
                    continue
                
                player_move = self.get_valid_move(player_input)
                break
                
            except ValueError:
                print("❌ Invalid move! Type 'rock', 'paper', or 'scissors'.")
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                sys.exit(0)
        
        # Get computer move
        computer_move = self.get_computer_move()
        
        # Display moves
        print(f"\nYou chose: {player_move.value.title()}")
        print(f"Computer chose: {computer_move.value.title()}")
        
        # Determine winner
        result = self.determine_winner(player_move, computer_move)
        
        # Display result
        print(f"\n{self.get_result_message(result)}")
        
        # Update statistics
        self.update_stats(player_move, computer_move, result)
        
        return True
    
    def get_result_message(self, result: str) -> str:
        """Get appropriate result message."""
        if result == "player":
            return "🎉 You win!"
        elif result == "computer":
            return "💻 Computer wins!"
        else:
            return "🤝 It's a tie!"
    
    def show_help(self):
        """Show help information."""
        print("\n📖 GAME HELP")
        print("=" * 15)
        print("Moves:")
        print("- rock (or r): Beats scissors, loses to paper")
        print("- paper (or p): Beats rock, loses to scissors")
        print("- scissors (or s): Beats paper, loses to rock")
        print("\nCommands:")
        print("- stats: Show your statistics")
        print("- difficulty: Change AI difficulty")
        print("- help: Show this help")
        print("- quit: Exit the game")
    
    def play(self):
        """Main game loop."""
        self.print_welcome()
        
        while True:
            if not self.play_round():
                break
            
            # Ask to continue
            while True:
                try:
                    continue_game = input("\nPlay again? (y/n): ").strip().lower()
                    if continue_game in ['y', 'yes']:
                        break
                    elif continue_game in ['n', 'no']:
                        self.display_stats()
                        print("\n👋 Thanks for playing Rock Paper Scissors!")
                        return
                    else:
                        print("Please enter 'y' or 'n'.")
                except KeyboardInterrupt:
                    print("\n\n👋 Game interrupted. Goodbye!")
                    return


def main():
    """Main function to start the game."""
    try:
        game = RockPaperScissors()
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try running the game again.")


if __name__ == "__main__":
    main()