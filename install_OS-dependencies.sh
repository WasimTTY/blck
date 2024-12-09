#!/bin/bash

# Update the system repositories
echo "Updating package repositories..."
sudo apt update -y

# Upgrade all the packages to their latest versions
echo "Upgrading all packages..."
sudo apt upgrade -y

# Install the required packages
echo "Installing required packages..."
sudo apt install -y gcc libev-dev python3-dev python3

# Display a message when installation is complete
echo "Package installation complete!"
