package main

import (
    "fmt"
    "os"
    "strings"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ./ch32 <password>")
        return
    }
    
    password := os.Args[1]
    
    // Simple password validation logic
    if validatePassword(password) {
        fmt.Println("Password correct! Flag: ROOTME{GoLang_Reverse_Engineering}")
    } else {
        fmt.Println("Wrong password!")
    }
}

func validatePassword(input string) bool {
    // This is a simple validation - in real challenges it would be more complex
    expected := "golang123"
    return strings.Compare(input, expected) == 0
}
