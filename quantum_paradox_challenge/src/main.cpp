#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstring>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <thread>
#include <chrono>
#include <random>
#include <cmath>

#ifdef _WIN32
#include <windows.h>
#else
// Linux/Unix anti-debugging
#include <sys/ptrace.h>
#include <unistd.h>
#endif

// Anti-debugging macros
#define ANTI_DEBUG_1 __asm__("int3")
#define ANTI_DEBUG_2 __asm__("nop")
#define ANTI_DEBUG_3 __asm__("xchg %eax, %eax")

// Obfuscated strings using XOR
const char* obfuscated_strings[] = {
    "\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64", // "Hello World"
    "\x51\x75\x61\x6e\x74\x75\x6d\x20\x50\x61\x72\x61\x64\x6f\x78", // "Quantum Paradox"
    "\x46\x6c\x61\x67\x20\x66\x6f\x75\x6e\x64", // "Flag found"
    "\x49\x6e\x76\x61\x6c\x69\x64\x20\x69\x6e\x70\x75\x74", // "Invalid input"
    "\x44\x65\x62\x75\x67\x67\x65\x72\x20\x64\x65\x74\x65\x63\x74\x65\x64" // "Debugger detected"
};

// XOR key for string deobfuscation
const int XOR_KEY = 0x42;

// Deobfuscate string function
std::string deobfuscate(const char* str) {
    std::string result;
    for (int i = 0; str[i] != '\0'; i++) {
        result += str[i] ^ XOR_KEY;
    }
    return result;
}

// Anti-debugging function
bool checkDebugger() {
    ANTI_DEBUG_1;
    // Check for common debugger signatures
#ifdef _WIN32
    if (IsDebuggerPresent()) {
        std::cout << deobfuscate(obfuscated_strings[4]) << std::endl;
        exit(1);
    }
#else
    // Linux/Unix anti-debugging
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        std::cout << deobfuscate(obfuscated_strings[4]) << std::endl;
        exit(1);
    }
#endif
    ANTI_DEBUG_2;
    return false;
}

// Fake flag 1 - Easy to find
std::string fakeFlag1() {
    return "HTB{f4k3_fl4g_1_qu4ntum_3rr0r}";
}

// Fake flag 2 - Medium difficulty
std::string fakeFlag2() {
    std::string encoded = "\x48\x54\x42\x7b\x66\x34\x6b\x33\x5f\x66\x6c\x34\x67\x5f\x32\x5f\x70\x61\x72\x61\x64\x6f\x78\x7d";
    std::string result;
    for (char c : encoded) {
        result += c ^ 0x11;
    }
    return result;
}

// Complex mathematical function that leads nowhere
double quantumFunction(double x, double y) {
    ANTI_DEBUG_3;
    double result = 0;
    for (int i = 0; i < 1000; i++) {
        result += sin(x * i) * cos(y * i) * exp(-i * 0.001);
    }
    return result;
}

// Obfuscated validation function
bool validateInput(const std::string& input) {
    if (input.length() != 32) return false;
    
    // Check for specific pattern
    std::string pattern = "quantum_paradox_2024";
    std::string encoded_pattern;
    for (char c : pattern) {
        encoded_pattern += c ^ 0x33;
    }
    
    // This is a red herring - not the real validation
    return input.find(encoded_pattern) != std::string::npos;
}

// Another fake validation
bool validateQuantumKey(const std::string& key) {
    // This function is designed to waste time
    std::vector<int> primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};
    int sum = 0;
    for (char c : key) {
        sum += static_cast<int>(c);
    }
    
    // Check if sum is prime
    for (int prime : primes) {
        if (sum == prime) {
            return true;
        }
    }
    return false;
}

// Main quantum paradox function
void quantumParadox() {
    std::cout << deobfuscate(obfuscated_strings[0]) << std::endl;
    std::cout << "Welcome to " << deobfuscate(obfuscated_strings[1]) << std::endl;
    std::cout << "This is a quantum computing simulation..." << std::endl;
    
    // Simulate quantum operations
    for (int i = 0; i < 5; i++) {
        std::cout << "Quantum state " << i << ": ";
        double result = quantumFunction(i * 0.1, i * 0.2);
        std::cout << std::fixed << std::setprecision(6) << result << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
}

// Hidden function that contains the real flag
std::string getRealFlag() {
    // This function is never called directly
    // The flag is hidden in the binary and must be extracted through memory analysis
    std::string realFlag = "HTB{qu4ntum_paradox_solved_2024_real_flag}";
    
    // Obfuscate the flag in memory
    std::string obfuscatedFlag;
    for (char c : realFlag) {
        obfuscatedFlag += c ^ 0xAA;
    }
    
    return obfuscatedFlag;
}

// Function that seems important but is a decoy
void processQuantumData() {
    std::cout << "Processing quantum data..." << std::endl;
    
    // Generate fake quantum data
    std::vector<double> quantumData;
    for (int i = 0; i < 100; i++) {
        quantumData.push_back(sin(i * 0.1) * cos(i * 0.2));
    }
    
    // This looks like it might contain the flag, but it doesn't
    std::string fakeFlag = fakeFlag1();
    std::cout << "Quantum analysis complete. Flag: " << fakeFlag << std::endl;
}

// Another decoy function
void analyzeParadox() {
    std::cout << "Analyzing quantum paradox..." << std::endl;
    
    // Complex calculations that lead nowhere
    double paradoxValue = 0;
    for (int i = 0; i < 10000; i++) {
        paradoxValue += pow(-1, i) / (2 * i + 1);
    }
    paradoxValue *= 4; // This approximates pi, but it's irrelevant
    
    std::cout << "Paradox value: " << std::fixed << std::setprecision(10) << paradoxValue << std::endl;
    
    // Another fake flag
    std::string fakeFlag = fakeFlag2();
    std::cout << "Paradox analysis complete. Flag: " << fakeFlag << std::endl;
}

// Main function with multiple paths
int main() {
    // Anti-debugging check
    if (checkDebugger()) {
        return 1;
    }
    
    std::cout << "=== Quantum Paradox Challenge ===" << std::endl;
    std::cout << "Enter your quantum key: ";
    
    std::string input;
    std::getline(std::cin, input);
    
    // Multiple validation paths - all lead to fake flags
    if (validateInput(input)) {
        std::cout << "Input validated! Processing..." << std::endl;
        processQuantumData();
    } else if (validateQuantumKey(input)) {
        std::cout << "Quantum key accepted! Analyzing..." << std::endl;
        analyzeParadox();
    } else {
        std::cout << deobfuscate(obfuscated_strings[3]) << std::endl;
        std::cout << "Running quantum simulation anyway..." << std::endl;
        quantumParadox();
    }
    
    // The real flag is never displayed - it must be found through reversing
    // It's hidden in the getRealFlag() function and obfuscated in memory
    
    return 0;
}