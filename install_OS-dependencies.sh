#!/bin/bash

# Update the system repositories
echo "Updating package repositories..."
sudo apt update -y

# Upgrade all the packages to their latest versions
echo "Upgrading all packages..."
sudo apt upgrade -y

# Function to check if a package is installed and working correctly
check_package() {
  PACKAGE=$1
  INSTALL_CMD="sudo apt install -y $PACKAGE"
  
  # Check if the package is installed
  if dpkg -l | grep -q "^ii  $PACKAGE "; then
    echo "$PACKAGE is already installed."
  else
    echo "$PACKAGE is not installed. Installing..."
    $INSTALL_CMD
  fi
  
  # Check if the package command works (verify correct installation)
  if $2 --version &>/dev/null; then
    echo "$PACKAGE is installed and working correctly."
  else
    echo "$PACKAGE installation failed. Reinstalling..."
    $INSTALL_CMD
  fi
}

# Check and install required packages if not installed
echo "Checking and installing required packages..."

check_package "gcc" "gcc"
check_package "libev-dev" "pkg-config --libs libev"
check_package "python3-dev" "python3-config --configdir"
check_package "python3" "python3"

# Display a message when installation is complete
echo "Package installation complete!"
