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

RUN python -m pip install -U pip "setuptools<81" wheel

COPY constraints.txt ./
RUN python -m pip install --retries 3 --no-cache-dir --no-build-isolation openai-whisper==20230314 -c constraints.txt

COPY requirements.txt ./
RUN python -m pip install --retries 3 --no-cache-dir --compile -r requirements.txt -c constraints.txt

ENV NLTK_DATA=/usr/share/nltk_data
RUN mkdir -p $NLTK_DATA && chmod -R 777 $NLTK_DATA
RUN python -m nltk.downloader -d $NLTK_DATA averaged_perceptron_tagger_eng
RUN python -m nltk.downloader -d $NLTK_DATA cmudict

RUN mkdir -p /app/animations
