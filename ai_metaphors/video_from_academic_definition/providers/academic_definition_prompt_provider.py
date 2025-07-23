from abc import ABC
from pathlib import Path

from ai_metaphors.core.providers.prompt_provider import PromptProvider
from ai_metaphors.core.utils.manim_type import SafeDict, ManimType

class AcademicDefinitionPromptProvider(PromptProvider, ABC):

    _term: dict[str, str]

    _PATH_TO_CODE: Path = Path("ai_metaphors/video_from_academic_definition/prompts")
    _ADDITIONAL_INSTRUCTIONS_FOR_MANIM_CODE: Path = _PATH_TO_CODE / "additional_instructions_for_manim_code.txt"
    _EXAMPLE_CLASSES: Path = _PATH_TO_CODE / "example_classes.txt"
    _INPUT_DATA: Path = _PATH_TO_CODE / "input_data.txt"
    _INPUT_EXPLANATION: Path = _PATH_TO_CODE / "input_explanation.txt"

    _SYSTEM_PROMPT_DEFINITION_TEMPLATE: Path = _PATH_TO_CODE / "term_definition/system_prompt_term_definition.txt"
    _USER_PROMPT_DEFINITION_TEMPLATE: Path = _PATH_TO_CODE / "term_definition/user_prompt_term_definition.txt"

    _SYSTEM_PROMPT_ONE_LINE_DEFINITION_TEMPLATE: Path = _PATH_TO_CODE / "one_line_term_definition/system_prompt_one_line_term_definition.txt"
    _USER_PROMPT_ONE_LINE_DEFINITION_TEMPLATE: Path = _PATH_TO_CODE / "one_line_term_definition/user_prompt_one_line_term_definition.txt"

    def __init__(self, term: dict[str, str], manim_type: ManimType):
        super().__init__(manim_type)
        self._term = term

    def _get_subject_name(self) -> str:
        return self._term["name"]

    def _get_example_for_classes(self) -> str:
        return self._EXAMPLE_CLASSES.read_text()

    def _get_input_explanation(self) -> str:
        return self._INPUT_EXPLANATION.read_text()

    def _get_input_data(self) -> str:
        return self._INPUT_DATA.read_text().format_map(
            SafeDict(name=self._term["name"])
        )

    def _get_additional_instructions_for_manim_code(self) -> str:
        return self._ADDITIONAL_INSTRUCTIONS_FOR_MANIM_CODE.read_text()

    def get_system_prompt_term_definition(self) -> str:
        return self._SYSTEM_PROMPT_DEFINITION_TEMPLATE.read_text().format_map(
            SafeDict(input_explanation=self._get_input_explanation())
        )

    def get_user_prompt_term_definition(self) -> str:
        return self._USER_PROMPT_DEFINITION_TEMPLATE.read_text().format_map(
            SafeDict(input_data=self._get_input_data())
        )

    def get_system_prompt_one_line_term_definition(self) -> str:
        return self._SYSTEM_PROMPT_ONE_LINE_DEFINITION_TEMPLATE.read_text().format_map(
            SafeDict(input_explanation=self._get_input_explanation())
        )

    def get_user_prompt_one_line_term_definition(self, term_definition: str) -> str:
        return self._USER_PROMPT_ONE_LINE_DEFINITION_TEMPLATE.read_text().format_map(
            SafeDict(
                input_data=self._get_input_data(),
                definition=term_definition
            )
        )
