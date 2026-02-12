CURRENT_DIR=$(pwd)
if [ $# -eq 1 ]; then
    TASK_ID=$1
    FLOAT_MODEL_DIR="$CURRENT_DIR/animations/$TASK_ID/float_model"
else
    FLOAT_MODEL_DIR="$CURRENT_DIR/animations/float_model"
fi

if [ ! -d "$FLOAT_MODEL_DIR" ] || [ ! -d "$FLOAT_MODEL_DIR/checkpoints/wav2vec2-base-960h" ]; then

    if [ ! -d "$FLOAT_MODEL_DIR" ]; then
        mkdir -p "$FLOAT_MODEL_DIR"
        git clone https://github.com/yurinoviello/float.git "$FLOAT_MODEL_DIR"
    fi

    cd "$FLOAT_MODEL_DIR" || exit

    huggingface-cli download facebook/wav2vec2-base-960h \
        --local-dir ./checkpoints/wav2vec2-base-960h \
        --local-dir-use-symlinks False

    huggingface-cli download r-f/wav2vec-english-speech-emotion-recognition \
        --local-dir ./checkpoints/wav2vec-english-speech-emotion-recognition \
        --local-dir-use-symlinks False
else
    echo "Checkpoints already exist in $FLOAT_MODEL_DIR. Skipping download."
    cd "$FLOAT_MODEL_DIR" || exit
fi

cd "$CURRENT_DIR"