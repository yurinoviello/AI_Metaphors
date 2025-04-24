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
COPY . .

RUN mkdir -p /app/animations
VOLUME /app/animations

ENTRYPOINT ["python", "-m", "ai_metaphors.main", "--bin-directory", "/usr/local/bin"]
CMD []