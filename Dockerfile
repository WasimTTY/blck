# Use the official slim version of Debian Bullseye as the base image
FROM debian:bullseye-slim

# Set environment variables to ensure non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list, upgrade packages, install required packages, and clean up
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        python3 \
        python3-pip \
        libev-dev \
        gcc \
        libmagic1 && \
    # Clean up APT cache and remove package lists to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Copy the application code into the container
COPY . .

# Install Python dependencies from the requirements.txt file
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the application port (13321 in this case)
EXPOSE 13321

# Set the entrypoint to run your application with -d (debug) flag
ENTRYPOINT ["python3", "blck.py", "-d"]

