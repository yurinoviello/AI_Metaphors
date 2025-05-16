import logging
import os
import subprocess
import shutil
from pathlib import Path

from ai_metaphors.providers.grazie_provider import GrazieProvider


class AvatarProvider:
    _AVATAR: str = "avatar"

    _working_dir: Path
    _grazie_provider: GrazieProvider

    _avatar_dir: Path
    _output_prefix: str = _AVATAR
    _narration_audio_dir: Path
    _avatar_face_file = Path("ai_metaphors/resources/avatar_face.jpg")
    _float_model_dir: Path

    def __init__(self, working_dir: Path, narration_audio_dir: Path, term: dict, grazie_provider: GrazieProvider):
        self._working_dir = working_dir
        self._narration_audio_dir = narration_audio_dir
        self._grazie_provider = grazie_provider
        self._avatar_dir = self._working_dir / self._AVATAR / term['value'].replace(' ', '_')
        if self._avatar_dir.exists():
            shutil.rmtree(self._avatar_dir)
        self._avatar_dir.mkdir(parents=True, exist_ok=True)
        self._float_model_dir = self._working_dir / "float_model"

    def _generate_avatar(self):
        output_path = self._avatar_dir / f"Avatar.mp4"
        original_dir = os.getcwd()
        try:
            os.chdir(self._float_model_dir)
            subprocess.run([
                "python", "generate.py",
                "--ref_path", f"../../{self._avatar_face_file}",
                "--aud_path", str(self._narration_audio_dir / "GenScene.wav"),
                "--seed", "15",
                "--a_cfg_scale", "2",
                "--e_cfg_scale", "2",
                "--ckpt_path", "./checkpoints/float.pth",
                "--emo", "neutral",
                "--res_video_path", str(output_path)
            ], check=True)
            logging.info("Avatar generated and saved in %s", str(output_path))
        except subprocess.CalledProcessError as e:
            logging.error("Failed to generate avatar")
            raise
        finally:
            os.chdir(original_dir)

    def _attach_avatar_to_movie(self):
        movie_file = self._narration_audio_dir / "GenScene.mp4"
        avatar_file = self._avatar_dir / f"Avatar.mp4"
        output_path = self._narration_audio_dir / "GenScene_with_avatar.mp4"
        try:
            subprocess.run([
                "ffmpeg",
                "-i", str(movie_file),
                "-i", str(avatar_file),
                "-filter_complex", "[1:v]scale=300:300[overlay]; [0:v][overlay]overlay=1:main_h-300-1[out]",
                "-map", "[out]",
                "-map", "0:a",
                "-c:v", "libx264",
                "-crf", "18",
                "-preset", "slow",
                "-c:a", "copy",
                str(output_path)
            ], check=True)
            logging.info("Avatar attached")
            return output_path
        except subprocess.CalledProcessError as e:
            logging.error("Failed to generate avatar")
            raise



    def generate_avatar_and_attach_to_movie(self) -> Path:
        subprocess.run(["sh", "ai_metaphors/resources/setup_float_model.sh"], check=True)

        self._generate_avatar()
        return self._attach_avatar_to_movie()