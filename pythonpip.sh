#!/bin/bash

# Function to open URL based on OS
open_url() {
    case "$(uname -s)" in
        Linux*)     xdg-open "$1" ;;
        Darwin*)    open "$1" ;;
        *)          echo "Visit $1." ;;
    esac
}

# Check if Python 3 is installed
if command -v python3 &> /dev/null; then
    echo "Python 3 is already installed, checking if pip is installed"
elif command -v python &>/dev/null; then
    python_version=$(python --version 3>&1)
    if [[ $python_version == *"Python 3."* ]]; then
        echo "Python 3 is already installed, checking if pip is installed"
    else
        echo "Python 3 is not installed. Installing it..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get update
            sudo apt-get install python3
        elif command -v yum &>/dev/null; then
            sudo yum install python3
        elif command -v brew &>/dev/null; then
            brew install python@3
        else
            echo "Unable to determine package manager. Please install Python 3 manually."
            python_download_url="https://www.python.org/downloads/"
            open_url "$python_download_url"
            read -n 1 -s -r -p "Press any key to exit..."
            exit 1
        fi
    fi
else
    echo "Python is not installed. Installing Python 3..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update
        sudo apt-get install python3
    elif command -v yum &>/dev/null; then
        sudo yum install python3
    elif command -v brew &>/dev/null; then
        brew install python@3
    else
        echo "Unable to determine package manager. Please install Python 3 manually."
        python_download_url="https://www.python.org/downloads/"
        open_url "$python_download_url"
        read -n 1 -s -r -p "Press any key to exit..."
        exit 1
    fi
fi

# Check if pip is installed
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    echo "Pip is already installed"
    read -n 1 -s -r -p "Press any key to exit..."
    exit
else
    echo "Pip is not installed. Installing pip..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install python3-pip
    elif command -v brew &> /dev/null; then
        brew install python3-pip
    else
        echo "Unable to determine package manager. Please install pip manually."
        pip_install_url="https://pip.pypa.io/en/stable/installation/"
        open_url "$pip_install_url"
        read -n 1 -s -r -p "Press any key to exit..."
        exit 1
    fi
fi
