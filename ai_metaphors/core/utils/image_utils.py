import base64
from pathlib import Path


def encode_image(image_path: Path) -> str:
    with image_path.open(mode="rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_key_frames(frames_dir: Path) -> list[str]:
    return [encode_image(image_file) for image_file in frames_dir.iterdir() if image_file.is_file()]
