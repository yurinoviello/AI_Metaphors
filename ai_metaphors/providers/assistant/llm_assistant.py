from abc import ABC, abstractmethod
from enum import Enum

import tiktoken
from grazie.api.client.chat.roles import ChatRole

from ai_metaphors.utils.manim_type import ManimType
from ai_metaphors.utils.text_utils import wrap_keyword
from pathlib import Path


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

class ContentType(Enum):
    TEXT = "text"
    IMAGE = "image_url"

class LlmAssistant(ABC):

    class Message:
        def __init__(self, role: ChatRole, content: str, content_type: ContentType = ContentType.TEXT) -> None:
            self.role = role
            self.content = content
            self.content_type = content_type

    def __init__(self, model: str, temperature: float, manim_type: ManimType) -> None:
        self.model = model
        self.temperature = temperature
        self.manim_type = manim_type
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.num_tokens = 0

    @abstractmethod
    def _chat_message_list(self, messages: list[Message]) -> str:
        raise NotImplementedError

    def __chat_prompt(self, system_prompt: str, user_prompt: str) -> str:
        return self._chat_message_list(
            [
                LlmAssistant.Message(role=ChatRole.SYSTEM, content=system_prompt),
                LlmAssistant.Message(role=ChatRole.USER, content=user_prompt),
            ]
        )

    def change_model(self, model: str):
        self.model = model

    def get_metaphor(self, term: dict) -> str:
        return self.__chat_prompt(
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
        return self.__chat_prompt(
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
        return self.__chat_prompt(
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
        return self.__chat_prompt(
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
            return self.__chat_prompt(
                system_prompt=Path(SYSTEM_PROMPT_MANIM)
                .read_text()
                .format(
                    example_code=self.manim_type.value.get_example_code(),
                    start_code=self.manim_type.value.get_start_code(term["value"].replace(' ', '_')),
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
        return self.__chat_prompt(
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
        return self.__chat_prompt(
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

    def request_video_refinement(self, instructions: str, errors_explanation: str, code: str, svg: str) -> str:
        return self.__chat_prompt(
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

    def request_video_evaluation(self, code: str, instructions: str, images: list[str]) -> str:
        messages = [
            LlmAssistant.Message(
                role=ChatRole.SYSTEM,
                content=Path(SYSTEM_EVALUATE_VIDEO_PROMPT).read_text(),
            ),
            LlmAssistant.Message(
                role=ChatRole.USER,
                content=Path(USER_EVALUATE_VIDEO_PROMPT)
                .read_text()
                .format_map({"instructions": instructions, "code": code}),
            )
        ]

        for i, img in enumerate(images):
            messages.append(
                LlmAssistant.Message(
                    role=ChatRole.USER,
                    content=f"Frame {i + 1}:",
                )
            )
            messages.append(
                LlmAssistant.Message(
                    role=ChatRole.USER,
                    content=f"data:image/jpeg;base64,{img}",
                    content_type=ContentType.IMAGE,
                )
            )
        return self._chat_message_list(messages)

    @abstractmethod
    def get_narration_audio(self, text: str, narration_audio_file: Path):
        raise NotImplementedError