FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "keepalive.py"]
