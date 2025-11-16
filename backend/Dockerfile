# Backend Dockerfile for Deepfake Detection System
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with increased timeout and retries
RUN pip install --default-timeout=1000 --retries 5 -r requirements.txt

# Create necessary directories
RUN mkdir -p uploads/images uploads/videos uploads/camera instance

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the application
# Note: In development, the volume mount will overlay this directory
# with your local code, so changes sync automatically
CMD ["python", "app.py"]
