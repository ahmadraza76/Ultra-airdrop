FROM python:3.11-buster

WORKDIR /app

# Update package list and install essential system packages for Python C extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create logs and data directories to prevent FileNotFoundError
RUN mkdir -p logs data
RUN chmod -R 777 /app/data
RUN chmod -R 777 /app/logs

CMD ["python", "bot.py"]