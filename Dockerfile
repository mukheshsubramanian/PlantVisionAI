# PlantVision AI - Production Container
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy application files
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
COPY samples/ /app/samples/
COPY model/ /app/model/
COPY disease_info.json /app/disease_info.json
COPY run.py /app/run.py

# Default Environment Variables
ENV HOST=0.0.0.0
ENV PORT=8000
ENV RELOAD=false
ENV NO_BROWSER=true
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI application
CMD ["python", "run.py"]
