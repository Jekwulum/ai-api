FROM python:3.11-slim

# Install Ollama dependencies
RUN apt-get update && apt-get install -y curl libmupdf-dev supervisor && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Preload TinyLlama model
RUN ollama pull tinyllama

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

CMD ["/usr/bin/supervisord"]
