# Previous - HackTheBox Machine

## Machine Information
- **Name**: Previous
- **IP**: 10.10.11.83
- **OS**: Linux
- **Difficulty**: Medium (30 points)
- **Release Date**: August 23, 2025
- **Creator**: brun0ne
- **User Owns**: 1304
- **Root Owns**: 1191
- **Rating**: 4.4/5

## Enumeration

### Initial Scan
```bash
# Quick port scan
nmap -sV -sC -oN initial_scan.txt 10.10.11.83

# Full port scan
nmap -p- -T4 -oN full_scan.txt 10.10.11.83

# UDP scan (if needed)
nmap -sU --top-ports 100 -oN udp_scan.txt 10.10.11.83
```

### Service Enumeration
- [ ] Port 22 (SSH)
- [ ] Port 80/443 (HTTP/HTTPS)
- [ ] Other services

## Exploitation

### Initial Access

### Privilege Escalation

## Flags
- **User Flag**: 
- **Root Flag**: 

## Notes & Observations