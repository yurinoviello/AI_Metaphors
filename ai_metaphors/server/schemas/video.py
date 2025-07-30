from datetime import datetime
from typing import Literal, Optional, List
from pydantic import BaseModel, Field
from enum import Enum

from ai_metaphors.common.core.utils import TermType

AnimationType = Literal['basic', 'voice', 'avatar', 'cartoon-avatar']


class Status(Enum):
    queued = 'queued'
    processing = 'processing'
    completed = 'completed'
    failed = 'failed'


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
    video_url: Optional[str] = None


class VideoTaskList(BaseModel):
    tasks: List[VideoTaskStatus]

