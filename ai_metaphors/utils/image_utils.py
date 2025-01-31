import base64
import os.path
import subprocess
import tempfile
from pathlib import Path

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def create_partial_movies_file_dict(partial_movies_file: Path) -> dict:
    file_dict = {}
    try:
        with partial_movies_file.open() as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                # Extract the path by stripping the prefix "file 'file:" and the trailing "'"
                if line.startswith("file 'file:"):
                    path = line.strip().replace("file 'file:", "").replace("'", "")
                    file_dict[f"{index:02}"] = path
    except FileNotFoundError:
        print(f"Error: File '{partial_movies_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
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
                "select=eq(n\,0)",
                "-vsync",
                "vfr",
                os.path.join(frames_dir, f"{index}_first.jpg"),
            ]
            subprocess.run(command_first_frame, capture_output=True, text=True, check=False)
            key_frames.append(encode_image(os.path.join(frames_dir, f"{index}_first.jpg")))
    return key_frames