# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \                  
    libsndfile1 \      
&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/
COPY .env .env

# Set environment variables
ENV PYTHONUNBUFFERED=1
# Optional: makes path explicit
ENV CHROMA_DB_PATH=/app/chroma_db  

# Create volume for persistent Chroma DB
VOLUME ["/app/chroma_db"]

# Expose the FastAPI port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
