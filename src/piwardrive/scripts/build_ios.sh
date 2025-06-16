#!/bin/bash
# Build PiWardrive for iOS using kivy-ios
#
# Required tools:
#   - python3 and pip
#   - Xcode command line tools
#   - the 'toolchain' command from kivy-ios
# This script installs missing Python packages before invoking the
# kivy-ios toolchain.
set -e

packages=(kivy-ios sh pbxproj cookiecutter)
for pkg in "${packages[@]}"; do
    if ! pip show "$pkg" >/dev/null 2>&1; then
        pip install --quiet "$pkg"
    fi
done

toolchain create piwardrive ios-build || true
toolchain build python3 kivy kivymd
toolchain pip install -r requirements.txt
