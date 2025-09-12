# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run with Uvicorn (production server for FastAPI)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
