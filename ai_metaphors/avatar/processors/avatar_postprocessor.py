import logging
import os
import subprocess
import shutil
from pathlib import Path

class AvatarPostProcessor:
    _AVATAR: str = "avatar"

    _working_dir: Path
    _avatar_dir: Path
    _output_prefix: str = _AVATAR
    _movie_dir: Path
    _high_quality: bool = False
    _avatar_face_file = Path("ai_metaphors/resources/avatar_face.jpg")
    _float_model_dir: Path

    def __init__(self, working_dir: Path, movie_dir: Path, subject_id: str, high_quality: bool):
        self._working_dir = working_dir
        self._movie_dir = movie_dir

        self._avatar_dir = self._working_dir / self._AVATAR / subject_id
        if self._avatar_dir.exists():
            shutil.rmtree(self._avatar_dir)
        self._avatar_dir.mkdir(parents=True, exist_ok=True)

        self._high_quality = high_quality

        self._float_model_dir = self._working_dir / "float_model"

    def _generate_avatar(self):
        output_path = self._avatar_dir / f"Avatar.mp4"
        original_dir = os.getcwd()
        try:
            os.chdir(self._float_model_dir)
            subprocess.run([
                "python", "generate.py",
                "--ref_path", f"../../{self._avatar_face_file}",
                "--aud_path", str(self._movie_dir / "GenScene.wav"),
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
        movie_file = self._movie_dir / "GenScene.mp4"
        avatar_file = self._avatar_dir / f"Avatar.mp4"
        output_path = self._movie_dir / "GenScene_with_Avatar.mp4"
        scale = 300 if self._high_quality else 133
        try:
            subprocess.run([
                "ffmpeg",
                "-y",
                "-i", str(movie_file),
                "-i", str(avatar_file),
                "-filter_complex", f"[1:v]scale=-1:{scale}[overlay]; [0:v][overlay]overlay=1:main_h-overlay_h-1[out]",
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
        self._generate_avatar()
        return self._attach_avatar_to_movie()
