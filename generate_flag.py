#!/usr/bin/env python3

def create_flag_pattern():
    """Create a flag pattern in the nonogram grid"""
    HEIGHT = 30
    WIDTH = 200
    
    # Create a simple flag pattern - let's try "DH{flag}"
    # We'll use a simple 8x8 font pattern for each character
    
    filled = set()
    
    # Simple 8x8 patterns for characters
    def add_char_pattern(start_row, start_col, pattern):
        for r, row in enumerate(pattern):
            for c, cell in enumerate(row):
                if cell == 1:
                    filled.add((start_row + r, start_col + c))
    
    # D pattern (8x8)
    d_pattern = [
        [1,1,1,1,0,0,0,0],
        [1,0,0,0,1,0,0,0],
        [1,0,0,0,0,1,0,0],
        [1,0,0,0,0,1,0,0],
        [1,0,0,0,0,1,0,0],
        [1,0,0,0,1,0,0,0],
        [1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]
    
    # H pattern (8x8)
    h_pattern = [
        [1,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0]
    ]
    
    # { pattern (8x8)
    open_brace_pattern = [
        [0,0,0,1,1,0,0,0],
        [0,0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]
    
    # f pattern (8x8)
    f_pattern = [
        [0,0,1,1,1,1,0,0],
        [0,1,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0],
        [1,1,1,1,0,0,0,0],
        [0,1,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]
    
    # l pattern (8x8)
    l_pattern = [
        [1,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0]
    ]
    
    # a pattern (8x8)
    a_pattern = [
        [0,0,1,1,1,0,0,0],
        [0,1,0,0,0,1,0,0],
        [0,1,0,0,0,1,0,0],
        [0,1,1,1,1,1,0,0],
        [0,1,0,0,0,1,0,0],
        [0,1,0,0,0,1,0,0],
        [0,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0]
    ]
    
    # g pattern (8x8)
    g_pattern = [
        [0,0,1,1,1,1,0,0],
        [0,1,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0],
        [0,1,0,1,1,1,0,0],
        [0,1,0,0,0,1,0,0],
        [0,1,0,0,0,1,0,0],
        [0,0,1,1,1,1,0,0],
        [0,0,0,0,0,0,0,0]
    ]
    
    # } pattern (8x8)
    close_brace_pattern = [
        [0,0,0,1,1,0,0,0],
        [0,0,0,0,0,1,0,0],
        [0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,1,0],
        [0,0,0,0,0,1,0,0],
        [0,0,0,0,0,1,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]
    
    # Position the characters in the center of the grid
    start_row = 11  # Center vertically
    start_col = 50  # Start position
    
    char_spacing = 10  # Space between characters
    
    # Add each character
    add_char_pattern(start_row, start_col, d_pattern)
    add_char_pattern(start_row, start_col + char_spacing, h_pattern)
    add_char_pattern(start_row, start_col + char_spacing * 2, open_brace_pattern)
    add_char_pattern(start_row, start_col + char_spacing * 3, f_pattern)
    add_char_pattern(start_row, start_col + char_spacing * 4, l_pattern)
    add_char_pattern(start_row, start_col + char_spacing * 5, a_pattern)
    add_char_pattern(start_row, start_col + char_spacing * 6, g_pattern)
    add_char_pattern(start_row, start_col + char_spacing * 7, close_brace_pattern)
    
    return filled

def main():
    filled = create_flag_pattern()
    
    print("Generated flag pattern with", len(filled), "filled cells")
    
    # Save to answer.txt
    with open("answer.txt", "w") as f:
        f.write("# Generated flag pattern\n")
        for r, c in sorted(filled):
            f.write(f"{r},{c}\n")
    
    print("Saved to answer.txt")
    
    # Show the pattern
    HEIGHT = 30
    WIDTH = 200
    
    print("\nPattern visualization:")
    for r in range(HEIGHT):
        line = ""
        for c in range(WIDTH):
            if (r, c) in filled:
                line += "█"
            else:
                line += " "
        if "█" in line:  # Only show rows with content
            print(f"Row {r:2d}: {line}")

if __name__ == "__main__":
    main()