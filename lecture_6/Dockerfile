# Dockerfile for FastAPI health check application
# Innowise Laboratory - Lecture 6

# Base image with Python 3.9
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application source code
COPY app.py .

# Install required Python packages
RUN pip install --no-cache-dir fastapi uvicorn

# Document that the application uses port 8000
EXPOSE 8000

# Run the FastAPI application with uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]