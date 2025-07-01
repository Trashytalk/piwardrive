#!/bin/bash
# Basic cURL examples for PiWardrive API

# Unauthenticated Wi-Fi scan
curl -X GET "http://127.0.0.1:8000/wifi/scan?interface=wlan0" -H "Accept: application/json"

# Wi-Fi scan with POST and bearer token
TOKEN="<your token>"
curl -X POST "http://127.0.0.1:8000/wifi/scan" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"interface": "wlan0"}'
