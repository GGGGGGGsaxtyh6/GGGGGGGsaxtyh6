#!/usr/bin/env python3

import json
import itertools

def solve_line(line_length, clues):
    """Solve a single line of a nonogram given clues"""
    if not clues:
        return [0] * line_length
    
    # Generate all possible arrangements
    total_filled = sum(clues)
    total_gaps = line_length - total_filled
    num_gaps = len(clues) + 1  # gaps before, between, and after
    
    if total_gaps < num_gaps - 1:
        return None  # Impossible
    
    # Distribute gaps
    min_gaps = [0] + [1] * (len(clues) - 1) + [0]  # minimum gaps needed
    extra_gaps = total_gaps - sum(min_gaps)
    
    solutions = []
    
    # Try all possible gap distributions
    for gap_dist in itertools.combinations_with_replacement(range(extra_gaps + 1), num_gaps):
        if sum(gap_dist) != extra_gaps:
            continue
            
        gaps = [min_gaps[i] + gap_dist[i] for i in range(num_gaps)]
        
        # Build the line
        line = []
        for i, clue in enumerate(clues):
            line.extend([0] * gaps[i])  # empty cells
            line.extend([1] * clue)     # filled cells
        line.extend([0] * gaps[-1])     # final empty cells
        
        if len(line) == line_length:
            solutions.append(line)
    
    return solutions

def solve_nonogram(height, width, row_clues, col_clues):
    """Solve the nonogram puzzle"""
    print(f"Solving nonogram {height}x{width}")
    
    # Initialize grid with unknown cells (-1)
    grid = [[-1 for _ in range(width)] for _ in range(height)]
    
    # Solve rows first
    print("Solving rows...")
    for r in range(height):
        if row_clues[r]:
            solutions = solve_line(width, row_clues[r])
            if solutions:
                if len(solutions) == 1:
                    # Unique solution
                    for c in range(width):
                        grid[r][c] = solutions[0][c]
                else:
                    # Multiple solutions - find common cells
                    for c in range(width):
                        if all(sol[c] == solutions[0][c] for sol in solutions):
                            grid[r][c] = solutions[0][c]
    
    # Solve columns
    print("Solving columns...")
    for c in range(width):
        if col_clues[c]:
            # Extract current column
            col = [grid[r][c] for r in range(height)]
            
            solutions = solve_line(height, col_clues[c])
            if solutions:
                if len(solutions) == 1:
                    # Unique solution
                    for r in range(height):
                        grid[r][c] = solutions[0][r]
                else:
                    # Multiple solutions - find common cells
                    for r in range(height):
                        if all(sol[r] == solutions[0][r] for sol in solutions):
                            grid[r][c] = solutions[0][r]
    
    return grid

def visualize_grid(grid):
    """Visualize the solved grid"""
    height = len(grid)
    width = len(grid[0])
    
    print("\nSolved nonogram:")
    print("=" * (width + 2))
    
    for r in range(height):
        line = ""
        for c in range(width):
            if grid[r][c] == 1:
                line += "█"
            elif grid[r][c] == 0:
                line += " "
            else:
                line += "?"  # Unknown
        print(f"|{line}|")
    print("=" * (width + 2))

def extract_text_from_grid(grid):
    """Try to extract text from the solved grid"""
    print("\nExtracting text from solution...")
    
    # Find rows with content
    text_rows = []
    for r, row in enumerate(grid):
        if any(cell == 1 for cell in row):
            line = ""
            for cell in row:
                if cell == 1:
                    line += "█"
                else:
                    line += " "
            text_rows.append((r, line))
    
    print(f"Found {len(text_rows)} rows with content:")
    for r, line in text_rows:
        print(f"Row {r:2d}: {line}")

def main():
    # The actual puzzle data from the web interface
    height = 30
    width = 200
    
    # Row clues (only non-empty ones)
    row_clues = [[] for _ in range(height)]
    row_clues[11] = [4, 1, 1, 2, 4, 1, 3, 4, 2]
    row_clues[12] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    row_clues[13] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    row_clues[14] = [1, 1, 8, 1, 4, 1, 5, 1, 3, 1]
    row_clues[15] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    row_clues[16] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    row_clues[17] = [4, 1, 1, 2, 1, 8, 1, 1, 4, 2]
    
    # Column clues (only non-empty ones)
    col_clues = [[] for _ in range(width)]
    col_clues[67] = [7]
    col_clues[68] = [1, 1]
    col_clues[69] = [1, 1]
    col_clues[70] = [1, 1]
    col_clues[71] = [1, 1]
    col_clues[72] = [3]
    col_clues[77] = [7]
    col_clues[78] = [1]
    col_clues[79] = [1]
    col_clues[80] = [1]
    col_clues[81] = [1]
    col_clues[82] = [1]
    col_clues[83] = [1]
    col_clues[84] = [7]
    col_clues[88] = [1]
    col_clues[89] = [2, 2]
    col_clues[90] = [1, 1]
    col_clues[91] = [1, 1]
    col_clues[95] = [1]
    col_clues[96] = [6]
    col_clues[97] = [1, 1]
    col_clues[98] = [1, 1]
    col_clues[99] = [1]
    col_clues[100] = [1]
    col_clues[104] = [7]
    col_clues[105] = [1]
    col_clues[106] = [1]
    col_clues[107] = [1]
    col_clues[108] = [1]
    col_clues[109] = [1]
    col_clues[110] = [1]
    col_clues[111] = [1]
    col_clues[115] = [6]
    col_clues[116] = [1, 1]
    col_clues[117] = [1, 1]
    col_clues[118] = [1, 1]
    col_clues[119] = [6]
    col_clues[125] = [5]
    col_clues[126] = [1, 1]
    col_clues[127] = [1, 1, 1]
    col_clues[128] = [1, 1, 1]
    col_clues[129] = [1, 4]
    col_clues[135] = [1, 1]
    col_clues[136] = [1, 1]
    col_clues[137] = [2, 2]
    col_clues[138] = [1]
    
    print("=== Real Nonogram Solver ===")
    print(f"Grid size: {height} x {width}")
    
    # Count non-empty clues
    non_empty_rows = sum(1 for clue in row_clues if clue)
    non_empty_cols = sum(1 for clue in col_clues if clue)
    print(f"Non-empty row clues: {non_empty_rows}")
    print(f"Non-empty column clues: {non_empty_cols}")
    
    # Solve the puzzle
    grid = solve_nonogram(height, width, row_clues, col_clues)
    
    # Visualize the result
    visualize_grid(grid)
    
    # Try to extract text
    extract_text_from_grid(grid)
    
    # Check if we have a complete solution
    unknown_count = sum(1 for row in grid for cell in row if cell == -1)
    print(f"\nUnknown cells remaining: {unknown_count}")
    
    if unknown_count == 0:
        print("✅ Puzzle solved completely!")
    else:
        print("⚠️  Puzzle partially solved")

if __name__ == "__main__":
    main()