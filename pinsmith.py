#!/usr/bin/env python3

def generate_valid_pins(template):
    """
    Generate all valid PINs based on the template.
    - Known digits are fixed
    - Unknown positions (*) can be any digit 0-9
    - No two adjacent digits can be the same
    """
    result = []
    
    def is_valid(pin):
        """Check if PIN has no adjacent repeated digits"""
        for i in range(len(pin) - 1):
            if pin[i] == pin[i + 1]:
                return False
        return True
    
    def backtrack(index, current):
        """Recursively build valid PINs"""
        if index == len(template):
            if is_valid(current):
                result.append(current)
            return
        
        if template[index] != '*':
            # Fixed digit
            backtrack(index + 1, current + template[index])
        else:
            # Unknown digit - try all possibilities
            for digit in '0123456789':
                # Check if this digit would create adjacent repeats
                if index > 0 and current and current[-1] == digit:
                    continue  # Skip if it would create adjacent repeat
                if index < len(template) - 1 and template[index + 1] != '*' and template[index + 1] == digit:
                    continue  # Skip if next fixed digit is the same
                
                backtrack(index + 1, current + digit)
    
    backtrack(0, "")
    
    # Sort results lexicographically
    result.sort()
    return result

def solve():
    # Read the PIN template
    template = input().strip()
    
    # Generate all valid PINs
    valid_pins = generate_valid_pins(template)
    
    # Output each valid PIN
    for pin in valid_pins:
        print(pin)

if __name__ == "__main__":
    solve()