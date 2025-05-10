FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libpango1.0-dev \
    portaudio19-dev \
    sox \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN mkdir -p /app/animations
