import os, subprocess
from ai_metaphors.providers.grazie_provider import GrazieProvider
from ai_metaphors.utils.text_utils import  extract_python_code

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
    :param executable: The path to the Manim executable directory. Defaults to
                       "/home/user/anaconda3/envs/jetbrains/bin".
    :param working_dir: The directory where scripts, media, and logs are
                        stored. Defaults to "./animations".
    """
    def __init__(self,
                 provider : GrazieProvider, term: dict,
                 executable: str = "/home/user/anaconda3/envs/jetbrains/bin",
                 working_dir: str = "./animations",):
        self.provider = provider
        self.term = term
        self.executable = executable
        self.working_dir = working_dir

        self.scripts_dir = os.path.join(self.working_dir, "scripts")
        os.makedirs(self.scripts_dir, exist_ok=True)
        self.media_dir = os.path.join(self.working_dir, "media")
        os.makedirs(self.media_dir, exist_ok=True)
        self.log_dir = os.path.join(self.working_dir, "logs")
        os.makedirs(self.log_dir, exist_ok=True)

        self.file_path = os.path.join(self.scripts_dir, f"{term['value'].replace(' ', '_')}.py")



    def write_python(self, text: str, font_path: str = "./resources/JetBrainsSans-Regular.ttf") -> bool:

        code = extract_python_code(text)
        if code:
            try:
                with open(self.file_path, "w") as file:
                    file.write(f"import manimpango\nmanimpango.register_font('{font_path}')\nfrom manim import DARK_BROWN as BROWN\n{code}")
            except:
                raise Exception("Cannot write python file")
            return True

        try:
            with open(self.file_path, "w") as file:
                file.write(f"import manimpango\nmanimpango.register_font('{font_path}')\nfrom manim import DARK_BROWN as BROWN\n{text}")
        except:
            raise Exception("Cannot write python file")
        return False



    def execute_manim_script(self) -> str:

        command = [os.path.join(self.executable, "manim"),
                   "-pql", self.file_path,
                   "--media_dir", self.media_dir,
                   "--log_dir", self.log_dir,]
        process = subprocess.run(command, capture_output=True, text=True)

        errors = process.stderr

        if process.returncode == 0:
            return "100"
        return errors

    def fix_code(self, error: str) -> str:
        print("There was an error during execution.")

        command = [os.path.join(self.executable, "pylint"), "-E", self.file_path]
        process = subprocess.run(command, capture_output=True, text=True)
        static_errors = process.stdout
        print(static_errors)

        manim_script = self.provider.refine_manim(
            code = open(self.file_path).read(),
            runtime_error = error,
            static_error = static_errors
        )

        self.write_python(manim_script)
        return self.execute_manim_script()
