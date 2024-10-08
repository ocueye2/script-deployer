#!/bin/bash

# Exit script on any error
set -e

# Function to print messages
log() {
  echo "[INFO] $1"
}

# Update package lists and install Python venv if not already installed
log "Updating package lists..."
sudo apt update


# Check if Python3.10 is installed
if ! command -v python3.10 &>/dev/null; then
    log "Python 3.10 could not be found. Installing Python 3.10 from savoury1"
    sudo add-apt-repository ppa:savoury1/python
    sudo apt update
    sudo apt-get install python3.10
else
    log "Python 3.10 is already installed."
fi

# Create a virtual environment named .venv if it doesn't already exist
if [ ! -d ".venv" ]; then
    log "Creating virtual environment..."
    python3.10 -m venv .venv
else
    log "Virtual environment already exists. Skipping creation."
fi

# Activate the virtual environment
log "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip to the latest version
log "Upgrading pip..."
pip install --upgrade pip

# Install CherryPy and Mako
log "Installing required packages..."
pip install cherrypy mako

# Run the Python script
log "Running the Python script..."
python run.py

log "Script execution completed."
