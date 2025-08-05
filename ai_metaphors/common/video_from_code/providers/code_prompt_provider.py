from abc import ABC
from pathlib import Path

from ai_metaphors.common.core.providers.prompt_provider import PromptProvider
from ai_metaphors.common.core.utils.manim_type import SafeDict, ManimType
import ai_metaphors.common.core.utils.text_utils

class CodePromptProvider(PromptProvider, ABC):

    _term: dict[str, str]

    _PATH_TO_CODE: Path = Path("ai_metaphors/common/video_from_code/prompts")
    _ADDITIONAL_INSTRUCTIONS_FOR_MANIM_CODE: Path = _PATH_TO_CODE / "additional_instructions_for_manim_code.txt"
    _ADDITIONAL_METHODS_FOR_MANIM_VOICE_START_CODE: Path = _PATH_TO_CODE / "additional_instructions_for_manim_voice_start_code.txt"
    _ADDITIONAL_GUIDELINES_FOR_DESCRIPTION: Path = _PATH_TO_CODE / "additional_guidelines_for_description.txt"
    _EXAMPLE_CLASSES: Path = _PATH_TO_CODE / "example_classes.txt"
    _EXAMPLE_METAPHOR: Path = _PATH_TO_CODE / "example_metaphor.txt"
    _EXAMPLE_ONE_LINE_METAPHOR: Path = _PATH_TO_CODE / "example_one_line_metaphor.txt"
    _INPUT_DATA: Path = _PATH_TO_CODE / "input_data.txt"
    _INPUT_EXPLANATION: Path = _PATH_TO_CODE / "input_explanation.txt"

    def __init__(self, code_block: dict[str, str], manim_type: ManimType):
        super().__init__(manim_type)
        self._term = code_block

    def _get_subject_name(self) -> str:
        return self._term["name"]

    def _get_working_dir(self):
        return self._term["working_dir"]

    def _get_example_for_classes(self) -> str:
        return self._EXAMPLE_CLASSES.read_text()

    def _get_input_explanation(self) -> str:
        return self._INPUT_EXPLANATION.read_text()

    def _get_input_data(self) -> str:
        return self._INPUT_DATA.read_text().format_map(
            SafeDict(
                name=self._term["name"],
                code_block=ai_metaphors.common.core.utils.text_utils.extract_code_from_html(Path(self._term["code_folder"]) / "index.html"),
                steps=ai_metaphors.common.core.utils.text_utils.extract_steps_from_js(Path(self._term["code_folder"]) / "script.js")
            )
        )

    def _get_additional_instructions_for_manim_code(self) -> str:
        return self._ADDITIONAL_INSTRUCTIONS_FOR_MANIM_CODE.read_text()

    def _get_additional_methods_for_manim_voice_start_code(self) -> str:
        return self._ADDITIONAL_METHODS_FOR_MANIM_VOICE_START_CODE.read_text()

    def _get_additional_guidelines_for_description(self) -> str:
        return self._ADDITIONAL_GUIDELINES_FOR_DESCRIPTION.read_text()

    def _get_example_for_metaphor(self) -> str:
        return self._EXAMPLE_METAPHOR.read_text()

    def _get_example_for_one_line_metaphor(self) -> str:
        return self._EXAMPLE_ONE_LINE_METAPHOR.read_text()