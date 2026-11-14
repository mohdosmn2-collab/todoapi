# Lightweight official Python base image
FROM python:3.12-slim

# Avoid .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Run as a non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 5000

# Production-grade server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
