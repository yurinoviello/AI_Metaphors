import logging
import re
from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip
from pytoon.animator import animate

from ai_metaphors.core.output_structure.output_structure import OutputStructure


class CartoonAvatarProcessor:
    _one_line_metaphor: str
    _description: str
    _video_path: str
    _audio_path: str
    _output_path: str
    _fps: int

    def __init__(self,
                 description: str,
                 one_line_metaphor: str,
                 output_structure: OutputStructure):
        self._one_line_metaphor = one_line_metaphor
        self._description = description
        self._video_path = str(output_structure.get_final_video_path())
        self._audio_path = str(output_structure.get_final_audio_path())
        self._output_path = str(output_structure.get_video_directory() / f"temp.{output_structure.get_video_format()}")
        self._fps = output_structure.get_fps()

    def _get_transcript(self):
        narration_text_matches \
            = re.findall(r'\*\*Narrator Emotions\*\*:\s*```(.*?)```', self._description, re.DOTALL)
        narration_text_joined \
            = " ".join(
                [f"<explain> {self._one_line_metaphor}"] +
                narration_text_matches +
                ["<happy> Thanks for watching!"]
            )
        logging.info("Transcript generated")
        logging.info("Transcript: %s", narration_text_joined)
        return narration_text_joined

    def _rename_output_video(self):
        Path(self._video_path).unlink()
        Path(self._output_path).rename(Path(self._output_path).parent / "GenScene.mp4")

    def generate_video_with_avatar(self):
        animation = animate(audio_file=self._audio_path, transcript=self._get_transcript(), fps=self._fps)
        background_clip = VideoFileClip(self._video_path).with_duration(animation.duration)
        animation.export(path=self._output_path, background=background_clip)
        self._rename_output_video()
