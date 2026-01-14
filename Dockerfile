# Stage 1: Build CSS using Node.js
FROM node:20-slim AS builder
WORKDIR /app

# Copy only files needed for npm install
COPY package.json package-lock.json ./
RUN npm ci

# Copy configuration and source files needed for Tailwind build
COPY tailwind.config.js postcss.config.js ./
COPY static/css/input.css ./static/css/
# Copy templates because Tailwind scans them for class names
COPY app/templates ./app/templates

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
RUN uv sync --frozen --no-dev --no-install-project

# Copy only necessary application files
COPY main.py .
COPY app ./app
COPY static ./static

# Copy built CSS from builder stage (overwriting static/css/style.css if it exists from previous copy)
COPY --from=builder /app/static/css/style.css ./static/css/style.css

# Set environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
