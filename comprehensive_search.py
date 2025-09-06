#!/usr/bin/env python3

import struct
import binascii
import re
import string

def read_pcapng_block(f):
    """Read a pcapng block"""
    try:
        block_type = struct.unpack('<I', f.read(4))[0]
        block_length = struct.unpack('<I', f.read(4))[0]
        
        if block_length < 12:
            return None, None
        
        block_data = f.read(block_length - 12)
        block_length2 = struct.unpack('<I', f.read(4))[0]
        
        if block_length != block_length2:
            return None, None
        
        return block_type, block_data
    except:
        return None, None

def comprehensive_search(filename):
    with open(filename, 'rb') as f:
        # Skip file header
        read_pcapng_block(f)
        
        packet_count = 0
        all_data = b''
        
        print("Collecting all USB data...")
        
        while True:
            try:
                block_type, block_data = read_pcapng_block(f)
                if block_type is None:
                    break
                
                # Enhanced Packet Block (0x00000006)
                if block_type == 0x00000006:
                    if len(block_data) < 32:
                        continue
                    
                    packet_count += 1
                    captured_length = struct.unpack('<I', block_data[12:16])[0]
                    packet_data = block_data[32:32+captured_length]
                    
                    if len(packet_data) > 24:
                        usb_data = packet_data[24:]
                        all_data += usb_data
                    
                    if packet_count > 1000:
                        break
                        
            except:
                break
        
        print(f"Collected {len(all_data)} bytes from {packet_count} packets")
        
        # Save all data
        with open("all_usb_data.bin", "wb") as af:
            af.write(all_data)
        print("Saved all USB data to all_usb_data.bin")
        
        # Search for flag patterns in all data
        text_content = all_data.decode('utf-8', errors='ignore')
        
        print("\nSearching for flag patterns...")
        
        # Common flag patterns
        flag_patterns = [
            r'flag\{[^}]+\}',
            r'FLAG\{[^}]+\}',
            r'ctf\{[^}]+\}',
            r'CTF\{[^}]+\}',
            r'nullcon\{[^}]+\}',
            r'NULLCON\{[^}]+\}',
            r'[a-f0-9]{32,}',
            r'[A-Za-z0-9+/]{20,}={0,2}',
            r'[A-Za-z0-9]{20,}',
        ]
        
        found_flags = []
        for pattern in flag_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            found_flags.extend(matches)
        
        if found_flags:
            print("*** POTENTIAL FLAGS FOUND ***")
            for flag in set(found_flags):  # Remove duplicates
                print(f"Flag: {flag}")
        else:
            print("No obvious flag patterns found")
        
        # Look for any readable strings
        print("\nSearching for readable strings...")
        strings = re.findall(r'[a-zA-Z0-9_\-\.]{4,}', text_content)
        
        # Filter for potentially interesting strings
        interesting_strings = []
        for s in strings:
            if any(keyword in s.lower() for keyword in ['flag', 'secret', 'private', 'password', 'key', 'token', 'credential', 'ctf', 'nullcon']):
                interesting_strings.append(s)
        
        if interesting_strings:
            print("Interesting strings found:")
            for s in set(interesting_strings):
                print(f"  {s}")
        
        # Look for file signatures anywhere in the data
        print("\nSearching for file signatures...")
        file_signatures = {
            b'PK': 'ZIP',
            b'\x89PNG': 'PNG',
            b'\xff\xd8\xff': 'JPEG',
            b'%PDF': 'PDF',
            b'\x7fELF': 'ELF',
            b'BM': 'BMP',
            b'GIF8': 'GIF',
            b'RIFF': 'WAV/AVI',
            b'\x50\x4b\x03\x04': 'ZIP (alternative)',
            b'\x50\x4b\x05\x06': 'ZIP (end)',
        }
        
        for sig, file_type in file_signatures.items():
            pos = all_data.find(sig)
            if pos != -1:
                print(f"*** {file_type} signature found at position {pos} ***")
                # Extract some data around the signature
                start = max(0, pos - 100)
                end = min(len(all_data), pos + 1000)
                with open(f"file_signature_{file_type.lower()}_at_{pos}.bin", "wb") as sf:
                    sf.write(all_data[start:end])
                print(f"Saved context to file_signature_{file_type.lower()}_at_{pos}.bin")
        
        # Try to extract any base64-like content
        print("\nSearching for base64-like content...")
        base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
        base64_matches = re.findall(base64_pattern, text_content)
        
        if base64_matches:
            print("Base64-like strings found:")
            for match in set(base64_matches)[:10]:  # Show first 10 unique matches
                print(f"  {match}")
                # Try to decode
                try:
                    import base64
                    decoded = base64.b64decode(match + '==')  # Add padding if needed
                    decoded_text = decoded.decode('utf-8', errors='ignore')
                    if any(c.isprintable() for c in decoded_text):
                        print(f"    Decoded: {decoded_text[:100]}")
                except:
                    pass

if __name__ == "__main__":
    comprehensive_search("usbstorage.pcapng")