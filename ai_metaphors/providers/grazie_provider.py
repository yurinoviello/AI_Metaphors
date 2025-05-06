import os
from pathlib import Path

import attrs
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.gateway import GrazieApiGatewayClient
from grazie.api.client.llm_parameters import LLMParameters, Parameters
from grazie.api.client.profiles import LLMProfile
from openai import OpenAI
import tiktoken

from ai_metaphors.utils.manim_type import ManimType
from ai_metaphors.utils.text_utils import wrap_keyword

SYSTEM_PROMPT_METAPHOR = "ai_metaphors/prompts/metaphors/SystemPromptMetaphor.txt"
USER_PROMPT_METAPHOR = "ai_metaphors/prompts/metaphors/UserPromptMetaphor.txt"

SYSTEM_PROMPT_ONE_LINE_METAPHOR = "ai_metaphors/prompts/metaphors/SystemPromptOneLineMetaphor.txt"
USER_PROMPT_ONE_LINE_METAPHOR = "ai_metaphors/prompts/metaphors/UserPromptOneLineMetaphor.txt"

SYSTEM_PROMPT_CLASSES = "ai_metaphors/prompts/manim/SystemPromptClasses.txt"
USER_PROMPT_CLASSES = "ai_metaphors/prompts/manim/UserPromptClasses.txt"

SYSTEM_PROMPT_DESCRIPTION = "ai_metaphors/prompts/manim/SystemPromptDescription.txt"
USER_PROMPT_DESCRIPTION = "ai_metaphors/prompts/manim/UserPromptDescription.txt"

SYSTEM_PROMPT_MANIM = "ai_metaphors/prompts/manim/SystemPromptManim.txt"
SYSTEM_PROMPT_MANIM_NO_DESC = "ai_metaphors/prompts/manim/SystemPromptManimNoDesc.txt"
USER_PROMPT_MANIM = "ai_metaphors/prompts/manim/UserPromptManim.txt"

SYSTEM_PROMPT_REFINE = "ai_metaphors/prompts/manim/SystemPromptRefineManim.txt"
USER_PROMPT_REFINE = "ai_metaphors/prompts/manim/UserPromptRefineManim.txt"

SYSTEM_EVALUATE_VIDEO_PROMPT = "ai_metaphors/prompts/validate/SystemEvaluateVideo.txt"
USER_EVALUATE_VIDEO_PROMPT = "ai_metaphors/prompts/validate/UserEvaluateVideo.txt"

SYSTEM_FIX_VIDEO_PROMPT = "ai_metaphors/prompts/validate/SystemFixVideo.txt"
USER_FIX_VIDEO_PROMPT = "ai_metaphors/prompts/validate/UserFixVideo.txt"


class GrazieProvider:
    """
    GrazieProvider is a class designed to interact with the Grazie API using a specified language model.
    It facilitates generating various forms of output based on provided prompts and parameters.

    :param client: An instance of GrazieApiGatewayClient used for sending chat requests.
    :param model: A string representing the model to be used for generating responses. Defaults to "openai-gpt-4o".
    :param temperature: A float that determines the randomness of the model's output. Defaults to 0.0.
    """

    def __init__(self, client: GrazieApiGatewayClient, model: str, temperature: float, manim_type: ManimType) -> None:
        self.client = client
        self.model = model
        self.temperature = temperature
        self.manim_type = manim_type
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.num_tokens = 0

    def __safe_call(self, system_prompt: str, user_prompt: str) -> str:
        @attrs.define(auto_attribs=True, frozen=True)
        class MyProfile(LLMProfile):
            name: str = self.model

        if self.model == "openai-o1":
            return self.client.chat(
                chat=ChatPrompt().add_user(system_prompt + "\n" + user_prompt),
                profile=MyProfile(),
            ).content

        response = self.client.chat(
            chat=ChatPrompt().add_system(system_prompt).add_user(user_prompt),
            profile=MyProfile(),
            parameters={}
            if "o3" in self.model
            else {
                LLMParameters.Temperature: Parameters.FloatValue(self.temperature),
            },
        ).content

        self.num_tokens += len(self.tokenizer.encode(system_prompt + user_prompt + response))
        return response

    def change_model(self, model: str) -> None:
        self.model = model

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

    def get_one_line_metaphor(self, term: dict, metaphor: str) -> str:
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_ONE_LINE_METAPHOR).read_text(),
            user_prompt=Path(USER_PROMPT_ONE_LINE_METAPHOR)
            .read_text()
            .format_map(
                {
                    "topic": term["value"].strip(),
                    "definition": term["definition"].strip(),
                    "metaphor": metaphor.strip(),
                },
            ),
        )

    def get_classes(self, term: dict, metaphor: str, svg: str) -> str:
        return self.__safe_call(
            system_prompt=wrap_keyword(Path(SYSTEM_PROMPT_CLASSES).read_text(), "SVGs").format(
                SVGs=svg,
            ),
            user_prompt=Path(USER_PROMPT_CLASSES)
            .read_text()
            .format_map(
                {
                    "topic": term["value"].strip(),
                    "definition": term["definition"].strip(),
                    "metaphor": metaphor.strip(),
                },
            ),
        )

    def get_description(self, term: dict, metaphor: str, one_line_metaphor: str, classes: str) -> str:
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_DESCRIPTION).read_text(),
            user_prompt=Path(USER_PROMPT_DESCRIPTION)
            .read_text()
            .format_map(
                {
                    "topic": term["value"].strip(),
                    "definition": term["definition"].strip(),
                    "metaphor": metaphor.strip(),
                    "one_line_metaphor": one_line_metaphor.strip(),
                    "classes": classes.strip(),
                },
            ),
        )

    def get_manim(
        self,
        term: dict,
        metaphor: str,
        one_line_metaphor: str,
        classes: str,
        svg: str,
        instructions: str = "",
    ) -> str:
        if instructions != "":
            return self.__safe_call(
                system_prompt=Path(SYSTEM_PROMPT_MANIM)
                .read_text()
                .format(
                    example_code=self.manim_type.value.get_example_code(),
                    start_code=self.manim_type.value.get_start_code(term["value"]),
                    SVGs=svg,
                ),
                user_prompt=Path(USER_PROMPT_MANIM)
                .read_text()
                .format_map(
                    {
                        "topic": term["value"].strip(),
                        "definition": term["definition"].strip(),
                        "metaphor": metaphor.strip(),
                        "one_line_metaphor": one_line_metaphor.strip(),
                        "classes": classes.strip(),
                        "instructions": instructions.strip(),
                    },
                ),
            )
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_MANIM_NO_DESC)
            .read_text()
            .format(
                example_code=self.manim_type.value.get_example_code(),
                start_code=self.manim_type.value.get_start_code(term["value"]),
                SVGs=svg,
            ),
            user_prompt=Path(USER_PROMPT_DESCRIPTION)
            .read_text()
            .format_map(
                {
                    "topic": term["value"].strip(),
                    "definition": term["definition"].strip(),
                    "metaphor": metaphor.strip(),
                    "one_line_metaphor": one_line_metaphor.strip(),
                    "classes": classes.strip(),
                },
            ),
        )

    def request_static_refinement(self, term: dict, code: str, runtime_error: str, static_error: str, svg: str) -> str:
        return self.__safe_call(
            system_prompt=Path(SYSTEM_PROMPT_REFINE)
            .read_text()
            .format(
                start_code=self.manim_type.value.get_start_code(term["value"]),
                SVGs=svg,
            ),
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

    def request_video_evaluation(self, code: str, instructions: str, images: list[str]) -> str:
        # This should be done by GrazieProvider, for now it is devoted to OPENAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        messages = [
            {
                "role": "developer",
                "content": [
                    {
                        "type": "text",
                        "text": Path(SYSTEM_EVALUATE_VIDEO_PROMPT).read_text(),
                    },
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": Path(USER_EVALUATE_VIDEO_PROMPT)
                        .read_text()
                        .format_map({"instructions": instructions, "code": code}),
                    },
                ],
            },
        ]

        for i, img in enumerate(images):
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Frame {i + 1}:",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img}",
                            },
                        },
                    ],
                },
            )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=3_000,
            seed=10,
        )
        return response.choices[0].message.content

    def request_video_refinement(self, instructions: str, errors_explanation: str, code: str, svg: str) -> str:
        return self.__safe_call(
            system_prompt=Path(SYSTEM_FIX_VIDEO_PROMPT)
            .read_text()
            .format(
                SVGs=svg,
            ),
            user_prompt=Path(USER_FIX_VIDEO_PROMPT)
            .read_text()
            .format_map(
                {
                    "instructions": instructions.strip(),
                    "errors_explanation": errors_explanation.strip(),
                    "code": code.strip(),
                },
            ),
        )
