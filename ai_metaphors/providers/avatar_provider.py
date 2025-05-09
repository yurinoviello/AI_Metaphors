import json
import logging
import os
import subprocess
import shutil
from pathlib import Path

from ai_metaphors.providers.grazie_provider import GrazieProvider


class AvatarProvider:
    _AVATAR: str = "avatar"
    _AVATAR_FRAME_DIR: str = "avatar_frames"
    _FPS: int = 12
    _PHRASES_MAPPING_FILE_NAME: str = "phrases.json"

    _working_dir: Path
    _description: str
    _grazie_provider: GrazieProvider

    _avatar_dir: Path
    _output_prefix: str = _AVATAR
    _text_to_dir_name: dict[str, str] = {}
    _narration_text_file: Path
    _narration_audio_dir: Path
    _avatar_video_dir: Path
    _avatar_face_file = Path("ai_metaphors/resources/avatar_face.jpg")
    _float_model_dir: Path
    _phrases_mapping_dir: Path

    def __init__(self, working_dir: Path, description: str, term: dict, grazie_provider: GrazieProvider):
        self._working_dir = working_dir
        self._description = description
        self._grazie_provider = grazie_provider
        self._avatar_dir = self._working_dir / self._AVATAR / term['value'].replace(' ', '_')
        if self._avatar_dir.exists():
            shutil.rmtree(self._avatar_dir)
        self._avatar_dir.mkdir(parents=True, exist_ok=True)
        self._narration_text_file = self._avatar_dir / "narration_text.txt"
        self._narration_audio_dir = self._avatar_dir / "narration_audio"
        self._narration_audio_dir.mkdir(parents=True, exist_ok=True)
        self._float_model_dir = self._working_dir / "float_model"
        self._phrases_mapping_dir = self._avatar_dir / self._PHRASES_MAPPING_FILE_NAME

    def _extract_frames_from_video(self, video_path: Path):
        output_dir = self._avatar_video_dir / self._AVATAR_FRAME_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        output_pattern = output_dir / f"{self._output_prefix}_%04d.png"
        command = [
            "ffmpeg",
            "-i", str(video_path),
            "-vf", f"fps={self._FPS}",
            str(output_pattern)
        ]
        subprocess.run([c for c in command if c], capture_output=True, text=True, check=True)

    def _generate_narration_audio(self, step: str, text: str) -> Path:
        file = self._narration_audio_dir / f"{step}.mp3"
        self._grazie_provider.get_narration_audio(text, file)
        logging.info("Narration audio created for %s step", step)
        return file

    def _generate_avatar(self, step: str, audio_file: Path) -> Path:
        self._avatar_video_dir = self._avatar_dir / f"avatar_video_{step}"
        self._avatar_video_dir.mkdir(parents=True, exist_ok=True)
        output_path = self._avatar_video_dir / f"{step}.mp4"
        original_dir = os.getcwd()
        try:
            os.chdir(self._float_model_dir)
            subprocess.run([
                "python", "generate.py",
                "--ref_path", f"../../{self._avatar_face_file}",
                "--aud_path", str(audio_file),
                "--seed", "15",
                "--a_cfg_scale", "2",
                "--e_cfg_scale", "2",
                "--ckpt_path", "./checkpoints/float.pth",
                "--emo", "neutral",
                "--res_video_path", str(output_path)
            ], check=True)
            logging.info("Avatar generated for %s step", step)
            return output_path
        except subprocess.CalledProcessError as e:
            logging.error("Failed to generate avatar for %s step: %s", step, e)
            raise
        finally:
            os.chdir(original_dir)

    def _save_texts_to_json(self):
        json_str = json.dumps(self._text_to_dir_name, ensure_ascii=False)
        with open(self._phrases_mapping_dir, "w", encoding="utf-8") as f:
            f.write(json_str)

    def generate_avatar_and_break_into_frames(self, texts: list[str]):
        subprocess.run(["sh", "ai_metaphors/resources/setup_float_model.sh"], check=True)

        self._text_to_dir_name = {text: str(i) for i, text in enumerate(texts)}
        self._save_texts_to_json()

        for text, index in self._text_to_dir_name.items():
            audio_file = self._generate_narration_audio(index, text)
            output_path = self._generate_avatar(index, audio_file)
            self._extract_frames_from_video(output_path)
