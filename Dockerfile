# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=QAU_API.settings

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# # Create media directory for file uploads
# RUN mkdir -p /app/media && chmod 777 /app/media

# Collect static files
# RUN python QAU_API/manage.py collectstatic --noinput

# # Run gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "QAU_API.wsgi:application"]
