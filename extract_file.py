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

def extract_file_content(filename):
    with open(filename, 'rb') as f:
        # Skip file header
        read_pcapng_block(f)
        
        packet_count = 0
        file_content = b''
        
        while True:
            try:
                block_type, block_data = read_pcapng_block(f)
                if block_type is None:
                    break
                
                # Enhanced Packet Block (0x00000006)
                if block_type == 0x00000006:
                    if len(block_data) < 32:
                        continue
                    
                    # Parse packet header
                    interface_id = struct.unpack('<I', block_data[0:4])[0]
                    timestamp_high = struct.unpack('<I', block_data[4:8])[0]
                    timestamp_low = struct.unpack('<I', block_data[8:12])[0]
                    captured_length = struct.unpack('<I', block_data[12:16])[0]
                    original_length = struct.unpack('<I', block_data[16:20])[0]
                    
                    # Get packet data
                    packet_data = block_data[32:32+captured_length]
                    
                    packet_count += 1
                    
                    # Look for packets with substantial content (likely file data)
                    if len(packet_data) > 24 and packet_count >= 350:  # Focus on later packets
                        usb_data = packet_data[24:]  # Skip USB header
                        
                        # Look for interesting content patterns
                        if len(usb_data) > 100:
                            # Check if this looks like file content
                            text_content = usb_data.decode('utf-8', errors='ignore')
                            
                            # Look for specific patterns that might indicate file content
                            if any(keyword in text_content.lower() for keyword in ['flag', 'secret', 'private', 'password', 'key', 'token']):
                                print(f"Found interesting content in packet {packet_count}:")
                                print(f"Length: {len(usb_data)} bytes")
                                print(f"Content preview: {repr(text_content[:500])}")
                                file_content += usb_data
                            
                            # Also check for readable text patterns
                            elif sum(1 for c in text_content if c.isprintable()) > len(text_content) * 0.7:
                                print(f"Found readable content in packet {packet_count}:")
                                print(f"Length: {len(usb_data)} bytes")
                                print(f"Content: {repr(text_content[:200])}")
                                file_content += usb_data
                    
                    if packet_count > 400:
                        break
                        
            except:
                break
        
        return file_content

if __name__ == "__main__":
    content = extract_file_content("usbstorage.pcapng")
    
    if content:
        print(f"\nTotal extracted content: {len(content)} bytes")
        
        # Try to save as different file types
        with open("recovered_file.txt", "wb") as f:
            f.write(content)
        
        print("Saved recovered content to 'recovered_file.txt'")
        
        # Try to extract just the readable text
        text_content = content.decode('utf-8', errors='ignore')
        readable_text = ''.join(c if c.isprintable() else ' ' for c in text_content)
        
        # Clean up the text
        words = readable_text.split()
        clean_text = ' '.join(word for word in words if len(word) > 2)
        
        print(f"\nClean readable text:\n{clean_text}")
        
        # Save clean text
        with open("clean_recovered_text.txt", "w") as f:
            f.write(clean_text)
        
        print("\nSaved clean text to 'clean_recovered_text.txt'")
    else:
        print("No file content found")