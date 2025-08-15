# <u>Practice Only</u> (Python and NLP Libraries) On-Premise AI Legal Transcript Processor

## Overview
- Processes meeting transcripts with or without speaker labels or timestamps
- Extracts structured legal and business data
- Generates structured legal documents using Gavel.com's API: [Gavel.com](https://www.gavel.io)
- Runs locally to maintain attorney-client privelege and protect sensitive information
- Implements authentication, encryption, and access control
- Uses the smalles performant open-source LLM for local inference (e.g., Mistral 7B or LLaMA-2-7B-Chat in quantized form)

This tool was developed with the intent of **Practice in Python and Docker**

Hypothetical use cases are: **law firms** and **legal professionals** who's professions demand confidentiality and cannot rely on cloud-based AI tools.

---

## Features
- **Local LLM Inference**
 Uses a small, performant open-source LLM via Hugging Face `transformers` and   `ctransformers` for CPU/GPU on-premise execution.

- **Transcript Processing**
 Handles transcripts with or without speaker labels or timestamps. NLP preprocessing powered by `spacy`.

- **Structured Data Extraction**
 Extacts parties, dates, obligations, monetary amounts, and other key legal entities into JSON

- **Secure Authentication**
 Real user authentication with bcrypt-hashed passwords and role-based access control (RBAC).

- **Encryption**
 AES-256 encryption for stored transcripts.

- **Gavel.com Integration**
 Sends structured data to Gavel templates for instant legal document generation.

- **CLI Tooling**
 Fully usable from the terminal - no GUI required.

- **Dockerized Deployment**
 Runs isolated from your host OS for reproducibility and security.

---

## Structure

.
├── auth.py # Authentication & RBAC \
├── users.db # SQLite database for users \
├── encryption.py # AES-256 encryption utilities \
├── logger.py # Audit logging \
├── nlp.py # NLP preprocessing with spaCy \
├── llm_inference.py # Local LLM integration \
├── gavel_api.py # Gavel.com API integration \
├── structured_data/ # JSON structured data outputs \
├── cli.py # Command line interface \
├── requirements.txt \
├── Dockerfile \
├── docker-compose.yml \
└── README.md 

---

## Prerequisites
- **Docker** & **Docker Compose** installed
- **Gavel.com API credentials**
- At least **8GB RAM** recommended for smooth LLM inference
- Internet connection (for initial dependency & model download only)

---

## Setup Instructions

### Clone the Repository
```bash
git clone <your_repo_url>
cd <your_repo_name>

# .env
GAVEL_API_KEY=your_gavel_api_key_here
SECRET_KEY=your_32_byte_random_secret_key

#build docker image
docker-compose build --no-cache

#create admin 
docker-compose run app python -c "from auth import Auth; Auth().add_user('admin', 'YourPassword123', 'admin')"

#login
docker-compose run app login admin

#upload a transcript
docker-compose run app upload-transcript data/transcript/example.txt

#run full processing pipeline
docker-compose run app run-pipeline example.txt

#view structured data
docker-compose run app view-data example.txt

#submit to gavel
docker-compose run app submit-gavel example.txt "Contract Template Name"

#view logs
docker-compose run app view-logs
```

# Trancscript ex. w/ labels
[00:00:02] John Smith: Let's begin the meeting regarding the contract for ACME Corp. \
[00:00:10] Jane Doe: Yes, the agreed price is $250,000, payable over 12 months. \
[00:00:18] John Smith: ACME will deliver the first batch on October 1, 2025. \

# w/out labels
Let's begin the meeting regarding the contract for ACME Corp. \
Yes, the agreed price is $250,000, payable over 12 months. \
ACME will deliver the first batch on October 1, 2025.
