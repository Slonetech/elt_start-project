FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client-17 \
        libpq-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY elt_script.py .

CMD ["python", "elt_script.py"]