# syntax=docker/dockerfile:1
# check=error=true

# Test stage
FROM python:3.11-alpine AS tester
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest
COPY . .
CMD ["pytest", "tests/"]

# Production stage
FROM python:3.11-alpine AS production
WORKDIR /app
RUN apk add --no-cache gcc musl-dev libffi-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]