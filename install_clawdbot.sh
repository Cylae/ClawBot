#!/bin/bash

# Installation script for ClawdBot (OpenClaw / Moltbot)
# Note: This script is a template. You must update the REPO_URL variable
# with the actual GitHub repository URL once it is known.

# Configuration
REPO_URL="https://github.com/EXEMPLE/clawdbot-repo.git" # <--- UPDATE HERE
INSTALL_DIR="${INSTALL_DIR:-clawdbot_install}"

# Exit immediately if a command fails, treat unset variables as an error, and catch pipe failures
set -euo pipefail

echo "=================================================="
echo "   ClawdBot Installation (Sandbox Mode)"
echo "=================================================="

# 1. Check prerequisites
echo "[1/4] Checking necessary tools..."

if ! command -v git &> /dev/null; then
    echo "ERROR: git is not installed."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed."
    exit 1
fi

echo "Detected tools: Git and Python3."

# 2. Clone repository
echo "[2/4] Preparing project directory..."

if [ -d "$INSTALL_DIR" ]; then
    echo "The directory '$INSTALL_DIR' already exists."
else
    # NOTE: In a real scenario, uncomment the following line:
    # git clone "$REPO_URL" "$INSTALL_DIR" || exit 1

    # For demonstration, we create the directory manually
    echo "Simulating cloning of $REPO_URL..."
    mkdir -p "$INSTALL_DIR" || { echo "ERROR: Cannot create directory $INSTALL_DIR."; exit 1; }

    # Creating dummy files to simulate repository content
    echo "requests" > "$INSTALL_DIR/requirements.txt"
    echo "openai" >> "$INSTALL_DIR/requirements.txt"
    echo "anthropic" >> "$INSTALL_DIR/requirements.txt"
    echo "python-dotenv" >> "$INSTALL_DIR/requirements.txt"

    echo "print('ClawdBot successfully started!')" > "$INSTALL_DIR/main.py"

    echo "Directory created and files simulated."
fi

# 3. Configure virtual environment
echo "[3/4] Configuring Python virtual environment..."

cd "$INSTALL_DIR" || { echo "ERROR: Cannot access $INSTALL_DIR."; exit 1; }

if [ ! -d "venv" ]; then
    python3 -m venv venv || { echo "ERROR: Cannot create virtual environment."; exit 1; }
    echo "Virtual environment 'venv' created."
else
    echo "The virtual environment already exists."
fi

# 4. Install dependencies
echo "[4/4] Installing dependencies..."

# Activate virtual environment
source venv/bin/activate || { echo "ERROR: Cannot activate virtual environment."; exit 1; }

# Check if dependencies need to be installed or updated
MARKER_FILE="venv/.installed"

if [ ! -f "$MARKER_FILE" ] || [ "requirements.txt" -nt "$MARKER_FILE" ]; then
    # Upgrade pip
    pip install --upgrade pip > /dev/null 2>&1 || true

    # Install from requirements.txt
    if [ -f "requirements.txt" ]; then
        echo "Installing packages listed in requirements.txt..."
        pip install -r requirements.txt || { echo "ERROR: Cannot install dependencies."; exit 1; }
        touch "$MARKER_FILE"
    else
        echo "No requirements.txt file found."
    fi
else
    echo "Dependencies are already up-to-date."
fi

echo ""
echo "=================================================="
echo "   Installation completed!"
echo "=================================================="
echo "To start the bot:"
echo "1. cd $INSTALL_DIR"
echo "2. source venv/bin/activate"
echo "3. python main.py"
echo ""
echo "Do not forget to configure your API keys (often in a .env file)."
