#!/usr/bin/env python3

import re
from pathlib import Path
import json

def parse_answer_file(path: Path, height: int, width: int):
    """Parse the answer file to get filled cells"""
    filled = set()
    if not path.exists():
        print(f"[!] {path} not found.")
        return filled

    rx = re.compile(r"^\s*(\d+)\s*[, ]\s*(\d+)\s*$")
    with path.open("r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = rx.match(line)
            if not m:
                print(f"skip line {ln}: {line!r}")
                continue
            r, c = int(m.group(1)), int(m.group(2))
            if 0 <= r < height and 0 <= c < width:
                filled.add((r, c))
            else:
                print(f"out-of-bounds ({r},{c}) at line {ln}; ignored")
    return filled

def runs_from_line(bits):
    """Calculate runs of consecutive 1s in a line"""
    runs = []
    cur = 0
    for b in bits:
        if b:
            cur += 1
        else:
            if cur:
                runs.append(cur)
                cur = 0
    if cur:
        runs.append(cur)
    return runs

def compute_clues(height: int, width: int, filled):
    """Compute row and column clues from filled cells"""
    row_clues = []
    for r in range(height):
        line = [1 if (r, c) in filled else 0 for c in range(width)]
        row_clues.append(runs_from_line(line))

    col_clues = []
    for c in range(width):
        line = [1 if (r, c) in filled else 0 for r in range(height)]
        col_clues.append(runs_from_line(line))
    return row_clues, col_clues

def visualize_solution(height: int, width: int, filled):
    """Create a visual representation of the solution"""
    print("Nonogram Solution Visualization:")
    print("=" * (width + 2))
    
    for r in range(height):
        line = ""
        for c in range(width):
            if (r, c) in filled:
                line += "█"
            else:
                line += " "
        print(f"|{line}|")
    print("=" * (width + 2))

def extract_text_from_solution(height: int, width: int, filled):
    """Try to extract readable text from the solution"""
    print("\nExtracting text from solution...")
    
    # Create a grid
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for r, c in filled:
        grid[r][c] = "█"
    
    # Print the grid
    for row in grid:
        print("".join(row))
    
    # Try to find patterns that might be text
    # Look for rows that might contain text
    text_rows = []
    for r in range(height):
        row_text = "".join(grid[r])
        if "█" in row_text:  # If row has any filled cells
            text_rows.append(row_text)
    
    print(f"\nFound {len(text_rows)} rows with content")
    for i, row in enumerate(text_rows):
        print(f"Row {i}: {row}")

def main():
    HEIGHT = 30
    WIDTH = 200
    ANSWER_FILE = Path("answer.txt")
    
    print("=== Nonogram Puzzle Solver ===")
    print(f"Grid size: {HEIGHT} x {WIDTH}")
    
    # Parse the answer file
    filled = parse_answer_file(ANSWER_FILE, HEIGHT, WIDTH)
    print(f"Found {len(filled)} filled cells")
    
    if len(filled) == 0:
        print("No solution found in answer.txt")
        return
    
    # Compute clues
    row_clues, col_clues = compute_clues(HEIGHT, WIDTH, filled)
    
    print(f"\nRow clues (first 10 rows):")
    for i, clue in enumerate(row_clues[:10]):
        print(f"Row {i}: {clue}")
    
    print(f"\nColumn clues (first 20 columns):")
    for i, clue in enumerate(col_clues[:20]):
        print(f"Col {i}: {clue}")
    
    # Visualize the solution
    visualize_solution(HEIGHT, WIDTH, filled)
    
    # Try to extract text
    extract_text_from_solution(HEIGHT, WIDTH, filled)
    
    # Save the puzzle data for the web interface
    puzzle_data = {
        "height": HEIGHT,
        "width": WIDTH,
        "row_clues": row_clues,
        "col_clues": col_clues,
        "solution_count": len(filled),
        "solution": sorted(list(filled)),
    }
    
    with open("puzzle_data.json", "w") as f:
        json.dump(puzzle_data, f, indent=2)
    
    print(f"\nPuzzle data saved to puzzle_data.json")

if __name__ == "__main__":
    main()