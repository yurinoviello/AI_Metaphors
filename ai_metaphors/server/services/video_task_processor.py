import logging
import shutil
from pathlib import Path

import datasets

from ai_metaphors.common.core import MetaphorProcessor, ManimType
from ai_metaphors.common.core.utils import TermType
from ai_metaphors.server.models.video_task import VideoTask
from ai_metaphors.server.schemas.video import Status
from ai_metaphors.server.services.storage_service import GCSStorageService
from ai_metaphors.common.video_from_academic_definition import AcademicDefinitionPromptProvider
from ai_metaphors.common.video_from_code import CodePromptProvider
from ai_metaphors.common.video_from_definition import DefinitionPromptProvider


class VideoTaskProcessor:
    _bin_directory: Path
    _ds: datasets.Dataset
    storage_service: GCSStorageService
    working_dir: Path
    storage_url: str | None
    metaphor_processor: MetaphorProcessor

    manim_type_map = {
        "basic": ManimType.DEFAULT,
        "voice": ManimType.VOICE,
        "avatar": ManimType.AVATAR,
        "cartoon-avatar": ManimType.CARTOON_AVATAR
    }

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self._bin_directory = Path("/opt/conda/bin")
        self._ds = datasets.load_from_disk("ai_metaphors/resources/examples/definitions")
        self.storage_service = GCSStorageService()
        self.storage_url = None

    async def process_video_generation_task(self, task_id: str):
        task = await VideoTask.get(task_id)
        if not task:
            logging.error(f"Task {task_id} not found")
            return

        try:
            self.working_dir = self._set_up_working_dir(task_id)

            logging.info(f"Starting video generation task {task_id}")
            await task.update(task_id=task_id, status=Status.processing)

            self.metaphor_processor = self.processor_setup(task, task_id)
            self.metaphor_processor.generate_video()

            logging.info(f"Video generation completed successfully")

            self.upload_video(task_id)
            logging.info(f"Video uploaded successfully")
            await task.update(task_id=task_id, status=Status.completed, s3_video_url=self.storage_url)

        except Exception as e:
            logging.error(f"Error in video generation task {task_id}: {str(e)}")
            await task.update(task_id=task_id, status=Status.failed)

        finally:
            if self.working_dir.exists():
                shutil.rmtree(self.working_dir)
                logging.info(f"Deleted working directory {self.working_dir}")
            logging.info(f"Video generation task {task_id} completed")

    def processor_setup(self, task: VideoTask, task_id: str) -> MetaphorProcessor:
        term_name: str | None = task.term_name
        term_value: str | None = task.term_definition
        metaphor: str | None = task.metaphor
        if task.use_dataset_example != -1:
            match task.term_type:
                case TermType.DEFINITION_METAPHOR:
                    ds = datasets.load_from_disk("ai_metaphors/resources/examples/definitions")
                    term_name = ds[task.use_dataset_example]["name"]
                    term_value = ds[task.use_dataset_example]["definition"]
                    metaphor = ds[task.use_dataset_example]["metaphor"]
                case TermType.CODE_METAPHOR:
                    ds = datasets.load_from_disk("ai_metaphors/resources/examples/codes")
                    term_name = ds[task.use_dataset_example]["name"]
                    term_value = ds[task.use_dataset_example]["folder"]
                case _:
                    raise ValueError(f"Not supported term type: {task.term_type} for dataset example")
        else:
            if term_name is None:
                raise ValueError("Term must not be empty when no example is used.")
            if task.term_type != TermType.ACADEMIC_DEFINITION and term_value is None:
                raise ValueError("Definition must not be empty when no example is used.")
            if task.term_type != TermType.ACADEMIC_DEFINITION and not task.generate_metaphor_text and task.metaphor is None:
                raise ValueError("Metaphor must not be empty if not generating it.")

        manim_type = self.manim_type_map.get(task.animation_type, ManimType.DEFAULT)

        match task.term_type:
            case TermType.DEFINITION_METAPHOR:
                term = {
                    "name": term_name,
                    "definition": term_value
                }
                prompt_provider = DefinitionPromptProvider(term, manim_type)
            case TermType.CODE_METAPHOR:
                term = {
                    "name": term_name,
                    "code_folder": term_value
                }
                prompt_provider = CodePromptProvider(term, manim_type)
            case TermType.ACADEMIC_DEFINITION:
                term = {"name": term_name}
                prompt_provider = AcademicDefinitionPromptProvider(term, manim_type)
            case _:
                raise ValueError(f"Unknown term type: {task.term_type}")

        subject_id = term_name.replace(' ', '_')

        return MetaphorProcessor(
            subject_id=subject_id,
            prompt_provider=prompt_provider,
            metaphor=metaphor,
            term_type=task.term_type,
            manim_type=manim_type,
            bin_directory=self._bin_directory,
            working_dir=self.working_dir,
            model=task.model,
            model_classes=task.model_classes,
            model_manim=task.model_manim,
            temperature=task.temperature,
            vllm_fix=task.vllm_fix,
            auto_play=False,
            high_quality=task.high_quality,
            task_id=task_id
        )

    def upload_video(self, task_id: str):
        output_structure = self.metaphor_processor.get_output_structure()
        video_path = output_structure.get_final_video_path()

        storage_key = f"{task_id}/{video_path.name}"
        self.storage_url = self.storage_service.upload_file(video_path, storage_key)

        if self.storage_url is None:
            raise RuntimeError("Failed to upload video to storage")

    @staticmethod
    def _set_up_working_dir(task_id: str):
        working_dir = Path("/app/animations") / Path(task_id)
        working_dir.mkdir(parents=True, exist_ok=True)

        return working_dir
