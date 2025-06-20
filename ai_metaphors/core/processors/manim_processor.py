import logging
from pathlib import Path
import subprocess
import re
import json

from ai_metaphors.core.providers.grazie_provider import GrazieProvider
from ai_metaphors.core.utils.image_utils import extract_key_frames
from ai_metaphors.core.utils.text_utils import extract_python_code


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
    _media_dir: Path
    _log_dir: Path
    _frames_dir: Path
    _MAX_TRIES = 10

    high_quality: bool
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
        self.high_quality = high_quality

        self.svg = "\n".join([f"'{svg.as_posix()}'" for svg in Path("ai_metaphors/resources/SVGs").iterdir()])

        self._media_dir = working_dir / "media"
        self._media_dir.mkdir(parents=True, exist_ok=True)

        video_resolution = "1080p60" if self.high_quality else "480p15"
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

    def write_python(self, text: str):
        code = extract_python_code(text)

        if code:
            try:
                with self.script_path.open("w") as file:
                    file.write(code)
            except FileNotFoundError as e:
                raise RuntimeError("Cannot write manim code") from e
        else:
            try:
                with self.script_path.open("w") as file:
                    file.write(text)
            except FileNotFoundError as e:
                raise RuntimeError("Cannot write manim text") from e

    def write_and_run_python(self, text: str):
        logging.info("Execution...")
        self.write_python(text)

        error = self.execute_manim_script()
        if error == "success":
            return

        for _ in range(self._MAX_TRIES):
            logging.info("Execution...")
            error = self.refine_code_with_static_analysis(error)
            if error == "success":
                return
        raise RuntimeError("Cannot execute Manim script")

    def execute_manim_script(self) -> str:
        command = [
            self._bin_directory / "manim",
            "-p" if self._auto_play else None,
            "-qh" if self.high_quality else "-ql",
            self.script_path,
            "--save_sections",
            "--media_dir",
            self._media_dir,
            "--log_dir",
            self._log_dir,
        ]

        try:
            process = subprocess.run([c for c in command if c], capture_output=True, text=True, check=False)
        except FileNotFoundError as e:
            raise RuntimeError("Manim executable not found") from e

        errors = process.stderr

        if process.returncode == 0:
            self.split_animation()
            return "success"
        return errors

    def refine_code_with_static_analysis(self, error: str) -> str:
        logging.warning("There was an error during execution: %s", error)
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
            manim_script = self._grazie_provider.request_static_refinement(
                code=f.read(),
                runtime_error=error,
                static_error=static_errors,
                svg=self.svg,
            )

        self.write_python(manim_script)
        return self.execute_manim_script()

    @staticmethod
    def validate_video() -> int:
        # This is just a temp code, the system should be able to automatically detect if we need to refine or not
        logging.warning("This feature is still under development")
        refine_video_quality = input("Do you want to refine the video quality? Enter 0 for NO or 1 for YES:")
        while refine_video_quality not in ["0", "1"]:
            logging.warning("Invalid input. Please enter 0 for NO or 1 for YES.")
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
        if not self._section_file.exists():
            logging.error("Section file %s not found - skipping split.", self._section_file)
            return

        if not self._movie_file.exists():
            logging.error("Movie file %s not found - cannot split.", self._movie_file)
            return

        # Helper: turn an arbitrary section title into a safe file-name
        def _sanitize(name: str) -> str:
            return re.sub(r"[^0-9A-Za-z._-]+", "_", name.strip()) or "section"

        try:
            sections = json.loads(self._section_file.read_text(encoding="utf-8"))
        except Exception as exc:                             # noqa: BLE001
            logging.error("Cannot read sections JSON: %s - cannot split.", exc)
            return

        sections_dir = self._section_file.parent
        sections_dir.mkdir(parents=True, exist_ok=True)

        # Remove all .mp4 files in the output directory
        for file in sections_dir.glob("*.mp4"):
            try:
                file.unlink()
                logging.info("Deleted %s", file.name)
            except Exception as exc:
                logging.error("Failed to delete %s: %s - cannot split.", file.name, exc)

        width = max(2, len(str(len(sections) - 1)))

        start_time = 0.0
        for index, section in enumerate(sections):
            try:
                duration = float(section["duration"])
            except (KeyError, ValueError):
                logging.error("Section %s has no valid duration – skipping.", section)
                continue

            title = section.get("name", f"sec_{index}")
            safe_title = _sanitize(title)
            target = sections_dir / f"{index:0{width}d}_{safe_title}.mp4"

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
                logging.info("Wrote %s", target.name)
            except subprocess.CalledProcessError as exc:
                logging.error("FFmpeg failed for section %s (%s): %s", index, title, exc)

            start_time += duration