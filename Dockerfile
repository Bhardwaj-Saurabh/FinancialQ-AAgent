FROM python:3.11-slim

# Copy UV binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files and sync env
COPY uv.lock pyproject.toml README.md ./
RUN uv sync --frozen --no-cache

# Copy your application code
COPY src/ragagent ragagent/
COPY run run/

# Run with uv ensuring correct venv
CMD ["uv", "run", "uvicorn", "ragagent.infra.app:app", "--host", "0.0.0.0", "--port", "8000"]
