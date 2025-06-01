FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y wget unzip gnupg2 curl && \
    apt-get install -y chromium chromium-driver && \
    pip install selenium

ENV PATH="/usr/lib/chromium/:$PATH"

COPY . /app
WORKDIR /app

CMD ["python", "keepalive.py"]
