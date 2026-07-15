FROM python:3.10-slim

# Install system dependencies for audio processing and download tools
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    espeak-ng \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pre-download Kokoro model assets to bake them into the Docker image
RUN curl -L -f -o model.onnx "https://github.com/thewh1teagle/kokoro-onnx/releases/download/v0.2.0/kokoro-v0.19.onnx"
RUN curl -L -f -o voices.json "https://github.com/thewh1teagle/kokoro-onnx/releases/download/v0.2.0/voices.json"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
