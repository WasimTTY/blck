# Use Alpine 3.21.0 as the base image
FROM alpine:3.21.0

# Install necessary dependencies using apk (Alpine package manager)
RUN apk update && apk upgrade && \
    apk add --no-cache \
    curl \
    python3 \
    python3-dev \
    gcc \
    libev-dev \
    libmagic \
    clang \
    build-base \
    && rm -rf /var/cache/apk/*

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
RUN uv add -r requirements.txt

# Expose a port (if your app listens on a port)
EXPOSE 13321

# Set the entrypoint to run your Python application with UV run command
ENTRYPOINT ["uv", "run", "python3", "blck.py", "-d"]
