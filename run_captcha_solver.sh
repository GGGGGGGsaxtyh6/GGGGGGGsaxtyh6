#!/bin/bash

# CAPTCHA Solver Runner Script
# This script helps you run the CAPTCHA solver with proper setup

echo "🤖 CAPTCHA Solver for Root-Me Challenge"
echo "========================================"

# Check if virtual environment exists
if [ ! -d "captcha_env" ]; then
    echo "❌ Virtual environment not found. Please run the setup first."
    echo "Run: python3 -m venv captcha_env && source captcha_env/bin/activate && pip install pytesseract requests"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source captcha_env/bin/activate

# Check if required tools are installed
echo "🔍 Checking required tools..."

if ! command -v tesseract &> /dev/null; then
    echo "❌ Tesseract not found. Installing..."
    sudo apt-get install -y tesseract-ocr
fi

if ! command -v gocr &> /dev/null; then
    echo "❌ GOCR not found. Installing..."
    sudo apt-get install -y gocr
fi

echo "✅ All tools are ready!"

# Check if session cookie is provided
if [ -z "$1" ]; then
    echo ""
    echo "📋 Usage: $0 [session_cookie]"
    echo ""
    echo "To get your session cookie:"
    echo "1. Go to https://www.root-me.org/ and log in"
    echo "2. Open browser developer tools (F12)"
    echo "3. Go to Application/Storage tab"
    echo "4. Copy the PHPSESSID cookie value"
    echo "5. Run: $0 your_session_cookie_here"
    echo ""
    echo "Or run without authentication (may not work):"
    echo "python captcha_solver_final.py"
    echo ""
    exit 1
fi

echo "🚀 Running CAPTCHA solver with session cookie..."
python captcha_solver_authenticated.py --cookie "$1"