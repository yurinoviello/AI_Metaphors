import json
import re
import subprocess
import shutil
from pathlib import Path

class AvatarProvider:
    _AVATAR: str = "avatar"
    _AVATAR_FRAME_DIR: str = "avatar_frame"
    _FPS: int = 12
    _PHRASES_MAPPING_FILE_NAME: str = "phrases.json"

    _working_dir: Path
    _description: str
    _avatar_dir: Path
    _output_prefix: str = _AVATAR
    _avatar_file_name: str = f"{_AVATAR}.mp4"
    _text_to_dir_name: dict[str, str] = {}

    def __init__(self, working_dir: Path, description: str, term_name: str):
        self._working_dir = working_dir
        self._description = description
        self._avatar_dir = self._working_dir / self._AVATAR / term_name
        if self._avatar_dir.exists():
            shutil.rmtree(self._avatar_dir)
        self._avatar_dir.mkdir(parents=True, exist_ok=True)

    def _extract_frames_from_video(self, video_path: Path, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)
        output_pattern = output_dir / f"{self._output_prefix}_%04d.png"
        command = [
            "ffmpeg",
            "-i", str(video_path),
            "-vf", f"fps={self._FPS}",
            str(output_pattern)
        ]
        subprocess.run([c for c in command if c], capture_output=True, text=True, check=True)

    def _generate_avatar(self, text: str):
        output_path = self._avatar_dir / self._text_to_dir_name[text]
        output_path.mkdir(parents=True, exist_ok=True)
        raise NotImplementedError # TODO: generate and save in output_path

    def _extract_spoken_phrases(self) -> list[str]:
        # TODO: maybe using a model to get the text that needs to be voiced
        pattern = r'"([^"\n]+)"'
        return re.findall(pattern, self._description, flags=re.IGNORECASE)

    def _save_texts_to_json(self):
        output_path = self._avatar_dir / self._PHRASES_MAPPING_FILE_NAME
        json_str = json.dumps(self._text_to_dir_name, ensure_ascii=False)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)

    def generate_avatar_and_break_into_frames(self):
        texts = self._extract_spoken_phrases()
        self._text_to_dir_name = {text: f"text_{i + 1}" for i, text in enumerate(texts)}
        self._save_texts_to_json()

        for text in texts:
            self._generate_avatar(text)
            dir_name = self._avatar_dir / self._text_to_dir_name[text]
            avatar_path = dir_name / self._avatar_file_name
            output_dir = dir_name / self._AVATAR_FRAME_DIR
            self._extract_frames_from_video(avatar_path, output_dir)
