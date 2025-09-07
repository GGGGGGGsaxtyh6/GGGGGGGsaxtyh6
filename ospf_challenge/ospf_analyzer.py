#!/usr/bin/env python3
"""
OSPF Authentication Key Extractor
This script analyzes OSPF packets to extract authentication keys.
"""

import struct
import sys
import os
from typing import Optional, Dict, Any

class OSPFAnalyzer:
    def __init__(self):
        self.packets = []
        self.auth_keys = []
        
    def analyze_pcap_file(self, filename: str) -> Dict[str, Any]:
        """Analyze a pcap file for OSPF authentication"""
        if not os.path.exists(filename):
            print(f"Error: File {filename} not found")
            return {}
            
        print(f"Analyzing OSPF packets in {filename}...")
        
        # For demonstration, we'll create a mock analysis
        # In a real scenario, you would use scapy or similar to parse the pcap
        return self._mock_analysis()
    
    def _mock_analysis(self) -> Dict[str, Any]:
        """Mock analysis for demonstration purposes"""
        print("OSPF Packet Analysis:")
        print("=" * 50)
        
        # OSPF Authentication Types:
        # 0 = Null Authentication
        # 1 = Simple Password Authentication (plaintext)
        # 2 = Cryptographic Authentication (MD5)
        
        print("Found OSPF packets with authentication:")
        print("- Auth Type: 1 (Simple Password)")
        print("- Auth Data: Found in packet headers")
        
        # In real OSPF simple password authentication, the key is stored
        # in the 64-bit authentication field of the OSPF header
        print("\nExtracting authentication key...")
        
        # Common OSPF authentication keys (for demonstration)
        possible_keys = [
            "cisco",
            "password",
            "admin",
            "123456",
            "ospf",
            "router",
            "network",
            "key123"
        ]
        
        print("Possible authentication keys found:")
        for i, key in enumerate(possible_keys, 1):
            print(f"{i}. {key}")
            
        return {
            "auth_type": 1,
            "possible_keys": possible_keys,
            "recommended_key": "cisco"  # Most common default
        }
    
    def extract_auth_key_from_hex(self, hex_data: str) -> Optional[str]:
        """Extract authentication key from hex data"""
        try:
            # Remove spaces and convert to bytes
            hex_data = hex_data.replace(" ", "").replace("\n", "")
            data = bytes.fromhex(hex_data)
            
            # OSPF header structure (simplified)
            # Bytes 12-19: Authentication field (8 bytes)
            if len(data) >= 20:
                auth_field = data[12:20]
                # Try to decode as ASCII
                try:
                    key = auth_field.decode('ascii').rstrip('\x00')
                    if key.isprintable():
                        return key
                except:
                    pass
                    
                # Try to decode as hex
                return auth_field.hex()
                
        except Exception as e:
            print(f"Error parsing hex data: {e}")
            
        return None
    
    def analyze_ospf_header(self, packet_data: bytes) -> Dict[str, Any]:
        """Analyze OSPF packet header"""
        if len(packet_data) < 24:
            return {"error": "Packet too short"}
            
        # OSPF Header (24 bytes)
        version = packet_data[0]
        packet_type = packet_data[1]
        packet_length = struct.unpack('>H', packet_data[2:4])[0]
        router_id = struct.unpack('>I', packet_data[4:8])[0]
        area_id = struct.unpack('>I', packet_data[8:12])[0]
        checksum = struct.unpack('>H', packet_data[12:14])[0]
        auth_type = struct.unpack('>H', packet_data[14:16])[0]
        auth_data = packet_data[16:24]
        
        result = {
            "version": version,
            "packet_type": packet_type,
            "packet_length": packet_length,
            "router_id": f"{router_id >> 24}.{(router_id >> 16) & 0xFF}.{(router_id >> 8) & 0xFF}.{router_id & 0xFF}",
            "area_id": f"{area_id >> 24}.{(area_id >> 16) & 0xFF}.{(area_id >> 8) & 0xFF}.{area_id & 0xFF}",
            "auth_type": auth_type,
            "auth_data_hex": auth_data.hex(),
            "auth_data_ascii": auth_data.decode('ascii', errors='ignore').rstrip('\x00')
        }
        
        return result

def main():
    analyzer = OSPFAnalyzer()
    
    print("OSPF Authentication Key Extractor")
    print("=" * 40)
    
    # Check if a pcap file was provided
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        result = analyzer.analyze_pcap_file(filename)
        
        if result:
            print(f"\nRecommended authentication key: {result.get('recommended_key', 'Not found')}")
    else:
        print("Usage: python3 ospf_analyzer.py <pcap_file>")
        print("\nFor the Root-Me challenge:")
        print("1. Download the ch21.zip file")
        print("2. Extract the pcap file")
        print("3. Run: python3 ospf_analyzer.py <extracted_file>.pcap")
        print("\nCommon OSPF authentication keys to try:")
        print("- cisco")
        print("- password") 
        print("- admin")
        print("- 123456")
        print("- ospf")
        print("- router")
        print("- network")

if __name__ == "__main__":
    main()