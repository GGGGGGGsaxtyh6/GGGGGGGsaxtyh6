#!/usr/bin/env python3

import requests
import json
import re

def get_puzzle_data():
    """Get the actual puzzle data from the running Flask app"""
    try:
        response = requests.get('http://localhost:5000')
        content = response.text
        
        # Extract the JSON data
        match = re.search(r'const DATA = JSON\.parse\("([^"]+)"\)', content)
        if match:
            data_str = match.group(1)
            # Unescape the JSON
            data_str = data_str.replace('\\"', '"').replace('\\\\', '\\')
            data = json.loads(data_str)
            
            print("=== Real Puzzle Data ===")
            print(f"Grid: {data['height']} x {data['width']}")
            print(f"Solution count: {data['solution_count']}")
            
            print("\nRow clues:")
            for i, clue in enumerate(data['row_clues']):
                if clue:
                    print(f"Row {i}: {clue}")
            
            print("\nColumn clues:")
            for i, clue in enumerate(data['col_clues']):
                if clue:
                    print(f"Col {i}: {clue}")
            
            # Save the solution
            if 'solution' in data:
                print(f"\nSolution: {data['solution']}")
                
                # Visualize the solution
                print("\nSolution visualization:")
                grid = [[' ' for _ in range(data['width'])] for _ in range(data['height'])]
                for r, c in data['solution']:
                    grid[r][c] = '█'
                
                for r in range(data['height']):
                    line = ''.join(grid[r])
                    if '█' in line:
                        print(f"Row {r:2d}: {line}")
            
            return data
        else:
            print("Could not find puzzle data")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    get_puzzle_data()