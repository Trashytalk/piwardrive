FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential libdbus-1-dev libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY . .
RUN pip install --no-cache-dir -e .

CMD ["pytest"]

