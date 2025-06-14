#!/bin/bash
# Configure Kivy to run in a headless environment.
# Source this script before running tests or the app without a display.
export KIVY_NO_ARGS=1
export KIVY_WINDOW=mock

echo "Headless environment variables set: KIVY_WINDOW=$KIVY_WINDOW"

