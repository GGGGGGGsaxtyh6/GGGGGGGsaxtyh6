#!/usr/bin/env python3

import struct
import binascii
import io

def read_pcapng_block(f):
    """Read a pcapng block"""
    # Read block header
    block_type = struct.unpack('<I', f.read(4))[0]
    block_length = struct.unpack('<I', f.read(4))[0]
    
    if block_length < 12:  # Minimum block size
        return None, None
    
    # Read block data (minus header)
    block_data = f.read(block_length - 12)
    
    # Read block length again (for verification)
    block_length2 = struct.unpack('<I', f.read(4))[0]
    
    if block_length != block_length2:
        print(f"Block length mismatch: {block_length} vs {block_length2}")
        return None, None
    
    return block_type, block_data

def parse_usb_data(data):
    """Parse USB data from packet"""
    # USB header is typically at the beginning
    if len(data) < 24:
        return None
    
    # Try to find USB endpoint data
    # Look for SCSI/UFI commands (common in USB storage)
    usb_data = data[24:]  # Skip USB header
    
    # Look for SCSI commands
    if len(usb_data) > 10:
        # SCSI WRITE (10) command starts with 0x2A
        # SCSI READ (10) command starts with 0x28
        if usb_data[0] == 0x2A or usb_data[0] == 0x28:
            return usb_data
    
    # Look for file system data
    # Check for FAT32 boot sector signature
    if b'\x55\xAA' in usb_data:
        return usb_data
    
    # Check for file content patterns
    if len(usb_data) > 512:  # Likely file content
        return usb_data
    
    return None

def analyze_pcapng(filename):
    with open(filename, 'rb') as f:
        # Skip file header (first block)
        read_pcapng_block(f)
        
        packet_count = 0
        interesting_packets = []
        
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
                    
                    # Parse USB data
                    usb_data = parse_usb_data(packet_data)
                    if usb_data:
                        interesting_packets.append({
                            'packet_num': packet_count,
                            'timestamp': (timestamp_high << 32) | timestamp_low,
                            'data': usb_data,
                            'length': len(usb_data)
                        })
                    
                    # Limit to avoid memory issues
                    if packet_count > 50000:
                        break
                        
            except (struct.error, IOError):
                break
        
        print(f"Analyzed {packet_count} packets")
        print(f"Found {len(interesting_packets)} interesting packets")
        
        # Analyze interesting packets
        for i, packet in enumerate(interesting_packets[:50]):
            print(f"\nPacket {packet['packet_num']}:")
            print(f"Length: {packet['length']} bytes")
            
            data = packet['data']
            
            # Look for file signatures
            if data.startswith(b'PK'):
                print("ZIP file signature found!")
            elif data.startswith(b'\x89PNG'):
                print("PNG file signature found!")
            elif data.startswith(b'\xff\xd8\xff'):
                print("JPEG file signature found!")
            
            # Look for text content
            try:
                text = data.decode('utf-8', errors='ignore')
                if any(c.isprintable() for c in text[:100]):
                    print(f"Text content: {repr(text[:200])}")
            except:
                pass
            
            # Show hex dump of interesting parts
            if len(data) > 0:
                print(f"Hex (first 64 bytes): {binascii.hexlify(data[:64]).decode()}")

if __name__ == "__main__":
    analyze_pcapng("usbstorage.pcapng")