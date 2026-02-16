import logging
import multiprocessing
import os
import re
from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip
from pytoon.animator import animate

from ai_metaphors.common.output_structure.output_structure import OutputStructure


def _run_pytoon_in_process(working_dir: Path, audio_path: str, transcript: str, video_path: str, fps: int, output_path: str):
    """
    Runs pytoon animation in a separate process to isolate the working directory and 'temp' folder.
    """
    os.chdir(working_dir)
    # Re-import inside the process to ensure isolation if needed, 
    # though it should be fine as it's a separate process.
    animation = animate(audio_file=audio_path, transcript=transcript)
    
    # We also do the export inside the process because it might create temp files too
    background_clip = VideoFileClip(video_path).with_fps(fps).with_duration(animation.duration)
    animation.export(path=output_path, background=background_clip, scale=0.4)


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

    def generate_video_with_avatar(self):
        # Run in a separate process to isolate os.chdir and 'temp' directory
        process = multiprocessing.Process(
            target=_run_pytoon_in_process,
            args=(
                self._working_dir,
                self._audio_path,
                self._get_transcript(),
                self._video_path,
                self._fps,
                self._output_path
            )
        )
        process.start()
        process.join()

        if process.exitcode != 0:
            raise RuntimeError(f"Cartoon avatar generation failed with exit code {process.exitcode}")

        self._rename_output_video()
