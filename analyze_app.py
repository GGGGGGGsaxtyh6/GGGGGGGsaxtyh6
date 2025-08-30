#!/usr/bin/env python3
import requests
import json
import re

# URL base del challenge
BASE_URL = "http://94.237.57.115:35694"

def analyze_app():
    print("[*] Analizando la aplicación SocialConnect...")
    
    # Obtener la página principal
    r = requests.get(BASE_URL)
    print(f"\n[+] Status Code: {r.status_code}")
    
    # Obtener el JavaScript principal
    js_match = re.search(r'src="(/assets/index-[^"]+\.js)"', r.text)
    if js_match:
        js_url = BASE_URL + js_match.group(1)
        print(f"[+] JavaScript encontrado: {js_url}")
        
        js_content = requests.get(js_url).text
        
        # Buscar endpoints API
        api_endpoints = re.findall(r'["\'](/api/[^"\']+)["\']', js_content)
        if api_endpoints:
            print("\n[+] Endpoints API encontrados:")
            for endpoint in set(api_endpoints):
                print(f"    - {endpoint}")
        
        # Buscar rutas
        routes = re.findall(r'path:\s*["\'](/[^"\']+)["\']', js_content)
        if routes:
            print("\n[+] Rutas encontradas:")
            for route in set(routes):
                print(f"    - {route}")
        
        # Buscar información de usuario/perfil
        user_patterns = [
            r'username["\']?\s*[:=]\s*["\']([\w\-\.@]+)["\']',
            r'email["\']?\s*[:=]\s*["\']([\w\-\.@]+)["\']',
            r'profile["\']?\s*[:=]\s*["\']([\w\-\.@/]+)["\']',
            r'github["\']?\s*[:=]\s*["\']([\w\-\.@/]+)["\']',
            r'linkedin["\']?\s*[:=]\s*["\']([\w\-\.@/]+)["\']',
            r'twitter["\']?\s*[:=]\s*["\']([\w\-\.@/]+)["\']',
            r'facebook["\']?\s*[:=]\s*["\']([\w\-\.@/]+)["\']',
            r'instagram["\']?\s*[:=]\s*["\']([\w\-\.@/]+)["\']',
        ]
        
        print("\n[+] Buscando información de usuario...")
        for pattern in user_patterns:
            matches = re.findall(pattern, js_content, re.IGNORECASE)
            if matches:
                for match in set(matches):
                    print(f"    - {match}")
        
        # Buscar comentarios interesantes
        comments = re.findall(r'//.*|/\*[\s\S]*?\*/', js_content)
        if comments:
            print("\n[+] Comentarios encontrados:")
            for comment in comments[:10]:  # Solo los primeros 10
                if len(comment) > 20 and len(comment) < 200:
                    print(f"    {comment}")
        
        # Buscar flags o información sensible
        flag_patterns = [
            r'HTB\{[^}]+\}',
            r'flag["\']?\s*[:=]\s*["\'](.*?)["\']',
            r'secret["\']?\s*[:=]\s*["\'](.*?)["\']',
            r'password["\']?\s*[:=]\s*["\'](.*?)["\']',
            r'token["\']?\s*[:=]\s*["\'](.*?)["\']',
            r'api_key["\']?\s*[:=]\s*["\'](.*?)["\']',
        ]
        
        print("\n[+] Buscando información sensible...")
        for pattern in flag_patterns:
            matches = re.findall(pattern, js_content, re.IGNORECASE)
            if matches:
                for match in set(matches):
                    print(f"    [!] Encontrado: {match}")
        
        # Buscar nombres de usuario específicos
        print("\n[+] Buscando nombres de usuario específicos...")
        usernames = re.findall(r'["\'](john[\w]*|admin|root|user[\w]*|test[\w]*|demo[\w]*|alex[\w]*|sarah[\w]*|mike[\w]*|emily[\w]*)["\']', js_content, re.IGNORECASE)
        if usernames:
            for username in set(usernames):
                if len(username) > 3:
                    print(f"    - {username}")
        
        # Buscar URLs externas
        print("\n[+] Buscando URLs externas...")
        urls = re.findall(r'https?://[^\s"\'<>]+', js_content)
        for url in set(urls):
            if 'hackthebox' not in url.lower() and len(url) < 100:
                print(f"    - {url}")

    # Obtener el CSS
    css_match = re.search(r'href="(/assets/index-[^"]+\.css)"', r.text)
    if css_match:
        css_url = BASE_URL + css_match.group(1)
        print(f"\n[+] CSS encontrado: {css_url}")
        
        css_content = requests.get(css_url).text
        # Buscar comentarios en CSS
        css_comments = re.findall(r'/\*[\s\S]*?\*/', css_content)
        if css_comments:
            print("\n[+] Comentarios en CSS:")
            for comment in css_comments[:5]:
                if len(comment) > 20 and len(comment) < 200:
                    print(f"    {comment}")

if __name__ == "__main__":
    analyze_app()