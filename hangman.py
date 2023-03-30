""" 
This code is a simple implementation of the Hangman game, where the player tries to guess a secret word by suggesting letters within a limited 
number of chances.

The code randomly selects a word from a list of fruits and gives a hint about the word being a fruit. It then initializes a set to store the 
letters guessed by the player, sets the number of remaining chances to the length of the word plus two, and starts a loop until the player has 
used all of their chances or guessed the word correctly.

Inside the loop, the code prompts the player to input a letter to guess. It validates the input to ensure it is a single letter, adds the guessed 
letter to the set of guessed letters, and checks whether the letter is in the word or not. If the guessed letter is in the word, the code prints "
Correct!", otherwise it prints "Incorrect!" and decrements the remaining chances.

The code then prints the word with underscores in place of unguessed letters and the correct letters in place of the guessed letters. If the 
player has guessed all of the letters in the word, the code prints a message congratulating the player and exits the loop. If the player has used 
all of their chances and has not correctly guessed the word, the code prints a message informing the player that they lost and reveals the word.
 """
 
# Import the random module
import random

# List of fruits that can be used as secret words in the game
FRUITS = ['apple', 'banana', 'mango', 'strawberry', 'orange', 'grape', 'pineapple',
          'apricot', 'lemon', 'coconut', 'watermelon', 'cherry', 'papaya', 'berry',
          'peach', 'lychee', 'muskmelon']

def play_hangman():
    # Choose a random fruit from the list
    word = random.choice(FRUITS)
    # Create a set of letters in the word for efficient membership tests
    word_set = set(word)
    # Create a set for the letters guessed by the player
    guessed_set = set()
    # Calculate the number of remaining chances the player has
    remaining_chances = len(word) + 2

    # Print a message for the player
    print(
        f"Guess the word! HINT: word is a name of a fruit ({len(word)} letters).")

    # Loop until the player runs out of chances or correctly guesses the word
    while remaining_chances > 0:
        print()
        remaining_chances -= 1

        try:
            # Get a letter guess from the player
            guess = input("Enter a letter to guess: ").strip().lower()
        except KeyboardInterrupt:
            # Allow the player to exit the game with Ctrl-C
            print("\nBye! Try again.")
            return

        # Validate the player's guess
        if len(guess) != 1 or not guess.isalpha():
            print("Enter only a single letter!")
            continue

        if guess in guessed_set:
            print("You have already guessed that letter!")
            continue

        # Add the letter to the set of guessed letters
        guessed_set.add(guess)

        # Check if the guess is in the word
        if guess in word_set:
            print("Correct!")
        else:
            print("Incorrect!")
            if remaining_chances == 0:
                # The player has run out of chances and lost the game
                print(f"You lost! The word was {word}.")
                return

        # Print the current state of the word
        correct = 0
        for i, char in enumerate(word):
            if char in guessed_set:
                print(char, end=' ')
                correct += 1
            else:
                print('_', end=' ')

        if correct == len(word):
            # The player has correctly guessed all letters in the word
            print(f"\nThe word is: {word}")
            print("Congratulations, you won!")
            return

if __name__ == '__main__':
    play_hangman()