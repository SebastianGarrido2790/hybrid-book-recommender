# Use official Python 3.12 slim image
FROM python:3.12-slim

# Install uv directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., for build tools if needed by dependencies)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy configuration files to install dependencies 
# Doing this first allows caching the dependency layer
COPY pyproject.toml uv.lock ./

# Install dependencies into the system or a virtual environment
# --frozen ensures we use exact versions from uv.lock
# --system installs into the system python environment (simplifies path, but uv default is venv)
# We will stick to uv's default venv which is robust
RUN uv sync --frozen

# Copy the rest of the application
COPY . .

# Expose the Gradio port
EXPOSE 7860

# Run the application
# uv run will automatically use the environment created by uv sync
CMD ["uv", "run", "app.py"]
