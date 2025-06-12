from dataclasses import dataclass
from enum import Enum
from pathlib import Path

@dataclass
class ManimConfig:
    _start_code: Path
    _example_code: Path

    def __init__(self, start_code: str, example_code: str):
        self._start_code = Path(start_code)
        self._example_code = Path(example_code)

    def get_start_code(self, term_name: str, additional_methods: str) -> str:
        return self._start_code.read_text().format_map(
            SafeDict(
                term_name=term_name.replace(' ', '_'),
                additional_methods=additional_methods
            ))

    def get_example_code(self) -> str:
        return self._example_code.read_text()


class ManimType(Enum):
    DEFAULT = ManimConfig("ai_metaphors/core/prompts/manim_start_code/manim.txt",
                          "ai_metaphors/core/prompts/manim_example_code/manim.txt")
    VOICE = ManimConfig("ai_metaphors/core/prompts/manim_start_code/manim_voice.txt",
                        "ai_metaphors/core/prompts/manim_example_code/manim_voice.txt")
    AVATAR = ManimConfig("ai_metaphors/core/prompts/manim_start_code/manim_avatar.txt",
                         "ai_metaphors/core/prompts/manim_example_code/manim.txt")


class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'
