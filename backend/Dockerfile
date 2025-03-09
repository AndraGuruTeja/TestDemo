FROM python:3.9-slim

WORKDIR /app

# In backend/Dockerfile
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Add pip upgrade before installing requirements
RUN pip install --upgrade pip

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app /app/app
COPY backend/tests /app/tests
COPY backend/pyproject.toml /app/

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]