#!/usr/bin/env python3

import struct
import binascii

def parse_pcap_header(data):
    """Parse pcap global header"""
    magic, version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack('<LHHLLLL', data[:24])
    return {
        'magic': magic,
        'version_major': version_major,
        'version_minor': version_minor,
        'snaplen': snaplen,
        'network': network
    }

def parse_packet_header(data):
    """Parse pcap packet header"""
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<LLLL', data[:16])
    return {
        'ts_sec': ts_sec,
        'ts_usec': ts_usec,
        'incl_len': incl_len,
        'orig_len': orig_len
    }

def analyze_usb_pcap(filename):
    with open(filename, 'rb') as f:
        # Read global header
        global_header = f.read(24)
        header_info = parse_pcap_header(global_header)
        print(f"Pcap file info: {header_info}")
        
        packet_count = 0
        usb_packets = []
        data_packets = []
        
        while True:
            # Read packet header
            packet_header_data = f.read(16)
            if len(packet_header_data) < 16:
                break
                
            packet_header = parse_packet_header(packet_header_data)
            packet_data = f.read(packet_header['incl_len'])
            
            if len(packet_data) < packet_header['incl_len']:
                break
                
            packet_count += 1
            
            # Look for USB packets (assuming USB capture format)
            if len(packet_data) > 24:  # USB header is typically 24 bytes
                # USB header structure varies, let's look for data patterns
                usb_data = packet_data[24:]  # Skip USB header
                
                # Look for file-like data (ASCII text, common file signatures)
                if len(usb_data) > 10:
                    # Check for text content
                    try:
                        text_content = usb_data.decode('utf-8', errors='ignore')
                        if any(c.isprintable() for c in text_content):
                            data_packets.append({
                                'packet_num': packet_count,
                                'timestamp': packet_header['ts_sec'],
                                'data': usb_data,
                                'text': text_content[:200]  # First 200 chars
                            })
                    except:
                        pass
                    
                    # Check for file signatures
                    if usb_data.startswith(b'PK') or usb_data.startswith(b'\x89PNG') or usb_data.startswith(b'\xff\xd8\xff'):
                        data_packets.append({
                            'packet_num': packet_count,
                            'timestamp': packet_header['ts_sec'],
                            'data': usb_data,
                            'type': 'file_signature'
                        })
            
            # Limit analysis to avoid memory issues
            if packet_count > 10000:
                break
        
        print(f"Analyzed {packet_count} packets")
        print(f"Found {len(data_packets)} potential data packets")
        
        # Look for interesting content
        for i, packet in enumerate(data_packets[:20]):  # Show first 20 interesting packets
            print(f"\nPacket {packet['packet_num']} (timestamp: {packet['timestamp']}):")
            print(f"Data length: {len(packet['data'])}")
            if 'text' in packet:
                print(f"Text content: {repr(packet['text'][:100])}")
            if 'type' in packet:
                print(f"Type: {packet['type']}")
            print(f"Hex dump (first 64 bytes): {binascii.hexlify(packet['data'][:64]).decode()}")

if __name__ == "__main__":
    analyze_usb_pcap("usbstorage.pcapng")