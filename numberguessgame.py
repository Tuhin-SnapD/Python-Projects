"""
This code implements a simple number guessing game where the user tries to guess a random number within a specified range. The code repeatedly 
generates a new random number and prompts the user to guess it. After each guess, the code tells the user if their guess was too high or too low, 
and prompts them to guess again. Once the user correctly guesses the random number, the code prints a congratulatory message with the number of  
guesses the user made. The user can then choose to play again or exit the program.
"""

# Import the random module
import random

while True:
    # Get the range of the random number
    top_of_range = input("What is the range: ")

    try:
        top_of_range = int(top_of_range)

        if top_of_range <= 0:
            print('Please type a number larger than 0 next time.')
            continue
    except ValueError:
        print('Please type a number next time.')
        continue

    # Generate a random number within the range
    random_number = random.randint(0, top_of_range)
    guesses = 0

    # Start the guessing game
    while True:
        guesses += 1
        user_guess = input("Make a guess: ")

        try:
            user_guess = int(user_guess)
        except ValueError:
            print('Please type a number next time.')
            continue

        if user_guess == random_number:
            print("You got it in", guesses, "guesses!")
            break
        elif user_guess > random_number:
            print("You were above the number!")
        else:
            print("You were below the number!")

    # Ask the user if they want to play again
    play_again = input("Do you want to play again? (y/n) ")

    if play_again.lower() != 'y':
        break