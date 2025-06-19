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

ENV NLTK_DATA=/usr/share/nltk_data
RUN mkdir -p $NLTK_DATA && chmod -R 777 $NLTK_DATA
RUN python -m nltk.downloader -d $NLTK_DATA averaged_perceptron_tagger_eng

RUN mkdir -p /app/animations
