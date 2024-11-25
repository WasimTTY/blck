# Use the official slim version of Debian Bullseye as the base image
FROM debian:bullseye-slim

# Update the package list, install required packages, and clean up
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

# Set the working directory (optional, depending on your use case)
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Copy the application code into the container
COPY . .

# Install Python dependencies from the requirements.txt file
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the entrypoint for your application
ENTRYPOINT ["python3", "blck.py"]
