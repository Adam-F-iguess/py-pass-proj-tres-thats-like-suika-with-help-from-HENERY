#!/bin/bash

echo "Building Bad Suika Game for macOS..."
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script must be run on macOS"
    exit 1
fi

# Install dependencies if needed
echo "Installing dependencies..."
pip3 install pyinstaller pillow pygame

# Create icon
echo "Creating macOS icon..."
python3 convert_icon_mac.py

# Build the app
echo "Building application..."
pyinstaller bad_suika_game_mac.spec

# Create DMG installer
echo "Creating DMG installer..."
if [ -d "dist/Bad Suika Game.app" ]; then
    # Create temporary directory for DMG contents
    mkdir -p "dmg_contents"
    cp -R "dist/Bad Suika Game.app" "dmg_contents/"
    
    # Create symbolic link to Applications folder
    ln -sf /Applications "dmg_contents/Applications"
    
    # Create the DMG
    hdiutil create -volname "Bad Suika Game" -srcfolder "dmg_contents" -ov -format UDZO "Bad Suika Game Installer.dmg"
    
    # Clean up
    rm -rf "dmg_contents"
    
    echo ""
    echo "Build complete!"
    echo "Created: Bad Suika Game Installer.dmg"
    echo "Users can drag the app to Applications folder to install"
else
    echo "Error: App bundle not found. Build may have failed."
fi