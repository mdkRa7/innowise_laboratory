"""
FastAPI Health Check Application

This module provides a simple FastAPI application with a single health check endpoint.
It's designed to be containerized using Docker as part of the Innowise laboratory assignment.
"""

import uvicorn
from fastapi import FastAPI
from typing import Dict

# Initialize FastAPI application
app = FastAPI(
    title="Health Check API",
    description="A simple FastAPI application for health monitoring",
    version="1.0.0"
)


@app.get("/healthcheck", tags=["Health"], summary="Check service health")
async def healthcheck() -> Dict[str, str]:
    """
    Health check endpoint

    Returns:
        Dict[str, str]: A dictionary containing the service status.

    Example Response:
        {"status": "ok"}
    """
    return {"status": "ok"}


if __name__ == "__main__":
    """
    Entry point for local development.

    This allows running the application directly with: python app.py
    In Docker environment, the application is launched via uvicorn command.
    """
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,  # Standard FastAPI port
        reload=True  # Enable auto-reload during development
    )