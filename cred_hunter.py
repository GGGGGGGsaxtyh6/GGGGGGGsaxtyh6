#!/usr/bin/env python3

import re
from collections import defaultdict

def is_valid_email(s):
    """Check if string is a valid email format"""
    # Email pattern: username@domain
    email_pattern = r'^[a-z]+@[a-z]+(\.[a-z]+)*$'
    return bool(re.match(email_pattern, s))

def extract_firstname_from_email(email):
    """Extract firstname from email (everything before last letter of username)"""
    username = email.split('@')[0]
    if len(username) > 1:
        # firstname is all characters except the last one
        return username[:-1]
    return ""

def solve():
    # Read number of lines
    n = int(input())
    
    # Collect emails and passwords
    emails = []
    passwords = []
    
    for _ in range(n):
        line = input().strip()
        if is_valid_email(line):
            emails.append(line)
        else:
            passwords.append(line)
    
    # Find valid pairs
    valid_pairs = []
    
    for email in emails:
        firstname = extract_firstname_from_email(email)
        if firstname:
            # Find all passwords that contain this firstname as substring
            matching_passwords = []
            for password in passwords:
                if firstname in password:
                    matching_passwords.append(password)
            
            # Sort passwords lexicographically
            matching_passwords.sort()
            
            # Add all valid pairs
            for password in matching_passwords:
                valid_pairs.append((email, password))
    
    # Sort valid pairs by email first, then by password
    valid_pairs.sort(key=lambda x: (x[0], x[1]))
    
    # Output all valid pairs
    for email, password in valid_pairs:
        print(f"{email} {password}")

if __name__ == "__main__":
    solve()