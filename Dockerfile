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

# Set the working directory for the application
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Expose a port (if your app listens on a port)
EXPOSE 13321

# Set the entrypoint to run your Python application with UV run command
ENTRYPOINT ["uv", "run", "blck.py", "-d"]
