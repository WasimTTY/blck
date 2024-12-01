# Use Ubuntu as the base image
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    curl \
    python3 \
    python3-pip \
    gcc \
    libev-dev \
    libmagic1 \
    clang \ 
    build-essential \     
    && rm -rf /var/lib/apt/lists/*

# Install UV Astra (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure the UV binary is in the PATH by setting it explicitly
ENV PATH="/root/.local/bin:${PATH}"

# Make sure the env script has execute permissions and then run it
RUN chmod +x /root/.local/bin/env && /root/.local/bin/env

# Display the installed UV version for confirmation
RUN uv version

# Set the working directory for the application
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install Python dependencies from requirements.txt using UV Astra
RUN uv add -r requirements.in

# Expose a port (if your app listens on a port)
EXPOSE 13321

# Set the entrypoint to run your Python application with UV run command
ENTRYPOINT ["uv", "run", "python3", "blck.py", "-d"]
