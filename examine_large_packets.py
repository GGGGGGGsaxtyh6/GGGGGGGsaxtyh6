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

def examine_large_packets(filename):
    with open(filename, 'rb') as f:
        # Skip file header
        read_pcapng_block(f)
        
        packet_count = 0
        
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
                        
                        # Focus on the very large packets (122KB)
                        if len(usb_data) > 100000:
                            print(f"\n=== VERY LARGE PACKET {packet_count} ===")
                            print(f"Length: {len(usb_data)} bytes")
                            
                            # Save the raw data
                            with open(f"large_packet_{packet_count}.bin", "wb") as pf:
                                pf.write(usb_data)
                            print(f"Saved to large_packet_{packet_count}.bin")
                            
                            # Look for strings
                            text_content = usb_data.decode('utf-8', errors='ignore')
                            
                            # Extract all printable strings
                            strings = re.findall(r'[a-zA-Z0-9_\-\.]{4,}', text_content)
                            
                            print(f"Found {len(strings)} strings")
                            print("Sample strings:", strings[:20])
                            
                            # Look for flag patterns
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
                            
                            found_flags = []
                            for pattern in flag_patterns:
                                matches = re.findall(pattern, text_content, re.IGNORECASE)
                                found_flags.extend(matches)
                            
                            if found_flags:
                                print("*** POTENTIAL FLAGS FOUND ***")
                                for flag in found_flags:
                                    print(f"Flag: {flag}")
                            
                            # Look for file signatures
                            if usb_data.startswith(b'PK'):
                                print("ZIP file signature found!")
                            elif usb_data.startswith(b'\x89PNG'):
                                print("PNG file signature found!")
                            elif usb_data.startswith(b'\xff\xd8\xff'):
                                print("JPEG file signature found!")
                            elif usb_data.startswith(b'%PDF'):
                                print("PDF file signature found!")
                            
                            # Show hex dump of beginning
                            print(f"Hex dump (first 64 bytes): {binascii.hexlify(usb_data[:64]).decode()}")
                    
                    if packet_count > 1000:
                        break
                        
            except:
                break

if __name__ == "__main__":
    examine_large_packets("usbstorage.pcapng")