#!/usr/bin/env python3

import struct
import binascii

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

def analyze_specific_packets(filename):
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
                    
                    # Focus on packets around 356 where we saw interesting content
                    if 350 <= packet_count <= 370:
                        captured_length = struct.unpack('<I', block_data[12:16])[0]
                        packet_data = block_data[32:32+captured_length]
                        
                        if len(packet_data) > 24:
                            usb_data = packet_data[24:]
                            
                            if len(usb_data) > 100:
                                print(f"\n=== PACKET {packet_count} ===")
                                print(f"Length: {len(usb_data)} bytes")
                                
                                # Show hex dump
                                print(f"Hex (first 128 bytes): {binascii.hexlify(usb_data[:128]).decode()}")
                                
                                # Show as text
                                text_content = usb_data.decode('utf-8', errors='ignore')
                                print(f"Text content: {repr(text_content[:300])}")
                                
                                # Look for specific patterns
                                if 'flag' in text_content.lower() or 'ctf' in text_content.lower():
                                    print("*** POTENTIAL FLAG FOUND ***")
                                    # Extract potential flag
                                    lines = text_content.split('\n')
                                    for line in lines:
                                        if 'flag' in line.lower() or 'ctf' in line.lower():
                                            print(f"Flag candidate: {line.strip()}")
                                
                                # Save this packet's data
                                if packet_count == 356:  # The packet that showed interesting content
                                    with open(f"packet_{packet_count}_data.bin", "wb") as pf:
                                        pf.write(usb_data)
                                    print(f"Saved packet {packet_count} data to file")
                    
                    if packet_count > 400:
                        break
                        
            except:
                break

if __name__ == "__main__":
    analyze_specific_packets("usbstorage.pcapng")