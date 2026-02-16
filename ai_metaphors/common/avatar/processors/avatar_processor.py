import json
import logging
import os
import shutil
import subprocess
from pathlib import Path

from starlette.concurrency import run_in_threadpool

from ai_metaphors import PROJECT_ROOT
from ai_metaphors.common.core.providers import GrazieProvider
from ai_metaphors.common.utils.gpu_lock import GPULock
from ai_metaphors.server.settings.settings import settings


class AvatarProcessor:
    _AVATAR: str = "avatar"
    _AVATAR_FRAME_DIR: str = "avatar_frames"
    _FPS: int = 12
    _PHRASES_MAPPING_FILE_NAME: str = "phrases.json"

    _working_dir: Path
    _description: str

    _avatar_dir: Path
    _output_prefix: str = _AVATAR
    _text_to_dir_name: dict[str, str] = {}
    _narration_text_file: Path
    _narration_audio_dir: Path
    _avatar_video_dir: Path
    _avatar_face_file = PROJECT_ROOT / "resources/avatar_face.jpg"
    _float_model_dir: Path
    _phrases_mapping_dir: Path
    _task_id: str | None

    def __init__(self, working_dir: Path, description: str, subject_id: str, task_id: str | None = None):
        self._working_dir = working_dir
        self._task_id = task_id
        self._description = description
        self._avatar_dir = self._working_dir / self._AVATAR / subject_id
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
        GrazieProvider.get_narration_audio(text, file)
        logging.debug(f"Narration audio created for {step} step")
        return file

    async def _generate_avatar(self, step: str, audio_file: Path) -> Path:
        self._avatar_video_dir = self._avatar_dir / f"avatar_video_{step}"
        self._avatar_video_dir.mkdir(parents=True, exist_ok=True)
        output_path = self._avatar_video_dir / f"{step}.mp4"
        
        ref_path = str(self._avatar_face_file)

        env = os.environ.copy()
        fraction = settings.GPU_FRACTION
        env["CUDA_MEMORY_FRACTION"] = str(fraction)
        env["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64,garbage_collection_threshold:0.8"

        script_path = PROJECT_ROOT / "common/avatar/processors/run_avatar.py"

        command = [
            "python", str(script_path),
            "--ref_path", ref_path,
            "--aud_path", str(audio_file),
            "--res_video_path", str(output_path),
            "--working_dir", str(self._float_model_dir),
            "--fraction", str(fraction)
        ]
            
        try:
            await run_in_threadpool(subprocess.run, command, check=True, env=env)
            logging.debug(f"Avatar generated for {step} step")
            return output_path
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to generate avatar for {step} step:\n{e}")
            raise

    def _save_texts_to_json(self):
        json_str = json.dumps(self._text_to_dir_name, ensure_ascii=False)
        with open(self._phrases_mapping_dir, "w", encoding="utf-8") as f:
            f.write(json_str)

    async def generate_avatar_and_break_into_frames(self, texts: list[str]):
        if self._task_id is None:
            subprocess.run(["sh", "ai_metaphors/resources/setup_float_model.sh"], check=True)
        else:
            subprocess.run(["sh", "ai_metaphors/resources/setup_float_model.sh", self._task_id], check=True)
        self._text_to_dir_name = {text: str(i) for i, text in enumerate(texts)}
        self._save_texts_to_json()

        async with GPULock():
            for text, index in self._text_to_dir_name.items():
                audio_file = self._generate_narration_audio(index, text)
                output_path = await self._generate_avatar(index, audio_file)
                self._extract_frames_from_video(output_path)
