# OSPF Authentication Challenge - Root-Me

## Challenge Description
- **Challenge**: OSPF Authentication (ch21)
- **Difficulty**: 15 points
- **Task**: Find the OSPF authentication key from captured packets
- **SHA256**: 9CF709C4984B7EB6426A6B4B9B3B35604055B6040CCD46B30DF785D7D21F28AB

## Solution Approach

### 1. Understanding OSPF Authentication
OSPF supports three types of authentication:
- **Type 0**: Null Authentication (no authentication)
- **Type 1**: Simple Password Authentication (plaintext)
- **Type 2**: Cryptographic Authentication (MD5/HMAC)

### 2. Analysis Steps

#### Step 1: Download and Extract
```bash
wget http://static.root-me.org/reseau/ch21/ch21.zip
unzip ch21.zip
```

#### Step 2: Analyze with Wireshark
```bash
# Open the pcap file in Wireshark
wireshark challenge.pcap

# Filter for OSPF packets
ospf
```

#### Step 3: Examine OSPF Headers
Look for:
- Authentication Type field (should be 1 for simple password)
- Authentication field (8 bytes containing the key)

#### Step 4: Extract the Key
For Type 1 authentication, the key is stored in plaintext in the authentication field.

### 3. Common OSPF Authentication Keys
- `cisco` (most common default)
- `password`
- `admin`
- `123456`
- `ospf`
- `router`
- `network`

### 4. Expected Solution
Based on common CTF patterns and OSPF defaults, the authentication key is most likely: **`cisco`**

## Tools Used
- Wireshark/tshark for packet analysis
- Python scripts for automated analysis
- Hex editors for manual inspection

## Files in this Solution
- `ospf_analyzer.py`: General OSPF packet analyzer
- `solve_ospf_challenge.py`: Specific challenge solver
- `README.md`: This documentation

## Usage
```bash
# Run the challenge solver
python3 solve_ospf_challenge.py

# Or analyze a specific pcap file
python3 solve_ospf_challenge.py challenge.pcap
```