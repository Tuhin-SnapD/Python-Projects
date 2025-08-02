"""
Text-based Adventure Game

A simple text-based adventure game where players make choices that affect the story outcome.
The game features multiple paths, better error handling, and more engaging content.
"""

import random
import time
import sys


class AdventureGame:
    """Main game class that handles the adventure game logic."""
    
    def __init__(self):
        self.player_name = ""
        self.score = 0
        self.choices_made = []
        
    def print_slow(self, text, delay=0.03):
        """Print text with a typewriter effect."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def get_valid_input(self, prompt, valid_options):
        """Get and validate user input."""
        while True:
            try:
                user_input = input(prompt).strip().lower()
                if user_input in valid_options:
                    return user_input
                else:
                    print(f"Please choose from: {', '.join(valid_options)}")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                sys.exit(0)
    
    def intro(self):
        """Display game introduction and get player name."""
        self.print_slow("🌲 Welcome to the Mysterious Forest Adventure! 🌲")
        self.print_slow("You find yourself at the edge of an ancient forest...")
        time.sleep(1)
        
        while not self.player_name.strip():
            try:
                self.player_name = input("What is your name, brave adventurer? ").strip()
                if not self.player_name:
                    print("Please enter a valid name.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                sys.exit(0)
        
        self.print_slow(f"Welcome, {self.player_name}! Your adventure begins...")
        time.sleep(1)
    
    def left_path(self):
        """Handle the left path scenario."""
        self.print_slow("You choose the left path and walk deeper into the forest...")
        time.sleep(1)
        self.print_slow("After a while, you come across a mysterious river.")
        self.print_slow("The water is crystal clear but you can't see the bottom.")
        
        choice = self.get_valid_input(
            "Do you want to 'swim' across or 'walk' around the river? ",
            ['swim', 'walk']
        )
        self.choices_made.append(f"Left path - {choice}")
        
        if choice == "swim":
            self.print_slow("You decide to swim across the river...")
            time.sleep(1)
            if random.random() < 0.7:  # 70% chance of being eaten
                self.print_slow("Suddenly, you feel something brush against your leg...")
                time.sleep(1)
                self.print_slow("🐊 An alligator emerges from the depths!")
                self.print_slow("You were eaten by an alligator. Game Over!")
                return False
            else:
                self.print_slow("You successfully swim across the river!")
                self.score += 10
                return self.continue_adventure()
        else:  # walk
            self.print_slow("You decide to walk around the river...")
            time.sleep(1)
            self.print_slow("The path is much longer than expected...")
            time.sleep(1)
            if random.random() < 0.6:  # 60% chance of running out of water
                self.print_slow("After hours of walking, you run out of water...")
                self.print_slow("You collapse from exhaustion. Game Over!")
                return False
            else:
                self.print_slow("You find a hidden spring and continue your journey!")
                self.score += 15
                return self.continue_adventure()
    
    def right_path(self):
        """Handle the right path scenario."""
        self.print_slow("You choose the right path and discover an old wooden bridge...")
        time.sleep(1)
        self.print_slow("The bridge looks ancient and somewhat unstable.")
        
        choice = self.get_valid_input(
            "Do you want to 'cross' the bridge or go 'back'? ",
            ['cross', 'back']
        )
        self.choices_made.append(f"Right path - {choice}")
        
        if choice == "back":
            self.print_slow("You decide to go back...")
            time.sleep(1)
            self.print_slow("But you realize you're lost and can't find your way back.")
            self.print_slow("You wander aimlessly until nightfall. Game Over!")
            return False
        else:  # cross
            self.print_slow("You carefully cross the bridge...")
            time.sleep(1)
            if random.random() < 0.3:  # 30% chance of bridge collapse
                self.print_slow("The bridge creaks ominously...")
                time.sleep(1)
                self.print_slow("💥 The bridge collapses! You fall into the river below.")
                self.print_slow("Game Over!")
                return False
            else:
                self.print_slow("You successfully cross the bridge!")
                self.score += 20
                return self.meet_stranger()
    
    def meet_stranger(self):
        """Handle the stranger encounter."""
        self.print_slow("On the other side, you meet a mysterious stranger...")
        time.sleep(1)
        self.print_slow("They look friendly but you can't be sure...")
        
        choice = self.get_valid_input(
            "Do you want to 'talk' to them or 'ignore' them? ",
            ['talk', 'ignore']
        )
        self.choices_made.append(f"Stranger - {choice}")
        
        if choice == "talk":
            self.print_slow("You decide to talk to the stranger...")
            time.sleep(1)
            if random.random() < 0.8:  # 80% chance of positive outcome
                self.print_slow("The stranger smiles warmly...")
                time.sleep(1)
                self.print_slow("🎁 They give you a magical amulet and a bag of gold!")
                self.print_slow("You WIN! The stranger was a benevolent wizard!")
                self.score += 100
                return True
            else:
                self.print_slow("The stranger seems friendly at first...")
                time.sleep(1)
                self.print_slow("But then they reveal themselves to be a trickster!")
                self.print_slow("They steal your belongings and disappear. Game Over!")
                return False
        else:  # ignore
            self.print_slow("You decide to ignore the stranger...")
            time.sleep(1)
            self.print_slow("The stranger looks offended and casts a spell...")
            time.sleep(1)
            self.print_slow("You are turned into a frog! Game Over!")
            return False
    
    def continue_adventure(self):
        """Continue the adventure after surviving the first challenge."""
        self.print_slow("You continue deeper into the forest...")
        time.sleep(1)
        self.print_slow("You discover an ancient temple!")
        
        choice = self.get_valid_input(
            "Do you want to 'enter' the temple or 'explore' around it? ",
            ['enter', 'explore']
        )
        self.choices_made.append(f"Temple - {choice}")
        
        if choice == "enter":
            self.print_slow("You enter the temple...")
            time.sleep(1)
            self.print_slow("🏆 You find a treasure chest filled with ancient artifacts!")
            self.print_slow("You WIN! You've discovered the temple's secrets!")
            self.score += 50
            return True
        else:  # explore
            self.print_slow("You explore around the temple...")
            time.sleep(1)
            self.print_slow("You find a hidden garden with magical flowers!")
            self.print_slow("You WIN! The garden grants you eternal wisdom!")
            self.score += 75
            return True
    
    def play(self):
        """Main game loop."""
        self.intro()
        
        self.print_slow("You come to a fork in the road...")
        self.print_slow("The left path leads into a dense forest.")
        self.print_slow("The right path leads toward a mysterious bridge.")
        
        choice = self.get_valid_input(
            "Which path do you choose? ('left' or 'right') ",
            ['left', 'right']
        )
        self.choices_made.append(f"Initial choice - {choice}")
        
        if choice == "left":
            won = self.left_path()
        else:  # right
            won = self.right_path()
        
        self.end_game(won)
    
    def end_game(self, won):
        """End the game and show results."""
        print("\n" + "="*50)
        if won:
            self.print_slow("🎉 Congratulations! You've completed your adventure!")
        else:
            self.print_slow("💀 Your adventure has ended...")
        
        self.print_slow(f"Final Score: {self.score}")
        self.print_slow(f"Choices made: {', '.join(self.choices_made)}")
        
        if won:
            self.print_slow("You are a true adventurer!")
        else:
            self.print_slow("Better luck next time!")
        
        self.print_slow(f"Thank you for playing, {self.player_name}!")
        print("="*50)


def main():
    """Main function to start the game."""
    try:
        game = AdventureGame()
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try running the game again.")


if __name__ == "__main__":
    main()
