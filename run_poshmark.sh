#!/bin/bash
# Poshmark Auto-Relister - Mac/Linux Shell Script
# Run with: ./run_poshmark.sh (or double-click on Mac)

echo "================================"
echo "Poshmark Auto-Relister"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from python.org"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
if ! python3 -c "import selenium" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

echo ""
echo "Starting Poshmark relister..."
echo ""

# Run the Python script
python3 poshmark_relister.py

echo ""
echo "================================"
echo "Process Complete"
echo "================================"
echo "Check the log file for details."
echo ""

# On Mac, keep terminal open
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Press Enter to close..."
fi
