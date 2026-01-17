# Stage 1: Build CSS using Node.js
FROM node:20-slim AS builder
WORKDIR /app

# Copy only files needed for npm install
COPY package*.json ./
RUN npm install

# Copy configuration and source files needed for Tailwind build
COPY tailwind.config.js postcss.config.js ./
COPY static/css/input.css ./static/css/
# Copy templates because Tailwind scans them for class names
COPY app/templates ./app/templates
COPY static/js ./static/js

RUN npm run build:css

# Stage 2: Python Application
FROM python:3.12-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy only necessary application files
COPY main.py .
COPY app ./app
COPY static ./static

# Copy built CSS from builder stage (overwriting static/css/style.css if it exists from previous copy)
COPY --from=builder /app/static/css/style.css ./static/css/style.css

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV HOST=0.0.0.0

# Run the application
# Use shell form to allow variable expansion for $PORT and $HOST
CMD ["sh", "-c", "uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8080}"]
