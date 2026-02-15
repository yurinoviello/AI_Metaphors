from abc import ABC, abstractmethod
from pathlib import Path

from ai_metaphors.common.core.utils import ManimType, SafeDict
from ai_metaphors import PROJECT_ROOT
from ai_metaphors.common.static_color_refining.palette import PALETTE_HEX


class PromptProvider(ABC):
    _LANGUAGE = "Python"
    _BASE_PATH: Path = PROJECT_ROOT / "common/core/prompts"
    _SVG_DIRECTORY: Path = PROJECT_ROOT / "resources/SVGs"

    # Remove black color from allowed, because the background is black already
    _ALLOWED_SVG_COLORS = ", ".join(PALETTE_HEX).replace(", #000000", "")

    _SVG_EXAMPLE: Path = _BASE_PATH / "svg_handling/svg_example_code.txt"
    _SVG_ELEMENTS_INSTRUCTIONS_CONTENT: Path = _BASE_PATH / "svg_handling/svg_elements_creation_strategy.txt"
    _SVG_ELEMENTS_INSTRUCTIONS_MANIM_CONTENT: Path = _BASE_PATH / "svg_handling/svg_elements_manim_using_strategy.txt"
    _SVG_ELEMENTS_INSTRUCTIONS_TEMPLATE: Path = _BASE_PATH / "svg_handling/svg_elements_instruction_template.txt"
    _MANIM_LIBRARY_TEMPLATE: Path = _BASE_PATH / "manim_library.txt"

    _SYSTEM_PROMPT_CLASSES_TEMPLATE: Path = _BASE_PATH / "classes/system_prompt_classes.txt"
    _USER_PROMPT_CLASSES_TEMPLATE: Path = _BASE_PATH / "classes/user_prompt_classes.txt"
    _OUTPUT_FORMAT_CLASSES_TEMPLATE: Path = _BASE_PATH / "classes/output_format.txt"

    _SYSTEM_PROMPT_DESCRIPTION_TEMPLATE: Path = _BASE_PATH / "description/system_prompt_description.txt"
    _USER_PROMPT_DESCRIPTION_TEMPLATE: Path = _BASE_PATH / "description/user_prompt_description.txt"

    _SYSTEM_PROMPT_MANIM_TEMPLATE: Path = _BASE_PATH / "manim_code/system_prompt_manim.txt"
    _USER_PROMPT_MANIM_TEMPLATE: Path = _BASE_PATH / "manim_code/user_prompt_manim.txt"

    _SYSTEM_PROMPT_REFINE_MANIM_TEMPLATE: Path = _BASE_PATH / "refine_manim/system_prompt_refine_manim.txt"
    _USER_PROMPT_REFINE_MANIM_TEMPLATE: Path = _BASE_PATH / "refine_manim/user_prompt_refine_manim.txt"

    _SYSTEM_PROMPT_METAPHOR_TEMPLATE: Path = _BASE_PATH / "metaphor/system_prompt_metaphor.txt"
    _USER_PROMPT_METAPHOR_TEMPLATE: Path = _BASE_PATH / "metaphor/user_prompt_metaphor.txt"

    _SYSTEM_PROMPT_ONE_LINE_METAPHOR_TEMPLATE: Path = _BASE_PATH / "one_line_metaphor/system_prompt_one_line_metaphor.txt"
    _USER_PROMPT_ONE_LINE_METAPHOR_TEMPLATE: Path = _BASE_PATH / "one_line_metaphor/user_prompt_one_line_metaphor.txt"

    _SYSTEM_PROMPT_EVALUATE_VIDEO_TEMPLATE: Path = _BASE_PATH / "validate/system_evaluate_video.txt"
    _USER_PROMPT_EVALUATE_VIDEO_TEMPLATE: Path = _BASE_PATH / "validate/user_evaluate_video.txt"

    _SYSTEM_PROMPT_FIX_VIDEO_TEMPLATE: Path = _BASE_PATH / "validate/system_fix_video.txt"
    _USER_PROMPT_FIX_VIDEO_TEMPLATE: Path = _BASE_PATH / "validate/user_fix_video.txt"

    def __init__(self, manim_type: ManimType):
        self._manim_type = manim_type

    def get_system_prompt_term_definition(self) -> str:
        return ""

    def get_user_prompt_term_definition(self) -> str:
        return ""

    def get_system_prompt_one_line_term_definition(self) -> str:
        return ""

    def get_user_prompt_one_line_term_definition(self, term_definition: str) -> str:
        return ""

    def get_system_prompt_classes(self, svg: str) -> str:
        return self._SYSTEM_PROMPT_CLASSES_TEMPLATE.read_text().format_map(
            SafeDict(
                input_explanation=self._get_input_explanation(),
                output_format=self._OUTPUT_FORMAT_CLASSES_TEMPLATE.read_text(),
                example=self._get_example_for_classes(),
                svg_instructions=self._get_svg_elements_instructions(svg)
            )
        )

    @abstractmethod
    def _get_example_for_classes(self) -> str:
        pass

    @abstractmethod
    def _get_input_explanation(self) -> str:
        pass

    @abstractmethod
    def _get_input_data(self) -> str:
        pass

    def _get_svg_example(self) -> str:
        return self._SVG_EXAMPLE.read_text()

    def _get_svg_elements_instructions_content(self) -> str:
        return self._SVG_ELEMENTS_INSTRUCTIONS_CONTENT.read_text().format_map(
            SafeDict(SVG_directory=self._SVG_DIRECTORY, SVG_code=self._get_svg_example(),
                     allowed_colors=self._ALLOWED_SVG_COLORS))

    def _get_svg_elements_instructions_manim_content(self, svg: str) -> str:
        return self._SVG_ELEMENTS_INSTRUCTIONS_MANIM_CONTENT.read_text().format_map(
            SafeDict(SVGs=svg, SVG_directory=self._SVG_DIRECTORY))

    def _get_svg_elements_instructions(self, svg: str) -> str:
        return self._SVG_ELEMENTS_INSTRUCTIONS_TEMPLATE.read_text().format_map(
            SafeDict(SVGs=svg, SVG_directory=self._SVG_DIRECTORY,
                     instructions=self._get_svg_elements_instructions_content())
        )

    def _get_svg_elements_instructions_manim(self, svg: str) -> str:
        return self._SVG_ELEMENTS_INSTRUCTIONS_TEMPLATE.read_text().format_map(
            SafeDict(SVGs=svg, SVG_directory=self._SVG_DIRECTORY,
                     instructions=self._get_svg_elements_instructions_manim_content(svg))
        )

    def _get_manim_library_documentation(self) -> str:
        return self._MANIM_LIBRARY_TEMPLATE.read_text()

    def get_user_prompt_classes(self, story: str) -> str:
        return self._USER_PROMPT_CLASSES_TEMPLATE.read_text().format_map(
            SafeDict(
                input_data=self._get_input_data(),
                story=story
            )
        )

    def get_system_prompt_description(self) -> str:
        return self._SYSTEM_PROMPT_DESCRIPTION_TEMPLATE.read_text().format_map(
            SafeDict(
                input_explanation=self._get_input_explanation(),
                additional_guidelines=self._get_additional_guidelines_for_description()
            )
        )

    def _get_additional_guidelines_for_description(self) -> str:
        return ""

    def get_user_prompt_description(self, story: str, one_line_story: str, classes: str) -> str:
        return self._USER_PROMPT_DESCRIPTION_TEMPLATE.read_text().format_map(
            SafeDict(
                input_data=self._get_input_data(),
                story=story,
                one_line_story=one_line_story,
                classes=classes
            )
        )

    def get_system_prompt_manim(self, svg: str) -> str:
        return self._SYSTEM_PROMPT_MANIM_TEMPLATE.read_text().format_map(
            SafeDict(
                input_explanation=self._get_input_explanation(),
                additional_instructions=self._get_additional_instructions_for_manim_code(),
                example_code=self._manim_type.value.get_example_code(),
                start_code=self._manim_type.value.get_start_code(
                    self._get_subject_name(),
                    self._get_additional_methods_for_manim_voice_start_code(),
                    self._get_working_dir(),
                ),
                manim_library=self._get_manim_library_documentation(),
                svg_instructions=self._get_svg_elements_instructions_manim(svg),
                allowed_colors=self._ALLOWED_SVG_COLORS,
            )
        )

    def _get_additional_instructions_for_manim_code(self) -> str:
        return ""

    def _get_additional_methods_for_manim_voice_start_code(self) -> str:
        return ""

    def get_user_prompt_manim(self, story: str, one_line_story: str, classes: str, instructions: str = "") -> str:
        return self._USER_PROMPT_MANIM_TEMPLATE.read_text().format_map(
            SafeDict(
                input_data=self._get_input_data(),
                story=story,
                one_line_story=one_line_story,
                classes=classes,
                instructions=instructions,
            )
        )

    def get_system_prompt_refine_manim(self, svg: str) -> str:
        return self._SYSTEM_PROMPT_REFINE_MANIM_TEMPLATE.read_text().format_map(
            SafeDict(
                SVGs=svg,
                additional_instructions=self._get_additional_instructions_for_refine_manim(),
                start_code=self._manim_type.value.get_start_code(
                    self._get_subject_name(),
                    self._get_additional_methods_for_manim_voice_start_code(),
                    self._get_working_dir(),
                ),
                manim_library=self._get_manim_library_documentation()
            )
        )

    def _get_additional_instructions_for_refine_manim(self) -> str:
        return ""

    def get_user_prompt_refine_manim(self, code: str, runtime_error: str, static_error: str) -> str:
        return self._USER_PROMPT_REFINE_MANIM_TEMPLATE.read_text().format_map(
            SafeDict(
                code=code,
                runtime_error=runtime_error,
                static_error=static_error
            )
        )

    def get_system_prompt_metaphor(self) -> str:
        return self._SYSTEM_PROMPT_METAPHOR_TEMPLATE.read_text().format_map(
            SafeDict(
                language=self._LANGUAGE,
                input_explanation=self._get_input_explanation(),
                example=self._get_example_for_metaphor()
            )
        )

    def _get_example_for_metaphor(self) -> str:
        return ""

    def get_user_prompt_metaphor(self) -> str:
        return self._USER_PROMPT_METAPHOR_TEMPLATE.read_text().format_map(
            SafeDict(
                input_data=self._get_input_data()
            )
        )

    def get_system_prompt_one_line_metaphor(self) -> str:
        return self._SYSTEM_PROMPT_ONE_LINE_METAPHOR_TEMPLATE.read_text().format_map(
            SafeDict(
                input_explanation=self._get_input_explanation(),
                example=self._get_example_for_one_line_metaphor()
            )
        )

    def _get_example_for_one_line_metaphor(self) -> str:
        return ""

    def get_user_prompt_one_line_metaphor(self, metaphor: str) -> str:
        return self._USER_PROMPT_ONE_LINE_METAPHOR_TEMPLATE.read_text().format_map(
            SafeDict(
                input_data=self._get_input_data(),
                metaphor=metaphor
            )
        )

    def get_system_prompt_evaluate_video(self) -> str:
        return self._SYSTEM_PROMPT_EVALUATE_VIDEO_TEMPLATE.read_text()

    def get_user_prompt_evaluate_video(self, code: str, instructions: str) -> str:
        return self._USER_PROMPT_EVALUATE_VIDEO_TEMPLATE.read_text().format_map(
            SafeDict(
                instructions=instructions,
                code=code,
            )
        )

    def get_system_prompt_fix_video(self, svg: str) -> str:
        return self._SYSTEM_PROMPT_FIX_VIDEO_TEMPLATE.read_text().format_map(
            SafeDict(
                example_code=self._manim_type.value.get_example_code(),
                start_code=self._manim_type.value.get_start_code(self._get_subject_name(), working_dir=self._get_working_dir()),
                manim_library=self._get_manim_library_documentation(),
                svg_instructions=self._get_svg_elements_instructions(svg),
            )
        )

    def get_user_prompt_fix_video(self, instructions: str, errors_explanation: str, code: str) -> str:
        return self._USER_PROMPT_FIX_VIDEO_TEMPLATE.read_text().format_map(
            SafeDict(
                instructions=instructions,
                errors_explanation=errors_explanation,
                code=code,
            )
        )

    @abstractmethod
    def _get_subject_name(self):
        pass

    @abstractmethod
    def _get_working_dir(self):
        pass