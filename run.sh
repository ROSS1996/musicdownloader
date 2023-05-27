#!/bin/bash

if command -v python3 &> /dev/null; then
    python3 music.py
    exit
elif command -v python &> /dev/null; then
    python_version=$(python --version 2>&1)
    if [[ $python_version == *"Python 3."* ]]; then
        python music.py
        exit
    else
        read -n 1 -s -r -p "Python 3 is not installed. Try installing it using pythonpip.sh and try again"
        exit 1
    fi
else
    # Python not found, so install Python 3
    read -n 1 -s -r -p "Python 3 is not installed. Try installing it using pythonpip.sh and try again"
    exit 1
fi
