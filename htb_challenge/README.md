# Quantum Paradox Challenge

**Difficulty**: INSANE  
**Type**: Reverse Engineering  
**Expected Time**: 2+ hours  

## Description
A heavily obfuscated binary with anti-debugging protection. Contains multiple fake flags - only one real flag exists. The real flag is hidden in the binary and must be extracted through reverse engineering.

## Warning
Multiple fake flags are present. Only submit the real flag.

## Tools Recommended
- IDA Pro or Ghidra
- GDB with anti-debugging bypass
- Hex editor

## Real Flag
The real flag is obfuscated with XOR key 0x42 in the binary.