import json
import logging
from pathlib import Path
import re

from ai_metaphors.avatar.processors.avatar_processor import AvatarProcessor
from ai_metaphors.avatar.processors.cartoon_avatar_processor import CartoonAvatarProcessor
from ai_metaphors.core.utils import TermType
from ai_metaphors.core.output_structure.output_structure import OutputStructure
from ai_metaphors.core.providers.prompt_provider import PromptProvider
from ai_metaphors.core.providers.grazie_provider import GrazieProvider
from ai_metaphors.core.processors.manim_processor import ManimProcessor
from ai_metaphors.core.utils.manim_type import ManimType
from ai_metaphors.core.utils.text_utils import extract_json, extract_content


class MetaphorProcessor:
    _subject_id: str
    _manim_type: ManimType
    _term_type: TermType
    _working_dir: Path
    _model_manim: str
    _vllm_fix: bool

    _story: str | None   #  metaphor or definition
    _one_line_story: str | None
    _classes_dict: str | None
    _description: str | None

    _grazie_provider: GrazieProvider
    _manim_provider: ManimProcessor

    _output_structure: OutputStructure

    def __init__(
            self,
            subject_id: str,
            prompt_provider: PromptProvider,
            metaphor: str | None,
            term_type: TermType,
            manim_type: ManimType,
            bin_directory: Path,
            working_dir: Path,
            model: str,
            model_classes: str,
            model_manim: str,
            temperature: float,
            vllm_fix: bool,
            auto_play: bool,
            high_quality: bool
    ) -> None:
        if not bin_directory.exists():
            raise ValueError(f"bin_directory does not exist: {bin_directory}")
        if not working_dir.exists():
            raise ValueError(f"working_dir does not exist: {working_dir}")

        self._subject_id = subject_id
        self._manim_type = manim_type
        self._story = metaphor
        self._term_type = term_type
        self._working_dir = working_dir
        self._model = model
        self._model_classes = model_classes
        self._model_manim = model_manim
        self._vllm_fix = vllm_fix

        self._grazie_provider = GrazieProvider(
            model=model,
            temperature=temperature,
            prompt_provider=prompt_provider
        )

        self._manim_provider = ManimProcessor(
            grazie_provider=self._grazie_provider,
            subject_id=self._subject_id,
            bin_directory=bin_directory,
            working_dir=self._working_dir,
            high_quality=high_quality,
            auto_play=auto_play,
        )

        self._output_structure = OutputStructure(
            working_dir,
            subject_id,
            high_quality
        )

    def _generate_story(self):
        if self._term_type == TermType.ACADEMIC_DEFINITION:
            self._story = extract_content(self._grazie_provider.get_term_definition())
            logging.info("Term definition: %s", self._story)
        elif self._story is None:
            self._story = extract_content(self._grazie_provider.get_metaphor())
            logging.info("Metaphor: %s", self._story)

    def _generate_one_line_story(self):
        if self._story is None:
            return
        if self._term_type == TermType.ACADEMIC_DEFINITION:
            self._one_line_story = extract_content(self._grazie_provider.get_one_line_term_definition(self._story))
            logging.info("One-line term definition: %s", self._one_line_story)
        else:
            self._one_line_story = extract_content(self._grazie_provider.get_one_line_metaphor(self._story))
            logging.info("One-line Metaphor: %s", self._one_line_story)

    def _generate_classes(self):
        self._grazie_provider.change_model(self._model_classes)
        classes = self._grazie_provider.get_classes(self._story, self._manim_provider.svg)
        logging.info("Classes created")
        self._classes_dict = extract_json(classes)
        with self._manim_provider.classes_file.open(mode="w", encoding="utf-8") as json_file:
            json.dump(self._classes_dict, json_file, indent=4)
        self._grazie_provider.change_model(self._model)
        logging.info("Classes extracted")

    def _generate_description(self):
        self._description = self._grazie_provider.get_description(self._story, self._one_line_story, str(self._classes_dict))
        with self._manim_provider.description_file.open(mode="w", encoding="utf-8") as text_file:
            text_file.write(self._description)
        logging.info("Description created")

    def _generate_manim_code(self) -> str:
        if self._model_manim != "default":
            self._grazie_provider.change_model(self._model_manim)

        manim_code = self._grazie_provider.get_manim(
            self._story,
            self._one_line_story,
            str(self._classes_dict),
            self._manim_provider.svg,
            self._description,
        )
        logging.info("Manim code created")
        return manim_code

    def _generate_avatar(self):
        if self._manim_type == ManimType.AVATAR:
            narration_text = re.findall(r'\*\*Narrator\*\*:\s*```(.*?)```', self._description, re.DOTALL)
            AvatarProcessor(
                working_dir=self._working_dir,
                description=self._description,
                subject_id=self._subject_id,
            ).generate_avatar_and_break_into_frames(narration_text)

    def _refine_video(self):
        if self._vllm_fix and self._manim_provider.validate_video():
            video_analysis = self._manim_provider.evaluate_video()
            logging.info("Evaluation complete")
            logging.info("Video Evaluation: %s", video_analysis)

            video_refined_code = self._grazie_provider.request_video_refinement(
                instructions=self._manim_provider.description_file.read_text(),
                code=self._manim_provider.script_path.read_text(),
                errors_explanation=video_analysis,
                svg=self._manim_provider.svg,
            )

            self._manim_provider.write_and_run_python(video_refined_code)

    def _add_cartoon_avatar(self):
        if self._manim_type != ManimType.CARTOON_AVATAR:
            return
        logging.info("Adding cartoon avatar...")
        CartoonAvatarProcessor(
            description=self._description,
            one_line_story=self._one_line_story,
            output_structure=self._output_structure
        ).generate_video_with_avatar()

    def generate_video(self):
        self._generate_story()
        self._generate_one_line_story()
        self._generate_classes()
        self._generate_description()
        manim_code = self._generate_manim_code()
        self._generate_avatar()
        self._manim_provider.write_and_run_python(manim_code)

        logging.info("Current token usage: %d", self._grazie_provider.num_tokens)
        logging.info("Current token usage: %f $", 5 / 1_000_000 * self._grazie_provider.num_tokens)

        self._refine_video()
        self._add_cartoon_avatar()
