#!/usr/bin/env python3
import json
import subprocess

# Get token
with open('/workspace/htb-mcp-server/.env', 'r') as f:
    for line in f:
        if line.startswith('HTB_TOKEN='):
            token = line.strip().split('=', 1)[1]
            break

# Get challenges
cmd = f'curl -s -H "Authorization: Bearer {token}" -H "Accept: application/json" "https://labs.hackthebox.com/api/v4/challenge/list/retired"'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
data = json.loads(result.stdout)

challenges = data.get('challenges', [])
print(f"=== TOTAL CHALLENGES: {len(challenges)} ===\n")

# Group by category
categories = {}
for ch in challenges:
    cat_id = ch.get('challenge_category_id', 0)
    if cat_id not in categories:
        categories[cat_id] = []
    categories[cat_id].append(ch)

# Category names
cat_names = {
    1: 'Reversing',
    2: 'Crypto', 
    3: 'Stego',
    4: 'Pwn',
    5: 'Web',
    6: 'Misc',
    7: 'Forensics',
    8: 'Mobile',
    9: 'OSINT',
    11: 'Hardware',
    12: 'Blockchain',
    13: 'GamePwn'
}

# Show challenges by category
for cat_id, chs in sorted(categories.items()):
    cat_name = cat_names.get(cat_id, f'Category {cat_id}')
    print(f"📁 {cat_name} ({len(chs)} challenges):")
    
    # Show first 5 challenges
    for ch in chs[:5]:
        print(f"  - {ch.get('name', '?')} (ID: {ch.get('id', '?')}, {ch.get('difficulty', '?')})")
    
    if len(chs) > 5:
        print(f"  ... y {len(chs)-5} más")
    print()

print("\n=== PARA INICIAR UN CHALLENGE ===")
print("Usa el ID del challenge que quieras iniciar")
print("Por ejemplo, para el challenge con ID 39:")
print('python3 -c "from start_challenge import start_challenge; start_challenge(39)"')