from datetime import datetime
from enum import Enum
from typing import Literal, Optional, List, TYPE_CHECKING

from pydantic import BaseModel, Field

from ai_metaphors.server.models.status import Status
from ai_metaphors.common.core.utils import TermType

if TYPE_CHECKING:
    from ai_metaphors.server.models.video_task import VideoTask

AnimationType = Literal['basic', 'voice', 'avatar', 'cartoon-avatar']


class VideoRequest(BaseModel):
    term_name: Optional[str] = Field(None, description="Term name")
    term_definition: Optional[str] = Field(None, description="Term definition")
    metaphor: Optional[str] = Field(None, description="Metaphor")
    term_type: str = Field(TermType.DEFINITION_METAPHOR, description="Term type")

    use_dataset_example: Optional[int] = Field(-1, description="Dataset example (0-13), -1 to ignore")

    generate_metaphor_text: Optional[bool] = Field(True, description="Generate metaphor text")
    animation_type: Optional[AnimationType] = Field("basic",
                                                    description="Animation type: basic, voice, avatar, or cartoon-avatar")

    model: Optional[str] = Field("openai-gpt-4o", description="LLM to be used for processing")
    model_manim: Optional[str] = Field("default", description="LLM to be used to process only the manim script")
    temperature: Optional[float] = Field(0.1, description="Temperature for LLM generation")

    vllm_fix: Optional[bool] = Field(False, description="Perform automatic vllm analysis and code correction")
    high_quality: Optional[bool] = Field(False, description="Generate high quality animation (1080p60p)")


class VideoResponse(BaseModel):
    task_id: str
    status: Status


class VideoTaskStatus(BaseModel):
    task_id: str
    status: Status
    created_at: datetime
    video_url: str | None = None

    term_name: str | None = None
    term_definition: str | None = None
    metaphor: str | None = None
    term_type: TermType
    use_dataset_example: int
    generate_metaphor_text: bool
    animation_type: str
    model: str
    model_classes: str
    model_manim: str
    temperature: float
    vllm_fix: bool
    high_quality: bool
    user_name: str | None = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_model(cls, task: 'VideoTask', user_name: str | None = None) -> 'VideoTaskStatus':
        return cls(
            task_id=task.id,
            status=task.status,
            created_at=task.created_at,
            video_url=task.s3_video_url if task.status == Status.completed else None,
            term_name=task.term_name,
            term_definition=task.term_definition,
            metaphor=task.metaphor,
            term_type=task.term_type,
            use_dataset_example=task.use_dataset_example,
            generate_metaphor_text=task.generate_metaphor_text,
            animation_type=task.animation_type,
            model=task.model,
            model_classes=task.model_classes,
            model_manim=task.model_manim,
            temperature=task.temperature,
            vllm_fix=task.vllm_fix,
            high_quality=task.high_quality,
            user_name=user_name
        )


class VideoTaskList(BaseModel):
    tasks: List[VideoTaskStatus]
    total: int
    skip: int
    limit: int
