import logging
import os
import re
import subprocess
from pathlib import Path

from starlette.concurrency import run_in_threadpool

from ai_metaphors import PROJECT_ROOT
from ai_metaphors.common.output_structure.output_structure import OutputStructure
from ai_metaphors.common.utils.gpu_lock import GPULock
from ai_metaphors.server.settings.settings import settings


class CartoonAvatarProcessor:
    _one_line_story: str
    _description: str
    _video_path: str
    _audio_path: str
    _output_path: str
    _fps: int
    _working_dir: Path

    def __init__(self,
                 description: str,
                 one_line_story: str,
                 output_structure: OutputStructure,
                 working_dir: Path):
        self._one_line_story = one_line_story
        self._description = description
        self._video_path = str(output_structure.get_final_video_path())
        self._audio_path = str(output_structure.get_final_audio_path())
        self._output_path = str(output_structure.get_video_directory() / f"temp.{output_structure.get_video_format()}")
        self._fps = output_structure.get_fps()
        self._working_dir = working_dir

    def _get_transcript(self):
        narration_text_matches \
            = re.findall(r'\*\*Narrator Emotions\*\*:\s*```(.*?)```', self._description, re.DOTALL)
        narration_text_joined \
            = " ".join(
                [f"<explain> {self._one_line_story}"] +
                narration_text_matches +
                ["<happy> Thanks for watching!"]
            )
        logging.debug(f"Transcript generated:\n{narration_text_joined}")
        return narration_text_joined

    def _rename_output_video(self):
        Path(self._video_path).unlink()
        Path(self._output_path).rename(Path(self._output_path).parent / "GenScene.mp4")

    async def generate_video_with_avatar(self):
        # Use subprocess to run the generation in a completely isolated environment
        env = os.environ.copy()
        fraction = settings.GPU_FRACTION
        env["CUDA_MEMORY_FRACTION"] = str(fraction)
        env["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64,garbage_collection_threshold:0.8"

        script_path = PROJECT_ROOT / "common/avatar/processors/run_cartoon_avatar.py"

        command = [
            "python", str(script_path),
            "--audio_path", self._audio_path,
            "--transcript", self._get_transcript(),
            "--video_path", self._video_path,
            "--output_path", self._output_path,
            "--fps", str(self._fps),
            "--working_dir", str(self._working_dir),
            "--fraction", str(fraction)
        ]

        async with GPULock():
            try:
                await run_in_threadpool(subprocess.run, command, check=True, env=env)
                logging.info("Cartoon avatar generation subprocess completed successfully.")
            except Exception as e:
                logging.error(f"Cartoon avatar generation failed: {e}")
                raise

        self._rename_output_video()
