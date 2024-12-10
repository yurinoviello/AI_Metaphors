from grazie.api.client.gateway import  GrazieApiGatewayClient
from grazie.api.client.chat.prompt import ChatPrompt
import attrs, re, os, json, subprocess
from grazie.api.client.profiles import LLMProfile
from grazie.api.client.llm_parameters import LLMParameters, Parameters

SYSTEM_PROMPT_CLASSES = "./prompts/SystemPromptClasses.txt"
USER_PROMPT_CLASSES = "./prompts/UserPromptClasses.txt"

SYSTEM_PROMPT_DESCRIPTION = "./prompts/SystemPromptDescription.txt"
USER_PROMPT_DESCRIPTION = "./prompts/UserPromptDescription.txt"

SYSTEM_PROMPT_METAPHOR = "./prompts/SystemPromptMetaphor.txt"
USER_PROMPT_METAPHOR = "./prompts/UserPromptMetaphor.txt"

SYSTEM_PROMPT_MANIM = "./prompts/SystemPromptManim.txt"
SYSTEM_PROMPT_MANIM_NO_DESC = "./prompts/SystemPromptManimNoDesc.txt"

USER_PROMPT_MANIM = "./prompts/UserPromptManim.txt"

SYSTEM_PROMPT_REFINE = "./prompts/SystemPromptRefineManim.txt"
USER_PROMPT_REFINE = "./prompts/UserPromptRefineManim.txt"


class GrazieProvider:
    """
    GrazieProvider is a class designed to interact with the Grazie API using a specified language model.
    It facilitates generating various forms of output based on provided prompts and parameters.

    :param client: An instance of GrazieApiGatewayClient used for sending chat requests.
    :param model: A string representing the model to be used for generating responses. Defaults to "openai-gpt-4o".
    :param temperature: A float that determines the randomness of the model's output. Defaults to 0.0.
    """
    def __init__(self, client: GrazieApiGatewayClient,
                 model: str = "openai-gpt-4o",
                 temperature: float = 0.0,):
        self.client = client
        self.model = model
        self.temperature = temperature

    def __safe_call(self, system_prompt: str, user_prompt: str):
        @attrs.define(auto_attribs=True, frozen=True)
        class MyProfile(LLMProfile):
            name: str = self.model

        if self.model == "openai-o1":
            return self.client.chat(
                chat=ChatPrompt().add_user(system_prompt + '\n' + user_prompt),
                profile=MyProfile(),
            ).content

        return self.client.chat(
            chat=ChatPrompt().add_system(system_prompt).add_user(user_prompt),
            profile=MyProfile(),
            parameters={LLMParameters.Temperature: Parameters.FloatValue(self.temperature)}
        ).content


    def get_classes(self, term: dict, metaphor: str,):
        return self.__safe_call(
            system_prompt = open(SYSTEM_PROMPT_CLASSES).read(),
            user_prompt = open(USER_PROMPT_CLASSES).read().format_map({
            "topic" : term['value'].strip(),
            "definition" : term['definition'].strip(),
            "metaphor" : metaphor.strip()})
        )

    def get_description(self, term: dict, metaphor: str, classes: str):
        return self.__safe_call(
            system_prompt = open(SYSTEM_PROMPT_DESCRIPTION).read(),
            user_prompt = open(USER_PROMPT_DESCRIPTION).read().format_map({
                "topic": term['value'].strip(),
                "definition": term['definition'].strip(),
                "metaphor": metaphor.strip(),
                "classes" : classes.strip()
            })
        )

    def get_manim(self, term: dict, metaphor: str, classes: str, instructions: str = ""):
        if instructions != "":
            return self.__safe_call(
                system_prompt = open(SYSTEM_PROMPT_MANIM).read(),
                user_prompt = open(USER_PROMPT_MANIM).read().format_map({
                    "topic": term['value'].strip(),
                    "definition": term['definition'].strip(),
                    "metaphor": metaphor.strip(),
                    "classes" : classes.strip(),
                    "instructions" : instructions.strip()
                })
            )
        return self.__safe_call(
                system_prompt = open(SYSTEM_PROMPT_MANIM_NO_DESC).read(),
                user_prompt = open(USER_PROMPT_DESCRIPTION).read().format_map({
                    "topic": term['value'].strip(),
                    "definition": term['definition'].strip(),
                    "metaphor": metaphor.strip(),
                    "classes" : classes.strip(),
                })
            )


    def refine_manim(self, code: str, runtime_error: str, static_error: str):
        return self.__safe_call(
            system_prompt = open(SYSTEM_PROMPT_REFINE).read(),
            user_prompt = open(USER_PROMPT_REFINE).read().format_map({
                "code": code.strip(),
                "runtime-error": runtime_error.strip(),
                "static-error": static_error.strip()
            })
        )


def extract_python_code(text: str) -> str | None:
    """
    :param text: A string that may contain Python code block encapsulated within triple backticks.
    :return: Extracted Python code from the provided text, if found; otherwise, returns None.
    """
    pattern = re.compile(r"```(?:python)?\n(.*?)```", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None

def extract_json(text):
    """
    :param text: A string that potentially contains a JSON object wrapped in triple backticks.
    :return: A dictionary representing the extracted JSON object if valid JSON is found and decoded successfully, otherwise None.
    """
    json_pattern = r'```json(.*?)```'
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        json_content = match.group(1)
        try:
            return json.loads(json_content)
        except json.JSONDecodeError:
            print("Invalid JSON found.")
            return None
    return None


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
                       "/home/ynoviello/anaconda3/envs/jetbrains/bin".
    :param working_dir: The directory where scripts, media, and logs are
                        stored. Defaults to "./animations".
    """
    def __init__(self,
                 provider : GrazieProvider, term: dict,
                 executable: str = "/home/ynoviello/anaconda3/envs/jetbrains/bin",
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



    def write_python(self, text: str) -> bool:

        code = extract_python_code(text)
        if code:
            try:
                with open(self.file_path, "w") as file:
                    file.write(f"import manimpango\nmanimpango.register_font('./JetBrainsSans-Regular.ttf')\nfrom manim import DARK_BROWN as BROWN\n{code}")
            except:
                raise Exception("Cannot write python file")
            return True

        try:
            with open(self.file_path, "w") as file:
                file.write(f"import manimpango\nmanimpango.register_font('./JetBrainsSans-Regular.ttf')\nfrom manim import DARK_BROWN as BROWN\n{text}")
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
