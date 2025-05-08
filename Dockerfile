# --- Base image ---
FROM python:3.13-alpine AS base
WORKDIR /app

# --- Builder stage ---
FROM base AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# Install dependencies
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

# Install app
COPY src /app/src
COPY LICENSE README.md /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# --- Final image ---
FROM base

# Copy the application and dependencies from the builder stage
COPY --from=builder /app /app

# Activate the virtual environment manually
ENV PATH="/app/.venv/bin:$PATH"

# Set the stopsignal
STOPSIGNAL SIGINT

# Set the command
CMD ["app"]
