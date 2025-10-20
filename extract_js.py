#!/usr/bin/env python3
import re

with open('/workspace/page.html', 'r') as f:
    content = f.read()

# Extract the JavaScript code
match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if match:
    js_code = match.group(1).strip()
    
    # Find the obfuscated part
    match2 = re.search(r'return (.*?)\n', js_code, re.DOTALL)
    if match2:
        obfuscated = match2.group(1)
        print("OBFUSCATED CODE LENGTH:", len(obfuscated))
        
        # Save to file
        with open('/workspace/obf.js', 'w') as f2:
            f2.write(obfuscated)
        print("Saved to obf.js")
