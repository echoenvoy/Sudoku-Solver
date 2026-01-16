"""
Sudoku Solver using Backtracking in Python
A complete implementation with all features in one file
"""

import time
import sys
from typing import List, Tuple, Optional

class SudokuSolver:
    """Main Sudoku solver class with all features"""
    
    def __init__(self, size: int = 9):
        """Initialize solver with board size (default 9x9)"""
        self.size = size
        self.subgrid_size = int(size ** 0.5)
        self.recursive_calls = 0
        self.start_time = 0
        self.step_by_step = False
        self.step_delay = 0.1  # Reduced delay
        self.timeout = 10  # 10 second timeout for tests
        self.time_limit_exceeded = False
        
    def print_board(self, board: List[List[int]]) -> None:
        """Print the Sudoku board with formatted 3x3 blocks"""
        print("\n" + "=" * 25)
        for i in range(self.size):
            if i % self.subgrid_size == 0 and i != 0:
                print("-" * 25)
            
            for j in range(self.size):
                if j % self.subgrid_size == 0 and j != 0:
                    print(" | ", end="")
                
                if board[i][j] == 0:
                    print(". ", end="")
                else:
                    if self.size > 9:
                        print(f"{board[i][j]:2d}", end=" ")
                    else:
                        print(f"{board[i][j]} ", end="")
            print()
        print("=" * 25)
    
    def find_best_empty(self, board: List[List[int]]) -> Optional[Tuple[int, int, List[int]]]:
        """
        Find the empty cell with minimum remaining values (MRV heuristic).
        Returns (row, col, possible_values) or None if board is solved.
        """
        best_cell = None
        min_options = self.size + 1
        
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    # Count possible values for this cell
                    possible = []
                    for num in range(1, self.size + 1):
                        if self.is_valid(board, i, j, num):
                            possible.append(num)
                    
                    # MRV: Choose cell with fewest possibilities
                    if len(possible) < min_options:
                        min_options = len(possible)
                        best_cell = (i, j, possible)
                        
                        # If we found a cell with only 1 possibility, return immediately
                        if min_options == 1:
                            return best_cell
        
        return best_cell
    
    def find_empty(self, board: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Find the next empty cell (0) in the board - simple version"""
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid"""
        # Check row
        for j in range(self.size):
            if board[row][j] == num and j != col:
                return False
        
        # Check column
        for i in range(self.size):
            if board[i][col] == num and i != row:
                return False
        
        # Check subgrid
        start_row = (row // self.subgrid_size) * self.subgrid_size
        start_col = (col // self.subgrid_size) * self.subgrid_size
        
        for i in range(start_row, start_row + self.subgrid_size):
            for j in range(start_col, start_col + self.subgrid_size):
                if board[i][j] == num and (i, j) != (row, col):
                    return False
        
        return True
    
    def validate_board(self, board: List[List[int]]) -> Tuple[bool, str]:
        """Validate the initial Sudoku board"""
        # Check size
        if len(board) != self.size or any(len(row) != self.size for row in board):
            return False, f"Board must be {self.size}x{self.size}"
        
        # Check values and detect conflicts
        for i in range(self.size):
            for j in range(self.size):
                num = board[i][j]
                if not 0 <= num <= self.size:
                    return False, f"Value {num} at ({i},{j}) is not between 0 and {self.size}"
                
                if num != 0:
                    # Temporarily set to 0 to check conflict
                    board[i][j] = 0
                    if not self.is_valid(board, i, j, num):
                        board[i][j] = num
                        return False, f"Conflict: {num} at ({i},{j}) violates Sudoku rules"
                    board[i][j] = num
        
        return True, "Valid board"
    
    def solve_with_mrv(self, board: List[List[int]]) -> bool:
        """Backtracking solver with Minimum Remaining Values heuristic"""
        if time.time() - self.start_time > self.timeout:
            self.time_limit_exceeded = True
            return False
            
        self.recursive_calls += 1
        
        # Find best empty cell using MRV heuristic
        best_cell = self.find_best_empty(board)
        if best_cell is None:
            return True  # Board is solved
        
        row, col, possible_values = best_cell
        
        # Try possible values in order
        for num in possible_values:
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                
                if self.step_by_step:
                    print(f"\nStep {self.recursive_calls}: Placing {num} at ({row},{col})")
                    self.print_board(board)
                    time.sleep(self.step_delay)
                
                if self.solve_with_mrv(board):
                    return True
                
                # Backtrack
                board[row][col] = 0
                
                if self.step_by_step:
                    print(f"\nBacktracking: Removing {num} from ({row},{col})")
                    self.print_board(board)
                    time.sleep(self.step_delay)
        
        return False
    
    def solve_simple(self, board: List[List[int]]) -> bool:
        """Simple backtracking solver (without MRV) for comparison"""
        if time.time() - self.start_time > self.timeout:
            self.time_limit_exceeded = True
            return False
            
        self.recursive_calls += 1
        
        empty = self.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        
        for num in range(1, self.size + 1):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                
                if self.solve_simple(board):
                    return True
                
                board[row][col] = 0
        
        return False
    
    def measure_performance(self, board: List[List[int]], use_mrv: bool = True) -> Tuple[bool, float, int]:
        """Solve board and measure performance"""
        self.recursive_calls = 0
        self.start_time = time.time()
        self.time_limit_exceeded = False
        
        # Create a copy to avoid modifying original
        board_copy = [row[:] for row in board]
        
        # Validate board first
        is_valid, message = self.validate_board(board_copy)
        if not is_valid:
            print(f"Invalid board: {message}")
            return False, 0, 0
        
        print(f"Solving using {'MRV heuristic' if use_mrv else 'simple backtracking'}...")
        
        if use_mrv:
            result = self.solve_with_mrv(board_copy)
        else:
            result = self.solve_simple(board_copy)
            
        end_time = time.time()
        
        if result:
            # Copy solution back to original board
            for i in range(self.size):
                for j in range(self.size):
                    board[i][j] = board_copy[i][j]
        
        return result, end_time - self.start_time, self.recursive_calls
    
    def input_board(self, method: str = "user") -> List[List[int]]:
        """Get Sudoku board from different input methods"""
        board = []
        
        if method == "hardcoded_easy":
            # Easy Sudoku
            board = [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ]
        
        elif method == "hardcoded_hard":
            # Hard but solvable Sudoku (not the impossible one)
            board = [
                [0, 0, 5, 3, 0, 0, 0, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 7, 0, 0, 1, 0, 5, 0, 0],
                [4, 0, 0, 0, 0, 5, 3, 0, 0],
                [0, 1, 0, 0, 7, 0, 0, 0, 6],
                [0, 0, 3, 2, 0, 0, 0, 8, 0],
                [0, 6, 0, 5, 0, 0, 0, 0, 9],
                [0, 0, 4, 0, 0, 0, 0, 3, 0],
                [0, 0, 0, 0, 0, 9, 7, 0, 0]
            ]
        
        elif method == "hardcoded_expert":
            # Expert level but solvable within timeout
            board = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 3, 0, 8, 5],
                [0, 0, 1, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 5, 0, 7, 0, 0, 0],
                [0, 0, 4, 0, 0, 0, 1, 0, 0],
                [0, 9, 0, 0, 0, 0, 0, 0, 0],
                [5, 0, 0, 0, 0, 0, 0, 7, 3],
                [0, 0, 2, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 9]
            ]
        
        elif method == "user":
            print(f"\nEnter your {self.size}x{self.size} Sudoku board.")
            print(f"Use 0 for empty cells, numbers 1-{self.size}, space or comma separated.")
            print(f"Example row for 9x9: '5 3 0 0 7 0 0 0 0'")
            
            for i in range(self.size):
                while True:
                    try:
                        row_input = input(f"Row {i+1}: ").strip()
                        if ',' in row_input:
                            row = [int(x.strip()) for x in row_input.split(',')]
                        else:
                            row = [int(x) for x in row_input.split()]
                        
                        if len(row) != self.size:
                            print(f"Error: Row must have {self.size} numbers")
                            continue
                        
                        if any(x < 0 or x > self.size for x in row):
                            print(f"Error: Numbers must be between 0 and {self.size}")
                            continue
                        
                        board.append(row)
                        break
                    except ValueError:
                        print("Error: Please enter valid numbers")
        
        elif method == "file":
            filename = input("Enter filename: ")
            try:
                with open(filename, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if ',' in line:
                                row = [int(x.strip()) for x in line.split(',')]
                            else:
                                row = [int(x) for x in line.split()]
                            board.append(row)
                
                if len(board) != self.size:
                    print(f"Error: File must have {self.size} rows")
                    return self.input_board(method)
                    
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found")
                return self.input_board(method)
            except ValueError:
                print("Error: File contains invalid data")
                return self.input_board(method)
        
        return board
    
    def export_solution(self, board: List[List[int]], filename: str = "sudoku_solution.txt") -> None:
        """Export solved board to a file"""
        with open(filename, 'w') as f:
            f.write(f"Sudoku Solution ({self.size}x{self.size})\n")
            f.write("=" * (self.size * 2 + 3) + "\n")
            
            for i in range(self.size):
                if i % self.subgrid_size == 0 and i != 0:
                    f.write("-" * (self.size * 2 + 3) + "\n")
                
                for j in range(self.size):
                    if j % self.subgrid_size == 0 and j != 0:
                        f.write(" | ")
                    
                    if board[i][j] == 0:
                        f.write(". ")
                    else:
                        if self.size > 9:
                            f.write(f"{board[i][j]:2d}")
                        else:
                            f.write(f"{board[i][j]} ")
                f.write("\n")
            
            f.write("=" * (self.size * 2 + 3) + "\n")
        print(f"Solution exported to {filename}")
    
    def compare_algorithms(self, board: List[List[int]]) -> None:
        """Compare MRV heuristic vs simple backtracking"""
        print("\n" + "="*50)
        print("ALGORITHM COMPARISON")
        print("="*50)
        
        # Test MRV heuristic
        board_copy1 = [row[:] for row in board]
        self.timeout = 30  # Increase timeout for comparison
        
        print("\n1. Solving with MRV heuristic (optimized)...")
        result1, time1, calls1 = self.measure_performance(board_copy1, use_mrv=True)
        
        if self.time_limit_exceeded:
            print("   ⏰ Timeout! Exceeded 30 seconds")
        elif result1:
            print(f"   ✓ Solved in {time1:.4f} seconds")
            print(f"   Recursive calls: {calls1:,}")
        else:
            print("   ✗ No solution found")
        
        # Test simple backtracking
        board_copy2 = [row[:] for row in board]
        self.time_limit_exceeded = False
        
        print("\n2. Solving with simple backtracking...")
        result2, time2, calls2 = self.measure_performance(board_copy2, use_mrv=False)
        
        if self.time_limit_exceeded:
            print("   ⏰ Timeout! Exceeded 30 seconds")
        elif result2:
            print(f"   ✓ Solved in {time2:.4f} seconds")
            print(f"   Recursive calls: {calls2:,}")
        else:
            print("   ✗ No solution found")
        
        # Comparison
        if not self.time_limit_exceeded and result1 and result2:
            print("\n" + "-"*50)
            print("COMPARISON RESULTS:")
            print("-"*50)
            speedup = time2 / time1 if time1 > 0 else float('inf')
            calls_reduction = calls2 / calls1 if calls1 > 0 else float('inf')
            
            print(f"MRV is {speedup:.1f}x faster")
            print(f"MRV uses {calls_reduction:.1f}x fewer recursive calls")
        
        self.timeout = 10  # Reset to default
    
    def run_test_cases(self) -> None:
        """Run predefined test cases"""
        print("\n" + "="*50)
        print("RUNNING TEST CASES")
        print("="*50)
        
        test_cases = [
            ("Easy Sudoku", [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ]),
            ("Hard Sudoku", [
                [0, 0, 5, 3, 0, 0, 0, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 7, 0, 0, 1, 0, 5, 0, 0],
                [4, 0, 0, 0, 0, 5, 3, 0, 0],
                [0, 1, 0, 0, 7, 0, 0, 0, 6],
                [0, 0, 3, 2, 0, 0, 0, 8, 0],
                [0, 6, 0, 5, 0, 0, 0, 0, 9],
                [0, 0, 4, 0, 0, 0, 0, 3, 0],
                [0, 0, 0, 0, 0, 9, 7, 0, 0]
            ]),
            ("Already Solved", [
                [5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 4, 5, 2, 8, 6, 1, 7, 9]
            ]),
            ("Impossible (Conflict)", [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 5]  # Conflict: two 5's in last column
            ]),
            ("4x4 Sudoku", [
                [1, 0, 0, 0],
                [0, 0, 3, 0],
                [0, 2, 0, 0],
                [0, 0, 0, 4]
            ], 4)
        ]
        
        for test_name, *test_data in test_cases:
            print(f"\n{'='*40}")
            print(f"Test: {test_name}")
            print('='*40)
            
            if len(test_data) == 2:
                board, size = test_data
                solver = SudokuSolver(size)
            else:
                board = test_data[0]
                solver = SudokuSolver(9)
            
            print("\nInitial Board:")
            solver.print_board(board)
            
            result, solve_time, calls = solver.measure_performance(board)
            
            if solver.time_limit_exceeded:
                print(f"\n⏰ Timeout! Test exceeded {solver.timeout} seconds")
                print("This puzzle is too difficult for basic backtracking.")
                print("Try using the algorithm comparison feature instead.")
            elif result:
                print("\n✓ Solution found!")
                solver.print_board(board)
                print(f"\nPerformance:")
                print(f"  Time: {solve_time:.4f} seconds")
                print(f"  Recursive calls: {calls:,}")
            else:
                print("\n✗ No solution exists for this board")
                print(f"Time spent: {solve_time:.4f} seconds")
                print(f"Recursive calls: {calls:,}")

def main():
    """Main program loop"""
    print("\n" + "="*60)
    print("SUDOKU SOLVER using Backtracking Algorithm")
    print("="*60)
    print("Features: MRV heuristic, timeout handling, performance tracking")
    
    # Configure solver
    print("\nSelect Sudoku size:")
    print("1. Standard 9x9")
    print("2. 4x4 (for testing)")
    print("3. 16x16 (Hexadoku - advanced)")
    
    size_choice = input("Enter choice (1-3, default 1): ").strip()
    if size_choice == '2':
        size = 4
    elif size_choice == '3':
        size = 16
    else:
        size = 9
    
    solver = SudokuSolver(size)
    
    # Main program loop
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Solve a new Sudoku")
        print("2. Run test cases")
        print("3. Compare algorithms (MRV vs Simple)")
        print("4. Toggle step-by-step mode (currently: " + 
              ("ON" if solver.step_by_step else "OFF") + ")")
        print("5. Set timeout (currently: " + 
              f"{solver.timeout} seconds)")
        print("6. Export last solution to file")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\nChoose input method:")
            print("1. Easy example")
            print("2. Hard example")
            print("3. Expert example (timeout risk)")
            print("4. Manual input")
            print("5. Load from file")
            
            input_choice = input("Enter choice (1-5): ").strip()
            
            if input_choice == '1':
                board = solver.input_board("hardcoded_easy")
            elif input_choice == '2':
                board = solver.input_board("hardcoded_hard")
            elif input_choice == '3':
                board = solver.input_board("hardcoded_expert")
                print("\n⚠️ Warning: This is a very difficult puzzle.")
                print("It may timeout with simple backtracking.")
                print("Try the algorithm comparison feature!")
            elif input_choice == '4':
                board = solver.input_board("user")
            elif input_choice == '5':
                board = solver.input_board("file")
            else:
                print("Invalid choice, using easy example")
                board = solver.input_board("hardcoded_easy")
            
            if not board:
                continue
            
            print("\nYour Sudoku board:")
            solver.print_board(board)
            
            # Choose solving method
            print("\nChoose solving method:")
            print("1. MRV heuristic (recommended)")
            print("2. Simple backtracking")
            method_choice = input("Enter choice (1-2): ").strip()
            use_mrv = method_choice != '2'
            
            # Solve the board
            result, solve_time, calls = solver.measure_performance(board, use_mrv=use_mrv)
            
            if solver.time_limit_exceeded:
                print(f"\n⏰ Timeout! Exceeded {solver.timeout} seconds")
                print("This puzzle is too difficult for the current method.")
                print("Try using MRV heuristic or a simpler puzzle.")
            elif result:
                print("\n✓ Solution found!")
                solver.print_board(board)
                print(f"\nPerformance:")
                print(f"  Time: {solve_time:.4f} seconds")
                print(f"  Recursive calls: {calls:,}")
                
                # Ask to export
                export = input("\nExport solution to file? (y/n): ").lower()
                if export == 'y':
                    filename = input("Enter filename (default: sudoku_solution.txt): ")
                    if not filename:
                        filename = "sudoku_solution.txt"
                    solver.export_solution(board, filename)
            else:
                print("\n✗ No solution exists for this Sudoku!")
                print(f"Time spent: {solve_time:.4f} seconds")
                print(f"Recursive calls: {calls:,}")
        
        elif choice == '2':
            solver.run_test_cases()
        
        elif choice == '3':
            print("\nChoose a puzzle to compare algorithms:")
            print("1. Easy puzzle")
            print("2. Hard puzzle")
            print("3. Enter custom puzzle")
            
            comp_choice = input("Enter choice (1-3): ").strip()
            
            if comp_choice == '1':
                board = solver.input_board("hardcoded_easy")
            elif comp_choice == '2':
                board = solver.input_board("hardcoded_hard")
            elif comp_choice == '3':
                board = solver.input_board("user")
            else:
                board = solver.input_board("hardcoded_easy")
            
            if board:
                print("\nInitial board:")
                solver.print_board(board)
                solver.compare_algorithms(board)
        
        elif choice == '4':
            solver.step_by_step = not solver.step_by_step
            print(f"Step-by-step mode is now {'ON' if solver.step_by_step else 'OFF'}")
            if solver.step_by_step:
                print("Note: This will significantly slow down solving")
        
        elif choice == '5':
            try:
                timeout = float(input("Enter timeout in seconds (e.g., 30): "))
                if timeout <= 0:
                    print("Timeout must be positive")
                else:
                    solver.timeout = timeout
                    print(f"Timeout set to {timeout} seconds")
            except ValueError:
                print("Invalid input")
        
        elif choice == '6':
            print("This feature requires a solved board. Please solve a Sudoku first.")
        
        elif choice == '7':
            print("\nThank you for using Sudoku Solver!")
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()