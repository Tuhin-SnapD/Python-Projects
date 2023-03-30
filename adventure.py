"""
This code defines a text-based adventure game that prompts the player to make choices and responds to their input based on those choices. The 
game begins by asking the player for their name and welcoming them to the adventure. Then, the player is presented with a fork in the road and 
asked to choose which way to go. Depending on the choice they make, they will be presented with further options and the game will respond 
accordingly. If the player makes an invalid choice at any point, they lose the game. The game ends with a message thanking the player for playing.
"""

# Define the main game logic as a function
def play_adventure_game():
    # Prompt the player to enter their name
    name = input("Type your name: ")
    # Print a welcome message using the player's name
    print("Welcome, {} to this adventure!".format(name))

    # Prompt the player to choose between going left or right at a fork in the road
    answer = input(
        "You are on a dirt road, it has come to an end and you can go left or right. Which way would you like to go? ").lower()

    # If the player goes left
    if answer == "left":
        # Prompt the player to choose between walking around or swimming across a river
        answer = input(
            "You come to a river, you can walk around it or swim across? Type 'walk' to walk around and 'swim' to swim across: ").lower()

        # If the player chooses to swim
        if answer == "swim":
            print("You swam across and were eaten by an alligator. You lose.")
        # If the player chooses to walk
        elif answer == "walk":
            print(
                "You walked for many miles, ran out of water and you lost the game. You lose.")
        # If the player makes an invalid choice
        else:
            print("Not a valid option. You lose.")

    # If the player goes right
    elif answer == "right":
        # Prompt the player to choose between crossing a bridge or going back
        answer = input(
            "You come to a bridge, it looks wobbly, do you want to cross it or head back (cross/back)? ").lower()

        # If the player chooses to go back
        if answer == "back":
            print("You go back and lose. You lose.")
        # If the player chooses to cross the bridge
        elif answer == "cross":
            # Prompt the player to choose whether to talk to a stranger or not
            answer = input(
                "You cross the bridge and meet a stranger. Do you talk to them (yes/no)? ").lower()

            # If the player chooses to talk to the stranger
            if answer == "yes":
                print("You talk to the stranger and they give you gold. You WIN!")
            # If the player chooses not to talk to the stranger
            elif answer == "no":
                print(
                    "You ignore the stranger and they are offended and you lose. You lose.")
            # If the player makes an invalid choice
            else:
                print("Not a valid option. You lose.")

        # If the player makes an invalid choice
        else:
            print("Not a valid option. You lose.")

    # If the player makes an invalid choice
    else:
        print("Not a valid option. You lose.")

    # Print a message thanking the player for playing
    print("Thank you for playing, {}.".format(name))


# If this file is run as the main program
if __name__ == "__main__":
    # Call the play_adventure_game function to start the game
    play_adventure_game()
