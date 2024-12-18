from pathlib import Path

import attrs
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.gateway import GrazieApiGatewayClient
from grazie.api.client.llm_parameters import LLMParameters, Parameters
from grazie.api.client.profiles import LLMProfile

SYSTEM_PROMPT_CLASSES = "ai_metaphors/prompts/SystemPromptClasses.txt"
USER_PROMPT_CLASSES = "ai_metaphors/prompts/UserPromptClasses.txt"

SYSTEM_PROMPT_DESCRIPTION = "ai_metaphors/prompts/SystemPromptDescription.txt"
USER_PROMPT_DESCRIPTION = "ai_metaphors/prompts/UserPromptDescription.txt"

SYSTEM_PROMPT_METAPHOR = "ai_metaphors/prompts/SystemPromptMetaphor.txt"
USER_PROMPT_METAPHOR = "ai_metaphors/prompts/UserPromptMetaphor.txt"

SYSTEM_PROMPT_MANIM = "ai_metaphors/prompts/SystemPromptManim.txt"
SYSTEM_PROMPT_MANIM_NO_DESC = "ai_metaphors/prompts/SystemPromptManimNoDesc.txt"

USER_PROMPT_MANIM = "ai_metaphors/prompts/UserPromptManim.txt"

SYSTEM_PROMPT_REFINE = "ai_metaphors/prompts/SystemPromptRefineManim.txt"
USER_PROMPT_REFINE = "ai_metaphors/prompts/UserPromptRefineManim.txt"


class GrazieProvider:
    """
    GrazieProvider is a class designed to interact with the Grazie API using a specified language model.
    It facilitates generating various forms of output based on provided prompts and parameters.

    :param client: An instance of GrazieApiGatewayClient used for sending chat requests.
    :param model: A string representing the model to be used for generating responses. Defaults to "openai-gpt-4o".
    :param temperature: A float that determines the randomness of the model's output. Defaults to 0.0.
    """

    def __init__(self, client: GrazieApiGatewayClient, model: str = "openai-gpt-4o", temperature: float = 0.0) -> None:
        self.client = client
        self.model = model
        self.temperature = temperature

    def __safe_call(self, system_prompt: str, user_prompt: str) -> str:
        @attrs.define(auto_attribs=True, frozen=True)
        class MyProfile(LLMProfile):
            name: str = self.model

        if self.model == "openai-o1":
            return self.client.chat(
                chat=ChatPrompt().add_user(system_prompt + "\n" + user_prompt),
                profile=MyProfile(),
            ).content

        return self.client.chat(
            chat=ChatPrompt().add_system(system_prompt).add_user(user_prompt),
            profile=MyProfile(),
            parameters={LLMParameters.Temperature: Parameters.FloatValue(self.temperature)},
        ).content

    def get_metaphor(self, term: dict) -> str:
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_METAPHOR).read_text(),
            user_prompt=Path(USER_PROMPT_METAPHOR)
            .read_text()
            .format_map(
                {
                    "topic": term["value"].strip(),
                    "definition": term["definition"].strip(),
                },
            ),
        )

    def get_classes(self, term: dict, metaphor: str) -> str:
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_CLASSES).read_text(),
            user_prompt=Path(USER_PROMPT_CLASSES)
            .read_text()
            .format_map({"topic": term["value"].strip(), "definition": term["definition"].strip(), "metaphor": metaphor.strip()}),
        )

    def get_description(self, term: dict, metaphor: str, classes: str) -> str:
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_DESCRIPTION).read_text(),
            user_prompt=Path(USER_PROMPT_DESCRIPTION)
            .read_text()
            .format_map(
                {
                    "topic": term["value"].strip(),
                    "definition": term["definition"].strip(),
                    "metaphor": metaphor.strip(),
                    "classes": classes.strip(),
                },
            ),
        )

    def get_manim(self, term: dict, metaphor: str, classes: str, instructions: str = "") -> str:
        if instructions != "":
            return self.__safe_call(
                system_prompt=Path(SYSTEM_PROMPT_MANIM_NO_DESC).read_text(),
                user_prompt=Path(USER_PROMPT_DESCRIPTION)
                .read_text()
                .format_map(
                    {
                        "topic": term["value"].strip(),
                        "definition": term["definition"].strip(),
                        "metaphor": metaphor.strip(),
                        "classes": classes.strip(),
                        "instructions": instructions.strip(),
                    },
                ),
            )
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_MANIM_NO_DESC).read_text(),
            user_prompt=Path(USER_PROMPT_DESCRIPTION)
            .read_text()
            .format_map(
                {
                    "topic": term["value"].strip(),
                    "definition": term["definition"].strip(),
                    "metaphor": metaphor.strip(),
                    "classes": classes.strip(),
                },
            ),
        )

    def refine_manim(self, code: str, runtime_error: str, static_error: str) -> str:
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_REFINE).read_text(),
            user_prompt=Path(USER_PROMPT_REFINE)
            .read_text()
            .format_map(
                {
                    "code": code.strip(),
                    "runtime-error": runtime_error.strip(),
                    "static-error": static_error.strip(),
                },
            ),
        )
