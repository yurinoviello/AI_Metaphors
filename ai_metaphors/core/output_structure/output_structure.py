from dataclasses import dataclass
from pathlib import Path

@dataclass
class OutputStructure:
    _scene_name = "GenScene"
    _video_format = "mp4"
    _audio_format = "wav"
    _quality: str
    _fps: int
    _final_video_path: Path
    _final_audio_path: Path
    _video_directory: Path

    def __init__(self, working_dir: Path, subject_id: str, high_quality: bool = False,):
        self._quality = "1080p60" if high_quality else "480p15"
        self._fps = 60 if high_quality else 15
        self._video_directory = working_dir / "media" / "videos" / subject_id / self._quality
        self._final_video_path = self._video_directory / f"{self._scene_name}.{self._video_format}"
        self._final_audio_path = self._video_directory / f"{self._scene_name}.{self._audio_format}"

    def get_video_format(self):
        return self._video_format

    def get_video_directory(self):
        return self._video_directory

    def get_final_video_path(self):
        return self._final_video_path

    def get_final_audio_path(self):
        return self._final_audio_path

    def get_quality(self):
        return self._quality

    def get_fps(self):
        return self._fps
