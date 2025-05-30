# Use Ultralytics image with Streamlit support
FROM ultralytics/ultralytics:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ Install ffmpeg for video encoding
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy backend and UI code
COPY . .

# Run Streamlit app
CMD ["streamlit", "run", "saveVideo.py", "--server.port=8595", "--server.address=0.0.0.0"]
