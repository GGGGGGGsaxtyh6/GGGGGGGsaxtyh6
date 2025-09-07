#!/usr/bin/env python3

import requests
import json
import re

def extract_puzzle_data():
    """Extract the actual puzzle data from the web interface"""
    try:
        response = requests.get('http://localhost:5000')
        content = response.text
        
        # Find the DATA JSON
        match = re.search(r'const DATA = JSON\.parse\("([^"]+)"\)', content)
        if match:
            data_str = match.group(1)
            # Unescape the JSON string
            data_str = data_str.replace('\\"', '"').replace('\\\\', '\\')
            data = json.loads(data_str)
            
            print("=== Actual Puzzle Data ===")
            print(f"Grid size: {data['height']} x {data['width']}")
            print(f"Solution count: {data['solution_count']}")
            
            print("\nRow clues (non-empty only):")
            for i, clue in enumerate(data['row_clues']):
                if clue:
                    print(f"Row {i:2d}: {clue}")
            
            print("\nColumn clues (non-empty only):")
            for i, clue in enumerate(data['col_clues']):
                if clue:
                    print(f"Col {i:3d}: {clue}")
            
            return data
        else:
            print("Could not find puzzle data in response")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    extract_puzzle_data()