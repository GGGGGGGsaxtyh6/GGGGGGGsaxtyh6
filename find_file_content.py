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

def find_file_content(filename):
    with open(filename, 'rb') as f:
        # Skip file header
        read_pcapng_block(f)
        
        packet_count = 0
        file_signatures = {
            b'PK': 'ZIP',
            b'\x89PNG': 'PNG',
            b'\xff\xd8\xff': 'JPEG',
            b'%PDF': 'PDF',
            b'\x7fELF': 'ELF',
            b'BM': 'BMP',
            b'GIF8': 'GIF',
            b'RIFF': 'WAV/AVI',
        }
        
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
                        
                        # Look for file signatures
                        for sig, file_type in file_signatures.items():
                            if usb_data.startswith(sig):
                                print(f"*** {file_type} FILE FOUND in packet {packet_count} ***")
                                with open(f"found_{file_type.lower()}_packet_{packet_count}.bin", "wb") as pf:
                                    pf.write(usb_data)
                                print(f"Saved to found_{file_type.lower()}_packet_{packet_count}.bin")
                        
                        # Look for substantial readable text content
                        if len(usb_data) > 100:
                            text_content = usb_data.decode('utf-8', errors='ignore')
                            printable_ratio = sum(1 for c in text_content if c.isprintable()) / len(text_content)
                            
                            if printable_ratio > 0.5:  # More than 50% printable
                                # Extract meaningful words
                                words = re.findall(r'\b[a-zA-Z]{4,}\b', text_content)
                                if len(words) > 20:  # Substantial text content
                                    print(f"\n=== TEXT CONTENT in packet {packet_count} ===")
                                    print(f"Length: {len(usb_data)} bytes")
                                    print(f"Printable ratio: {printable_ratio:.2f}")
                                    print(f"Sample words: {words[:10]}")
                                    
                                    # Look for potential flags or secrets
                                    potential_flags = []
                                    for word in words:
                                        if any(keyword in word.lower() for keyword in ['flag', 'secret', 'private', 'password', 'key', 'token', 'credential']):
                                            potential_flags.append(word)
                                    
                                    if potential_flags:
                                        print(f"*** POTENTIAL SECRETS: {potential_flags} ***")
                                    
                                    # Save interesting text content
                                    with open(f"text_content_packet_{packet_count}.txt", "w") as tf:
                                        tf.write(text_content)
                                    print(f"Saved text content to text_content_packet_{packet_count}.txt")
                                    
                                    # Also save binary
                                    with open(f"text_content_packet_{packet_count}.bin", "wb") as bf:
                                        bf.write(usb_data)
                        
                        # Look for specific patterns that might be flags
                        flag_patterns = [
                            r'flag\{[^}]+\}',
                            r'FLAG\{[^}]+\}',
                            r'ctf\{[^}]+\}',
                            r'CTF\{[^}]+\}',
                            r'nullcon\{[^}]+\}',
                            r'NULLCON\{[^}]+\}',
                            r'[a-f0-9]{32,}',
                            r'[A-Za-z0-9+/]{20,}={0,2}',
                        ]
                        
                        text_content = usb_data.decode('utf-8', errors='ignore')
                        for pattern in flag_patterns:
                            matches = re.findall(pattern, text_content, re.IGNORECASE)
                            if matches:
                                print(f"*** FLAG PATTERN FOUND in packet {packet_count} ***")
                                for match in matches:
                                    print(f"Match: {match}")
                                with open(f"flag_match_packet_{packet_count}.bin", "wb") as pf:
                                    pf.write(usb_data)
                    
                    if packet_count > 1000:
                        break
                        
            except:
                break

if __name__ == "__main__":
    find_file_content("usbstorage.pcapng")