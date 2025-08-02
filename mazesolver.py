"""
Enhanced Maze Solver

A comprehensive maze solving application with multiple algorithms,
visualization, and interactive features.
"""

import time
import random
from typing import List, Tuple, Optional, Set
from enum import Enum


class Algorithm(Enum):
    """Available maze solving algorithms."""
    DFS = "Depth-First Search"
    BFS = "Breadth-First Search"
    A_STAR = "A* Search"
    DIJKSTRA = "Dijkstra's Algorithm"


class MazeSolver:
    """Enhanced maze solver with multiple algorithms and visualization."""
    
    def __init__(self, maze: Optional[List[List[int]]] = None, size: int = 10):
        self.size = size
        self.maze = maze if maze else self.generate_maze(size)
        self.solution = [[0] * size for _ in range(size)]
        self.visited = set()
        self.path = []
        self.start = (0, 0)
        self.end = (size - 1, size - 1)
        
    def generate_maze(self, size: int) -> List[List[int]]:
        """Generate a simple maze with guaranteed path from start to end."""
        # Initialize maze with walls
        maze = [[1 for _ in range(size)] for _ in range(size)]
        
        # Create a simple maze with a guaranteed path
        # Use a simple approach: create a path from start to end
        
        # Start with start and end positions
        maze[0][0] = 0
        maze[size-1][size-1] = 0
        
        # Create a simple path: go down, then right, then down, etc.
        x, y = 0, 0
        while (x, y) != (size-1, size-1):
            # Try to move down first
            if x + 1 < size and maze[x + 1][y] == 1:
                x += 1
                maze[x][y] = 0
            # Then try to move right
            elif y + 1 < size and maze[x][y + 1] == 1:
                y += 1
                maze[x][y] = 0
            # If we can't move down or right, we're at the end
            else:
                break
        
        # Add some random paths to make it more interesting
        for _ in range(size * 3):
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            if maze[x][y] == 1:  # Only add paths in wall spaces
                # Check if this creates a reasonable maze
                if random.random() < 0.4:  # 40% chance
                    maze[x][y] = 0
        
        return maze
    
    def is_valid(self, x: int, y: int) -> bool:
        """Check if a position is valid within the maze."""
        return (0 <= x < self.size and 0 <= y < self.size and 
                self.maze[x][y] == 0)
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighboring cells."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self.is_valid(new_x, new_y):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    def manhattan_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate Manhattan distance between two points."""
        return abs(x1 - x2) + abs(y1 - y2)
    
    def solve_dfs(self) -> bool:
        """Solve maze using Depth-First Search."""
        self.visited.clear()
        self.path.clear()
        
        def dfs(x: int, y: int) -> bool:
            if (x, y) == self.end:
                self.path.append((x, y))
                return True
            
            if (x, y) in self.visited:
                return False
            
            self.visited.add((x, y))
            self.solution[x][y] = 1
            
            # Try all neighbors
            for nx, ny in self.get_neighbors(x, y):
                if dfs(nx, ny):
                    self.path.append((x, y))
                    return True
            
            self.solution[x][y] = 0
            return False
        
        return dfs(self.start[0], self.start[1])
    
    def solve_bfs(self) -> bool:
        """Solve maze using Breadth-First Search."""
        self.visited.clear()
        self.path.clear()
        
        queue = [(self.start[0], self.start[1], [self.start])]
        self.visited.add(self.start)
        
        while queue:
            x, y, path = queue.pop(0)
            
            if (x, y) == self.end:
                self.path = path
                # Mark solution path
                for px, py in path:
                    self.solution[px][py] = 1
                return True
            
            for nx, ny in self.get_neighbors(x, y):
                if (nx, ny) not in self.visited:
                    self.visited.add((nx, ny))
                    queue.append((nx, ny, path + [(nx, ny)]))
        
        return False
    
    def solve_a_star(self) -> bool:
        """Solve maze using A* algorithm."""
        self.visited.clear()
        self.path.clear()
        
        # Priority queue: (f_score, current_pos, path)
        open_set = [(0, self.start, [self.start])]
        closed_set = set()
        
        while open_set:
            open_set.sort(key=lambda x: x[0])  # Sort by f_score
            f_score, (x, y), path = open_set.pop(0)
            
            if (x, y) == self.end:
                self.path = path
                # Mark solution path
                for px, py in path:
                    self.solution[px][py] = 1
                return True
            
            if (x, y) in closed_set:
                continue
            
            closed_set.add((x, y))
            
            for nx, ny in self.get_neighbors(x, y):
                if (nx, ny) not in closed_set:
                    new_path = path + [(nx, ny)]
                    g_score = len(new_path) - 1  # Cost from start to current
                    h_score = self.manhattan_distance(nx, ny, self.end[0], self.end[1])
                    f_score = g_score + h_score
                    
                    open_set.append((f_score, (nx, ny), new_path))
        
        return False
    
    def solve_dijkstra(self) -> bool:
        """Solve maze using Dijkstra's algorithm."""
        self.visited.clear()
        self.path.clear()
        
        # Priority queue: (distance, current_pos, path)
        open_set = [(0, self.start, [self.start])]
        distances = {self.start: 0}
        
        while open_set:
            open_set.sort(key=lambda x: x[0])  # Sort by distance
            dist, (x, y), path = open_set.pop(0)
            
            if (x, y) == self.end:
                self.path = path
                # Mark solution path
                for px, py in path:
                    self.solution[px][py] = 1
                return True
            
            if (x, y) in self.visited:
                continue
            
            self.visited.add((x, y))
            
            for nx, ny in self.get_neighbors(x, y):
                if (nx, ny) not in self.visited:
                    new_dist = dist + 1
                    if (nx, ny) not in distances or new_dist < distances[(nx, ny)]:
                        distances[(nx, ny)] = new_dist
                        new_path = path + [(nx, ny)]
                        open_set.append((new_dist, (nx, ny), new_path))
        
        return False
    
    def solve(self, algorithm: Algorithm) -> bool:
        """Solve the maze using the specified algorithm."""
        print(f"\n🔍 Solving maze using {algorithm.value}...")
        start_time = time.time()
        
        # Reset solution
        self.solution = [[0] * self.size for _ in range(self.size)]
        
        # Solve based on algorithm
        if algorithm == Algorithm.DFS:
            result = self.solve_dfs()
        elif algorithm == Algorithm.BFS:
            result = self.solve_bfs()
        elif algorithm == Algorithm.A_STAR:
            result = self.solve_a_star()
        elif algorithm == Algorithm.DIJKSTRA:
            result = self.solve_dijkstra()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        end_time = time.time()
        solve_time = end_time - start_time
        
        if result:
            print(f"✅ Solution found in {solve_time:.4f} seconds!")
            print(f"Path length: {len(self.path)} steps")
            print(f"Cells explored: {len(self.visited)}")
        else:
            print(f"❌ No solution found in {solve_time:.4f} seconds!")
        
        return result
    
    def display_maze(self, show_solution: bool = True, show_visited: bool = False):
        """Display the maze with optional solution and visited cells."""
        print(f"\n🗺️  Maze ({self.size}x{self.size}):")
        print("=" * (self.size * 2 + 3))
        
        for i in range(self.size):
            print("│", end=" ")
            for j in range(self.size):
                if (i, j) == self.start:
                    print("🚀", end=" ")  # Start
                elif (i, j) == self.end:
                    print("🎯", end=" ")  # End
                elif show_solution and self.solution[i][j] == 1:
                    print("🟢", end=" ")  # Solution path
                elif show_visited and (i, j) in self.visited:
                    print("🟡", end=" ")  # Visited cells
                elif self.maze[i][j] == 1:
                    print("⬛", end=" ")  # Wall
                else:
                    print("⬜", end=" ")  # Empty space
            print("│")
        
        print("=" * (self.size * 2 + 3))
        print("Legend: 🚀 Start | 🎯 End | 🟢 Solution | 🟡 Visited | ⬛ Wall | ⬜ Empty")
    
    def compare_algorithms(self):
        """Compare all algorithms and display results."""
        print("\n🏁 ALGORITHM COMPARISON")
        print("=" * 50)
        
        results = {}
        
        for algorithm in Algorithm:
            print(f"\nTesting {algorithm.value}...")
            
            # Reset for fair comparison
            self.visited.clear()
            self.path.clear()
            self.solution = [[0] * self.size for _ in range(self.size)]
            
            start_time = time.time()
            success = self.solve(algorithm)
            end_time = time.time()
            
            if success:
                results[algorithm] = {
                    'time': end_time - start_time,
                    'path_length': len(self.path),
                    'cells_explored': len(self.visited)
                }
            else:
                results[algorithm] = {
                    'time': end_time - start_time,
                    'path_length': 0,
                    'cells_explored': len(self.visited)
                }
        
        # Display comparison table
        print(f"\n📊 COMPARISON RESULTS:")
        print("-" * 80)
        print(f"{'Algorithm':<20} {'Time (s)':<12} {'Path Length':<12} {'Cells Explored':<15}")
        print("-" * 80)
        
        for algorithm, result in results.items():
            print(f"{algorithm.value:<20} {result['time']:<12.4f} {result['path_length']:<12} {result['cells_explored']:<15}")
        
        # Find best algorithm
        if results:
            best_time = min(results.keys(), key=lambda k: results[k]['time'])
            best_path = min(results.keys(), key=lambda k: results[k]['path_length'] if results[k]['path_length'] > 0 else float('inf'))
            
            print(f"\n🏆 Best performance:")
            print(f"   Fastest: {best_time.value} ({results[best_time]['time']:.4f}s)")
            print(f"   Shortest path: {best_path.value} ({results[best_path]['path_length']} steps)")


def main():
    """Main function to demonstrate the maze solver."""
    print("🧩 ENHANCED MAZE SOLVER")
    print("=" * 30)
    
    try:
        # Get maze size from user
        while True:
            try:
                size = int(input("Enter maze size (5-20): "))
                if 5 <= size <= 20:
                    break
                else:
                    print("Please enter a size between 5 and 20.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Create maze solver
        solver = MazeSolver(size=size)
        
        # Display original maze
        solver.display_maze(show_solution=False, show_visited=False)
        
        # Menu for user interaction
        while True:
            print(f"\n📋 OPTIONS:")
            print("1. Solve with DFS")
            print("2. Solve with BFS")
            print("3. Solve with A*")
            print("4. Solve with Dijkstra")
            print("5. Compare all algorithms")
            print("6. Generate new maze")
            print("7. Show maze with visited cells")
            print("8. Exit")
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                solver.solve(Algorithm.DFS)
                solver.display_maze(show_solution=True, show_visited=False)
            elif choice == '2':
                solver.solve(Algorithm.BFS)
                solver.display_maze(show_solution=True, show_visited=False)
            elif choice == '3':
                solver.solve(Algorithm.A_STAR)
                solver.display_maze(show_solution=True, show_visited=False)
            elif choice == '4':
                solver.solve(Algorithm.DIJKSTRA)
                solver.display_maze(show_solution=True, show_visited=False)
            elif choice == '5':
                solver.compare_algorithms()
            elif choice == '6':
                solver = MazeSolver(size=size)
                solver.display_maze(show_solution=False, show_visited=False)
            elif choice == '7':
                if solver.path:
                    solver.display_maze(show_solution=True, show_visited=True)
                else:
                    print("❌ No solution found yet. Solve the maze first!")
            elif choice == '8':
                print("👋 Thanks for using the Maze Solver!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 8.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Maze Solver interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()