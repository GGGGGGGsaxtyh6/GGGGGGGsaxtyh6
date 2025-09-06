#!/usr/bin/env python3

import struct
import binascii
import re

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

def search_for_flags(filename):
    with open(filename, 'rb') as f:
        # Skip file header
        read_pcapng_block(f)
        
        packet_count = 0
        all_strings = []
        
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
                        
                        # Look for packets with substantial content
                        if len(usb_data) > 1000:  # Large packets likely contain file data
                            print(f"\n=== LARGE PACKET {packet_count} ===")
                            print(f"Length: {len(usb_data)} bytes")
                            
                            # Extract all strings from this packet
                            text_content = usb_data.decode('utf-8', errors='ignore')
                            
                            # Look for potential flags using regex patterns
                            flag_patterns = [
                                r'flag\{[^}]+\}',
                                r'FLAG\{[^}]+\}',
                                r'ctf\{[^}]+\}',
                                r'CTF\{[^}]+\}',
                                r'nullcon\{[^}]+\}',
                                r'NULLCON\{[^}]+\}',
                                r'[a-f0-9]{32,}',  # Hex strings
                                r'[A-Za-z0-9+/]{20,}={0,2}',  # Base64-like
                            ]
                            
                            for pattern in flag_patterns:
                                matches = re.findall(pattern, text_content, re.IGNORECASE)
                                if matches:
                                    print(f"*** POTENTIAL FLAG FOUND in packet {packet_count} ***")
                                    for match in matches:
                                        print(f"Flag candidate: {match}")
                                    
                                    # Save this packet
                                    with open(f"flag_candidate_packet_{packet_count}.bin", "wb") as pf:
                                        pf.write(usb_data)
                                    print(f"Saved potential flag packet to file")
                            
                            # Also look for any readable text that might be interesting
                            printable_chars = sum(1 for c in text_content if c.isprintable())
                            if printable_chars > len(text_content) * 0.3:  # At least 30% printable
                                # Extract just the printable parts
                                clean_text = ''.join(c if c.isprintable() else ' ' for c in text_content)
                                words = clean_text.split()
                                meaningful_words = [w for w in words if len(w) > 3]
                                
                                if len(meaningful_words) > 10:
                                    print(f"Readable content preview: {' '.join(meaningful_words[:20])}")
                                    
                                    # Check if it contains any interesting keywords
                                    interesting_keywords = ['secret', 'private', 'password', 'key', 'token', 'credential', 'file', 'document']
                                    if any(keyword in ' '.join(meaningful_words).lower() for keyword in interesting_keywords):
                                        print("*** CONTAINS INTERESTING KEYWORDS ***")
                                        with open(f"interesting_packet_{packet_count}.bin", "wb") as pf:
                                            pf.write(usb_data)
                    
                    if packet_count > 1000:
                        break
                        
            except:
                break
        
        print(f"\nAnalyzed {packet_count} packets total")

if __name__ == "__main__":
    search_for_flags("usbstorage.pcapng")