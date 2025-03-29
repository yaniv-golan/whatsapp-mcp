#!/bin/bash

# WhatsApp MCP Authentication Script
# This script runs only the Go application to display a QR code for WhatsApp authentication

echo "Starting WhatsApp authentication..."
echo "Please scan the QR code with your WhatsApp mobile app when it appears."
echo "After starting the script it might take a few minutes to load your messages."
echo "========================================================================="

# Go to the project directory
cd "$(dirname "$0")"

# Run the Go application to show QR code
cd whatsapp-bridge
go run main.go
