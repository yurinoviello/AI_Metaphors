CURRENT_DIR=$(pwd)
FLOAT_MODEL_DIR="$CURRENT_DIR/animations/float_model"
need_to_download_checkpoints=false

if [ ! -d "$FLOAT_MODEL_DIR" ]; then
    mkdir -p "$FLOAT_MODEL_DIR"
    git clone https://github.com/deepbrainai-research/float.git "$FLOAT_MODEL_DIR"
    need_to_download_checkpoints=true
fi

cd "$FLOAT_MODEL_DIR"
pip install -r requirements.txt
pip install "numpy<2.0.0"

if [ "$need_to_download_checkpoints" = true ]; then
  sh download_checkpoints.sh

  pip install gdown huggingface-hub

  huggingface-cli download facebook/wav2vec2-base-960h \
      --local-dir ./checkpoints/wav2vec2-base-960h \
      --local-dir-use-symlinks False

  huggingface-cli download r-f/wav2vec-english-speech-emotion-recognition \
      --local-dir ./checkpoints/wav2vec-english-speech-emotion-recognition \
      --local-dir-use-symlinks False
fi

cd "$CURRENT_DIR"
