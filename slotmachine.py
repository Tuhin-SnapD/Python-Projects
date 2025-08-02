"""
Enhanced Slot Machine Game

A feature-rich slot machine simulation with multiple paylines,
bonus features, progressive jackpots, and improved gameplay.
"""

import random
import time
import sys
from typing import List, Dict, Tuple
from enum import Enum


class Symbol(Enum):
    """Slot machine symbols with their values and counts."""
    SEVEN = ("7️⃣", 100, 2)
    BELL = ("🔔", 50, 3)
    CHERRY = ("🍒", 25, 4)
    LEMON = ("🍋", 15, 5)
    ORANGE = ("🍊", 10, 6)
    PLUM = ("🫐", 8, 7)
    GRAPE = ("🍇", 5, 8)
    WATERMELON = ("🍉", 3, 10)
    
    def __init__(self, emoji: str, value: int, count: int):
        self.emoji = emoji
        self.value = value
        self.count = count


class SlotMachine:
    """Enhanced slot machine game."""
    
    def __init__(self):
        self.balance = 0
        self.total_bet = 0
        self.total_won = 0
        self.games_played = 0
        self.max_lines = 5
        self.max_bet = 100
        self.min_bet = 1
        self.rows = 3
        self.cols = 3
        self.progressive_jackpot = 1000
        self.bonus_spins = 0
        
    def print_welcome(self):
        """Display welcome message and game rules."""
        print("🎰 ENHANCED SLOT MACHINE! 🎰")
        print("=" * 40)
        print("Rules:")
        print("• Bet on 1-5 paylines")
        print("• Match 3 symbols on a line to win")
        print("• Higher value symbols pay more")
        print("• Progressive jackpot increases with each bet")
        print("• Bonus spins awarded for special combinations")
        print("=" * 40)
        time.sleep(2)
    
    def get_symbol_list(self) -> List[str]:
        """Get list of all symbols based on their counts."""
        symbols = []
        for symbol in Symbol:
            symbols.extend([symbol.emoji] * symbol.count)
        return symbols
    
    def spin_reels(self) -> List[List[str]]:
        """Spin the slot machine reels."""
        symbols = self.get_symbol_list()
        reels = []
        
        for _ in range(self.cols):
            reel = random.choices(symbols, k=self.rows)
            reels.append(reel)
        
        return reels
    
    def display_reels(self, reels: List[List[str]]):
        """Display the slot machine reels."""
        print("\n" + "=" * 25)
        print("🎰 SLOT MACHINE 🎰")
        print("=" * 25)
        
        for row in range(self.rows):
            line = " | ".join(reels[col][row] for col in range(self.cols))
            print(f"  {line}")
        
        print("=" * 25)
    
    def check_line(self, reels: List[List[str]], line: int) -> Tuple[bool, str, int]:
        """Check if a specific payline has a winning combination."""
        if line >= self.rows:
            return False, "", 0
        
        # Get symbols on the payline
        symbols = [reels[col][line] for col in range(self.cols)]
        
        # Check if all symbols are the same
        if len(set(symbols)) == 1:
            symbol = symbols[0]
            # Find symbol value
            for sym in Symbol:
                if sym.emoji == symbol:
                    return True, symbol, sym.value
            return True, symbol, 1
        
        return False, "", 0
    
    def check_all_lines(self, reels: List[List[str]], lines_bet: int, bet_per_line: int) -> List[Tuple[int, str, int]]:
        """Check all bet lines for wins."""
        winning_lines = []
        
        for line in range(lines_bet):
            is_win, symbol, value = self.check_line(reels, line)
            if is_win:
                winnings = value * bet_per_line
                winning_lines.append((line + 1, symbol, winnings))
        
        return winning_lines
    
    def check_bonus_features(self, reels: List[List[str]]) -> Dict[str, int]:
        """Check for bonus features."""
        bonuses = {}
        
        # Check for wild symbols (7️⃣ in all positions)
        all_sevens = True
        for col in range(self.cols):
            for row in range(self.rows):
                if reels[col][row] != Symbol.SEVEN.emoji:
                    all_sevens = False
                    break
            if not all_sevens:
                break
        
        if all_sevens:
            bonuses['jackpot'] = self.progressive_jackpot
            self.progressive_jackpot = 1000  # Reset jackpot
        
        # Check for bonus spins (3 bells in a row)
        for line in range(self.rows):
            symbols = [reels[col][line] for col in range(self.cols)]
            if all(sym == Symbol.BELL.emoji for sym in symbols):
                bonuses['bonus_spins'] = 3
                break
        
        # Check for scatter wins (same symbol in corners)
        corners = [
            reels[0][0], reels[0][2],  # Top corners
            reels[2][0], reels[2][2]   # Bottom corners
        ]
        if len(set(corners)) == 1:
            bonuses['scatter'] = 50
        
        return bonuses
    
    def get_deposit(self) -> int:
        """Get initial deposit from player."""
        while True:
            try:
                amount = input("💰 How much would you like to deposit? $").strip()
                if amount.lower() == 'quit':
                    return 0
                
                amount = int(amount)
                if amount > 0:
                    return amount
                else:
                    print("❌ Amount must be greater than 0.")
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                sys.exit(0)
    
    def get_bet_info(self) -> Tuple[int, int]:
        """Get number of lines and bet amount from player."""
        # Get number of lines
        while True:
            try:
                lines = input(f"📊 How many lines to bet on (1-{self.max_lines})? ").strip()
                if lines.lower() == 'quit':
                    return 0, 0
                
                lines = int(lines)
                if 1 <= lines <= self.max_lines:
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {self.max_lines}.")
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                sys.exit(0)
        
        # Get bet per line
        while True:
            try:
                bet = input(f"💵 Bet amount per line (${self.min_bet}-${self.max_bet})? $").strip()
                if bet.lower() == 'quit':
                    return 0, 0
                
                bet = int(bet)
                if self.min_bet <= bet <= self.max_bet:
                    break
                else:
                    print(f"❌ Please enter a bet between ${self.min_bet} and ${self.max_bet}.")
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                sys.exit(0)
        
        return lines, bet
    
    def spin(self) -> bool:
        """Perform a single spin."""
        # Get bet information
        lines, bet_per_line = self.get_bet_info()
        if lines == 0 or bet_per_line == 0:
            return False
        
        total_bet = lines * bet_per_line
        
        # Check if player has enough balance
        if total_bet > self.balance:
            print(f"❌ Insufficient balance! You have ${self.balance}, need ${total_bet}")
            return True
        
        # Deduct bet from balance
        self.balance -= total_bet
        self.total_bet += total_bet
        self.games_played += 1
        
        # Add to progressive jackpot
        self.progressive_jackpot += total_bet // 10
        
        print(f"\n🎰 Spinning {lines} lines at ${bet_per_line} each...")
        print(f"💰 Total bet: ${total_bet}")
        print(f"🎯 Progressive jackpot: ${self.progressive_jackpot}")
        
        # Animate spin
        for _ in range(3):
            temp_reels = self.spin_reels()
            self.display_reels(temp_reels)
            time.sleep(0.3)
            print("\033[A" * 8)  # Move cursor up
        
        # Final spin
        reels = self.spin_reels()
        self.display_reels(reels)
        
        # Check for wins
        winning_lines = self.check_all_lines(reels, lines, bet_per_line)
        total_winnings = 0
        
        if winning_lines:
            print(f"\n🎉 WINNING LINES:")
            for line_num, symbol, winnings in winning_lines:
                print(f"   Line {line_num}: {symbol} = ${winnings}")
                total_winnings += winnings
        
        # Check bonus features
        bonuses = self.check_bonus_features(reels)
        if bonuses:
            print(f"\n🎁 BONUS FEATURES:")
            for bonus_type, amount in bonuses.items():
                if bonus_type == 'jackpot':
                    print(f"   🏆 PROGRESSIVE JACKPOT: ${amount}")
                    total_winnings += amount
                elif bonus_type == 'bonus_spins':
                    print(f"   🎰 BONUS SPINS: {amount} free spins")
                    self.bonus_spins += amount
                elif bonus_type == 'scatter':
                    print(f"   ✨ SCATTER WIN: ${amount}")
                    total_winnings += amount
        
        # Update balance and statistics
        self.balance += total_winnings
        self.total_won += total_winnings
        
        if total_winnings > 0:
            print(f"\n💰 Total winnings: ${total_winnings}")
            print(f"💵 New balance: ${self.balance}")
        else:
            print(f"\n😔 No wins this time!")
            print(f"💵 Balance: ${self.balance}")
        
        return True
    
    def show_statistics(self):
        """Display game statistics."""
        print("\n📊 GAME STATISTICS")
        print("=" * 30)
        print(f"Games played: {self.games_played}")
        print(f"Total bet: ${self.total_bet}")
        print(f"Total won: ${self.total_won}")
        
        if self.total_bet > 0:
            roi = ((self.total_won - self.total_bet) / self.total_bet) * 100
            print(f"ROI: {roi:.1f}%")
        
        print(f"Current balance: ${self.balance}")
        print(f"Progressive jackpot: ${self.progressive_jackpot}")
        print(f"Bonus spins remaining: {self.bonus_spins}")
        print("=" * 30)
    
    def show_symbol_values(self):
        """Display symbol values."""
        print("\n🎯 SYMBOL VALUES")
        print("=" * 20)
        for symbol in Symbol:
            print(f"{symbol.emoji}: ${symbol.value}")
        print("=" * 20)
    
    def play_bonus_spins(self):
        """Play bonus spins if available."""
        if self.bonus_spins <= 0:
            return
        
        print(f"\n🎰 PLAYING {self.bonus_spins} BONUS SPINS!")
        print("=" * 30)
        
        for spin in range(self.bonus_spins):
            print(f"\n🎰 Bonus Spin {spin + 1}/{self.bonus_spins}")
            
            # Spin with same bet as last spin
            reels = self.spin_reels()
            self.display_reels(reels)
            
            # Check for wins (no bet deduction for bonus spins)
            winning_lines = self.check_all_lines(reels, min(3, self.max_lines), 1)
            total_winnings = 0
            
            if winning_lines:
                print(f"\n🎉 BONUS WINNINGS:")
                for line_num, symbol, winnings in winning_lines:
                    print(f"   Line {line_num}: {symbol} = ${winnings}")
                    total_winnings += winnings
                
                self.balance += total_winnings
                self.total_won += total_winnings
                print(f"💰 Total bonus winnings: ${total_winnings}")
            
            time.sleep(1)
        
        self.bonus_spins = 0
        print(f"\n💵 Final balance after bonus spins: ${self.balance}")
    
    def play(self):
        """Main game loop."""
        self.print_welcome()
        
        # Get initial deposit
        self.balance = self.get_deposit()
        if self.balance == 0:
            print("👋 Thanks for playing!")
            return
        
        print(f"💰 Starting balance: ${self.balance}")
        
        # Main game loop
        while True:
            print(f"\n💵 Current balance: ${self.balance}")
            
            if self.bonus_spins > 0:
                print(f"🎰 Bonus spins available: {self.bonus_spins}")
            
            print("\n📋 Options:")
            print("1. Spin")
            print("2. Show statistics")
            print("3. Show symbol values")
            print("4. Play bonus spins")
            print("5. Quit")
            
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == '1':
                    if not self.spin():
                        break
                elif choice == '2':
                    self.show_statistics()
                elif choice == '3':
                    self.show_symbol_values()
                elif choice == '4':
                    self.play_bonus_spins()
                elif choice == '5':
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-5.")
                
                # Check if player is out of money
                if self.balance <= 0:
                    print("\n💸 You're out of money!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                break
        
        # End game statistics
        self.show_statistics()
        print("\n👋 Thanks for playing the Enhanced Slot Machine!")


def main():
    """Main function to start the slot machine game."""
    try:
        slot_machine = SlotMachine()
        slot_machine.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try running the game again.")


if __name__ == "__main__":
    main()