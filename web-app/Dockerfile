# Dockerfile for Voice Logger Web App
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Copy app files
COPY app.py .
COPY templates/ ./templates/

# Create logs directory
RUN mkdir -p /data/obsidian

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
