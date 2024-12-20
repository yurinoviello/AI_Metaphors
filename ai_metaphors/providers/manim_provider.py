from pathlib import Path
import subprocess

from ai_metaphors.providers.grazie_provider import GrazieProvider
from ai_metaphors.utils.text_utils import extract_python_code


class ManimProvider:
    """
    ManimProvider is a class that provides functionality to handle and execute
    Manim scripts. It manages the directories used for storing scripts, media,
    and logs, and provides methods to write Python code to a file, execute it
    with Manim, and handle any errors by using the GrazieProvider.

    :param provider: An instance of GrazieProvider used for refining Manim
                     code.
    :param term: A dictionary containing keyword information, specifically a
                 'value' key for naming purposes.
    :param executable: The path to the Manim executable directory.
                        Defaults to "".
    :param working_dir: The directory where scripts, media, and logs are
                        stored. Defaults to "./animations".
    """

    def __init__(
        self,
        provider: GrazieProvider,
        term: dict,
        executable: str = "",
        working_dir: str = "./animations",
    ) -> None:
        self.provider = provider
        self.term = term
        self.executable = Path(executable)
        self.working_dir = Path(working_dir)

        self.scripts_dir = self.working_dir / "scripts"
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

        self.media_dir = self.working_dir / "media"
        self.media_dir.mkdir(parents=True, exist_ok=True)

        self.log_dir = self.working_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.file_path = self.scripts_dir / f"{term['value'].replace(' ', '_')}.py"

    def write_python(self, text: str, font_path: str = "./resources/JetBrainsSans-Regular.ttf") -> bool:
        code = extract_python_code(text)
        script_path = Path(self.file_path)
        if code:
            try:
                with script_path.open("w") as file:
                    file.write(
                        f"import manimpango\nmanimpango.register_font('{font_path}')\n"
                        f"from manim import DARK_BROWN as BROWN\n{code}",
                    )
            except FileNotFoundError as e:
                raise RuntimeError("Cannot write manim code") from e
            return True

        try:
            with script_path.open("w") as file:
                file.write(
                    f"import manimpango\nmanimpango.register_font('{font_path}')\n"
                    f"from manim import DARK_BROWN as BROWN\n{text}",
                )
        except FileNotFoundError as e:
            raise RuntimeError("Cannot write manim text") from e
        return False

    def execute_manim_script(self) -> str:
        command = [
            self.executable / "manim",
            "-pql",
            self.file_path,
            "--media_dir",
            self.media_dir,
            "--log_dir",
            self.log_dir,
        ]

        try:
            process = subprocess.run(command, capture_output=True, text=True, check=False)
        except FileNotFoundError as e:
            raise RuntimeError("Manim executable not found") from e

        errors = process.stderr

        if process.returncode == 0:
            return "success"
        return errors

    def fix_code(self, error: str) -> str:
        print("There was an error during execution.")

        command = [
            self.executable / "pylint",
            "-E",
            self.file_path,
        ]
        try:
            process = subprocess.run(command, capture_output=True, text=True, check=False)
        except FileNotFoundError as e:
            raise RuntimeError("Manim executable not found") from e

        static_errors = process.stdout
        print(static_errors)

        with Path(self.file_path).open() as f:
            manim_script = self.provider.refine_manim(
                code=f.read(),
                runtime_error=error,
                static_error=static_errors,
            )

        self.write_python(manim_script)
        return self.execute_manim_script()
