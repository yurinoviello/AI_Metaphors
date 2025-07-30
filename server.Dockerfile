FROM pytorch/pytorch:2.7.1-cuda11.8-cudnn9-runtime

ARG PORT=8898
ENV PORT=${PORT}

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libpango1.0-dev \
    portaudio19-dev \
    nvidia-cuda-toolkit \
    sox \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir --compile -r requirements.txt

COPY . .

EXPOSE ${PORT}

ENV NLTK_DATA=/usr/share/nltk_data
ENV PYTHONPATH=/app

RUN mkdir -p /app/animations && chmod -R 777 /app
RUN mkdir -p $NLTK_DATA && chmod -R 777 $NLTK_DATA
RUN mkdir /.cache && chmod -R 777 /.cache
RUN mkdir /.triton && chmod -R 777 /.triton
RUN mkdir /.local && chmod -R 777 /.local
RUN python -m nltk.downloader -d $NLTK_DATA averaged_perceptron_tagger_eng
RUN python -m nltk.downloader -d $NLTK_DATA averaged_perceptron_tagger
RUN python -m nltk.downloader -d $NLTK_DATA cmudict

RUN chmod +x /app/ai_metaphors/resources/setup_float_model.sh
RUN /app/ai_metaphors/resources/setup_float_model.sh

# RUN python -m ai_metaphors.server.db.init_db

COPY --chown=1001:1001 entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
