from abc import ABC
from pathlib import Path

from ai_metaphors.common.core.providers.prompt_provider import PromptProvider
from ai_metaphors.common.core.utils.manim_type import SafeDict, ManimType


class DefinitionPromptProvider(PromptProvider, ABC):

    _term: dict[str, str]

    _PATH_TO_TERM: Path = Path("ai_metaphors/common/video_from_definition/prompts")
    _ADDITIONAL_INSTRUCTIONS_FOR_MANIM_CODE: Path = _PATH_TO_TERM / "additional_instructions_for_manim_code.txt"
    _EXAMPLE_CLASSES: Path = _PATH_TO_TERM / "example_classes.txt"
    _EXAMPLE_METAPHOR: Path = _PATH_TO_TERM / "example_metaphor.txt"
    _EXAMPLE_ONE_LINE_METAPHOR: Path = _PATH_TO_TERM / "example_one_line_metaphor.txt"
    _INPUT_DATA: Path = _PATH_TO_TERM / "input_data.txt"
    _INPUT_EXPLANATION: Path = _PATH_TO_TERM / "input_explanation.txt"

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
            SafeDict(
                name=self._term["name"],
                definition=self._term["definition"]
            )
        )

    def _get_additional_instructions_for_manim_code(self) -> str:
        return self._ADDITIONAL_INSTRUCTIONS_FOR_MANIM_CODE.read_text()

    def _get_example_for_metaphor(self) -> str:
        return self._EXAMPLE_METAPHOR.read_text()

    def _get_example_for_one_line_metaphor(self) -> str:
        return self._EXAMPLE_ONE_LINE_METAPHOR.read_text()