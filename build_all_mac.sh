#!/bin/bash

echo "Building Bad Suika Game for macOS - All Formats"
echo "=============================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script must be run on macOS"
    exit 1
fi

# Run the main build
echo "Step 1: Building the app..."
chmod +x build_mac.sh
./build_mac.sh

# Create PKG installer
echo "Step 2: Creating PKG installer..."
chmod +x create_pkg_installer.sh
./create_pkg_installer.sh

echo ""
echo "Build complete! Created:"
echo "- Bad Suika Game Installer.dmg (drag-and-drop installer)"
echo "- Bad Suika Game.pkg (traditional installer)"
echo ""
echo "Distribute either file to your friends on macOS!"