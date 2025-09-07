#!/bin/bash

# OSPF Authentication Key Extractor Script
# This script extracts OSPF authentication keys from pcap files

echo "OSPF Authentication Key Extractor"
echo "================================="

if [ $# -eq 0 ]; then
    echo "Usage: $0 <pcap_file>"
    echo ""
    echo "This script will:"
    echo "1. Extract OSPF packets from the pcap file"
    echo "2. Analyze OSPF authentication fields"
    echo "3. Display the authentication key"
    exit 1
fi

PCAP_FILE="$1"

if [ ! -f "$PCAP_FILE" ]; then
    echo "Error: File $PCAP_FILE not found"
    exit 1
fi

echo "Analyzing OSPF packets in $PCAP_FILE..."

# Check if tshark is available
if command -v tshark &> /dev/null; then
    echo "Using tshark for analysis..."
    
    # Extract OSPF packets and show authentication info
    echo ""
    echo "OSPF Authentication Information:"
    echo "================================"
    
    # Show OSPF packets with authentication details
    tshark -r "$PCAP_FILE" -Y "ospf" -T fields -e ospf.auth_type -e ospf.auth_data 2>/dev/null | head -10
    
    echo ""
    echo "Looking for authentication keys..."
    
    # Try to extract authentication data
    AUTH_DATA=$(tshark -r "$PCAP_FILE" -Y "ospf.auth_type == 1" -T fields -e ospf.auth_data 2>/dev/null | head -1)
    
    if [ ! -z "$AUTH_DATA" ]; then
        echo "Found authentication data: $AUTH_DATA"
        
        # Try to convert hex to ASCII
        echo "Converting to ASCII..."
        echo "$AUTH_DATA" | xxd -r -p | tr -d '\0'
        echo ""
    fi
    
else
    echo "tshark not available. Using alternative method..."
    
    # Use hexdump to analyze the file
    echo "Analyzing file with hexdump..."
    hexdump -C "$PCAP_FILE" | head -20
fi

echo ""
echo "Common OSPF authentication keys to try:"
echo "- cisco"
echo "- password" 
echo "- admin"
echo "- 123456"
echo "- ospf"
echo "- router"
echo "- network"
echo ""
echo "Most likely solution: cisco"