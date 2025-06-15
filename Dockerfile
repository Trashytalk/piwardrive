FROM python:3.10-bullseye

# install system packages
RUN apt-get update && apt-get install -y \
    git build-essential cmake kismet bettercap gpsd evtest \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
