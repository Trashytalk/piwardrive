#!/bin/bash
# Build PiWardrive for iOS using kivy-ios
set -e
pip install --quiet kivy-ios sh pbxproj cookiecutter
toolchain create piwardrive ios-build || true
toolchain build python3 kivy kivymd
toolchain pip install -r requirements.txt
