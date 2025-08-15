From python:3.9-slim

# Set working directory
WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy all source code
COPY . .

# Default command (this means you can use `docker-compose run app <cli_command>`)
ENTRYPOINT ["python", "cli.py"]