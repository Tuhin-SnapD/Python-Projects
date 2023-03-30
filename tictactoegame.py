# This code is a Python implementation of a simple Tic Tac Toe game that can be played between a human player and the computer.

# The code defines several functions, such as drawBoard, which prints the current state of the Tic Tac Toe board, and inputPlayerLetter, which asks the player which letter they want to use (either X or O).

# The game flow is managed by the main function, which initializes the board, decides which player goes first, and repeatedly asks the player for their move and makes a computer move until the game is over.

# The code also defines various helper functions such as makeMove, isWinner, getBoardCopy, and chooseRandomMoveFromList to check for valid moves, check for a win, and choose random moves for the computer player.

# Finally, the playAgain function is used to ask the player if they want to play another game.

# Import the random module
import random

# Define a function to draw the board
def drawBoard(board):
    # Print the board using a string representation of the board list
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('-----------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-----------')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])

# Define a function to ask the player which letter they want to be
def inputPlayerLetter():
    letter = ''
    # Loop until the player enters either 'X' or 'O'
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()
    # Return a list containing the player's letter and the computer's letter
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

# Define a function to randomly determine who goes first
def whoGoesFirst():
    # Generate a random number between 0 and 1
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

# Define a function to ask the player if they want to play again
def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# Define a function to make a move on the board
def makeMove(board, letter, move):
    board[move] = letter

# Define a function to check if a player has won
def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or 
            (bo[4] == le and bo[5] == le and bo[6] == le) or 
            (bo[1] == le and bo[2] == le and bo[3] == le) or 
            (bo[7] == le and bo[4] == le and bo[1] == le) or 
            (bo[8] == le and bo[5] == le and bo[2] == le) or 
            (bo[9] == le and bo[6] == le and bo[3] == le) or 
            (bo[7] == le and bo[5] == le and bo[3] == le) or 
            (bo[9] == le and bo[5] == le and bo[1] == le))

# Define a function to make a copy of the board
def getBoardCopy(board):
    dupeBoard = []
    for i in board:
        dupeBoard.append(i)
    return dupeBoard

# Define a function to check if a space on the board is free
def isSpaceFree(board, move):
    return board[move] == ' '

# Function to get the player's move
def getPlayerMove(board):
    # Initialize the move variable to an empty string
    move = ' '
    
    # Keep asking for input until the user enters a valid move
    # (a number between 1 and 9) that corresponds to an empty space on the board
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    
    # Return the player's move as an integer
    return int(move)


# Function to choose a random move from a list of possible moves
def chooseRandomMoveFromList(board, movesList):
    # Initialize an empty list to hold the possible moves
    possibleMoves = []
    
    # Check each move in the list of possible moves
    for i in movesList:
        # If the space on the board corresponding to the move is empty,
        # add the move to the list of possible moves
        if isSpaceFree(board, i):
            possibleMoves.append(i)
    
    # If there are possible moves, choose one at random and return it
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    # If there are no possible moves, return None
    else:
        return None

# Function to get the computer's move
def getComputerMove(board, computerLetter):
	if computerLetter == 'X':
		playerLetter = 'O'
	else:
		playerLetter = 'X'
	
	# Check if there's a winning move for the computer
	for i in range(1, 10):
		copy = getBoardCopy(board)
		if isSpaceFree(copy, i):
			makeMove(copy, computerLetter, i)
			if isWinner(copy, computerLetter):
				return i
	
	# Check if there's a winning move for the player
	for i in range(1, 10):
		copy = getBoardCopy(board)
		if isSpaceFree(copy, i):
			makeMove(copy, playerLetter, i)
			if isWinner(copy, playerLetter):
				return i
	
	# Try to take one of the corners
	move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
	if move != None:
		return move
	
	# Try to take the center
	if isSpaceFree(board, 5):
		return 5
	
	# Choose a random move from the sides
	return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False

    return True

# Display welcome message
print('Welcome to Tic Tac Toe!')

# Loop to keep playing until user decides to quit
while True:
    # Create a new empty board and let the player choose their letter (X or O)
    theBoard = [' '] * 10
    playerLetter, computerLetter = inputPlayerLetter()
    
    # Decide who goes first (player or computer)
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    
    # Start the game loop
    gameIsPlaying = True
    while gameIsPlaying:
        # If it's the player's turn, draw the board, get their move and make the move
        if turn == 'player':
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            
            # Check if the player has won
            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            # If the board is full, it's a tie
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                # If the game is not over, it's the computer's turn
                else:
                    turn = 'computer'
        # If it's the computer's turn, get its move and make the move
        else:
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)
            
            # Check if the computer has won
            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you! You lose.')
                gameIsPlaying = False
            # If the board is full, it's a tie
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                # If the game is not over, it's the player's turn
                else:
                    turn = 'player'
    
    # Ask the player if they want to play again, and if not, exit the loop and end the game
    if not playAgain():
        break