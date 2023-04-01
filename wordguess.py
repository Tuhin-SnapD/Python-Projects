""" 
This code implements a simple word guessing game called "Lingo". Here's how the game works:

The computer chooses a random 4-letter word with no repeated letters from a file called words.txt.The player tries to guess the word by typing a 
4-letter word with no repeated letters. The computer tells the player which letters in their guess are correct and in the correct position by 
putting those letters in square brackets ([ ]).

The computer tells the player which letters in their guess are correct but in the wrong position by putting those letters in parentheses (( )).The 
player keeps guessing until they guess the word correctly or they type "revl" to reveal the word and keep playing.

The code defines two functions:

return_word(): This function reads the words.txt file, filters it to include only 4-letter words with no repeated letters, and returns a randomly 
chosen word from the filtered list.

play_game(): This function uses the return_word() function to choose a random word to guess, then asks the player to guess the word and gives 
feedback on their guess until they guess the word correctly or type "revl" to reveal the word. The function uses a list called new to keep track 
of the guessed letters and their formatting, and a set called guesslst to keep track of the guessed letters for comparison with the letters in the 
word. 
"""

# Import random module
import random

def return_word():
    # Open the file with a context manager to ensure it gets closed when we're done
    with open(r"C:\Users\Tuhin\Documents\Internship\Python\doc\words.txt", 'r') as f:
        # Read the file and split it into lines
        data = f.read().split('\n')
    # Filter the list to include only 4-letter words with no repeated letters
    Data = [word for word in data if len(word) == 4 and len(set(word)) == 4]
    # Choose a random word from the filtered list
    return random.choice(Data)

def play_game():
    # Get a random word to guess
    word = return_word()
    # Initialize the set of guessed letters
    guesslst = set()
    # Keep playing until the player guesses all the letters in the word
    while guesslst != set(word):
        # Initialize the list of characters to display (with placeholders for unguessed letters)
        new = []
        # Ask the player to guess a word
        guess = input("Guess the word: ")
        # If the player types "revl", reveal the word and continue playing
        if guess == 'revl':
            print(word)
            continue
        # Convert the guess to a set of unique letters
        guesslst = set(guess)
        # Iterate over the guessed letters and their indices
        for i, x in enumerate(guesslst):
            # If the guessed letter is in the word, iterate over the letters in the word and their indices
            if x in word:
                for j, y in enumerate(word):
                    # If the guessed letter matches a letter in the word, add it to the display list with appropriate formatting
                    if x == y:
                        if i == j:
                            new.append(f"[{x}]")
                        else:
                            new.append(f"({x})")
            # If the guessed letter is not in the word, add it to the display list as is
            else:
                new.append(x)
        # Print the updated display list
        print("".join(new))

# Start the game
play_game()