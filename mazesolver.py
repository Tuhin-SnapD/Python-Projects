""" 
This code solves a maze problem using a recursive backtracking algorithm. The maze is defined as a 2D array of 0s and 1s, where 0s represent open paths and 1s represent walls. The goal is to find a path from the top-left 
corner of the maze to the bottom-right corner.

The algorithm works as follows:

Starting from the top-left corner of the maze, the function explore_maze() recursively explores the adjacent cells to find a path to the 
bottom-right corner.

If a cell is found to be part of the solution path, it is marked as such in the solution array. If no solution is found from the current cell, it is marked as not part of the solution path and the algorithm backtracks to the previous cell to 
try another path.

If a solution is found, the solution array is printed to show the path taken.The code includes comments to make it easier to understand the various parts of the algorithm.
"""

SIZE = 5

# Define the maze as a 2D array
maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [1, 0, 0, 1, 0]
]

# Create a solution array to keep track of the path
solution = [[0]*SIZE for i in range(SIZE)]

# Define the recursive function to explore the maze
def explore_maze(row, col):
    # Check if the current cell is the end of the maze
    if (row == SIZE-1) and (col == SIZE-1):
        solution[row][col] = 1;
        return True;
    # Check if the current cell is within the bounds of the maze and has not been visited before
    if row >= 0 and col >= 0 and row < SIZE and col < SIZE and solution[row][col] == 0 and maze[row][col] == 0:
        # Mark the current cell as part of the solution
        solution[row][col] = 1
        # Print the current cell being explored
        print(f"Exploring cell ({row}, {col})")
        # Recursively explore the adjacent cells
        if explore_maze(row+1, col) or explore_maze(row, col+1) or explore_maze(row-1, col) or explore_maze(row, col-1):
            return True
        # If no solution is found, mark the current cell as not part of the solution
        solution[row][col] = 0;
        return False;
    return 0;

# Call the explore_maze function starting from the top-left cell
if explore_maze(0,0):
    # If a solution is found, print the solution array
    for i in solution:
        print (i)
else:
    # If no solution is found, print an error message
    print ("No solution")