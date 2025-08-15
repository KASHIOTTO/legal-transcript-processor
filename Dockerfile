From python:3.9-slim

# Set dir
WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy src code
COPY . .

ENTRYPOINT ["python", "cli.py"]