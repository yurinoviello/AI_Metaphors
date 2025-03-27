import logging
from pathlib import Path
import subprocess

from ai_metaphors.providers.grazie_provider import GrazieProvider
from ai_metaphors.utils.image_utils import extract_key_frames
from ai_metaphors.utils.text_utils import extract_python_code

MAX_TRIES = 10


class ManimProvider:
    """
    ManimProvider is a class that provides functionality to handle and execute
    Manim scripts. It manages the directories used for storing scripts, media,
    and logs, and provides methods to write Python code to a file, execute it
    with Manim, and handle any errors by using the GrazieProvider.

    :param grazie_provider: An instance of GrazieProvider used for refining Manim
                     code.
    :param term: A dictionary containing keyword information, specifically a
                 'value' key for naming purposes.
    :param bin_directory: The path to the Manim bin directory.
    :param working_dir: The directory where scripts, media, and logs are
                        stored.
    """

    def __init__(
        self,
        grazie_provider: GrazieProvider,
        term: dict,
        bin_directory: Path,
        working_dir: Path,
        auto_play: bool,
        high_quality: bool,
    ) -> None:
        self.grazie_provider = grazie_provider
        self.term = term
        self.bin_directory = bin_directory
        self.working_dir = working_dir
        self.auto_play = auto_play
        self.high_quality = high_quality

        self.svg = "\n".join([f"'{svg.as_posix()}'" for svg in Path("ai_metaphors/resources/SVGs").iterdir()])

        self.scripts_dir = self.working_dir / "scripts"
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

        self.media_dir = self.working_dir / "media"
        self.media_dir.mkdir(parents=True, exist_ok=True)

        self.movie_file = self.media_dir / "videos" / f"{term['value'].replace(' ', '_')}" / "480p15" / "GenScene.mp4"

        self.log_dir = self.working_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.description_dir = self.working_dir / "descriptions"
        self.description_dir.mkdir(parents=True, exist_ok=True)

        self.description_file = self.description_dir / f"{term['value'].replace(' ', '_')}.txt"

        self.classes_dir = self.working_dir / "classes"
        self.classes_dir.mkdir(parents=True, exist_ok=True)

        self.classes_file = self.classes_dir / f"{term['value'].replace(' ', '_')}.json"

        self.frames_dir = self.working_dir / "frames" / f"{term['value'].replace(' ', '_')}"
        self.frames_dir.mkdir(parents=True, exist_ok=True)

        self.script_path = self.scripts_dir / f"{term['value'].replace(' ', '_')}.py"

    def write_python(self, text: str):
        code = extract_python_code(text)

        script_path = Path(self.script_path)
        if code:
            try:
                with script_path.open("w") as file:
                    file.write(code)
            except FileNotFoundError as e:
                raise RuntimeError("Cannot write manim code") from e
        else:
            try:
                with script_path.open("w") as file:
                    file.write(text)
            except FileNotFoundError as e:
                raise RuntimeError("Cannot write manim text") from e

    def write_and_run_python(self, text: str):
        self.write_python(text)

        error = self.execute_manim_script()
        if error == "success":
            return

        for _ in range(MAX_TRIES):
            logging.info("Execution...")
            error = self.refine_code_with_static_analysis(error)
            if error == "success":
                return
        raise RuntimeError("Cannot execute Manim script")

    def execute_manim_script(self) -> str:
        command = [
            self.bin_directory / "manim",
            "-p" if self.auto_play else None,
            "-qh" if self.high_quality else "-ql",
            self.script_path,
            "--media_dir",
            self.media_dir,
            "--log_dir",
            self.log_dir,
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
        logging.warning("There was an error during execution.")
        print(error)
        command = [
            self.bin_directory / "pylint",
            "-E",
            self.script_path,
        ]
        try:
            process = subprocess.run(command, capture_output=True, text=True, check=False)
        except FileNotFoundError as e:
            raise RuntimeError("Manim executable not found") from e

        static_errors = process.stdout

        with Path(self.script_path).open() as f:
            manim_script = self.grazie_provider.request_static_refinement(
                code=f.read(),
                runtime_error=error,
                static_error=static_errors,
                svg=self.svg,
            )

        self.write_python(manim_script)
        return self.execute_manim_script()

    def validate_video(self) -> int:
        # This is just a temp code, the system should be able to automatically detect if we need to refine or not
        logging.warning("This feature is still under development")
        refine_video_quality = input("Do you want to refine the video quality? Enter 0 for NO or 1 for YES:")
        while refine_video_quality not in ["0", "1"]:
            logging.warning("Invalid input. Please enter 0 for NO or 1 for YES.")
            refine_video_quality = input("Do you want to refine the video quality? Enter 0 for NO or 1 for YES:")
        return refine_video_quality == 1

    def evaluate_video(self) -> str:
        key_frames = extract_key_frames(self.frames_dir)

        return self.grazie_provider.request_video_evaluation(
            code=self.script_path.read_text(),
            instructions=self.description_file.read_text(),
            images=key_frames,
        )
