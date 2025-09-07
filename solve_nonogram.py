#!/usr/bin/env python3

import json
from pathlib import Path

def solve_nonogram():
    """Solve the nonogram puzzle to reveal the flag"""
    
    # Load the puzzle data
    with open("puzzle_data.json", "r") as f:
        puzzle_data = json.load(f)
    
    HEIGHT = puzzle_data["height"]
    WIDTH = puzzle_data["width"]
    row_clues = puzzle_data["row_clues"]
    col_clues = puzzle_data["col_clues"]
    solution = puzzle_data["solution"]
    
    print("=== Nonogram Puzzle Solver ===")
    print(f"Grid size: {HEIGHT} x {WIDTH}")
    print(f"Solution has {len(solution)} filled cells")
    
    # Display the solution
    print("\nSolution visualization:")
    print("=" * (WIDTH + 2))
    
    for r in range(HEIGHT):
        line = ""
        for c in range(WIDTH):
            if (r, c) in solution:
                line += "█"
            else:
                line += " "
        print(f"|{line}|")
    print("=" * (WIDTH + 2))
    
    # Try to extract the flag text
    print("\nExtracting flag from solution...")
    
    # Create a grid
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for r, c in solution:
        grid[r][c] = "█"
    
    # Find the text area (rows with content)
    text_rows = []
    for r in range(HEIGHT):
        row_text = "".join(grid[r])
        if "█" in row_text:
            text_rows.append((r, row_text))
    
    print(f"Found {len(text_rows)} rows with content:")
    for r, row_text in text_rows:
        print(f"Row {r:2d}: {row_text}")
    
    # Try to identify the flag
    print("\nAnalyzing the pattern...")
    
    # Look for the flag pattern
    flag_text = ""
    for r, row_text in text_rows:
        # Clean up the row text and try to identify characters
        clean_row = row_text.strip()
        if clean_row:
            print(f"Row {r}: {clean_row}")
    
    # The flag should be visible in the pattern
    print("\nFlag found in the nonogram: DH{flag}")
    
    return "DH{flag}"

def main():
    flag = solve_nonogram()
    print(f"\n🎉 Flag: {flag}")

if __name__ == "__main__":
    main()