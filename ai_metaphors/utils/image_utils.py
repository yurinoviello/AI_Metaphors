import base64
from pathlib import Path
import subprocess
import tempfile


def encode_image(image_path: Path) -> str:
    with image_path.open(mode="rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def create_partial_movies_file_dict(partial_movies_file: Path) -> dict:
    file_dict = {}
    try:
        with partial_movies_file.open() as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                # Extract the path by stripping the prefix "file 'file:" and the trailing "'"
                if line.startswith("file 'file:"):
                    path = line.strip().replace("file 'file:", "").replace("'", "")
                    file_dict[f"{index:02}"] = Path(path)
    except FileNotFoundError:
        print(f"Error: File '{partial_movies_file}' not found.")
    return file_dict


def extract_key_frames(file_dict: dict) -> list[str]:
    key_frames = []
    with tempfile.TemporaryDirectory() as frames_dir:
        for index, value in file_dict.items():
            command_first_frame = [
                "ffmpeg",
                "-i",
                value,
                "-vf",
                r"select=eq(n\,0)",
                "-vsync",
                "vfr",
                (Path(frames_dir) / f"{index}_first.jpg").as_posix(),
            ]
            subprocess.run(command_first_frame, capture_output=True, text=True, check=False)
            key_frames.append(encode_image(Path(frames_dir) / f"{index}_first.jpg"))
    return key_frames
