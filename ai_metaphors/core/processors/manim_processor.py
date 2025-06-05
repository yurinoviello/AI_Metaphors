import logging
from pathlib import Path
import subprocess

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
            "-qh" if self._high_quality else "-ql",
            self.script_path,
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
