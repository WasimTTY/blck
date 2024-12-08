#!/bin/bash

# Update the system repositories
echo "Updating package repositories..."
sudo apt update -y

# Upgrade all the packages to their latest versions
echo "Upgrading all packages..."
sudo apt upgrade -y

# Function to check if a package is installed
check_package_installed() {
  if dpkg -l | grep -q "^ii  $1 "; then
    echo "$1 is already installed."
  else
    echo "$1 is not installed. Installing..."
    sudo apt install -y $1
  fi
}

# Function to check if a package is correctly installed (for gcc, libev-dev, python3-dev)
check_package_version() {
  PACKAGE=$1
  COMMAND=$2
  if $COMMAND --version &>/dev/null; then
    echo "$PACKAGE is installed correctly."
  else
    echo "$PACKAGE is not installed correctly. Installing..."
    sudo apt install -y $PACKAGE
  fi
}

# Check and install required packages if not installed
echo "Checking and installing required packages..."

check_package_installed "gcc"
check_package_installed "libev-dev"
check_package_installed "python3-dev"
check_package_installed "python3"

# Check if gcc is working correctly
echo "Verifying gcc installation..."
check_package_version "gcc" "gcc"

# Check if libev-dev is working correctly
echo "Verifying libev-dev installation..."
check_package_version "libev-dev" "pkg-config --libs libev"

# Check if python3-dev is working correctly
echo "Verifying python3-dev installation..."
check_package_version "python3-dev" "python3-config --configdir"

# Check if Python3 is working correctly
echo "Verifying Python3 installation..."
python3 --version

# Display a message when installation is complete
echo "Package installation complete!"
