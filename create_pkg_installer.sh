#!/bin/bash

echo "Creating PKG installer for Bad Suika Game..."

# Check if app exists
if [ ! -d "dist/Bad Suika Game.app" ]; then
    echo "Error: App not found. Run build_mac.sh first."
    exit 1
fi

# Create package structure
mkdir -p "pkg_build/Applications"
cp -R "dist/Bad Suika Game.app" "pkg_build/Applications/"

# Create package info
cat > "pkg_info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>com.yourname.badsuikagame</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
</dict>
</plist>
EOF

# Build the package
pkgbuild --root "pkg_build" --identifier "com.yourname.badsuikagame" --version "1.0.0" --install-location "/" "Bad Suika Game.pkg"

# Clean up
rm -rf "pkg_build"
rm "pkg_info.plist"

echo "PKG installer created: Bad Suika Game.pkg"