import json
import logging
import re
from pathlib import Path

from starlette.concurrency import run_in_threadpool

from ai_metaphors.common.avatar.processors.avatar_processor import AvatarProcessor
from ai_metaphors.common.avatar.processors.cartoon_avatar_processor import CartoonAvatarProcessor
from ai_metaphors.common.core.processors.manim_processor import ManimProcessor
from ai_metaphors.common.core.providers.grazie_provider import GrazieProvider
from ai_metaphors.common.core.providers.prompt_provider import PromptProvider
from ai_metaphors.common.core.utils import TermType
from ai_metaphors.common.core.utils.manim_type import ManimType
from ai_metaphors.common.core.utils.text_utils import extract_json, extract_content
from ai_metaphors.common.output_structure.output_structure import OutputStructure


class MetaphorProcessor:
    _subject_id: str
    _manim_type: ManimType
    _term_type: TermType
    _working_dir: Path
    _task_id: str | None
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
            high_quality: bool,
            task_id: str | None = None,
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
        self._task_id = task_id
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

    def get_output_structure(self):
        return self._output_structure

    async def _generate_story(self):
        if self._term_type == TermType.ACADEMIC_DEFINITION:
            content = await self._grazie_provider.get_term_definition()
            self._story = extract_content(content)
            logging.info(f"Term definition: {self._story}")
        elif self._story is None:
            content = await self._grazie_provider.get_metaphor()
            self._story = extract_content(content)
            logging.info(f"Metaphor: {self._story}")

    async def _generate_one_line_story(self):
        if self._story is None:
            return
        if self._term_type == TermType.ACADEMIC_DEFINITION:
            content = await self._grazie_provider.get_one_line_term_definition(self._story)
            self._one_line_story = extract_content(content)
            logging.info(f"One-line term definition: {self._one_line_story}")
        else:
            content = await self._grazie_provider.get_one_line_metaphor(self._story)
            self._one_line_story = extract_content(content)
            logging.info(f"One-line Metaphor: {self._one_line_story}")

    async def _generate_classes(self):
        if self._model_classes != "default":
            self._grazie_provider.change_model(self._model_classes)

        classes = await self._grazie_provider.get_classes(self._story, self._manim_provider.svg)
        logging.debug("Classes created")
        self._classes_dict = extract_json(classes)
        with self._manim_provider.classes_file.open(mode="w", encoding="utf-8") as json_file:
            json.dump(self._classes_dict, json_file, indent=4)
        self._grazie_provider.change_model(self._model)
        logging.debug("Classes extracted")

    async def _generate_description(self):
        self._description = await self._grazie_provider.get_description(
            self._story, self._one_line_story, str(self._classes_dict)
        )

        with self._manim_provider.description_file.open(mode="w", encoding="utf-8") as text_file:
            text_file.write(self._description)
        logging.info("Description created")

    async def _generate_manim_code(self) -> str:
        if self._model_manim != "default":
            self._grazie_provider.change_model(self._model_manim)

        manim_code = await self._grazie_provider.get_manim(
            self._story,
            self._one_line_story,
            str(self._classes_dict),
            self._manim_provider.svg,
            self._description,
        )
        logging.debug("Manim code created")
        return manim_code

    async def _generate_avatar(self):
        logging.info("Adding human avatar...")
        narration_text = re.findall(r'\*\*Narrator\*\*:\s*```(.*?)```', self._description, re.DOTALL)
        await AvatarProcessor(
            working_dir=self._working_dir,
            description=self._description,
            subject_id=self._subject_id,
            task_id=self._task_id
        ).generate_avatar_and_break_into_frames(narration_text)

    async def _refine_video(self) -> str | None:
        if self._vllm_fix and self._manim_provider.validate_video():
            video_analysis = await self._manim_provider.evaluate_video()
            logging.info("Evaluation complete")
            logging.debug(f"Video Evaluation: {video_analysis}")

            def get_refined_params():
                return {
                    "instructions": self._manim_provider.description_file.read_text(),
                    "code": self._manim_provider.script_path.read_text(),
                }

            params = await run_in_threadpool(get_refined_params)

            video_refined_code = await self._grazie_provider.request_video_refinement(
                instructions=params["instructions"],
                code=params["code"],
                errors_explanation=video_analysis,
                svg=self._manim_provider.svg,
            )

            return await self._manim_provider.write_and_run_python(video_refined_code)
        return None

    async def _add_cartoon_avatar(self):
        logging.info("Adding cartoon avatar...")
        await CartoonAvatarProcessor(
            description=self._description,
            one_line_story=self._one_line_story,
            output_structure=self._output_structure,
            working_dir=self._working_dir
        ).generate_video_with_avatar()

    async def generate_video(self) -> str:
        tokens_before = self._grazie_provider.num_tokens

        await self._generate_story()
        await self._generate_one_line_story()
        await self._generate_classes()
        await self._generate_description()
        manim_code = await self._generate_manim_code()
        if self._manim_type == ManimType.AVATAR:
            await self._generate_avatar()
        final_code = await self._manim_provider.write_and_run_python(manim_code)

        tokens_after = self._grazie_provider.num_tokens - tokens_before
        logging.info(f"Tokens used: {tokens_after}, money spent: {self._count_money(tokens_after)}$")

        quota = await self._grazie_provider.get_quota()
        logging.info(f"Current quota: {quota}")

        refined_code = await self._refine_video()
        if refined_code:
            final_code = refined_code

        if self._manim_type == ManimType.CARTOON_AVATAR:
            await self._add_cartoon_avatar()
        return final_code

    @staticmethod
    def _count_money(tokens: int) -> float:
        return 5 / 1_000_000 * tokens