#!/bin/bash

# Check if 'pip' command exists
if command -v pip &> /dev/null; then
    pip install --upgrade -r requirements.txt
    exit
elif command -v pip3 &> /dev/null; then
    pip3 install --upgrade -r requirements.txt
    exit
else
    read -n 1 -s -r -p "Pip is not installed. Try installing it using the pythonpip.sh installer and try again."
    exit 1
    fi
fi
