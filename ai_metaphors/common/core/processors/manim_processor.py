import json
import logging
import os
import re
import subprocess
from pathlib import Path

from ai_metaphors.common.core.providers.grazie_provider import GrazieProvider
from ai_metaphors.common.core.utils.image_utils import extract_key_frames
from ai_metaphors.common.core.utils.text_utils import extract_python_code
from ai_metaphors.server.settings.settings import settings


class ManimProcessor:
    """
    ManimProvider is a class that provides functionality to handle and execute
    Manim scripts. It manages the directories used for storing scripts, media,
    and logs, and provides methods to write Python code to a file, execute it
    with Manim, and handle any errors by using the GrazieProvider.

    :param grazie_provider: An instance of GrazieProvider used for refining Manim
                     code.
    :param subject_id: A string describing the subject for naming purposes.
    :param bin_directory: The path to the Manim bin directory.
    :param working_dir: The directory where scripts, media, and logs are
                        stored.
    """

    _grazie_provider: GrazieProvider
    _bin_directory: Path
    _auto_play: bool
    _high_quality: bool
    _media_dir: Path
    _log_dir: Path
    _frames_dir: Path
    _MAX_TRIES = 10

    svg: str
    description_file: Path
    classes_file: Path
    script_path: Path

    def __init__(
        self,
        grazie_provider: GrazieProvider,
        subject_id: str,
        bin_directory: Path,
        working_dir: Path,
        auto_play: bool,
        high_quality: bool,
    ) -> None:
        self._grazie_provider = grazie_provider
        self._bin_directory = bin_directory
        self._auto_play = auto_play
        self._high_quality = high_quality

        self.svg = "\n".join([f"'{svg.as_posix()}'" for svg in Path("ai_metaphors/resources/SVGs").iterdir()])

        self._media_dir = working_dir / "media"
        self._media_dir.mkdir(parents=True, exist_ok=True)

        video_resolution = "1080p60" if self._high_quality else "480p15"
        self.movie_dir = self._media_dir / "videos" / subject_id / video_resolution
        self._movie_file = self.movie_dir / "GenScene.mp4"
        self._section_file = self.movie_dir / "sections" / "GenScene.json"

        self._log_dir = working_dir / "logs"
        self._log_dir.mkdir(parents=True, exist_ok=True)

        description_dir = working_dir / "descriptions"
        description_dir.mkdir(parents=True, exist_ok=True)
        self.description_file = description_dir / f"{subject_id}.txt"

        classes_dir = working_dir / "classes"
        classes_dir.mkdir(parents=True, exist_ok=True)
        self.classes_file = classes_dir / f"{subject_id}.json"

        self._frames_dir = working_dir / "frames" / f"{subject_id}"
        self._frames_dir.mkdir(parents=True, exist_ok=True)

        scripts_dir = working_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        self.script_path = scripts_dir / f"{subject_id}.py"

    def write_python(self, text: str) -> str:
        code = extract_python_code(text)
        
        if not code:
            code = text

        if code:
            try:
                # Calculate a memory fraction for a hard limit
                fraction = min(0.95, settings.GPU_MEMORY_MB / settings.GPU_TOTAL_MEMORY_MB)
                memory_limit_header = (
                    "import torch\n\n"
                    f"if torch.cuda.is_available():\n"
                    f"    torch.cuda.set_per_process_memory_fraction({fraction:.4f}, 0)\n\n"
                )
                
                with self.script_path.open("w") as file:
                    file.write(memory_limit_header + code)
            except FileNotFoundError as e:
                raise RuntimeError("Cannot write manim code") from e
        
        return code

    def write_and_run_python(self, text: str) -> str:
        logging.debug("Starting execution...")
        code = self.write_python(text)

        error = self.execute_manim_script()
        if error == "success":
            return code

        for tryNum in range(self._MAX_TRIES):
            logging.debug(f"Execution, {tryNum} try ...")
            code, error = self.refine_code_with_static_analysis(error)
            if error == "success":
                return code
        raise RuntimeError("Cannot execute Manim script")

    def execute_manim_script(self) -> str:
        # Triton Fix
        env = os.environ.copy()
        env["SETUPTOOLS_USE_DISTUTILS"] = "stdlib"
        env["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128,garbage_collection_threshold:0.8"

        manim_command = [
            self._bin_directory / "manim",
            "-p" if self._auto_play else None,
            "-qh" if self._high_quality else "-ql",
            self.script_path,
            "--save_sections",
            "--media_dir",
            self._media_dir,
            "--log_dir",
            self._log_dir,
            "--progress_bar",
            "none"
        ]

        try:
            process = subprocess.run([c for c in manim_command if c], capture_output=True, text=True, check=False, env=env)
        except FileNotFoundError as e:
            raise RuntimeError("Manim executable not found") from e

        errors = process.stderr

        if process.returncode == 0:
            self.split_animation()
            return "success"
        return errors

    def refine_code_with_static_analysis(self, error: str) -> tuple[str, str]:
        logging.error(f"There was an error during execution:\n{error}")
        command = [
            self._bin_directory / "pylint",
            "-E",
            self.script_path,
        ]
        try:
            process = subprocess.run(command, capture_output=True, text=True, check=False)
        except FileNotFoundError as e:
            raise RuntimeError("Manim executable not found") from e

        static_errors = process.stdout

        with self.script_path.open() as f:
            manim_script_raw = self._grazie_provider.request_static_refinement(
                code=f.read(),
                runtime_error=error,
                static_error=static_errors,
                svg=self.svg,
            )

        code = self.write_python(manim_script_raw)
        return code, self.execute_manim_script()

    @staticmethod
    def validate_video() -> int:
        # This is just a temp code, the system should be able to automatically detect if we need to refine or not
        logging.warning("This feature is still under development")
        refine_video_quality = input("Do you want to refine the video quality? Enter 0 for NO or 1 for YES:")
        while refine_video_quality not in ["0", "1"]:
            logging.error("Invalid input. Please enter 0 for NO or 1 for YES.")
            refine_video_quality = input("Do you want to refine the video quality? Enter 0 for NO or 1 for YES:")
        return refine_video_quality == 1

    def evaluate_video(self) -> str:
        key_frames = extract_key_frames(self._frames_dir)

        return self._grazie_provider.request_video_evaluation(
            code=self.script_path.read_text(),
            instructions=self.description_file.read_text(),
            images=key_frames,
        )

    def split_animation(self) -> None:
        """Split the main animation into individual section videos."""
        if not self._validate_files():
            return
            
        sections = self._read_sections()
        if not sections:
            return
            
        sections_dir = self._prepare_output_directory()
        width = max(2, len(str(len(sections) - 1)))
        
        self._process_sections(sections, sections_dir, width)
    
    def _validate_files(self) -> bool:
        """Validate that required files exist."""
        if not self._section_file.exists():
            logging.error(f"Section file {self._section_file} not found - skipping split.")
            return False
        if not self._movie_file.exists():
            logging.error(f"Movie file {self._movie_file} not found - cannot split.")
            return False
        return True
    
    def _read_sections(self) -> list:
        """Read and parse the sections JSON file."""
        try:
            sections = json.loads(self._section_file.read_text(encoding="utf-8"))
            return sections
        except Exception as exc:                             # noqa: BLE001
            logging.error(f"Cannot read sections JSON - cannot split:\n{exc}")
            return []
    
    def _prepare_output_directory(self) -> Path:
        """Prepare the output directory by creating it and clearing old files."""
        sections_dir = self._section_file.parent
        sections_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove all .mp4 files in the output directory
        for file in sections_dir.glob("*.mp4"):
            try:
                file.unlink()
                logging.debug(f"Deleted {file.name}")
            except Exception as exc:
                logging.error(f"Failed to delete {file.name}, cannot split:\n{exc}")
        
        return sections_dir
    
    def _process_sections(self, sections: list, sections_dir: Path, width: int) -> None:
        """Process each section and create individual video files."""
        # Helper: turn an arbitrary section title into a safe file-name
        def _sanitize(name: str) -> str:
            return re.sub(r"[^0-9A-Za-z._-]+", "_", name.strip()) or "section"
            
        start_time = 0.0
        for index, section in enumerate(sections):
            try:
                duration = float(section["duration"])
            except (KeyError, ValueError):
                logging.error(f"Section {section} has no valid duration – skipping.", section)
                continue
                
            title = section.get("name", f"sec_{index}")
            safe_title = _sanitize(title)
            target = sections_dir / f"{index:0{width}d}_{safe_title}.mp4"
            
            self._extract_section_video(start_time, duration, target, index, title)
            start_time += duration
    
    def _extract_section_video(self, start_time: float, duration: float, 
                               target: Path, index: int, title: str) -> None:
        """Extract a section of the video using ffmpeg."""
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",                                   # overwrite if exists
            "-ss", f"{start_time:.3f}",             # seek to start time
            "-i", str(self._movie_file),
            "-t",  f"{duration:.3f}",               # exact length
            "-c",  "copy",                          # stream copy
            str(target),
        ]
        
        try:
            subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
            logging.debug(f"Wrote {target.name}")
        except subprocess.CalledProcessError as exc:
            logging.error(f"FFmpeg failed for section {index} ({title}):\n{exc}")