FROM python:3.12-slim

# Install PostgreSQL client
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client-17 \
        libpq-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY elt_script.py .
COPY logger_config.py .

CMD ["python", "elt_script.py"]